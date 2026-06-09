from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


SECRET_KEYS = {"api_key", "secret", "token", "password", "access_key"}


@dataclass(frozen=True)
class ReadinessResult:
    status: str
    issues: tuple[str, ...]
    report_path: Path


def audit_readiness(config_path: Path, report_path: Path) -> ReadinessResult:
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    issues = _collect_issues(config)
    status = "ready" if not issues else "blocked"
    _write_report(report_path, status, issues, config_path)
    return ReadinessResult(status=status, issues=tuple(issues), report_path=report_path)


def _collect_issues(config: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    secret_paths = _find_literal_secrets(config)
    if secret_paths:
        issues.append(
            "비밀값으로 보이는 항목을 설정 파일에서 제거하세요: "
            + ", ".join(secret_paths)
        )

    if config.get("external_calls_allowed") is not True:
        issues.append("외부 호출 승인이 필요합니다.")
    if config.get("dry_run_required") is not True:
        issues.append("첫 연결은 dry-run 필수로 설정해야 합니다.")
    if config.get("max_test_cuts") != 1:
        issues.append("첫 연결의 최대 테스트 컷 수는 1개여야 합니다.")
    if not isinstance(config.get("max_budget_krw"), (int, float)) or config.get(
        "max_budget_krw", 0
    ) <= 0:
        issues.append("사용 가능한 테스트 예산을 0원보다 크게 승인해야 합니다.")
    if config.get("rights_policy") not in {"fictional_only", "authorized_assets_only"}:
        issues.append("권리 정책을 fictional_only 또는 authorized_assets_only로 정해야 합니다.")

    seedance = config.get("seedance", {})
    kling = config.get("kling", {})
    comfy_cloud = config.get("comfy_cloud", {})
    if (
        not seedance.get("enabled")
        and not kling.get("enabled")
        and not comfy_cloud.get("enabled")
    ):
        issues.append("최소 한 개의 영상 서비스를 선택해야 합니다.")

    if seedance.get("enabled"):
        _check_seedance(seedance, issues)
    if kling.get("enabled"):
        _check_kling(kling, issues)
    if comfy_cloud.get("enabled"):
        _check_comfy_cloud(comfy_cloud, issues)

    return issues


def _find_literal_secrets(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.lower() in SECRET_KEYS and child not in (None, "", False):
                found.append(child_path)
            found.extend(_find_literal_secrets(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_literal_secrets(child, f"{path}[{index}]"))
    return found


def _check_seedance(seedance: dict[str, Any], issues: list[str]) -> None:
    required_true = {
        "account_ready": "Seedance 계정 준비",
        "model_activated": "Seedance 모델 활성화",
        "prepaid_resource_pack_confirmed": "Seedance 선불 리소스 팩 확인",
    }
    for field, label in required_true.items():
        if seedance.get(field) is not True:
            issues.append(f"{label}이 필요합니다.")

    if not seedance.get("api_key_env"):
        issues.append("Seedance API 키를 읽을 환경 변수 이름이 필요합니다.")
    if seedance.get("selected_model") in (None, "", "undecided"):
        issues.append("Seedance 모델을 선택해야 합니다.")
    if seedance.get("selected_mode") in (None, "", "undecided"):
        issues.append("Seedance 생성 모드를 선택해야 합니다.")
    if seedance.get("real_face_assets_allowed") is True:
        issues.append("첫 연결에서는 실제 얼굴 자산 사용을 허용하지 않습니다.")


def _check_kling(kling: dict[str, Any], issues: list[str]) -> None:
    if kling.get("account_ready") is not True:
        issues.append("Kling 계정 준비가 필요합니다.")
    if kling.get("credits_budget_approved") is not True:
        issues.append("Kling 크레딧 예산 승인이 필요합니다.")

    access_mode = kling.get("access_mode")
    if access_mode not in {"web_ui", "api"}:
        issues.append("Kling 접근 방식을 web_ui 또는 api로 선택해야 합니다.")
    if access_mode == "api" and kling.get("official_api_access_confirmed") is not True:
        issues.append("Kling 공식 API 접근 확인이 필요합니다.")


def _check_comfy_cloud(comfy_cloud: dict[str, Any], issues: list[str]) -> None:
    if comfy_cloud.get("subscription_ready") is not True:
        issues.append("Comfy Cloud API 사용 가능 구독 확인이 필요합니다.")
    if not comfy_cloud.get("api_key_env"):
        issues.append("Comfy Cloud API 키를 읽을 환경 변수 이름이 필요합니다.")
    if comfy_cloud.get("readonly_connection_verified") is not True:
        issues.append("Comfy Cloud 읽기 전용 API 연결 확인이 필요합니다.")
    if comfy_cloud.get("workflow_api_json_ready") is not True:
        issues.append("Comfy Cloud API 형식 작업 흐름 JSON이 필요합니다.")

    estimated = comfy_cloud.get("estimated_credits_per_run")
    maximum = comfy_cloud.get("max_credits_per_run")
    if not isinstance(maximum, (int, float)) or maximum <= 0:
        issues.append("Comfy Cloud 실행당 크레딧 상한을 0보다 크게 정해야 합니다.")
    elif not isinstance(estimated, (int, float)):
        issues.append("Comfy Cloud 예상 실행 크레딧을 기록해야 합니다.")
    elif estimated > maximum:
        issues.append(
            f"Comfy Cloud 예상 비용 {estimated} 크레딧이 상한 {maximum} 크레딧을 넘습니다."
        )


def _write_report(
    report_path: Path,
    status: str,
    issues: list[str],
    config_path: Path,
) -> None:
    status_label = "진입 가능" if status == "ready" else "진입 차단"
    issue_lines = (
        [f"{index}. {issue}" for index, issue in enumerate(issues, start=1)]
        if issues
        else ["- 모든 준비 조건을 통과했습니다."]
    )
    next_action = (
        "설정 내용을 사람이 다시 확인한 뒤, 외부 서비스 1컷 dry-run을 별도 승인합니다."
        if status == "ready"
        else "아래 미준비 항목을 해결하고 점검 도구를 다시 실행합니다."
    )
    report = "\n".join(
        [
            "# C단계 진입 준비 점검 보고서",
            "",
            "## 요약",
            "",
            f"- 최종 상태: {status_label}",
            f"- 검사한 설정: `{config_path.as_posix()}`",
            "- 실제 외부 서비스 호출: 하지 않음",
            "",
            "## 미준비 항목",
            "",
            *issue_lines,
            "",
            "## 다음 행동",
            "",
            next_action,
            "",
            "## 초보자 설명",
            "",
            "이 점검은 문이 잠겼는지 확인하는 과정입니다.",
            "진입 차단은 오류가 아니라 비용, 권리, 계정 준비가 끝나기 전에 멈추는 안전장치입니다.",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description="C단계 외부 연결 전 준비 상태를 점검합니다.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/C_STAGE_READINESS.json"),
        help="비밀값이 들어 있지 않은 준비 설정 파일",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/C_STAGE_READINESS_REPORT.md"),
        help="한글 점검 보고서 저장 위치",
    )
    args = parser.parse_args()

    result = audit_readiness(args.config, args.report)
    print(f"C단계 준비 상태: {'진입 가능' if result.status == 'ready' else '진입 차단'}")
    print(f"보고서: {result.report_path}")
    return 0 if result.status == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())

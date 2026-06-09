from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Callable, ContextManager, Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://cloud.comfy.org"
READONLY_ENDPOINT = "/api/system_stats"


@dataclass(frozen=True)
class ConnectionResult:
    status: str
    message: str
    endpoint: str


def check_connection(
    api_key: str,
    *,
    opener: Callable[..., ContextManager[Any]] = urlopen,
) -> ConnectionResult:
    endpoint = f"{BASE_URL}{READONLY_ENDPOINT}"
    if not api_key:
        return ConnectionResult(
            status="blocked",
            message="COMFY_CLOUD_API_KEY 환경 변수가 준비되지 않았습니다.",
            endpoint=endpoint,
        )

    request = Request(endpoint, headers={"X-API-Key": api_key}, method="GET")
    try:
        with opener(request, timeout=10) as response:
            json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return ConnectionResult(
            status="blocked",
            message=f"읽기 전용 연결이 거절되었습니다. HTTP {error.code}",
            endpoint=endpoint,
        )
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        return ConnectionResult(
            status="blocked",
            message=f"읽기 전용 연결을 확인하지 못했습니다: {type(error).__name__}",
            endpoint=endpoint,
        )

    return ConnectionResult(
        status="connected",
        message="Comfy Cloud 읽기 전용 API 연결을 확인했습니다.",
        endpoint=endpoint,
    )


def write_report(result: ConnectionResult, report_path: Path) -> None:
    status_label = "연결 확인" if result.status == "connected" else "연결 차단"
    report = "\n".join(
        [
            "# Comfy Cloud 읽기 전용 연결 보고서",
            "",
            "## 요약",
            "",
            f"- 최종 상태: {status_label}",
            f"- 확인 주소: `{result.endpoint}`",
            f"- 설명: {result.message}",
            "- 실제 생성 작업 제출: 하지 않음",
            "- Comfy 크레딧 사용 작업: 하지 않음",
            "- API 키 원문 기록: 하지 않음",
            "",
            "## 초보자 설명",
            "",
            "이 검사는 Comfy Cloud에 안전하게 로그인할 수 있는지만 확인합니다.",
            "영상 생성 버튼을 누르는 것과 달리 작업 흐름을 제출하지 않습니다.",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Comfy Cloud의 읽기 전용 API 연결만 확인합니다."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/COMFY_CLOUD_CONNECTION_REPORT.md"),
    )
    args = parser.parse_args()

    result = check_connection(os.environ.get("COMFY_CLOUD_API_KEY", ""))
    write_report(result, args.report)
    print(f"Comfy Cloud 연결 상태: {'확인됨' if result.status == 'connected' else '차단됨'}")
    print(f"보고서: {args.report}")
    return 0 if result.status == "connected" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from tools.generate_cut_list import generate_cut_list
from tools.generate_shot_sync_map import generate_shot_sync_map
from tools.validate_episode import write_review_report


@dataclass(frozen=True)
class PipelineResult:
    status: str
    completed_steps: tuple[str, ...]
    stopped_step: str | None
    message: str
    report_path: Path


def run_local_pipeline(
    episode_dir: Path,
    *,
    refresh_generated: bool = False,
) -> PipelineResult:
    audit_dir = episode_dir / "story_sync_audit"
    report_path = audit_dir / "PIPELINE_RUN_REPORT.md"
    review_report_path = audit_dir / "AUTO_REVIEW_REPORT.md"
    completed_steps: list[str] = []
    step_lines: list[str] = []

    try:
        cut_list = generate_cut_list(
            episode_dir,
            overwrite=refresh_generated,
        )
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        return _finish(
            episode_dir=episode_dir,
            report_path=report_path,
            status="blocked",
            completed_steps=completed_steps,
            stopped_step="cut_list",
            message=str(error),
            step_lines=[f"- 컷 목록 초안: 중단 - {error}"],
        )

    completed_steps.append("cut_list")
    step_lines.append(
        f"- 컷 목록 초안: 생성 완료 "
        f"(블록 {cut_list.block_count}개, 컷 초안 {cut_list.cut_count}개, "
        f"수동 분할 필요 {cut_list.manual_split_block_count}개)"
    )

    if cut_list.manual_split_block_count > 0:
        message = (
            f"수동 분할 필요 블록이 {cut_list.manual_split_block_count}개 있습니다. "
            "CUT_LIST_DRAFT.md를 검토하세요."
        )
        return _finish(
            episode_dir=episode_dir,
            report_path=report_path,
            status="blocked",
            completed_steps=completed_steps,
            stopped_step="cut_list",
            message=message,
            step_lines=step_lines
            + ["- 자동 검수: 실행하지 않음", "- shot_sync_map: 생성하지 않음"]
            + _stale_sync_map_warning(episode_dir),
        )

    validation = write_review_report(episode_dir, review_report_path)
    completed_steps.append("validation")
    step_lines.append(
        f"- 자동 검수: {'통과' if validation.ok else '수정 필요'} "
        f"(컷 {validation.cut_count}개, 계획 길이 {validation.total_duration_seconds}초)"
    )

    if not validation.ok:
        message = "자동 검수를 통과하지 못했습니다. AUTO_REVIEW_REPORT.md를 확인하세요."
        return _finish(
            episode_dir=episode_dir,
            report_path=report_path,
            status="blocked",
            completed_steps=completed_steps,
            stopped_step="validation",
            message=message,
            step_lines=step_lines
            + ["- shot_sync_map: 생성하지 않음"]
            + _stale_sync_map_warning(episode_dir),
        )

    try:
        sync_map = generate_shot_sync_map(
            episode_dir,
            overwrite=refresh_generated,
        )
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        return _finish(
            episode_dir=episode_dir,
            report_path=report_path,
            status="blocked",
            completed_steps=completed_steps,
            stopped_step="shot_sync_map",
            message=str(error),
            step_lines=step_lines + [f"- shot_sync_map: 중단 - {error}"],
        )

    completed_steps.append("shot_sync_map")
    step_lines.append(
        f"- shot_sync_map: 생성 완료 "
        f"(컷 {sync_map.cut_count}개, 총 {sync_map.total_duration_seconds}초)"
    )
    return _finish(
        episode_dir=episode_dir,
        report_path=report_path,
        status="completed",
        completed_steps=completed_steps,
        stopped_step=None,
        message="로컬 파이프라인을 완료했습니다.",
        step_lines=step_lines,
    )


def _finish(
    *,
    episode_dir: Path,
    report_path: Path,
    status: str,
    completed_steps: list[str],
    stopped_step: str | None,
    message: str,
    step_lines: list[str],
) -> PipelineResult:
    status_label = "완료" if status == "completed" else "중간 차단"
    beginner_lines = (
        [
            "모든 B단계 로컬 검사를 완료했습니다.",
            "외부 AI는 아직 호출하지 않았습니다. 결과물을 사람이 검토한 뒤 다음 단계로 진행합니다.",
        ]
        if status == "completed"
        else [
            "중간 차단은 오류를 숨기지 않고 다음 단계로 넘어가지 않았다는 뜻입니다.",
            "리포트에 적힌 문제를 고친 뒤 다시 실행합니다.",
        ]
    )
    report = "\n".join(
        [
            f"# {episode_dir.name} 로컬 파이프라인 실행 리포트",
            "",
            "## 요약",
            "",
            f"- 최종 상태: {status_label}",
            f"- 멈춘 단계: {stopped_step or '없음'}",
            f"- 설명: {message}",
            "",
            "## 단계별 결과",
            "",
            *step_lines,
            "",
            "## 초보자 설명",
            "",
            *beginner_lines,
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8-sig")
    return PipelineResult(
        status=status,
        completed_steps=tuple(completed_steps),
        stopped_step=stopped_step,
        message=message,
        report_path=report_path,
    )


def _stale_sync_map_warning(episode_dir: Path) -> list[str]:
    sync_map_path = episode_dir / "story_sync_audit" / "shot_sync_map.json"
    if not sync_map_path.exists():
        return []
    return ["- 기존 shot_sync_map 주의: 이번 실행에서 갱신되지 않았습니다."]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="B단계 로컬 도구를 안전한 순서로 실행합니다."
    )
    parser.add_argument("episode_dir", type=Path, help="처리할 에피소드 폴더")
    parser.add_argument(
        "--refresh-generated",
        action="store_true",
        help="기존 생성 산출물을 명시적으로 갱신합니다.",
    )
    args = parser.parse_args()

    result = run_local_pipeline(
        args.episode_dir,
        refresh_generated=args.refresh_generated,
    )
    print(f"파이프라인 상태: {'완료' if result.status == 'completed' else '중간 차단'}")
    print(f"리포트: {result.report_path}")
    print(f"설명: {result.message}")
    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

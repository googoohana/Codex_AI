from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


REQUIRED_MODEL_READINESS_FIELDS = (
    "target_video_model",
    "generation_mode",
    "reference_assets",
    "aspect_ratio",
    "audio_plan",
    "model_limit_note",
    "rights_or_face_policy",
    "generation_risk",
    "fallback_plan",
)


@dataclass(frozen=True)
class ValidationResult:
    episode_name: str
    cut_count: int
    total_duration_seconds: int
    ready_cut_count: int
    image_prompt_count: int
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_episode(episode_dir: Path) -> ValidationResult:
    episode_prefix = episode_dir.name.replace("_sample", "")
    shot_plan_path = episode_dir / f"{episode_prefix}_SHOT_PLAN.md"
    image_prompts_path = episode_dir / f"{episode_prefix}_IMAGE_PROMPTS.md"
    errors: list[str] = []

    if not shot_plan_path.exists():
        return ValidationResult(
            episode_name=episode_dir.name,
            cut_count=0,
            total_duration_seconds=0,
            ready_cut_count=0,
            image_prompt_count=0,
            errors=[f"SHOT_PLAN 파일이 없습니다: {shot_plan_path}"],
        )

    text = shot_plan_path.read_text(encoding="utf-8-sig")
    cut_count = len(re.findall(r"^### CUT_\d+", text, flags=re.MULTILINE))
    durations = [
        int(value)
        for value in re.findall(r"^- planned_duration:\s*(\d+)초", text, flags=re.MULTILINE)
    ]
    ready_cut_count = len(
        re.findall(
            r"^- review_status:\s*ready_for_image_prompt\s*$",
            text,
            flags=re.MULTILINE,
        )
    )
    image_prompt_count = 0

    if image_prompts_path.exists():
        image_prompts_text = image_prompts_path.read_text(encoding="utf-8-sig")
        image_prompt_count = len(
            re.findall(r"^## CUT_\d+", image_prompts_text, flags=re.MULTILINE)
        )
    else:
        errors.append(f"IMAGE_PROMPTS 파일이 없습니다: {image_prompts_path}")

    if len(durations) != cut_count:
        errors.append("모든 컷에 planned_duration이 있어야 합니다.")
    if cut_count == 0:
        errors.append("SHOT_PLAN에 CUT 항목이 없습니다.")
    if ready_cut_count != cut_count:
        errors.append("모든 컷의 review_status가 ready_for_image_prompt여야 합니다.")
    if image_prompt_count != cut_count:
        errors.append(
            f"SHOT_PLAN 컷 수({cut_count})와 IMAGE_PROMPTS 수({image_prompt_count})가 다릅니다."
        )

    for cut_name, cut_text in _parse_cuts(text):
        for field_name in REQUIRED_MODEL_READINESS_FIELDS:
            if not re.search(
                rf"^- {re.escape(field_name)}:[^\S\r\n]*\S+",
                cut_text,
                flags=re.MULTILINE,
            ):
                errors.append(f"{cut_name}: {field_name} 항목이 없습니다.")

    return ValidationResult(
        episode_name=episode_dir.name,
        cut_count=cut_count,
        total_duration_seconds=sum(durations),
        ready_cut_count=ready_cut_count,
        image_prompt_count=image_prompt_count,
        errors=errors,
    )


def _parse_cuts(text: str) -> list[tuple[str, str]]:
    headings = list(re.finditer(r"^### (CUT_\d+)\s*$", text, flags=re.MULTILINE))
    cuts: list[tuple[str, str]] = []

    for heading in headings:
        next_heading = re.search(
            r"^#{2,3}\s+\S+",
            text[heading.end() :],
            flags=re.MULTILINE,
        )
        end = (
            heading.end() + next_heading.start()
            if next_heading
            else len(text)
        )
        cuts.append((heading.group(1), text[heading.end() : end]))

    return cuts


def write_review_report(episode_dir: Path, report_path: Path) -> ValidationResult:
    result = validate_episode(episode_dir)
    verdict = "통과" if result.ok else "수정 필요"
    error_lines = (
        ["- 없음"]
        if result.ok
        else [f"- {error}" for error in result.errors]
    )
    report = "\n".join(
        [
            f"# {result.episode_name} 자동 검수 리포트",
            "",
            "## 요약",
            "",
            f"- 판정: {verdict}",
            f"- SHOT_PLAN 컷 수: {result.cut_count}",
            f"- IMAGE_PROMPTS 수: {result.image_prompt_count}",
            f"- 이미지 생성 준비 컷 수: {result.ready_cut_count}",
            f"- 계획 영상 길이: {result.total_duration_seconds}초",
            "",
            "## 발견된 문제",
            "",
            *error_lines,
            "",
            "## 초보자 설명",
            "",
            "이 리포트는 다음 제작 단계로 넘어가기 전에 문서 구조가 서로 맞는지 확인합니다.",
            "판정이 `수정 필요`이면 발견된 문제를 먼저 고친 뒤 다시 실행합니다.",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8-sig")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="에피소드 문서를 검사하고 한글 검수 리포트를 만듭니다."
    )
    parser.add_argument("episode_dir", type=Path, help="검사할 에피소드 폴더")
    parser.add_argument(
        "--report",
        type=Path,
        help="리포트 저장 경로. 생략하면 에피소드의 story_sync_audit 폴더에 저장합니다.",
    )
    args = parser.parse_args()
    report_path = args.report or (
        args.episode_dir / "story_sync_audit" / "AUTO_REVIEW_REPORT.md"
    )
    result = write_review_report(args.episode_dir, report_path)
    print(f"검수 결과: {'통과' if result.ok else '수정 필요'}")
    print(f"리포트: {report_path}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

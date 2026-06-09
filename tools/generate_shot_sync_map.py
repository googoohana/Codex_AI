from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re

from tools.validate_episode import validate_episode


@dataclass(frozen=True)
class ShotSyncMapResult:
    cut_count: int
    total_duration_seconds: int
    output_path: Path


def generate_shot_sync_map(
    episode_dir: Path,
    output_path: Path | None = None,
    *,
    overwrite: bool = False,
) -> ShotSyncMapResult:
    episode_id = episode_dir.name.replace("_sample", "")
    output_path = output_path or (
        episode_dir / "story_sync_audit" / "shot_sync_map.json"
    )

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"shot_sync_map.json이 이미 존재합니다: {output_path}")

    validation = validate_episode(episode_dir)
    if not validation.ok:
        problems = " / ".join(validation.errors)
        raise ValueError(f"에피소드 자동 검수를 통과해야 합니다: {problems}")

    shot_plan_path = episode_dir / f"{episode_id}_SHOT_PLAN.md"
    shot_plan_text = shot_plan_path.read_text(encoding="utf-8-sig")
    cuts = [_cut_to_sync_entry(cut_id, body) for cut_id, body in _parse_cuts(shot_plan_text)]
    total_duration = sum(cut["planned_duration_seconds"] for cut in cuts)

    data = {
        "schema_version": "1.0",
        "episode_id": episode_id,
        "status": "ready",
        "generated_from": {
            "shot_plan": shot_plan_path.name,
            "image_prompts": f"{episode_id}_IMAGE_PROMPTS.md",
        },
        "summary": {
            "cut_count": len(cuts),
            "total_duration_seconds": total_duration,
            "high_risk_cut_count": sum(
                cut["generation_risk"] == "high" for cut in cuts
            ),
        },
        "cuts": cuts,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return ShotSyncMapResult(
        cut_count=len(cuts),
        total_duration_seconds=total_duration,
        output_path=output_path,
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
        end = heading.end() + next_heading.start() if next_heading else len(text)
        cuts.append((heading.group(1), text[heading.end() : end]))

    return cuts


def _cut_to_sync_entry(cut_id: str, body: str) -> dict[str, object]:
    fields = {
        field_name: _field(body, field_name)
        for field_name in (
            "block",
            "purpose",
            "scene_goal",
            "characters",
            "character_reference",
            "location",
            "allowed_elements",
            "forbidden_elements",
            "shot_size",
            "camera_angle",
            "camera_movement",
            "action",
            "emotion",
            "dialogue_or_narration",
            "planned_duration",
            "target_video_model",
            "generation_mode",
            "aspect_ratio",
            "audio_plan",
            "model_limit_note",
            "reference_assets",
            "rights_or_face_policy",
            "generation_risk",
            "fallback_plan",
            "video_model_note",
            "review_status",
        )
    }
    required_fields = (
        "block",
        "purpose",
        "scene_goal",
        "characters",
        "character_reference",
        "location",
        "allowed_elements",
        "forbidden_elements",
        "shot_size",
        "camera_angle",
        "camera_movement",
        "action",
        "dialogue_or_narration",
        "planned_duration",
        "reference_assets",
        "rights_or_face_policy",
        "video_model_note",
        "review_status",
    )
    missing_fields = [field_name for field_name in required_fields if not fields[field_name]]
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ValueError(f"{cut_id}: 동기화 필수 값이 비었습니다: {missing}")

    duration_text = fields["planned_duration"]
    duration_match = re.fullmatch(r"(\d+)초", duration_text)
    if not duration_match:
        raise ValueError(f"{cut_id}: planned_duration 값을 읽을 수 없습니다.")

    file_stem = cut_id.lower()
    return {
        "cut_id": cut_id,
        "block": fields["block"],
        "purpose": fields["purpose"],
        "scene_goal": fields["scene_goal"],
        "characters": _split_values(fields["characters"]),
        "character_reference": fields["character_reference"],
        "location": fields["location"],
        "allowed_elements": _split_values(fields["allowed_elements"]),
        "forbidden_elements": _split_values(fields["forbidden_elements"]),
        "shot_size": fields["shot_size"],
        "camera_angle": fields["camera_angle"],
        "camera_movement": fields["camera_movement"],
        "action": fields["action"],
        "emotion": _split_values(fields["emotion"]),
        "dialogue_or_narration": fields["dialogue_or_narration"],
        "planned_duration_seconds": int(duration_match.group(1)),
        "target_video_model": fields["target_video_model"],
        "generation_mode": fields["generation_mode"],
        "aspect_ratio": fields["aspect_ratio"],
        "audio_plan": fields["audio_plan"],
        "model_limit_note": fields["model_limit_note"],
        "reference_assets": _split_values(fields["reference_assets"]),
        "rights_or_face_policy": fields["rights_or_face_policy"],
        "generation_risk": fields["generation_risk"],
        "fallback_plan": fields["fallback_plan"],
        "video_model_note": fields["video_model_note"],
        "review_status": fields["review_status"],
        "expected_assets": {
            "image": f"images_gpt/{file_stem}.png",
            "kling_video": f"video_generations/kling/{file_stem}_v01.mp4",
            "seedance_video": f"video_generations/seedance/{file_stem}_v01.mp4",
            "grok_video": f"video_generations/grok/{file_stem}_v01.mp4",
            "tts_audio": f"final_tts_subtitles/{file_stem}.wav",
            "subtitle": f"final_tts_subtitles/{file_stem}.srt",
        },
    }


def _field(body: str, field_name: str) -> str:
    match = re.search(
        rf"^- {re.escape(field_name)}:[^\S\r\n]*(.*)$",
        body,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def _split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="검수 통과한 SHOT_PLAN을 shot_sync_map.json으로 변환합니다."
    )
    parser.add_argument("episode_dir", type=Path, help="처리할 에피소드 폴더")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="기존 shot_sync_map.json을 명시적으로 덮어씁니다.",
    )
    args = parser.parse_args()

    try:
        result = generate_shot_sync_map(args.episode_dir, overwrite=args.overwrite)
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(f"생성 실패: {error}")
        return 1

    print(f"생성 완료: {result.output_path}")
    print(f"컷 {result.cut_count}개, 총 {result.total_duration_seconds}초")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

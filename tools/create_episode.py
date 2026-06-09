from __future__ import annotations

import argparse
from pathlib import Path
import re


TEMPLATE_NAMES = (
    "EP##_DESIGN.md",
    "EP##_SCRIPT.md",
    "EP##_CHARACTER_BIBLE.md",
    "EP##_SHOT_PLAN.md",
    "EP##_IMAGE_PROMPTS.md",
)

LEAF_DIRECTORIES = (
    "reference_assets/characters",
    "reference_assets/locations",
    "images_gpt",
    "video_generations/kling",
    "video_generations/seedance",
    "video_generations/grok",
    "videos_grok_480p_6s",
    "final_tts_subtitles",
    "story_sync_audit",
    "DOWNLOAD_READY",
)

SUPPORT_GUIDES = {
    "reference_assets/README.md": """# {episode_id} 참조 자산 안내

캐릭터 참조 자료는 `characters`에, 장소 참조 자료는 `locations`에 저장합니다.

실존 인물의 얼굴, 목소리, 사진은 사용 권리를 확인한 뒤 저장합니다.
""",
    "video_generations/README.md": """# {episode_id} 모델별 영상 결과 안내

Kling 결과는 `kling`, Seedance 결과는 `seedance`, Grok 결과는 `grok` 폴더에 저장합니다.

같은 컷의 여러 후보는 `cut_001_v01.mp4`, `cut_001_v02.mp4`처럼 버전을 구분합니다.
""",
}


def normalize_episode_id(raw_episode_id: str) -> str:
    match = re.fullmatch(r"(?:EP)?(\d{1,3})", raw_episode_id.strip(), flags=re.IGNORECASE)
    if not match:
        raise ValueError("에피소드 번호는 2, EP2, EP02 같은 형식이어야 합니다.")
    episode_number = int(match.group(1))
    if episode_number < 1:
        raise ValueError("에피소드 번호는 1 이상이어야 합니다.")
    return f"EP{episode_number:02d}"


def create_episode(project_root: Path, raw_episode_id: str) -> Path:
    episode_id = normalize_episode_id(raw_episode_id)
    templates_dir = project_root / "templates"
    episode_dir = project_root / "episodes" / episode_id

    if episode_dir.exists():
        raise FileExistsError(f"에피소드 폴더가 이미 존재합니다: {episode_dir}")

    missing_templates = [
        template_name
        for template_name in TEMPLATE_NAMES
        if not (templates_dir / template_name).exists()
    ]
    if missing_templates:
        missing = ", ".join(missing_templates)
        raise FileNotFoundError(f"필수 템플릿이 없습니다: {missing}")

    episode_dir.mkdir(parents=True)

    for template_name in TEMPLATE_NAMES:
        source_path = templates_dir / template_name
        output_name = template_name.replace("EP##", episode_id)
        output_path = episode_dir / output_name
        content = source_path.read_text(encoding="utf-8-sig").replace("EP##", episode_id)
        output_path.write_text(content, encoding="utf-8-sig")

    for relative_dir in LEAF_DIRECTORIES:
        leaf_dir = episode_dir / relative_dir
        leaf_dir.mkdir(parents=True)
        (leaf_dir / ".gitkeep").touch()

    for relative_path, content_template in SUPPORT_GUIDES.items():
        guide_path = episode_dir / relative_path
        guide_path.write_text(
            content_template.format(episode_id=episode_id),
            encoding="utf-8-sig",
        )

    return episode_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="템플릿에서 새 에피소드 작업 폴더를 안전하게 만듭니다."
    )
    parser.add_argument("episode_id", help="새 에피소드 번호: 예) 2, EP2, EP02")
    args = parser.parse_args()

    try:
        episode_dir = create_episode(Path.cwd(), args.episode_id)
    except (ValueError, FileExistsError, FileNotFoundError) as error:
        print(f"생성 실패: {error}")
        return 1

    print(f"생성 완료: {episode_dir}")
    print("다음 작업: 생성된 DESIGN 문서부터 작성하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

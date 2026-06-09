import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.generate_shot_sync_map import generate_shot_sync_map


class GenerateShotSyncMapTests(unittest.TestCase):
    def test_ep01_sync_map_contains_six_ready_cuts(self) -> None:
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "shot_sync_map.json"

            result = generate_shot_sync_map(
                Path("episodes/EP01_sample"),
                output_path,
            )
            data = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(result.cut_count, 6)
        self.assertEqual(result.total_duration_seconds, 45)
        self.assertEqual(data["schema_version"], "1.0")
        self.assertEqual(data["episode_id"], "EP01")
        self.assertEqual(data["status"], "ready")
        self.assertEqual(data["summary"]["cut_count"], 6)
        self.assertEqual(data["summary"]["total_duration_seconds"], 45)
        self.assertEqual(data["cuts"][0]["cut_id"], "CUT_001")
        self.assertEqual(data["cuts"][0]["block"], "B01")
        self.assertEqual(data["cuts"][0]["planned_duration_seconds"], 7)
        self.assertEqual(data["cuts"][0]["review_status"], "ready_for_image_prompt")
        self.assertEqual(
            data["cuts"][0]["camera_movement"],
            "static camera with very slow push-in",
        )
        self.assertIn("읽을 수 있는 글자", data["cuts"][0]["forbidden_elements"])
        self.assertIn("김정애 캐릭터 참조", data["cuts"][0]["reference_assets"])
        self.assertIn("실존 인물 얼굴", data["cuts"][0]["rights_or_face_policy"])
        self.assertEqual(
            data["cuts"][0]["expected_assets"]["image"],
            "images_gpt/cut_001.png",
        )
        self.assertEqual(
            data["cuts"][0]["expected_assets"]["kling_video"],
            "video_generations/kling/cut_001_v01.mp4",
        )

    def test_episode_that_fails_validation_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "shot_sync_map.json"

            with self.assertRaisesRegex(ValueError, "자동 검수"):
                generate_shot_sync_map(Path("episodes/EP02"), output_path)

        self.assertFalse(output_path.exists())

    def test_existing_sync_map_requires_explicit_overwrite(self) -> None:
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "shot_sync_map.json"
            output_path.write_text('{"keep": true}', encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "이미 존재합니다"):
                generate_shot_sync_map(
                    Path("episodes/EP01_sample"),
                    output_path,
                )

            preserved = output_path.read_text(encoding="utf-8")

        self.assertEqual(preserved, '{"keep": true}')

    def test_blank_sync_required_field_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99"
            episode_dir.mkdir()
            (episode_dir / "EP99_SHOT_PLAN.md").write_text(
                "\n".join(
                    [
                        "# EP99_SHOT_PLAN",
                        "",
                        "### CUT_001",
                        "- block:",
                        "- purpose: A-roll",
                        "- scene_goal: 시작 장면",
                        "- characters: 인물",
                        "- location: 장소",
                        "- action: 행동",
                        "- dialogue_or_narration: 내레이션",
                        "- planned_duration: 5초",
                        "- target_video_model: undecided",
                        "- generation_mode: image_to_video_first_frame",
                        "- reference_assets: 인물 참조",
                        "- aspect_ratio: 16:9",
                        "- audio_plan: tts_only",
                        "- model_limit_note: 확인 필요",
                        "- rights_or_face_policy: 가상 인물",
                        "- generation_risk: low",
                        "- fallback_plan: 재생성",
                        "- review_status: ready_for_image_prompt",
                    ]
                ),
                encoding="utf-8-sig",
            )
            (episode_dir / "EP99_IMAGE_PROMPTS.md").write_text(
                "## CUT_001\n",
                encoding="utf-8-sig",
            )
            output_path = episode_dir / "story_sync_audit" / "shot_sync_map.json"

            with self.assertRaisesRegex(ValueError, "block"):
                generate_shot_sync_map(episode_dir, output_path)

        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()

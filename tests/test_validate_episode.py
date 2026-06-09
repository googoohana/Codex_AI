from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.validate_episode import validate_episode, write_review_report


class ValidateEpisodeTests(unittest.TestCase):
    def test_ep01_sample_is_ready_for_image_generation(self) -> None:
        episode_dir = Path("episodes/EP01_sample")

        result = validate_episode(episode_dir)

        self.assertTrue(result.ok)
        self.assertEqual(result.cut_count, 6)
        self.assertEqual(result.total_duration_seconds, 45)
        self.assertEqual(result.ready_cut_count, 6)
        self.assertEqual(result.image_prompt_count, 6)
        self.assertEqual(result.errors, [])

    def test_missing_model_readiness_fields_are_reported(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99_sample"
            episode_dir.mkdir()
            (episode_dir / "EP99_SHOT_PLAN.md").write_text(
                "\n".join(
                    [
                        "# EP99_SHOT_PLAN",
                        "",
                        "### CUT_001",
                        "",
                        "- planned_duration: 7초",
                        "- review_status: ready_for_image_prompt",
                    ]
                ),
                encoding="utf-8-sig",
            )

            result = validate_episode(episode_dir)

        self.assertFalse(result.ok)
        self.assertIn("CUT_001: target_video_model 항목이 없습니다.", result.errors)
        self.assertIn("CUT_001: rights_or_face_policy 항목이 없습니다.", result.errors)
        self.assertIn("CUT_001: fallback_plan 항목이 없습니다.", result.errors)

    def test_blank_model_readiness_fields_are_reported(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99_sample"
            episode_dir.mkdir()
            (episode_dir / "EP99_SHOT_PLAN.md").write_text(
                "\n".join(
                    [
                        "# EP99_SHOT_PLAN",
                        "",
                        "### CUT_001",
                        "",
                        "- planned_duration: 7초",
                        "- target_video_model:",
                        "- generation_mode: image_to_video_first_frame",
                        "- reference_assets: character",
                        "- aspect_ratio: 16:9",
                        "- audio_plan: tts_only",
                        "- model_limit_note: 확인 필요",
                        "- rights_or_face_policy:",
                        "- generation_risk: low",
                        "- fallback_plan:",
                        "- review_status: ready_for_image_prompt",
                        "",
                        "## 모델 관련 필드 설명",
                        "",
                        "- target_video_model: Kling, Seedance 중 하나",
                        "- rights_or_face_policy: 권리 확인 내용을 적는다",
                        "- fallback_plan: 실패 시 대응을 적는다",
                    ]
                ),
                encoding="utf-8-sig",
            )

            result = validate_episode(episode_dir)

        self.assertIn("CUT_001: target_video_model 항목이 없습니다.", result.errors)
        self.assertIn("CUT_001: rights_or_face_policy 항목이 없습니다.", result.errors)
        self.assertIn("CUT_001: fallback_plan 항목이 없습니다.", result.errors)

    def test_review_report_is_written_in_korean(self) -> None:
        with TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "review.md"

            result = write_review_report(Path("episodes/EP01_sample"), report_path)
            report = report_path.read_text(encoding="utf-8-sig")

        self.assertTrue(result.ok)
        self.assertIn("# EP01_sample 자동 검수 리포트", report)
        self.assertIn("- 판정: 통과", report)
        self.assertIn("- SHOT_PLAN 컷 수: 6", report)
        self.assertIn("- IMAGE_PROMPTS 수: 6", report)
        self.assertIn("- 계획 영상 길이: 45초", report)

    def test_shot_plan_without_cuts_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99_sample"
            episode_dir.mkdir()
            (episode_dir / "EP99_SHOT_PLAN.md").write_text(
                "# EP99_SHOT_PLAN\n",
                encoding="utf-8-sig",
            )
            (episode_dir / "EP99_IMAGE_PROMPTS.md").write_text(
                "# EP99_IMAGE_PROMPTS\n",
                encoding="utf-8-sig",
            )

            result = validate_episode(episode_dir)

        self.assertFalse(result.ok)
        self.assertIn("SHOT_PLAN에 CUT 항목이 없습니다.", result.errors)


if __name__ == "__main__":
    unittest.main()

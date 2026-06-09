from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.generate_cut_list import generate_cut_list, parse_script_blocks


class GenerateCutListTests(unittest.TestCase):
    def test_ep01_explicit_cut_links_create_six_cut_drafts(self) -> None:
        script_path = Path("episodes/EP01_sample/EP01_SCRIPT.md")

        blocks = parse_script_blocks(script_path)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0].block_id, "B01")
        self.assertEqual(blocks[0].duration_seconds, 14)
        self.assertEqual(blocks[0].cut_ids, ("CUT_001", "CUT_002"))
        self.assertEqual(sum(len(block.cut_ids) for block in blocks), 6)

    def test_missing_cut_links_are_marked_for_manual_split(self) -> None:
        with TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "EP99_SCRIPT.md"
            script_path.write_text(
                "\n".join(
                    [
                        "# EP99_SCRIPT",
                        "",
                        "### B01 시작",
                        "",
                        "- 블록 목적: 이야기를 시작한다",
                        "- 예상 길이: 8초",
                        "- 내레이션: 첫 장면입니다.",
                    ]
                ),
                encoding="utf-8-sig",
            )

            blocks = parse_script_blocks(script_path)

        self.assertEqual(blocks[0].cut_ids, ())
        self.assertTrue(blocks[0].needs_manual_split)
        self.assertEqual(blocks[0].title, "시작")

    def test_blank_block_title_does_not_capture_next_field(self) -> None:
        with TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "EP99_SCRIPT.md"
            script_path.write_text(
                "### B01\n\n- 블록 목적: 시작 장면\n",
                encoding="utf-8-sig",
            )

            blocks = parse_script_blocks(script_path)

        self.assertEqual(blocks[0].title, "")
        self.assertEqual(blocks[0].purpose, "시작 장면")

    def test_cut_list_markdown_is_written_without_overwriting_shot_plan(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99"
            episode_dir.mkdir()
            (episode_dir / "EP99_SCRIPT.md").write_text(
                "\n".join(
                    [
                        "# EP99_SCRIPT",
                        "",
                        "## B01 시작",
                        "",
                        "- 블록 목적: 시작 장면",
                        "- 예상 길이: 8초",
                        "- 대응 컷: CUT_001, CUT_002",
                        "- 내레이션: 첫 장면입니다.",
                    ]
                ),
                encoding="utf-8-sig",
            )
            shot_plan_path = episode_dir / "EP99_SHOT_PLAN.md"
            shot_plan_path.write_text("SHOT PLAN KEEP", encoding="utf-8-sig")
            output_path = episode_dir / "story_sync_audit" / "CUT_LIST_DRAFT.md"

            result = generate_cut_list(episode_dir, output_path)
            output = output_path.read_text(encoding="utf-8-sig")
            preserved_shot_plan = shot_plan_path.read_text(encoding="utf-8-sig")

        self.assertEqual(result.cut_count, 2)
        self.assertEqual(result.manual_split_block_count, 0)
        self.assertIn("# EP99 컷 목록 초안", output)
        self.assertIn("| CUT_001 | B01 |", output)
        self.assertIn("| CUT_002 | B01 |", output)
        self.assertEqual(preserved_shot_plan, "SHOT PLAN KEEP")

    def test_existing_output_requires_explicit_overwrite(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99"
            episode_dir.mkdir()
            (episode_dir / "EP99_SCRIPT.md").write_text(
                "## B01\n- 블록 목적: 시작\n- 예상 길이: 5초\n- 내레이션: 시작\n",
                encoding="utf-8-sig",
            )
            output_path = episode_dir / "story_sync_audit" / "CUT_LIST_DRAFT.md"
            output_path.parent.mkdir()
            output_path.write_text("KEEP", encoding="utf-8-sig")

            with self.assertRaisesRegex(FileExistsError, "이미 존재합니다"):
                generate_cut_list(episode_dir, output_path)

    def test_duplicate_explicit_cut_ids_are_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP99"
            episode_dir.mkdir()
            (episode_dir / "EP99_SCRIPT.md").write_text(
                "\n".join(
                    [
                        "## B01 시작",
                        "- 대응 컷: CUT_001",
                        "",
                        "## B02 다음",
                        "- 대응 컷: CUT_001",
                    ]
                ),
                encoding="utf-8-sig",
            )

            with self.assertRaisesRegex(ValueError, "중복"):
                generate_cut_list(episode_dir)


if __name__ == "__main__":
    unittest.main()

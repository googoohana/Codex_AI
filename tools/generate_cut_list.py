from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class ScriptBlock:
    block_id: str
    title: str
    purpose: str
    duration_seconds: int | None
    narration: str
    cut_ids: tuple[str, ...]

    @property
    def needs_manual_split(self) -> bool:
        return not self.cut_ids


@dataclass(frozen=True)
class CutListResult:
    block_count: int
    cut_count: int
    manual_split_block_count: int
    output_path: Path


def parse_script_blocks(script_path: Path) -> list[ScriptBlock]:
    if not script_path.exists():
        raise FileNotFoundError(f"SCRIPT 파일이 없습니다: {script_path}")

    text = script_path.read_text(encoding="utf-8-sig")
    headings = list(
        re.finditer(
            r"^#{2,3}[^\S\r\n]+(B\d{2,3})(?:[^\S\r\n]+([^\r\n]+))?[^\S\r\n]*$",
            text,
            flags=re.MULTILINE,
        )
    )
    blocks: list[ScriptBlock] = []

    for heading in headings:
        next_heading = re.search(
            r"^#{2,3}\s+\S+",
            text[heading.end() :],
            flags=re.MULTILINE,
        )
        end = heading.end() + next_heading.start() if next_heading else len(text)
        body = text[heading.end() : end]
        duration_match = re.search(r"^- 예상 길이:\s*(\d+)초", body, flags=re.MULTILINE)
        cuts_match = re.search(r"^- 대응 컷:\s*(.+)$", body, flags=re.MULTILINE)
        cut_ids = (
            tuple(re.findall(r"CUT_\d{3}", cuts_match.group(1)))
            if cuts_match
            else ()
        )
        blocks.append(
            ScriptBlock(
                block_id=heading.group(1),
                title=(heading.group(2) or "").strip(),
                purpose=_field_value(body, "블록 목적"),
                duration_seconds=int(duration_match.group(1)) if duration_match else None,
                narration=_field_value(body, "내레이션"),
                cut_ids=cut_ids,
            )
        )

    if not blocks:
        raise ValueError("SCRIPT에 B01 같은 대본 블록이 없습니다.")

    return blocks


def generate_cut_list(
    episode_dir: Path,
    output_path: Path | None = None,
    *,
    overwrite: bool = False,
) -> CutListResult:
    episode_id = episode_dir.name.replace("_sample", "")
    script_path = episode_dir / f"{episode_id}_SCRIPT.md"
    output_path = output_path or (
        episode_dir / "story_sync_audit" / "CUT_LIST_DRAFT.md"
    )

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"컷 목록 초안이 이미 존재합니다: {output_path}")

    blocks = parse_script_blocks(script_path)
    explicit_cut_ids = [
        cut_id
        for block in blocks
        for cut_id in block.cut_ids
    ]
    duplicate_cut_ids = sorted(
        {
            cut_id
            for cut_id in explicit_cut_ids
            if explicit_cut_ids.count(cut_id) > 1
        }
    )
    if duplicate_cut_ids:
        duplicates = ", ".join(duplicate_cut_ids)
        raise ValueError(f"대응 컷 ID가 중복되었습니다: {duplicates}")

    rows: list[str] = []
    manual_split_blocks: list[str] = []
    cut_count = 0

    for block in blocks:
        if block.cut_ids:
            cut_ids = block.cut_ids
            status = "대응 컷 확인 필요"
        else:
            cut_ids = (f"DRAFT_{block.block_id}_01",)
            status = "수동 분할 필요"
            manual_split_blocks.append(block.block_id)

        for cut_id in cut_ids:
            cut_count += 1
            rows.append(
                f"| {cut_id} | {block.block_id} | {_cell(block.title)} | "
                f"{_cell(block.purpose)} | {_duration(block.duration_seconds)} | "
                f"{_cell(block.narration)} | {status} |"
            )

    report = "\n".join(
        [
            f"# {episode_id} 컷 목록 초안",
            "",
            "## 요약",
            "",
            f"- 대본 블록 수: {len(blocks)}",
            f"- 컷 초안 수: {cut_count}",
            f"- 수동 분할 필요 블록 수: {len(manual_split_blocks)}",
            "- 주의: 이 파일은 SHOT_PLAN이 아니라 사람이 검토할 초안입니다.",
            "",
            "## 컷 목록",
            "",
            "| 컷 ID | 블록 | 블록 제목 | 블록 목적 | 블록 예상 길이 | 내레이션 | 검토 상태 |",
            "|---|---|---|---|---:|---|---|",
            *rows,
            "",
            "## 다음 작업",
            "",
            "1. 한 블록에 여러 장면이 필요한지 사람이 판단합니다.",
            "2. 컷 ID와 컷 수를 확정합니다.",
            "3. 확정된 컷을 SHOT_PLAN에 작성합니다.",
            "4. SHOT_PLAN 자동 검수를 실행합니다.",
            "",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8-sig")

    return CutListResult(
        block_count=len(blocks),
        cut_count=cut_count,
        manual_split_block_count=len(manual_split_blocks),
        output_path=output_path,
    )


def _field_value(body: str, field_name: str) -> str:
    match = re.search(
        rf"^- {re.escape(field_name)}:[^\S\r\n]*(.*)$",
        body,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def _cell(value: str) -> str:
    return value.replace("|", "/").strip() or "미작성"


def _duration(value: int | None) -> str:
    return f"{value}초" if value is not None else "미작성"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SCRIPT의 대본 블록을 읽어 컷 목록 초안을 만듭니다."
    )
    parser.add_argument("episode_dir", type=Path, help="검사할 에피소드 폴더")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="기존 CUT_LIST_DRAFT.md를 명시적으로 덮어씁니다.",
    )
    args = parser.parse_args()

    try:
        result = generate_cut_list(args.episode_dir, overwrite=args.overwrite)
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(f"생성 실패: {error}")
        return 1

    print(f"생성 완료: {result.output_path}")
    print(f"블록 {result.block_count}개, 컷 초안 {result.cut_count}개")
    print(f"수동 분할 필요 블록: {result.manual_split_block_count}개")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

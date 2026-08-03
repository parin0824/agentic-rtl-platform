from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    description: str
    original: str
    replacement: str


MUTATIONS = (
    Mutation("full_guard_removed", "Allow writes while full", "wr_en && !full", "wr_en"),
    Mutation("empty_guard_removed", "Allow reads while empty", "rd_en && !empty", "rd_en"),
    Mutation("full_flag_inverted", "Invert the full flag", "full <= full_next;", "full <= !full_next;"),
    Mutation("empty_flag_inverted", "Invert the empty flag", "empty <= empty_next;", "empty <= !empty_next;"),
    Mutation("write_sync_bypassed", "Bypass one read-pointer synchronizer stage", "rd_gray_sync2 <= rd_gray_sync1;", "rd_gray_sync2 <= rd_gray;"),
)


def create_mutants(source: Path, output_dir: Path) -> list[Path]:
    text = source.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []
    for mutation in MUTATIONS:
        if mutation.original not in text:
            raise ValueError(f"Mutation target not found: {mutation.mutation_id}")
        target = output_dir / f"{mutation.mutation_id}.sv"
        target.write_text(text.replace(mutation.original, mutation.replacement, 1), encoding="utf-8")
        generated.append(target)
    return generated

"""Reliable local JSON persistence for the habit tracker."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class LoadResult:
    data: dict[str, Any]
    recovered_from_error: bool = False
    warnings: list[str] = field(default_factory=list)


class Storage:
    """Read and atomically write the application's local JSON file."""

    def __init__(self, file_path: str | os.PathLike[str]):
        self.file_path = Path(file_path)

    def load(self) -> LoadResult:
        if not self.file_path.exists():
            self.save({"habits": []})
            return LoadResult(data={"habits": []})

        try:
            raw_text = self.file_path.read_text(encoding="utf-8")
        except OSError as exc:
            return LoadResult(
                data={"habits": []},
                recovered_from_error=True,
                warnings=[f"Could not read the data file ({exc}). Starting fresh."],
            )

        if not raw_text.strip():
            backup = self._quarantine("empty file")
            return LoadResult(
                data={"habits": []},
                recovered_from_error=True,
                warnings=[backup],
            )

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            backup = self._quarantine(f"invalid JSON ({exc.msg} at line {exc.lineno})")
            return LoadResult(data={"habits": []}, recovered_from_error=True, warnings=[backup])

        if not isinstance(parsed, dict) or not isinstance(parsed.get("habits"), list):
            backup = self._quarantine('unexpected structure (expected {"habits": [...]})')
            return LoadResult(data={"habits": []}, recovered_from_error=True, warnings=[backup])

        return LoadResult(data=parsed)

    def save(self, data: dict[str, Any]) -> None:
        """Write JSON atomically so an interrupted save doesn't truncate the old file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path_str = tempfile.mkstemp(
            prefix=".habits_tmp_", suffix=".json", dir=str(self.file_path.parent)
        )
        tmp_path = Path(tmp_path_str)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as tmp_file:
                json.dump(data, tmp_file, indent=2, ensure_ascii=False)
                tmp_file.write("\n")
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            os.replace(tmp_path, self.file_path)
        except Exception:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            raise

    def _quarantine(self, reason: str) -> str:
        """Move an unreadable file aside instead of deleting it."""
        backup_path = self.file_path.with_suffix(".corrupted.bak")
        counter = 1
        while backup_path.exists():
            backup_path = self.file_path.with_suffix(f".corrupted.{counter}.bak")
            counter += 1
        try:
            self.file_path.rename(backup_path)
            return (
                f"The data file was invalid ({reason}). "
                f"It was backed up to '{backup_path.name}' and a fresh file will be used."
            )
        except OSError:
            return f"The data file was invalid ({reason}). A fresh file will be used."

"""Small helpers shared across the CLI and domain layer."""

from __future__ import annotations

import uuid
from datetime import date, datetime

DATE_FORMAT = "%Y-%m-%d"
BOX_WIDTH = 50


def today_str() -> str:
    return date.today().strftime(DATE_FORMAT)


def parse_date(date_str: str) -> date:
    """Parse an ISO YYYY-MM-DD date."""
    return datetime.strptime(date_str, DATE_FORMAT).date()


def clean_text(value: str) -> str:
    """Trim surrounding whitespace and collapse internal whitespace."""
    return " ".join(value.strip().split())


def is_blank(value: str) -> bool:
    return not clean_text(value)


def generate_habit_id() -> str:
    """Generate a short random identifier for a local habit."""
    return uuid.uuid4().hex[:8]


def banner(title: str, subtitle: str = "") -> str:
    top = "╔" + "═" * BOX_WIDTH + "╗"
    bottom = "╚" + "═" * BOX_WIDTH + "╝"
    lines = [top, "║" + title.center(BOX_WIDTH) + "║"]
    if subtitle:
        lines.append("║" + subtitle.center(BOX_WIDTH) + "║")
    lines.append(bottom)
    return "\n".join(lines)


def divider(char: str = "-", width: int = BOX_WIDTH + 2) -> str:
    return char * width


def ok(message: str) -> str:
    return f"[OK]    {message}"


def warn(message: str) -> str:
    return f"[!]     {message}"


def fail(message: str) -> str:
    return f"[ERROR] {message}"


def note(message: str) -> str:
    return f"[INFO]  {message}"

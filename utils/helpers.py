import json
import random
import string
from pathlib import Path
from typing import Any


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def is_sorted_asc(values: list) -> bool:
    return values == sorted(values)


def is_sorted_desc(values: list) -> bool:
    return values == sorted(values, reverse=True)


def parse_price(text: str | None) -> float:
    """'$29.99' ou 'Item total: $29.99' -> 29.99"""
    return float("".join(c for c in (text or "") if c.isdigit() or c == "."))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

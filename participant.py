"""Participant ID generation and random group assignment."""

import random
import re
from pathlib import Path

from config import DATA_DIR, GROUPS


def get_next_participant_id() -> str:
    """Scan data/ for existing CSVs and return the next participant ID."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = set()
    pattern = re.compile(r"participant_(\d+)\.csv")
    for f in DATA_DIR.iterdir():
        m = pattern.match(f.name)
        if m:
            existing.add(int(m.group(1)))
    next_id = max(existing) + 1 if existing else 1
    return f"participant_{next_id:03d}"


def assign_group() -> str:
    """Randomly assign to one of the three experimental groups."""
    random.seed()  # re-seed from OS entropy each call
    return random.choice(GROUPS)


def get_csv_path(participant_id: str) -> Path:
    return DATA_DIR / f"{participant_id}.csv"

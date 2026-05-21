"""CSV data persistence for experiment rounds."""

import csv
from pathlib import Path

from config import DATA_DIR


CSV_HEADER = ["participant_id", "experimental_group", "round", "role", "content", "timestamp"]


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_round(
    participant_id: str,
    group: str,
    round_num: int,
    role: str,
    content: str,
    timestamp: str,
) -> None:
    csv_path = DATA_DIR / f"{participant_id}.csv"
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(CSV_HEADER)
        writer.writerow([participant_id, group, round_num, role, content, timestamp])

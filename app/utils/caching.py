"""
Tiny TTL cache using the filesystem. Shows dicts, file I/O, and conditionals.
"""
import json
import time
from pathlib import Path
from typing import Any


def _cache_file(cache_dir: Path, key: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    safe_key = key.replace("/", "_")
    return cache_dir / f"{safe_key}.json"


def write_cache(cache_dir: Path, key: str, payload: dict) -> None:
    data = {"saved_at": time.time(), "payload": payload}
    file_path = _cache_file(cache_dir, key)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def read_cache(cache_dir: Path, key: str, ttl_seconds: int) -> Any | None:
    file_path = _cache_file(cache_dir, key)
    if not file_path.exists():
        return None
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    saved_at = data.get("saved_at")
    if saved_at is None:
        return None
    is_fresh = (time.time() - saved_at) <= ttl_seconds
    if is_fresh:
        return data.get("payload")
    return None

"""Preflight helpers for the Strata-free Kaggle launcher."""
from __future__ import annotations

import os
import shutil
from pathlib import Path


def disk_report(paths: list[str] | None = None) -> list[dict[str, object]]:
    paths = paths or ["/kaggle/working", "/kaggle/input", "/dev/shm", "/tmp"]
    report: list[dict[str, object]] = []
    for raw in paths:
        path = Path(raw)
        row: dict[str, object] = {"path": raw, "exists": path.exists()}
        if path.exists():
            try:
                usage = shutil.disk_usage(path)
                row.update(total_gib=round(usage.total / 2**30, 2),
                           used_gib=round(usage.used / 2**30, 2),
                           free_gib=round(usage.free / 2**30, 2))
            except OSError as exc:
                row["disk_usage_error"] = repr(exc)
            row["writable_probe"] = False
            try:
                probe = path / f".qwen-api-write-test-{os.getpid()}"
                with probe.open("wb") as f:
                    f.write(b"ok")
                    f.flush()
                    os.fsync(f.fileno())
                probe.unlink(missing_ok=True)
                row["writable_probe"] = True
            except OSError as exc:
                row["write_error"] = repr(exc)
        report.append(row)
    return report


def find_gguf_files(root: str = "/kaggle/input") -> list[Path]:
    base = Path(root)
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*.gguf") if p.is_file())


def validate_split_candidates(files: list[Path]) -> list[Path]:
    """Return likely first shards; llama-server can resolve sibling split shards."""
    return [p for p in files if "-00001-of-" in p.name]

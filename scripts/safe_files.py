"""외부 모델로 보낼 파일을 거른다. 애매하면 뺀다."""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DATA_DIRS = {"data", "raw", "output", "outputs", "results"}
DATA_EXTS = {".csv", ".parquet", ".xlsx", ".xls", ".feather", ".pkl", ".npy", ".npz", ".h5", ".db", ".sqlite"}
MAX_BYTES = 1_000_000
SECRET_PATTERNS = [
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(rb"ghp_[A-Za-z0-9]{30,}"),
]
BAN_PATTERNS = [
    re.compile(r"외부\s*AI.{0,10}(금지|불가)"),
    re.compile(r"업로드\s*금지"),
    re.compile(r"(not|never).{0,40}generative AI|generative AI.{0,40}(not|prohibited|forbidden)", re.I),
]


@dataclass
class Decision:
    path: str
    allowed: bool
    reason: str


def _reason(p: Path, root: Path) -> str:
    if p.is_symlink():
        return "symlink"
    try:
        parts = p.resolve().relative_to(root.resolve()).parts
    except ValueError:
        parts = p.parts
    if any(part.lower() in DATA_DIRS for part in parts[:-1]):
        return "data-dir"
    if p.name == ".env" or p.name.startswith(".env."):
        return "env"
    if p.suffix.lower() in DATA_EXTS:
        return "data-ext"
    if not p.is_file():
        return "not-file"
    if p.stat().st_size > MAX_BYTES:
        return "too-large"
    try:
        raw = p.read_bytes()
    except OSError:
        return "unreadable"
    if b"\x00" in raw:
        return "binary"
    if any(pat.search(raw) for pat in SECRET_PATTERNS):
        return "secret"
    return "ok"


def select(paths: list[Path], root: Path) -> list[Decision]:
    out = []
    for p in paths:
        try:
            rel = str(p.relative_to(root))
        except ValueError:
            rel = str(p)
        reason = _reason(p, root) if (p.exists() or p.is_symlink()) else "missing"
        out.append(Decision(rel, reason == "ok", reason))
    return out


def external_banned(root: Path, extra_texts: list[str] | None = None) -> bool:
    texts = list(extra_texts or [])
    for name in ("CLAUDE.md", "AGENTS.md"):
        f = root / name
        if f.is_file():
            texts.append(f.read_text(encoding="utf-8", errors="ignore"))
    return any(pat.search(t) for t in texts for pat in BAN_PATTERNS)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("files", nargs="*", type=Path)
    args = ap.parse_args(argv)
    for d in select([f if f.is_absolute() else args.root / f for f in args.files], args.root):
        if d.allowed:
            print(d.path)
        else:
            print(f"skip {d.path} ({d.reason})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

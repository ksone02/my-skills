"""rules/always.md의 상시 원칙 블록을 CLAUDE.md에 넣고 뺀다. 블록 바깥은 건드리지 않는다."""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

START = "<!-- my-skills:always:start -->"
END = "<!-- my-skills:always:end -->"
BLOCK_RE = re.compile(r"\n?\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
DEFAULT_RULES = Path(__file__).resolve().parents[1] / "rules" / "always.md"


def block_text(rules_path: Path) -> str:
    text = rules_path.read_text(encoding="utf-8")
    m = re.search(re.escape(START) + r".*?" + re.escape(END), text, re.S)
    if not m:
        raise ValueError(f"no always block in {rules_path}")
    return m.group(0)


def _write(target: Path, text: str) -> None:
    target = target.resolve()  # 심볼릭 링크면 원본 파일에 쓴다
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o644
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".always-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(tmp, mode)
    os.replace(tmp, target)


def install(target: Path, rules_path: Path = DEFAULT_RULES) -> str:
    block = block_text(rules_path)
    old = target.read_text(encoding="utf-8") if target.exists() else None
    if old is None:
        _write(target, block + "\n")
        return "installed"
    if START in old:
        current = re.search(re.escape(START) + r".*?" + re.escape(END), old, re.S).group(0)
        if current == block:
            return "unchanged"
        _write(target, old.replace(current, block))
        return "updated"
    sep = "" if old.endswith("\n\n") or old == "" else ("\n" if old.endswith("\n") else "\n\n")
    _write(target, old + sep + block + "\n")
    return "installed"


def remove(target: Path) -> str:
    if not target.exists():
        return "absent"
    old = target.read_text(encoding="utf-8")
    if START not in old:
        return "absent"
    new = BLOCK_RE.sub("\n", old, count=1)
    new = new.rstrip("\n") + "\n" if new.strip() else ""
    _write(target, new)
    return "removed"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["install", "remove"])
    ap.add_argument("--target", type=Path, default=Path.home() / ".claude" / "CLAUDE.md")
    args = ap.parse_args(argv)
    result = install(args.target) if args.action == "install" else remove(args.target)
    print(f"{result}: {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

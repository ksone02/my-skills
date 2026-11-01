"""Claude Code 세션 기록(jsonl)의 토큰 사용량을 합친다. 캐시 읽기와 쓰기는 따로 센다."""

import argparse
import json
import sys
from pathlib import Path

KEYS = ["input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"]


def _messages(path: Path) -> dict[str, tuple[str, dict]]:
    last: dict[str, tuple[str, dict]] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        msg = row.get("message") if isinstance(row, dict) else None
        if not isinstance(msg, dict) or not isinstance(msg.get("usage"), dict):
            continue
        key = msg.get("id") or f"line-{len(last)}"
        last[key] = (msg.get("model", "unknown"), msg["usage"])  # 스트리밍 조각은 마지막 값이 최종
    return last


def totals(path: Path) -> dict:
    out: dict = {k: 0 for k in KEYS} | {"turns": 0, "by_model": {}}
    for model, usage in _messages(path).values():
        m = out["by_model"].setdefault(model, {k: 0 for k in KEYS} | {"turns": 0})
        for k in KEYS:
            v = int(usage.get(k) or 0)
            out[k] += v
            m[k] += v
        out["turns"] += 1
        m["turns"] += 1
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args(argv)
    print("file | turns | input | output | cache_read | cache_write")
    for f in args.files:
        t = totals(f)
        print(f"{f.name} | {t['turns']} | {t['input_tokens']} | {t['output_tokens']} | "
              f"{t['cache_read_input_tokens']} | {t['cache_creation_input_tokens']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

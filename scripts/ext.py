"""외부 모델(Codex, DeepSeek via aside) 호출. 실패해도 예외 대신 상태를 돌려준다."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

import safe_files

ROOT = Path(__file__).resolve().parents[1]
LIMIT_RE = re.compile(r"rate limit|usage limit|quota|\b429\b", re.I)


@dataclass
class Result:
    status: str  # "ok" | "unavailable" | "banned"
    text: str
    reason: str
    seconds: float


def _log(tool: str, r: Result, skipped: list[str]) -> None:
    path = Path(os.environ.get("MY_SKILLS_LOG", ROOT / "evals" / "results" / "ext-calls.jsonl"))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": tool, "status": r.status, "reason": r.reason,
               "seconds": round(r.seconds, 2), "out_chars": len(r.text), "skipped_files": skipped}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass  # 기록 실패가 호출 결과를 바꾸면 안 된다


def _run(cmd: list[str], stdin: str | None, cwd: Path, timeout: int, out_file: Path | None = None) -> Result:
    start = time.monotonic()
    if shutil.which(cmd[0]) is None:
        return Result("unavailable", "", f"{cmd[0]} not found", 0.0)
    try:
        p = subprocess.run(cmd, input=stdin, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                           stdin=None if stdin is not None else subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return Result("unavailable", "", "timeout", time.monotonic() - start)
    except OSError as e:
        return Result("unavailable", "", f"os error: {e}", time.monotonic() - start)
    secs = time.monotonic() - start
    text = p.stdout
    if out_file and out_file.exists() and out_file.read_text().strip():
        text = out_file.read_text()
    if p.returncode != 0:
        return Result("unavailable", text, f"exit {p.returncode}: {p.stderr.strip()[:200]}", secs)
    m = LIMIT_RE.search(text + p.stderr)
    if m:
        return Result("unavailable", text, f"limit: {m.group(0)}", secs)
    return Result("ok", text, "", secs)


def ask_codex(prompt: str, files: list[Path], root: Path, timeout: int = 900) -> Result:
    decisions = safe_files.select(files, root)
    skipped = [d.path for d in decisions if not d.allowed]
    if safe_files.external_banned(root):
        r = Result("banned", "", "external AI banned in project", 0.0)
        _log("codex", r, skipped)
        return r
    allowed = [d.path for d in decisions if d.allowed]
    full = prompt + ("\n\n파일:\n" + "\n".join(f"- {a}" for a in allowed) if allowed else "")
    binary = os.environ.get("MY_SKILLS_CODEX", "codex")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "last.txt"
        cmd = [binary, "exec", "--skip-git-repo-check", "-s", "read-only", "-C", str(root), "-o", str(out), "-"]
        r = _run(cmd, full, root, timeout, out)
    _log("codex", r, skipped)
    return r


def ask_deepseek(prompt: str, root: Path, model: str = "deepseek/deepseek-v4-pro", timeout: int = 900) -> Result:
    if safe_files.external_banned(root):
        r = Result("banned", "", "external AI banned in project", 0.0)
        _log("deepseek", r, [])
        return r
    binary = os.environ.get("MY_SKILLS_ASIDE", "aside")
    r = _run([binary, "-m", model, prompt], None, root, timeout)
    _log("deepseek", r, [])
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tool", choices=["codex", "deepseek"])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--prompt-file", type=Path, required=True)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("files", nargs="*", type=Path)
    args = ap.parse_args(argv)
    prompt = args.prompt_file.read_text(encoding="utf-8")
    if args.tool == "codex":
        files = [f if f.is_absolute() else args.root / f for f in args.files]
        r = ask_codex(prompt, files, args.root, args.timeout)
    else:
        r = ask_deepseek(prompt, args.root, timeout=args.timeout)
    print(f"STATUS: {r.status}" + (f" ({r.reason})" if r.reason else ""))
    print(r.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""PreToolUse(Bash) 훅. 상태 파일이 있을 때만 위험 명령에서 확인을 요청한다. 어떤 실패도 세션을 막지 않는다."""

import json
import os
import re
import sys
from pathlib import Path

RISKY = [
    (r"git\s+push\b.*\b(main|master)\b", "운영 브랜치로 푸시"),
    (r"git\s+push\b.*(--force|-f\b)", "강제 푸시"),
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r", "rm -rf"),
    (r"git\s+reset\s+--hard", "git reset --hard"),
    (r"\b(cat|less|head|tail)\b.*\.(env|pem)\b", "비밀키 파일 읽기"),
    (r"^\s*(ssh|scp)\s", "원격 서버 접속"),
    (r"vercel\b.*--prod", "운영 배포"),
    (r"drop\s+table", "DROP TABLE"),
]


def state_file() -> Path:
    return Path(os.environ.get("MY_SKILLS_GUARD_FILE", Path.home() / ".claude" / "my-skills-guard.on"))


def check(command: str) -> str | None:
    for pattern, label in RISKY:
        if re.search(pattern, command, re.I | re.M):
            return label
    return None


def main() -> int:
    if not state_file().exists():
        return 0
    try:
        command = json.load(sys.stdin)["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0
    label = check(command)
    if label:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"my-skills guard: {label}",
        }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # 훅 오류로 세션을 깨지 않는다
        sys.exit(0)

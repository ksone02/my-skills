import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "hooks" / "guard.py"


def run(tmp_path, stdin, on=True):
    state = tmp_path / "guard.on"
    if on:
        state.touch()
    p = subprocess.run([sys.executable, str(GUARD)], input=stdin, capture_output=True, text=True,
                       env={"MY_SKILLS_GUARD_FILE": str(state), "PATH": "/usr/bin:/bin"})
    return p.returncode, p.stdout.strip()


def payload(cmd):
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})


def test_off_does_nothing(tmp_path):
    assert run(tmp_path, payload("rm -rf /"), on=False) == (0, "")


def test_on_risky_asks(tmp_path):
    code, out = run(tmp_path, payload("rm -rf build"))
    assert code == 0
    h = json.loads(out)["hookSpecificOutput"]
    assert h["hookEventName"] == "PreToolUse" and h["permissionDecision"] == "ask"
    assert h["permissionDecisionReason"].startswith("my-skills guard:")


def test_on_safe_silent(tmp_path):
    assert run(tmp_path, payload("ls -la")) == (0, "")


def test_bad_json_silent(tmp_path):
    assert run(tmp_path, "not json") == (0, "")


def test_push_main_asks(tmp_path):
    assert json.loads(run(tmp_path, payload("git push origin main"))[1])

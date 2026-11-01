import json
import stat

import ext


def fake(tmp_path, name, script):
    p = tmp_path / name
    p.write_text("#!/bin/sh\n" + script + "\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)
    return str(p)


def setup(tmp_path, monkeypatch, script, tool="MY_SKILLS_CODEX"):
    log = tmp_path / "log.jsonl"
    monkeypatch.setenv("MY_SKILLS_LOG", str(log))
    monkeypatch.setenv(tool, fake(tmp_path, "bin", script))
    root = tmp_path / "repo"
    root.mkdir()
    return root, log


def test_codex_ok_and_logged(tmp_path, monkeypatch):
    root, log = setup(tmp_path, monkeypatch, "cat >/dev/null; echo hello")
    r = ext.ask_codex("q", [], root)
    assert (r.status, r.text.strip()) == ("ok", "hello")
    rows = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["tool"] == "codex" and rows[0]["status"] == "ok"


def test_missing_binary(tmp_path, monkeypatch):
    monkeypatch.setenv("MY_SKILLS_LOG", str(tmp_path / "l"))
    monkeypatch.setenv("MY_SKILLS_CODEX", str(tmp_path / "nope"))
    r = ext.ask_codex("q", [], tmp_path)
    assert r.status == "unavailable" and "not found" in r.reason


def test_timeout(tmp_path, monkeypatch):
    root, _ = setup(tmp_path, monkeypatch, "sleep 5")
    r = ext.ask_codex("q", [], root, timeout=1)
    assert r.status == "unavailable" and r.reason == "timeout"


def test_nonzero_exit(tmp_path, monkeypatch):
    root, _ = setup(tmp_path, monkeypatch, "cat >/dev/null; exit 1")
    assert ext.ask_codex("q", [], root).status == "unavailable"


def test_usage_limit_text(tmp_path, monkeypatch):
    root, _ = setup(tmp_path, monkeypatch, "cat >/dev/null; echo 'Error: usage limit reached'")
    r = ext.ask_codex("q", [], root)
    assert r.status == "unavailable" and "limit" in r.reason


def test_banned_project_never_calls(tmp_path, monkeypatch):
    marker = tmp_path / "called"
    root, _ = setup(tmp_path, monkeypatch, f"touch {marker}; echo hi")
    (root / "CLAUDE.md").write_text("외부 AI 업로드 금지", encoding="utf-8")
    assert ext.ask_codex("q", [], root).status == "banned"
    assert not marker.exists()


def test_data_files_skipped(tmp_path, monkeypatch):
    seen = tmp_path / "prompt.txt"
    root, log = setup(tmp_path, monkeypatch, f"cat > {seen}; echo ok")
    (root / "data").mkdir()
    (root / "data/x.csv").write_text("a,b")
    (root / "app.py").write_text("print(1)")
    ext.ask_codex("q", [root / "data/x.csv", root / "app.py"], root)
    prompt = seen.read_text()
    assert "app.py" in prompt and "x.csv" not in prompt
    assert json.loads(log.read_text())["skipped_files"] == ["data/x.csv"]


def test_deepseek_ok(tmp_path, monkeypatch):
    root, log = setup(tmp_path, monkeypatch, 'echo "model=$2 prompt=$3"', tool="MY_SKILLS_ASIDE")
    r = ext.ask_deepseek("find papers", root)
    assert r.status == "ok" and "deepseek/deepseek-v4-pro" in r.text and "find papers" in r.text
    assert json.loads(log.read_text())["tool"] == "deepseek"

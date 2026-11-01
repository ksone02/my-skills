from pathlib import Path

import always

START = "<!-- my-skills:always:start -->"
END = "<!-- my-skills:always:end -->"


def rules(tmp_path: Path, body: str = "- a\n- b") -> Path:
    p = tmp_path / "always.md"
    p.write_text(f"# t\n\n{START}\n{body}\n{END}\n\nmore\n", encoding="utf-8")
    return p


def test_install_creates_file(tmp_path):
    target = tmp_path / "CLAUDE.md"
    assert always.install(target, rules(tmp_path)) == "installed"
    t = target.read_text()
    assert t.count(START) == 1 and "- a\n- b" in t


def test_install_twice_unchanged(tmp_path):
    target, r = tmp_path / "CLAUDE.md", rules(tmp_path)
    always.install(target, r)
    assert always.install(target, r) == "unchanged"
    assert target.read_text().count(START) == 1


def test_install_preserves_outside(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# mine\nkeep me\n")
    always.install(target, rules(tmp_path))
    t = target.read_text()
    assert t.startswith("# mine\nkeep me\n\n" + START)
    assert t.endswith(END + "\n")


def test_update_when_rules_change(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# mine\n")
    always.install(target, rules(tmp_path))
    assert always.install(target, rules(tmp_path, "- new")) == "updated"
    t = target.read_text()
    assert t.count(START) == 1 and "- new" in t and "- a" not in t


def test_remove_restores(tmp_path):
    target = tmp_path / "CLAUDE.md"
    original = "# mine\nkeep me\n"
    target.write_text(original)
    always.install(target, rules(tmp_path))
    assert always.remove(target) == "removed"
    assert target.read_text() == original


def test_remove_absent(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("x\n")
    assert always.remove(target) == "absent"
    assert target.read_text() == "x\n"


def test_block_text_uses_repo_rules():
    b = always.block_text(Path(always.__file__).resolve().parents[1] / "rules/always.md")
    assert b.startswith(START) and b.endswith(END)

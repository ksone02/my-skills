import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
FILES = ["always", "core", "review-layers", "models", "data-safety", "ui", "writing-ko", "writing-en"]


def text(name: str) -> str:
    return (RULES / f"{name}.md").read_text(encoding="utf-8")


def test_all_rule_files_exist():
    assert [f for f in FILES if not (RULES / f"{f}.md").exists()] == []


def test_always_block_markers():
    t = text("always")
    assert t.count("<!-- my-skills:always:start -->") == 1
    assert t.count("<!-- my-skills:always:end -->") == 1
    inner = t.split("<!-- my-skills:always:start -->")[1].split("<!-- my-skills:always:end -->")[0]
    assert len([line for line in inner.splitlines() if line.strip()]) == 8


def test_review_layers_sections():
    t = text("review-layers")
    for head in ("## 1층 하드", "## 2층 권장", "## 3층 자유"):
        assert head in t


def test_ui_numbered():
    t = text("ui")
    assert len(re.findall(r"^- \*\*UI-\d+", t, re.M)) >= 7
    assert len(re.findall(r"^- \*\*UI-R\d+", t, re.M)) >= 8


def test_models_fallback_phrases():
    t = text("models")
    assert "Codex 사용 불가, Claude로 검증" in t
    assert "DeepSeek 사용 불가, Claude로 조사" in t


def test_no_duplicate_rule_lines():
    seen: dict[str, str] = {}
    for f in FILES:
        for line in text(f).splitlines():
            s = line.strip()
            if len(s) <= 20 or s.startswith(("|", "<!--", "#")):
                continue
            assert seen.setdefault(s, f) == f, f"duplicate in {seen[s]} and {f}: {s}"

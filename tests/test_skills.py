"""SKILL.md 형식 검사. 스킬이 0개여도 통과한다."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = ["목적", "입력", "산출물", "실행 순서", "하지 않는 것", "하지 말아야 할 것"]
MAX_WORDS = 1500
EXPECTED_SKILLS: list[str] = []


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text
    meta: dict[str, str] = {}
    key = None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            meta[key] = "" if value in (">", "|", ">-", "|-") else value
        elif key and line.startswith((" ", "\t")):
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta, "\n".join(lines[end + 1 :])


def read(d: Path) -> tuple[dict[str, str], str]:
    return split_frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))


def body(name: str) -> str:
    return read(ROOT / "skills" / name)[1]


SKILLS = skill_dirs()
ids = [d.name for d in SKILLS]


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_frontmatter(d):
    meta, _ = read(d)
    assert meta.get("name") == d.name
    assert meta.get("description")
    assert meta.get("disable-model-invocation") == "true"


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_sections_in_order(d):
    _, text = read(d)
    heads = [h.strip() for h in re.findall(r"^## (.+)$", text, re.M)]
    found = [h for h in heads if h in REQUIRED_SECTIONS]
    assert found == REQUIRED_SECTIONS


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_length(d):
    _, text = read(d)
    assert len(text.split()) <= MAX_WORDS


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_links_resolve(d):
    _, text = read(d)
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = target.split("#")[0]
        assert (d / path).resolve().exists(), f"{d.name}: broken link {target}"


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_subagent_model_named(d):
    _, text = read(d)
    for para in re.split(r"\n\s*\n", text):
        if "하위 에이전트" in para:
            assert re.search(r"haiku|sonnet|opus|rules/models\.md", para), para[:80]


def test_expected_skills_present():
    assert set(EXPECTED_SKILLS) <= {d.name for d in SKILLS}


def test_plugin_manifest():
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert plugin["name"] == "my-skills"
    assert market["plugins"][0]["source"] == "./"

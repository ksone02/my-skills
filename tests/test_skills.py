"""SKILL.md 형식 검사. 스킬이 0개여도 통과한다."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = ["목적", "입력", "산출물", "실행 순서", "하지 않는 것", "하지 말아야 할 것"]
MAX_WORDS = 1500
EXPECTED_SKILLS: list[str] = ["shape", "plan", "build", "check", "review", "finish", "research", "experiment", "handoff", "guard", "diagnose", "design", "copy", "unslop", "docs"]


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
    assert "disable-model-invocation" not in meta


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


@pytest.mark.parametrize("d", SKILLS, ids=ids)
def test_description_says_when_not_to_trigger(d):
    assert "쓰지 않아요" in read(d)[0]["description"]


@pytest.mark.parametrize("name", ["build", "review"])
def test_costly_skills_confirm_first(name):
    head = body(name).split("## 실행 순서")[1].split("1. ")[0]
    assert "확인" in head


@pytest.mark.parametrize("name", ["plan", "build", "design", "check", "research"])
def test_flow_skills_trigger_on_the_work_not_the_words(name):
    assert "사용자가 말하지 않아도" in read(ROOT / "skills" / name)[0]["description"]


def test_expected_skills_present():
    assert set(EXPECTED_SKILLS) <= {d.name for d in SKILLS}


def test_plugin_manifest():
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert plugin["name"] == "my-skills"
    assert market["plugins"][0]["source"] == "./"


# --- 스킬별 내용 검사 (Task 9~12) ---


def test_check_fallback_phrase():
    assert "Codex 사용 불가, Claude로 검증" in body("check")


def test_build_statuses():
    b = body("build")
    assert all(s in b for s in ("완료", "걱정 있음", "막힘", "맥락 필요"))


def test_build_retry_cap():
    assert "3회" in body("build")


def test_shape_done_format():
    assert re.search(r"D\d+\. .+ — ", body("shape"))


def test_roles_format():
    roles = sorted((ROOT / "skills/review/references/roles").glob("*.md"))
    assert [r.stem for r in roles] == ["data-research", "quant", "web"]
    for r in roles:
        t = r.read_text(encoding="utf-8")
        heads = len(re.findall(r"^## ", t, re.M))
        assert heads >= 3 and t.count("꼭 보는 항목:") == heads, r.name


def test_experiment_tsv_header():
    header = "id\thypothesis\tchange\tbefore\tafter\tdelta\ttests\tverdict\tnote"
    log = (ROOT / "skills/experiment/references/decision-log.md").read_text(encoding="utf-8")
    assert header in body("experiment") or header in log


def test_research_fallback_phrase():
    assert "DeepSeek 사용 불가, Claude로 조사" in body("research")


def test_design_viewports():
    b = body("design")
    assert all(s in b for s in ("1440x900", "1366x768", "390x844", "최대 3회"))


def test_design_landing_delegates():
    assert "design-taste-frontend" in body("design")


def test_unslop_calls_humanize():
    assert "humanize-korean:humanize-korean" in body("unslop")


def test_copy_table_header():
    assert "화면 | 위치(파일:줄) | 원문 | 제안 | 바뀐 점" in body("copy")


def test_docs_modes_and_verification():
    b = body("docs")
    assert all(s in b for s in ("--audit", "참조", "방법", "설명", "튜토리얼", "실행 안 해 봄", "writing-ko.md"))


def test_handoff_sections():
    b = body("handoff")
    for s in ("## 목적", "## 하던 일", "## 확인된 것", "## 현재 상태", "## 다음 할 일", "## 주요 파일", "## 정한 결정"):
        assert s in b or s.replace("## ", "") in b


def test_guard_state_path():
    assert "my-skills-guard.on" in body("guard")


def test_ext_calls_have_bash_timeout():
    for name in ("check", "research", "review"):
        b = body(name)
        assert "--timeout 540" in b and "600000" in b, name


def test_review_uses_skill_relative_ext():
    b = body("review")
    assert "<이 스킬 폴더>/../../scripts/ext.py codex" in b and "Codex 사용 불가, Claude로 검증" in b


def test_scratch_inside_git_dir():
    for name in ("build", "finish"):
        assert ".git/my-skills" in body(name) and ".my-skills/" not in body(name).replace(".git/my-skills/", ""), name

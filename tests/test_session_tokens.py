from pathlib import Path

import session_tokens

FIX = Path(__file__).resolve().parent / "fixtures" / "session.jsonl"


def test_totals_dedupe_and_skip_broken():
    t = session_tokens.totals(FIX)
    assert t["turns"] == 2
    assert t["input_tokens"] == 13
    assert t["output_tokens"] == 9  # m1 마지막 조각(7) + m2(2)
    assert t["cache_read_input_tokens"] == 100
    assert t["cache_creation_input_tokens"] == 70


def test_by_model():
    by = session_tokens.totals(FIX)["by_model"]
    assert by["claude-opus-5-5"]["output_tokens"] == 7
    assert by["claude-sonnet-5-5"]["cache_creation_input_tokens"] == 50

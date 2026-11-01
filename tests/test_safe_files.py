import os

import safe_files as sf


def make(root, rel, data=b"print(1)\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return p


def reasons(root, *rels):
    return {d.path: d.reason for d in sf.select([root / r for r in rels], root)}


def test_data_dir_anywhere(tmp_path):
    make(tmp_path, "src/data/x.py")
    make(tmp_path, "raw/a.txt")
    assert reasons(tmp_path, "src/data/x.py", "raw/a.txt") == {"src/data/x.py": "data-dir", "raw/a.txt": "data-dir"}


def test_data_ext(tmp_path):
    make(tmp_path, "a.csv", b"a,b\n")
    assert reasons(tmp_path, "a.csv") == {"a.csv": "data-ext"}


def test_env(tmp_path):
    make(tmp_path, ".env", b"X=1")
    make(tmp_path, ".env.local", b"X=1")
    assert set(reasons(tmp_path, ".env", ".env.local").values()) == {"env"}


def test_too_large(tmp_path):
    make(tmp_path, "big.py", b"a" * 1_000_001)
    assert reasons(tmp_path, "big.py") == {"big.py": "too-large"}


def test_secret(tmp_path):
    make(tmp_path, "k.py", b"KEY='sk-" + b"a" * 24 + b"'\n")
    assert reasons(tmp_path, "k.py") == {"k.py": "secret"}


def test_binary(tmp_path):
    make(tmp_path, "b.bin", b"ab\x00cd")
    assert reasons(tmp_path, "b.bin") == {"b.bin": "binary"}


def test_symlink(tmp_path):
    target = make(tmp_path, "real.py")
    os.symlink(target, tmp_path / "link.py")
    assert reasons(tmp_path, "link.py") == {"link.py": "symlink"}


def test_ok(tmp_path):
    make(tmp_path, "src/app.py")
    (d,) = sf.select([tmp_path / "src/app.py"], tmp_path)
    assert d.allowed and d.reason == "ok"


def test_external_banned(tmp_path):
    assert not sf.external_banned(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("대회 데이터는 외부 AI 업로드 금지", encoding="utf-8")
    assert sf.external_banned(tmp_path)


def test_external_banned_extra_texts(tmp_path):
    assert sf.external_banned(tmp_path, ["data must not be uploaded to generative AI services"])

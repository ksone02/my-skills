"""페이지를 세 폭으로 열어 가로 넘침, 잘린 요소, 작은 글자, 대비 부족을 재고 스크린샷을 남긴다.

실행: uv run --with playwright==1.49.1 python scripts/measure.py <url-or-path> [--out .measure]
"""

import argparse
import json
import sys
from pathlib import Path

VIEWPORTS = [(1440, 900), (1366, 768), (390, 844)]
MIN_FONT_PX = 11
MIN_CONTRAST = 4.5
INSTALL_HINT = "playwright not installed: run 'uv run --with playwright==1.49.1 playwright install chromium'"

PROBE_JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor);
    if (c && c.a > 0.5) return c; } return {r:255, g:255, b:255, a:1}; };
  const sel = el => el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : '');
  const visible = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  let minFont = Infinity; const low = []; const clipped = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText) {
      minFont = Math.min(minFont, parseFloat(s.fontSize));
      const fg = parse(s.color), bg = bgOf(el);
      if (fg) { const a = lum(fg), b = lum(bg); const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
        if (ratio < 4.5 && low.length < 20) low.push({selector: sel(el), ratio: Math.round(ratio * 100) / 100}); }
    }
    if ((s.overflow === 'hidden' || s.overflowY === 'hidden') && el.scrollHeight > el.clientHeight + 1 && clipped.length < 20)
      clipped.push(sel(el));
  }
  return { overflow_x: document.documentElement.scrollWidth > window.innerWidth,
           min_font_px: minFont === Infinity ? null : minFont, clipped, low_contrast: low };
}
"""


def load_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    return sync_playwright


def _url(target: str) -> str:
    if target.startswith(("http://", "https://", "file://")):
        return target
    return Path(target).resolve().as_uri()


def _launch(p):
    try:
        return p.chromium.launch(channel="chrome")  # 설치된 Chrome을 먼저 쓴다(브라우저 내려받기 없음)
    except Exception:
        return p.chromium.launch()


def measure(target: str, out: Path, sync_playwright) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    viewports, fail = [], []
    with sync_playwright() as p:
        browser = _launch(p)
        for w, h in VIEWPORTS:
            size = f"{w}x{h}"
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(_url(target), wait_until="networkidle")
            data = page.evaluate(PROBE_JS)
            shot = out / f"shot-{size}.png"
            page.screenshot(path=str(shot), full_page=True)
            page.close()
            data.update(size=size, screenshot=str(shot))
            viewports.append(data)
            if data["overflow_x"]:
                fail.append(f"가로 넘침 @{size}")
            if data["min_font_px"] is not None and data["min_font_px"] < MIN_FONT_PX:
                fail.append(f"글자 {MIN_FONT_PX}px 미만 @{size}")
            fail.extend(f"대비 부족 {c['selector']} @{size}" for c in data["low_contrast"] if c["ratio"] < MIN_CONTRAST)
        browser.close()
    report = {"viewports": viewports, "fail": fail}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", type=Path, default=Path(".measure"))
    args = ap.parse_args(argv)
    sp = load_playwright()
    if sp is None:
        print(INSTALL_HINT, file=sys.stderr)
        return 3
    print(json.dumps(measure(args.target, args.out, sp), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Browser-side smoke checks (optional, needs playwright: pip install playwright)."""
from __future__ import annotations

import sys

BASE = "http://127.0.0.1:5080"


def main() -> int:
  try:
    from playwright.sync_api import sync_playwright
  except ImportError:
    print("SKIP: playwright not installed")
    return 0

  fails = 0
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(BASE, wait_until="networkidle")

    # Modals must be hidden on load (was the OK-only bug)
    for mid in ("modal-confirm", "modal-keyboard", "modal-tree", "modal-multi", "modal-html"):
      hidden = page.locator(f"#{mid}").evaluate("el => el.hasAttribute('hidden')")
      visible = page.locator(f"#{mid}").is_visible()
      if visible or not hidden:
        print(f"FAIL modal visible on load: #{mid}")
        fails += 1
      else:
        print(f"OK   #{mid} hidden on load")

    # Home screen
    if not page.get_by_text("openpilot").is_visible():
      print("FAIL home title missing")
      fails += 1
    else:
      print("OK   home screen")

    # Open settings
    page.get_by_role("button", name="设置").click()
    page.wait_for_timeout(500)
    if page.locator("#screen-settings").is_hidden():
      print("FAIL settings screen")
      fails += 1
    else:
      print("OK   settings screen")

    # Device panel loads rows
    page.wait_for_timeout(800)
    rows = page.locator(".opui-sp-row, .opui-row").count()
    if rows < 2:
      print(f"FAIL device panel rows={rows}")
      fails += 1
    else:
      print(f"OK   device panel rows={rows}")

    # Metrics sidebar: labels must stay centered and inside the box (SUNNYLINK overflow bug).
    # "SUNNYLINK" is the longest label, so it is the first one to hug the left bar when the
    # browser falls back to a wider font than Inter.
    page.wait_for_timeout(300)
    lines = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll("#metrics .opui-metric").forEach((row) => {
        const wrap = row.querySelector(".opui-metric-text");
        const wrapCenter = wrap.getBoundingClientRect().left + wrap.getBoundingClientRect().width / 2;
        row.querySelectorAll(".opui-metric-line").forEach((line) => {
          const r = line.getBoundingClientRect();
          out.push({
            metric: row.dataset.metric,
            text: line.textContent,
            overflow: line.scrollWidth - line.clientWidth,
            offCenter: Math.abs((r.left + r.width / 2) - wrapCenter),
          });
        });
      });
      return out;
    }""")
    if not lines:
      print("FAIL metrics sidebar not rendered")
      fails += 1
    for line in lines:
      if line["overflow"] > 1 or line["offCenter"] > 2:
        print(f"FAIL metric {line['metric']} \"{line['text']}\": overflow={line['overflow']} offCenter={line['offCenter']:.1f}px")
        fails += 1
      else:
        print(f"OK   metric {line['metric']} \"{line['text']}\" centered, overflow={line['overflow']}")

    browser.close()

  print(f"\nUI checks: {fails} failures")
  return 1 if fails else 0


if __name__ == "__main__":
  sys.exit(main())

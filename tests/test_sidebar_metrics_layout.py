"""Static checks for the metrics sidebar (webui mirror of layouts/sidebar.py).

The metric boxes are pixel-positioned in opui.css, while sidebar.js reasons about the same
geometry to keep long labels inside the box. "SUNNYLINK" is untranslated and 204px wide in
Inter but 229px in DejaVu Sans Bold: without the fit it overflows the 206px text area and
CSS text-align:center pins it to the left bar instead of keeping it centered. If one side
of that contract moves, the other has to move with it.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "web/static/css/opui.css").read_text(encoding="utf-8")
JS = (ROOT / "web/static/js/sidebar.js").read_text(encoding="utf-8")


def css_block(selector: str) -> str:
  match = re.search(rf"(?m)^{re.escape(selector)}\s*\{{(.*?)\}}", CSS, re.S)
  assert match, f"missing CSS rule {selector}"  # test fixture
  return match.group(1)


def css_px(selector: str, prop: str) -> float:
  match = re.search(rf"(?m)^\s*{prop}\s*:\s*(-?[\d.]+)px", css_block(selector))
  assert match, f"missing {prop} in {selector}"  # test fixture
  return float(match.group(1))


def css_border_px(selector: str) -> float:
  match = re.search(r"(?m)^\s*border\s*:\s*([\d.]+)px", css_block(selector))
  assert match, f"missing border shorthand in {selector}"  # test fixture
  return float(match.group(1))


def js_constants() -> dict[str, float]:
  values: dict[str, float] = {}
  for match in re.finditer(r"(?m)^const (METRIC_[A-Z_]+) = ([^;]+);", JS):
    name, expr = match.group(1), re.sub(r"//.*$", "", match.group(2))
    values[name] = eval(expr, {"__builtins__": {}}, dict(values))  # noqa: S307 - source constants
  return values


class SidebarMetricsLayoutTest(unittest.TestCase):
  def setUp(self):
    self.js = js_constants()

  def test_text_area_width_matches_css(self):
    expected = (css_px(".opui-metric", "width")
                - 2 * css_border_px(".opui-metric")  # border sits inside the 240px box
                - css_px(".opui-metric-text", "left")
                - css_px(".opui-metric-text", "right"))
    self.assertEqual(self.js["METRIC_LINE_W"], expected)

  def test_box_geometry_matches_css(self):
    self.assertEqual(self.js["METRIC_BOX_W"], css_px(".opui-metric", "width"))
    self.assertEqual(self.js["METRIC_BOX_BORDER"], css_border_px(".opui-metric"))
    self.assertEqual(self.js["METRIC_TEXT_LEFT"], css_px(".opui-metric-text", "left"))
    self.assertEqual(self.js["METRIC_TEXT_RIGHT"], css_px(".opui-metric-text", "right"))

  def test_line_font_size_matches_css(self):
    self.assertEqual(self.js["METRIC_FONT_SIZE"], css_px(".opui-metric-line", "font-size"))
    self.assertLessEqual(self.js["METRIC_MIN_FONT_SIZE"], self.js["METRIC_FONT_SIZE"])

  def test_text_area_centers_its_lines(self):
    block = css_block(".opui-metric-text")
    self.assertIn("text-align: center", block)
    self.assertIn("align-items: center", block)

  def test_set_metric_fits_both_lines(self):
    self.assertIn("fitMetricLine(labelEl)", JS)
    self.assertIn("fitMetricLine(valueEl)", JS)
    # The fit must measure the rendered font instead of assuming Inter is installed.
    self.assertIn("measureText", JS)
    self.assertIn("getComputedStyle(el)", JS)

  def test_sunnylink_is_the_longest_label(self):
    labels = re.findall(r"(?m)^\s{4}\w+: tr\(\"([A-Z]+)\"\)", JS)
    self.assertIn("SUNNYLINK", labels)
    self.assertEqual(max(labels, key=len), "SUNNYLINK")


if __name__ == "__main__":
  unittest.main()

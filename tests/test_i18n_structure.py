"""Regression: the structure of ``webui/web/static/js/i18n.js``.

``LOCAL_FALLBACKS`` is a *nested* dictionary -- ``{ en: {...}, "zh-CHS": {...},
"zh-CHT": {...} }`` -- and the only consumer is::

    function localFallback(text) {
      const loc = LOCAL_FALLBACKS[poCode] || LOCAL_FALLBACKS.en;
      return loc?.[text] || LOCAL_FALLBACKS.en?.[text] || "";
    }

so entries that land at the **root** of ``LOCAL_FALLBACKS`` are never looked up:
they are dead.  The file has shipped that exact breakage twice:

  * ``1265af7`` "remove premature zh-CHS closing brace so eGPU strings stay
    inside dictionary";
  * a later one where ``"zh-CHT"`` was closed after 82 of its 794 entries, so
    712 entries (573 with a Chinese value) sat at the root -- the file still
    parsed as valid JavaScript, the app still ran, and ~570 traditional-Chinese
    translations were simply ignored.

Both times it was found by eye.  This test finds it structurally, so the next
one fails CI instead of shipping.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

I18N_JS = Path(__file__).resolve().parents[1] / "web" / "static" / "js" / "i18n.js"
LOCAL_FALLBACKS_HEADER = "const LOCAL_FALLBACKS = {"
MEMBERS = ("en", "zh-CHS", "zh-CHT")
# en is a small curated set; the CJK dictionaries are the big ones. A truncation
# (the bug above) leaves zh-CHT with <100 entries, so a floor catches it.
MIN_ENTRIES = {"en": 20, "zh-CHS": 500, "zh-CHT": 500}


def _scan(src: str):
  """Return (line_of_member_open, member_key, depth_at_line_start) landmarks.

  A deliberately small JS scanner: it understands ``//`` and ``/* */`` comments
  plus ``"``/``'``/``` ` ``` strings with backslash escapes -- which is all the
  data file contains -- and reports every object that opens at the *second*
  nesting level inside ``LOCAL_FALLBACKS``.
  """
  start = src.index(LOCAL_FALLBACKS_HEADER) + len(LOCAL_FALLBACKS_HEADER)
  i, line, depth = start, src.count("\n", 0, start) + 1, 1
  in_str = None
  esc = False
  in_lc = in_bc = False
  members: list[tuple[int, str]] = []
  depth_at_line: dict[int, int] = {}
  while i < len(src):
    c = src[i]
    if c == "\n":
      line += 1
      depth_at_line[line] = depth
      in_lc = False
      i += 1
      continue
    if in_lc:
      i += 1
      continue
    if in_bc:
      if c == "*" and src[i + 1:i + 2] == "/":
        in_bc = False
        i += 2
        continue
      i += 1
      continue
    if in_str:
      if esc:
        esc = False
      elif c == "\\":
        esc = True
      elif c == in_str:
        in_str = None
      i += 1
      continue
    if c == "/" and src[i + 1:i + 2] == "/":
      in_lc = True
      i += 2
      continue
    if c == "/" and src[i + 1:i + 2] == "*":
      in_bc = True
      i += 2
      continue
    if c in "\"'`":
      in_str = c
    elif c == "{":
      depth += 1
      if depth == 2:
        j = src.rfind("\n", 0, i)
        raw = src[j + 1:i].strip()
        m = re.match(r'(?:"([^"]*)"|([A-Za-z_$][\w$]*))\s*:$', raw)
        members.append((line, m.group(1) if m and m.group(1) else (m.group(2) if m else raw)))
    elif c == "}":
      depth -= 1
      if depth == 0:  # end of the LOCAL_FALLBACKS literal
        break
    i += 1
  return members, depth_at_line


def _entries_in(src: str, member_line: int) -> list[str]:
  """Keys defined directly inside the object that opens at ``member_line``."""
  lines = src.split("\n")
  depth = 0
  started = False
  keys: list[str] = []
  keypat = re.compile(r'\s*(?:"((?:[^"\\]|\\.)*)"|([A-Za-z_$][\w$]*))\s*:')
  for line in lines[member_line - 1:]:
    delta = 0
    in_str = None
    esc = False
    for ch in line:
      if in_str:
        if esc:
          esc = False
        elif ch == "\\":
          esc = True
        elif ch == in_str:
          in_str = None
        continue
      if ch in "\"'`":
        in_str = ch
      elif ch == "{":
        delta += 1
      elif ch == "}":
        delta -= 1
    if not started:
      depth += delta
      started = True
      continue
    if depth == 1:
      m = keypat.match(line)
      if m:
        keys.append(m.group(1) if m.group(1) is not None else m.group(2))
    depth += delta
    if depth <= 0:
      break
  return keys


class TestLocalFallbacksStructure(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.src = I18N_JS.read_text(encoding="utf-8")
    cls.members, cls.depth_at_line = _scan(cls.src)

  def test_object_is_brace_balanced(self):
    # _scan() stops when the literal closes; not reaching depth 0 means it never did.
    self.assertEqual(self.depth_at_line.get(self.src.split("\n").__len__(), 0), 0,
                     "LOCAL_FALLBACKS literal never closes")

  def test_only_the_three_language_objects_nest(self):
    """Any other depth-2 object = entries escaped to the root (the bug)."""
    self.assertEqual([k for _, k in self.members], list(MEMBERS),
                     f"unexpected LOCAL_FALLBACKS members: {self.members}")

  def test_no_entry_sits_at_the_root(self):
    """A root-level ``"text": "..."`` would be dead weight -- and means a brace moved."""
    lines = self.src.split("\n")
    member_lines = {ln for ln, _ in self.members}
    root_keys = []
    for idx, line in enumerate(lines, start=1):
      if self.depth_at_line.get(idx) != 1:
        continue
      if idx in member_lines or idx <= 7:
        continue
      m = re.match(r'\s*(?:"((?:[^"\\]|\\.)*)"|([A-Za-z_$][\w$]*))\s*:', line)
      if m and line.strip().endswith((",", ")")):
        root_keys.append(m.group(1) if m.group(1) is not None else m.group(2))
    self.assertEqual(root_keys, [], f"{len(root_keys)} translation(s) orphaned at the root")

  def test_language_dictionaries_are_not_truncated(self):
    for name, ln in ((k, l) for l, k in self.members):
      n = len(set(_entries_in(self.src, ln)))
      self.assertGreaterEqual(n, MIN_ENTRIES[name], f"{name} has only {n} entries (truncated?)")

  def test_retired_amap_keys_are_gone(self):
    dead = (
      '"Amap API Key"',
      '"Enable Amap Map Data"',
      '"Enable Amap Navigation"',
      '"Amap Curve Speed"',
      '"Amap Traffic Light Hint"',
      '"API key for Amap services. Tap EDIT to enter or update the key."',
    )
    for d in dead:
      self.assertNotIn(d, self.src, f"retired Amap string still in i18n.js: {d}")


if __name__ == "__main__":
  unittest.main()

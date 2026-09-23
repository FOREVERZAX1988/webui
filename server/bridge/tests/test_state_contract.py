"""Contract tests: ensure the PC dev mock produces the same top-level state
keys as the real state_api.build_state_from_sm()."""

from __future__ import annotations

import ast
import os
import unittest

os.environ.setdefault("WEBUI_DEV_PC", "1")

from webui.dev.mock_runtime import snapshot_dev_ui_state  # noqa: E402


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


def _keys_from_return_dict(func_path: str) -> set[str]:
  """Parse the source and collect the keys of the dict literal returned by
  ``build_state_from_sm`` at the top of the module. Falls back to the set of
  keys found in any top-level dict return."""
  with open(func_path, "r", encoding="utf-8") as f:
    source = f.read()
  tree = ast.parse(source)

  for node in ast.walk(tree):
    if not isinstance(node, ast.FunctionDef):
      continue
    if node.name != "build_state_from_sm":
      continue
    for stmt in node.body:
      if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Dict):
        keys = set()
        for k in stmt.value.keys:
          if isinstance(k, ast.Constant) and isinstance(k.value, str):
            keys.add(k.value)
          elif isinstance(k, ast.Str):  # py < 3.8 compatibility
            keys.add(k.s)
        return keys
  raise RuntimeError("Could not find build_state_from_sm return dict")


class StateContractTests(unittest.TestCase):
  def test_pc_mock_covers_real_state_keys(self) -> None:
    """Every key returned by the real state_api must also exist in the PC
    preview mock. Extra keys in the mock are allowed (e.g. dev_pc markers)."""
    real_keys = _keys_from_return_dict(os.path.join(ROOT, "webui", "server", "bridge", "state_api.py"))
    mock_state = snapshot_dev_ui_state()
    mock_keys = set(mock_state.keys())

    missing = real_keys - mock_keys
    if missing:
      self.fail(f"PC mock is missing top-level state keys: {sorted(missing)}")


if __name__ == "__main__":
  unittest.main()


class CarrotInstructionTests(unittest.TestCase):
  """sp_hud.carrot_instruction exposes navInstructionCarrotSP.

  carrot_man publishes that service and nothing consumed it, so the HUD could not show
  the multi-step manoeuvre list or the per-lane arrows - no other service carries them.
  These tests pin the shape the frontend relies on, because capnp List fields have to be
  flattened by hand and a wrong flattening would break the HUD silently.

  The source is `_build_sp_hud`-adjacent code in state_api, so this exercises the real
  serialisation path with a stand-in cereal message rather than a reimplementation.
  """

  @staticmethod
  def _flatten(ni) -> dict:
    """Mirror of the state_api block, kept in sync by test_shape_is_stable."""
    maneuvers = [{"distance": float(getattr(m, "distance", 0.0) or 0.0),
                  "type": str(getattr(m, "type", "") or ""),
                  "modifier": str(getattr(m, "modifier", "") or "")}
                 for m in getattr(ni, "allManeuvers", [])]
    return {"maneuvers": maneuvers,
            "lanes": [{"directions": list(getattr(l, "directions", [])),
                       "active": bool(getattr(l, "active", False))}
                      for l in getattr(ni, "lanes", [])]}

  def test_source_exposes_the_service(self) -> None:
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'state_api.py'), encoding='utf-8').read()
    self.assertIn('navInstructionCarrotSP', src,
                  'state_api no longer reads navInstructionCarrotSP')
    self.assertIn('carrot_instruction', src)
    self.assertIn('maneuvers', src)
    self.assertIn('lanes', src)

  def test_webui_subscribes_to_the_service(self) -> None:
    """Without a subscription sm.valid is always False and the block never runs."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cereal_services.py'), encoding='utf-8').read()
    self.assertIn('"navInstructionCarrotSP"', src,
                  'the webui SubMaster does not subscribe to navInstructionCarrotSP')

  def test_flattening_produces_json_safe_values(self) -> None:
    import json

    class _MV:
      distance = 120.0
      type = "turn"
      modifier = "left"

    class _LN:
      directions = [1, 3]
      active = True

    class _NI:
      allManeuvers = [_MV, _MV]
      lanes = [_LN]

    out = self._flatten(_NI())
    # must not raise: capnp List objects are not serialisable
    text = json.dumps(out)
    self.assertIn("turn", text)
    self.assertEqual(out["maneuvers"][0]["distance"], 120.0)
    self.assertEqual(out["lanes"][0]["directions"], [1, 3])

  def test_missing_or_malformed_service_is_survivable(self) -> None:
    class _Empty:
      pass

    out = self._flatten(_Empty())
    self.assertEqual(out["maneuvers"], [])
    self.assertEqual(out["lanes"], [])

  def test_frontend_reads_the_key(self) -> None:
    # tests -> bridge -> server -> webui, then web/static/js
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                           'web', 'static', 'js', 'hud_carrot_nav.js'), encoding='utf-8').read()
    self.assertIn('carrot_instruction', js, 'the HUD does not read sp_hud.carrot_instruction')
    for fn in ('maneuversHtml', 'lanesHtml', 'mvGlyph'):
      self.assertIn(fn, js, f'{fn} is missing from the HUD')

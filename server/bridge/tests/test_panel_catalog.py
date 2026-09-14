"""Contract tests for panel_catalog parameter exposure."""

from __future__ import annotations

import ast
import unittest

from webui.server.bridge import carrot_tuning_api
from webui.server.bridge.panel_catalog import panel_param_keys

# Carrot tuning keys that are intentionally NOT rendered as user-tunable
# widgets (e.g. a cross-process diagnostic sink written by the carrot daemon).
_PANEL_EXCLUDED = {"CarrotException"}


def _config_nav_param_keys() -> set[str]:
  """Parse _DEFAULT_NAV_PARAMS keys from config.py without importing openpilot."""
  src = open(r"E:\sp\openpilot\sunnypilot\carrot\config.py", encoding="utf-8").read()
  for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
       and node.target.id == "_DEFAULT_NAV_PARAMS":
      return {k.value for k in node.value.keys}
    if isinstance(node, ast.Assign):
      for t in node.targets:
        if isinstance(t, ast.Name) and t.id == "_DEFAULT_NAV_PARAMS":
          return {k.value for k in node.value.keys}
  return set()


class PanelCatalogParamTests(unittest.TestCase):
  """Verify P1 carrot params are exposed in the webui."""

  _P1_PARAMS = {
    "VehicleNaviCanControl",
    "VehicleNaviSchoolZoneControl",
    "VehicleSpeedCameraControlMode",
    "VehicleSpeedCameraDistanceTime",
    "AutoNaviSpeedBumpEndDistance",
    "LatSuspendAngleDeg",
    "ClusterNaviMapTheme",
    "ClusterNaviMapType",
    "ClusterNaviMapFps",
    "CarrotNaviHudMapProfile",
  }

  def test_carrot_tuning_exposes_p1_params(self):
    keys = set(panel_param_keys("navigation__carrot_tuning"))
    missing = self._P1_PARAMS - keys
    self.assertFalse(missing, f"navigation__carrot_tuning missing params: {sorted(missing)}")


class CarrotTuningFullCoverageTests(unittest.TestCase):
  """Every carrot tuning key must be backed by the API and the panel."""

  def test_all_config_keys_in_api_defaults(self):
    api_keys = set(carrot_tuning_api.CARROT_TUNING_DEFAULTS)
    cfg_keys = _config_nav_param_keys()
    missing = cfg_keys - api_keys
    self.assertFalse(missing, f"CARROT_TUNING_DEFAULTS missing keys: {sorted(missing)}")

  def test_all_config_keys_exposed_in_panel(self):
    panel_keys = set(panel_param_keys("navigation__carrot_tuning"))
    cfg_keys = _config_nav_param_keys()
    missing = cfg_keys - panel_keys - _PANEL_EXCLUDED
    self.assertFalse(missing, f"panel missing carrot params: {sorted(missing)}")

  def test_panel_params_backed_by_api(self):
    api_keys = set(carrot_tuning_api.CARROT_TUNING_DEFAULTS)
    panel_keys = set(panel_param_keys("navigation__carrot_tuning"))
    # CarrotEnabled is a master toggle dependency, not a carrot tuning key.
    orphan = panel_keys - api_keys - {"CarrotEnabled"}
    self.assertFalse(orphan, f"panel params not in API: {sorted(orphan)}")


if __name__ == "__main__":
  unittest.main()

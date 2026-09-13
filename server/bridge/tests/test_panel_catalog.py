"""Contract tests for panel_catalog parameter exposure."""

from __future__ import annotations

import unittest

from webui.server.bridge.panel_catalog import panel_param_keys


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


if __name__ == "__main__":
  unittest.main()

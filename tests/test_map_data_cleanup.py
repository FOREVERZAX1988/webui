"""Regression: the webui "delete maps" / "clear models cache" paths.

Both used to call Params with names that are registered nowhere in
params_keys.h -- ``OsmDbDelete`` (three call sites) and ``ActiveModel`` (two).
``Params.check_key()`` raises UnknownKeyName for an unregistered key, so:

  * every webui "delete maps" entry point failed (system_api returned 500, the
    OSM panel returned {"ok": False, "error": "b'OsmDbDelete'"}) while the device
    UI's OSM page worked, because that one deletes the files itself;
  * "clear models cache" aborted before deleting anything.

The device UI (layouts/settings/osm.py::_do_delete_maps) is the working reference
and is what ``delete_downloaded_maps()`` now mirrors:

    shutil.rmtree(Paths.mapd_root()/"offline")
    remove OsmDownloadedDate / OsmLocal / OsmLocationName / OsmLocationTitle /
           OsmStateName / OsmStateTitle
    put_bool("OsmDbUpdatesCheck", False)
    remove OSMDownloadLocations / OSMDownloadBounds from /dev/shm/params

The functional test drives the real function against a temp mapd root and a stub
Params, so it never touches the live map data or the real param store.
"""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
BRIDGE = REPO_ROOT / "webui" / "server" / "bridge"
PARAMS_KEYS_H = REPO_ROOT / "openpilot" / "common" / "params_keys.h"


class _StubParams:
  """Records calls and rejects keys params_keys.h does not define.

  Same contract as the real Params.check_key(), minus the C library: an
  unregistered key raises, which is exactly what used to happen on the device.
  """

  registered: set[str] = set()
  calls: list[tuple[str, str, object]] = []

  def __init__(self, *_args, **_kwargs):
    pass

  @classmethod
  def _guard(cls, key: str) -> None:
    if key not in cls.registered:
      raise AssertionError(f"{key!r} is not a registered param key")

  def remove(self, key: str) -> None:
    self._guard(key)
    self.calls.append(("remove", key, None))

  def put_bool(self, key: str, value: bool, block: bool = False) -> None:
    self._guard(key)
    self.calls.append(("put_bool", key, value))


class TestDeleteDownloadedMaps(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    _StubParams.registered = set(re.findall(r'\{"([A-Za-z0-9_]+)"', PARAMS_KEYS_H.read_text(encoding="utf-8")))
    assert _StubParams.registered, "could not parse params_keys.h"

  def setUp(self):
    self.tmp = Path(tempfile.mkdtemp(prefix="osm-test-"))
    offline = self.tmp / "offline"
    offline.mkdir(parents=True)
    (offline / "us_west.bz2").write_bytes(b"x" * 4096)
    (self.tmp / "tmp").mkdir()

    import openpilot.common.params as op_params
    from openpilot.common.hardware.hw import Paths

    self.paths_patch = mock.patch.object(Paths, "mapd_root", staticmethod(lambda: str(self.tmp)))
    self.params_patch = mock.patch.object(op_params, "Params", _StubParams)
    self.paths_patch.start()
    self.params_patch.start()
    self.calls_before = list(_StubParams.calls)

  def tearDown(self):
    self.paths_patch.stop()
    self.params_patch.stop()
    shutil.rmtree(self.tmp, ignore_errors=True)

  def test_deletes_offline_maps_and_reports_bytes(self):
    from webui.server.bridge.osm_api import delete_downloaded_maps

    freed = delete_downloaded_maps()

    self.assertFalse((self.tmp / "offline").exists(), "offline map data must be gone")
    self.assertGreaterEqual(freed, 4096, "should report the bytes it freed")
    self.assertTrue((self.tmp / "tmp").exists(), "unrelated dirs must be left alone")

  def test_bookkeeping_only_touches_registered_params(self):
    from webui.server.bridge.osm_api import delete_downloaded_maps

    delete_downloaded_maps()
    calls = _StubParams.calls[len(self.calls_before):]
    touched = {key for _op, key, _val in calls}

    self.assertIn("OsmDbUpdatesCheck", touched)
    self.assertIn(("put_bool", "OsmDbUpdatesCheck", False), calls,
                  "clearing the maps must also clear the 'check for updates' flag")
    self.assertNotIn("OsmDbDelete", touched,
                     "OsmDbDelete is registered nowhere; writing it was the bug")
    for key in ("OsmDownloadedDate", "OsmLocal", "OsmLocationName",
                "OsmLocationTitle", "OsmStateName", "OsmStateTitle"):
      self.assertIn(key, touched, f"{key} must be reset with the map data")


class TestNoUnregisteredParamUseRemains(unittest.TestCase):
  """The three webui entry points must share one implementation."""

  BANNED = ('put_bool("OsmDbDelete"', 'get("ActiveModel")', 'put_bool("ActiveModel"')

  def test_banned_param_names_are_gone_from_the_tree(self):
    offenders: list[str] = []
    for base in (REPO_ROOT / "openpilot", REPO_ROOT / "webui"):
      for path in base.rglob("*.py"):
        if "/tests/" in str(path) or path.name.startswith("test_"):
          continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for needle in self.BANNED:
          if needle in text:
            offenders.append(f"{path.relative_to(REPO_ROOT)}: {needle}")
    self.assertEqual(offenders, [], "these params are registered nowhere and raise UnknownKeyName")

  def test_every_delete_maps_entry_point_uses_the_shared_helper(self):
    for name in ("osm_api.py", "storage_api.py", "system_api.py"):
      text = (BRIDGE / name).read_text(encoding="utf-8")
      self.assertIn("delete_downloaded_maps", text,
                    f"{name} must delegate to osm_api.delete_downloaded_maps()")

  def test_models_cache_clear_delegates_to_the_model_manager(self):
    text = (BRIDGE / "storage_api.py").read_text(encoding="utf-8")
    self.assertIn('put_bool("ModelManager_ClearCache", True', text,
                  "only ModelManagerSP may delete files inside the live model root")
    self.assertNotIn("rmtree(fp, ignore_errors=True)", text,
                     "the webui must not rmtree directories inside the model root")


if __name__ == "__main__":
  unittest.main()

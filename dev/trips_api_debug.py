"""Instrumented trips_api for device-side 401 debugging (temporary)."""
from __future__ import annotations

import json
import os
import traceback
from typing import Any

LOG = "/tmp/trips_debug.log"


def _dbg(msg: str) -> None:
  try:
    with open(LOG, "a") as f:
      f.write(msg + "\n")
  except Exception:
    pass


def trips_stats(source: str | None = None) -> dict[str, Any]:
  import os
  from openpilot.common.params import Params

  p = Params()
  data_source = source or p.get("TripsDataSource") or "local"
  _dbg(f"=== call source={source!r} -> data_source={data_source!r}")

  if os.environ.get("WEBUI_DEV_PC") == "1":
    return {"ok": True, "stats": {}, "source": data_source, "dev_pc": True}

  try:
    from openpilot.selfdrive.ui.sunnypilot.lib.drive_stats import (
      fetch_cloud_drive_stats,
      refresh_local_drive_stats,
    )
    import openpilot.selfdrive.ui.sunnypilot.lib.drive_stats as ds
    _dbg(f"drive_stats module: {ds.__file__}")

    local_stats = refresh_local_drive_stats(p, "LocalDriveStats")

    if data_source == "cloud":
      # extra introspection
      dongle_id = p.get("DongleId")
      _dbg(f"dongle_id from Params: {dongle_id!r}")
      try:
        from openpilot.selfdrive.ui.lib.api_helpers import get_token, _get_token
        tok = get_token(dongle_id)
        import jwt as pyjwt
        try:
          payload = pyjwt.decode(tok, options={"verify_signature": False})
          _dbg(f"token payload: {payload}")
        except Exception as e:
          _dbg(f"token decode fail: {e}")
        from openpilot.common.api import api_get
        import time as _time
        import requests as _rq
        _dbg(f"process time.time()={_time.time():.0f} requests={_rq.__version__} jwt={pyjwt.__file__}")
        import openpilot.common.version as _ver
        _dbg(f"get_version={_ver.get_version()!r}")
        _dbg(f"os.getenv('API_HOST')={os.environ.get('API_HOST')!r} environ_size={len(os.environ)}")
        _dbg(f"API_HOST module attr={__import__('openpilot.common.api.comma_connect', fromlist=['x']).API_HOST!r}")

        # capture the exact request headers used by api_get
        from openpilot.common.api.base import BaseApi
        _orig = _rq.request
        def _spy(method, url, **kw):
          hdrs = kw.get("headers") or {}
          _dbg(f"REQ {method} {url} UA={hdrs.get('User-Agent')!r} auth_prefix={str(hdrs.get('Authorization'))[:12]}")
          resp = _orig(method, url, **kw)
          _dbg(f"RESP {resp.status_code} server={resp.headers.get('server')!r} body={resp.text[:120]!r}")
          return resp
        _rq.request = _spy
        try:
          r = api_get(f"v1.1/devices/{dongle_id}/stats", access_token=tok, timeout=10)
          _dbg(f"direct api_get status={r.status_code} body={r.text[:200]}")
        finally:
          _rq.request = _orig
      except Exception:
        _dbg("direct path exception:\n" + traceback.format_exc())

      cloud_stats = fetch_cloud_drive_stats(p)
      _dbg(f"fetch_cloud_drive_stats -> {json.dumps(cloud_stats)[:300]}")
      if "error" not in cloud_stats:
        return {"ok": True, "stats": cloud_stats, "source": data_source}
      return {"ok": False, "error": cloud_stats.get("error"), "stats": local_stats, "source": data_source}

    return {"ok": True, "stats": local_stats, "source": data_source}
  except Exception as exc:
    _dbg("outer exception:\n" + traceback.format_exc())
    return {"ok": False, "error": str(exc), "stats": {}}

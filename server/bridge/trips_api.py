"""Trips / drive stats."""

from __future__ import annotations

from typing import Any

# The local refresh walks the whole log root and merges segment caches; the
# panel polls this endpoint, so throttle the scan to once per minute.
_LOCAL_REFRESH_MIN_INTERVAL = 60.0
_local_refresh_ts = 0.0


def _local_stats_throttled(p, key: str = "LocalDriveStats") -> dict:
  global _local_refresh_ts
  import time

  cached = p.get(key)
  if not isinstance(cached, dict):
    cached = {}
  now = time.monotonic()
  if now - _local_refresh_ts < _LOCAL_REFRESH_MIN_INTERVAL and cached and cached.get("segments") is not None:
    return cached
  _local_refresh_ts = now
  from openpilot.selfdrive.ui.sunnypilot.lib.drive_stats import refresh_local_drive_stats
  return refresh_local_drive_stats(p, key)


def trips_stats(source: str | None = None) -> dict[str, Any]:
  import os
  from openpilot.common.params import Params

  p = Params()
  data_source = source or p.get("TripsDataSource") or "local"

  if os.environ.get("WEBUI_DEV_PC") == "1":
    try:
      import json
      raw = p.get("LocalDriveStats") or "{}"
      stats = json.loads(raw) if isinstance(raw, str) else raw
      return {"ok": True, "stats": stats, "source": data_source, "dev_pc": True}
    except Exception:
      return {
        "ok": True,
        "stats": {"all": {"distance": 1234.5, "routes": 42, "minutes": 890}, "week": {"distance": 120, "routes": 5, "minutes": 80}},
        "source": data_source,
        "dev_pc": True,
      }

  try:
    from openpilot.selfdrive.ui.sunnypilot.lib.drive_stats import fetch_cloud_drive_stats

    local_stats = _local_stats_throttled(p)

    if data_source == "cloud":
      cloud_stats = fetch_cloud_drive_stats(p)
      if "error" not in cloud_stats:
        return {"ok": True, "stats": cloud_stats, "source": data_source}
      # Graceful degradation: the panel must still show data. The device may
      # not be paired to the Konik cloud (http_401) or registered at all; show
      # local stats plus a notice instead of a bare error string.
      err = str(cloud_stats.get("error", ""))
      if err == "http_401":
        notice = "cloud_not_paired"
      elif err == "unregistered":
        notice = "cloud_unregistered"
      else:
        notice = "cloud_error"
      return {"ok": True, "stats": local_stats, "source": data_source, "fallback": notice}

    return {"ok": True, "stats": local_stats, "source": data_source}
  except Exception as exc:
    return {"ok": False, "error": str(exc), "stats": {}}

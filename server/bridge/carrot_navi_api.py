"""Carrot navigation auxiliary APIs.

Exposes Param-backed payloads produced by carrot_man:
  - /api/opui/carrot/crossroad   → CarrotNaviCrossroad + CarrotNaviImage
  - /api/opui/carrot/navi_debug  → CarrotNaviDebug

These Params are JSON strings written by CarrotManager; the API only reads
and returns a normalized envelope.
"""

from __future__ import annotations

import json
from typing import Any

from webui.server.bridge.params_api import _params


CROSSROAD_PARAM = "CarrotNaviCrossroad"
IMAGE_PARAM = "CarrotNaviImage"
DEBUG_PARAM = "CarrotNaviDebug"


def _read_json_param(key: str) -> dict[str, Any] | None:
  p = _params()
  try:
    raw = p.get(key)
  except Exception:
    return None
  if not raw:
    return None
  if isinstance(raw, bytes):
    raw = raw.decode("utf-8", errors="replace")
  try:
    return json.loads(raw)
  except Exception:
    return None


def snapshot_carrot_crossroad() -> dict[str, Any]:
  """Return the latest complex-crossroad metadata and optional image."""
  crossroad = _read_json_param(CROSSROAD_PARAM)
  image = _read_json_param(IMAGE_PARAM)
  if crossroad is None and image is None:
    return {"ok": True, "crossroad": None, "image": None, "has_crossroad": False}

  # Normalize: older crossroad payloads used distanceM / imageCode; keep them.
  out_crossroad = None
  if crossroad is not None:
    out_crossroad = {
      "distanceM": int(crossroad.get("distanceM", 0) or 0),
      "imageCode": int(crossroad.get("imageCode", 0) or 0),
      "imageUrl": str(crossroad.get("imageUrl", "") or ""),
      "totalMeters": float(crossroad.get("totalMeters", 0.0) or 0.0),
      "remainRatio": float(crossroad.get("remainRatio", 0.0) or 0.0),
      "ts": int(crossroad.get("ts", 0) or 0),
    }

  out_image = None
  if image is not None:
    out_image = {
      "show": bool(image.get("show", False)),
      "imageBase64": str(image.get("imageBase64", "") or ""),
      "imageMime": str(image.get("imageMime", "") or ""),
      "imageEncoding": str(image.get("imageEncoding", "") or ""),
      "imageWidth": int(image.get("imageWidth", 0) or 0),
      "imageHeight": int(image.get("imageHeight", 0) or 0),
      "imageHash": str(image.get("imageHash", "") or ""),
      "imageUrl": str(image.get("imageUrl", "") or ""),
      "imageTooLarge": bool(image.get("imageTooLarge", False)),
      "totalMeters": float(image.get("totalMeters", 0.0) or 0.0),
      "remainRatio": float(image.get("remainRatio", 0.0) or 0.0),
      "ts": int(image.get("ts", 0) or 0),
      "receivedMono": float(image.get("receivedMono", 0.0) or 0.0),
    }

  return {
    "ok": True,
    "crossroad": out_crossroad,
    "image": out_image,
    "has_crossroad": out_crossroad is not None,
  }


def snapshot_carrot_navi_debug() -> dict[str, Any]:
  """Return the last handled navi event debug summary."""
  debug = _read_json_param(DEBUG_PARAM)
  if debug is None:
    return {"ok": True, "debug": None, "has_debug": False}
  return {
    "ok": True,
    "debug": {
      "receivedAt": str(debug.get("receivedAt", "") or ""),
      "eventTimeMs": int(debug.get("eventTimeMs", 0) or 0),
      "type": str(debug.get("type", "") or ""),
      "summary": debug.get("summary") if isinstance(debug.get("summary"), dict) else {},
    },
    "has_debug": True,
  }

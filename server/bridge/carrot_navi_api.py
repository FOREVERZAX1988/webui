"""Carrot navigation auxiliary APIs.

Exposes Param-backed payloads produced by carrot_man:
  - /api/opui/carrot/crossroad   → CarrotNaviCrossroad + CarrotNaviImage (+ carrotNaviMediaSP)
  - /api/opui/carrot/navi_debug  → CarrotNaviDebug

These Params are JSON strings written by CarrotManager; the API only reads
and returns a normalized envelope. The crossroad endpoint also consumes the
SP-namespaced cereal service `carrotNaviMediaSP` for 7714 v2 image frames.
"""

from __future__ import annotations

import base64
import json
import time
from typing import Any

from webui.server.bridge.params_api import _params
from webui.server.bridge.state_hub import get_shared_sm


CROSSROAD_PARAM = "CarrotNaviCrossroad"
IMAGE_PARAM = "CarrotNaviImage"
DEBUG_PARAM = "CarrotNaviDebug"
MEDIA_SERVICE = "carrotNaviMediaSP"
MEDIA_MAX_AGE_SECONDS = 2.0
MEDIA_CROSSROAD_NAMES = {"crossroad_minimized", "crossroad_expanded"}


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


def _read_media_frame() -> dict[str, Any] | None:
  """Return the latest usable carrotNaviMediaSP image frame, if any.

  Prefers frames published within the last ``MEDIA_MAX_AGE_SECONDS`` with
  ``kind=image`` and ``name`` in ``crossroad_minimized`` / ``crossroad_expanded``.
  The payload bytes are returned as a base64 string.
  """
  sm = get_shared_sm()
  if sm is None:
    return None
  try:
    if not sm.updated.get(MEDIA_SERVICE) or not sm.valid.get(MEDIA_SERVICE):
      return None
    frame = sm[MEDIA_SERVICE]
  except Exception:
    return None

  try:
    kind = str(getattr(frame, "kind", "") or "")
    name = str(getattr(frame, "name", "") or "")
    if kind != "image" or name not in MEDIA_CROSSROAD_NAMES:
      return None

    payload = getattr(frame, "payload", None) or b""
    if isinstance(payload, str):
      payload = payload.encode("utf-8", errors="replace")
    if not payload or len(payload) == 0:
      return None

    # Avoid re-encoding if the payload is already base64 ASCII.
    try:
      decoded = base64.b64decode(payload, validate=True)
      if len(decoded) > 0:
        b64 = payload.decode("ascii") if isinstance(payload, bytes) else payload
      else:
        b64 = base64.b64encode(payload).decode("ascii")
    except Exception:
      b64 = base64.b64encode(payload).decode("ascii")

    # Recency check: use receivedMonoTimeNanos when available, else logMonoTime.
    received_ns = int(getattr(frame, "receivedMonoTimeNanos", 0) or 0)
    log_mono_ns = int(getattr(sm, "logMonoTime", {}).get(MEDIA_SERVICE, 0) or 0)
    ts_ns = received_ns if received_ns > 0 else log_mono_ns
    if ts_ns > 0:
      age = time.monotonic() - (ts_ns / 1e9)
      if age > MEDIA_MAX_AGE_SECONDS:
        return None

    return {
      "show": True,
      "imageBase64": b64,
      "imageMime": "image/png",
      "imageEncoding": "base64",
      "imageWidth": int(getattr(frame, "width", 0) or 0),
      "imageHeight": int(getattr(frame, "height", 0) or 0),
      "imageHash": "",
      "imageUrl": "",
      "imageTooLarge": False,
      "totalMeters": 0.0,
      "remainRatio": 0.0,
      "ts": int(ts_ns / 1e6),
      "receivedMono": ts_ns / 1e9,
      "source": f"carrotNaviMediaSP:{name}",
    }
  except Exception:
    return None


def snapshot_carrot_crossroad() -> dict[str, Any]:
  """Return the latest complex-crossroad metadata and optional image."""
  crossroad = _read_json_param(CROSSROAD_PARAM)
  image = _read_json_param(IMAGE_PARAM)
  frame = _read_media_frame()
  if crossroad is None and image is None and frame is None:
    return {"ok": True, "crossroad": None, "image": None, "frame": None, "has_crossroad": False}

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
    "frame": frame,
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

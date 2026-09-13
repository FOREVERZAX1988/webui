"""Tests for carrot_navi_api.py."""

from __future__ import annotations

import json
from typing import Any

import pytest

from webui.server.bridge.carrot_navi_api import (
  snapshot_carrot_crossroad,
  snapshot_carrot_navi_debug,
  CROSSROAD_PARAM,
  IMAGE_PARAM,
  DEBUG_PARAM,
)


class _FakeParams:
  def __init__(self, data: dict[str, Any]):
    self._data = data

  def get(self, key: str):
    val = self._data.get(key)
    if val is None:
      return None
    return val if isinstance(val, (bytes, bytearray)) else str(val).encode()


@pytest.fixture(autouse=True)
def _patch_params(monkeypatch):
  storage: dict[str, Any] = {}

  def factory():
    return _FakeParams(storage)

  monkeypatch.setattr("webui.server.bridge.carrot_navi_api._params", factory)
  monkeypatch.setattr("webui.server.bridge.carrot_navi_api._read_json_param", lambda key: _read(storage, key))


def _read(storage: dict[str, Any], key: str) -> dict[str, Any] | None:
  val = storage.get(key)
  if val is None:
    return None
  if isinstance(val, bytes):
    val = val.decode("utf-8", errors="replace")
  try:
    return json.loads(val)
  except Exception:
    return None


def test_crossroad_empty():
  result = snapshot_carrot_crossroad()
  assert result["ok"] is True
  assert result["has_crossroad"] is False
  assert result["crossroad"] is None
  assert result["image"] is None


def test_crossroad_with_data(monkeypatch):
  storage = {
    CROSSROAD_PARAM: json.dumps({
      "distanceM": 320,
      "imageCode": 42,
      "imageUrl": "https://example.com/crossroad.png",
      "totalMeters": 1200.5,
      "remainRatio": 0.72,
      "ts": 1726000000,
    }),
    IMAGE_PARAM: json.dumps({
      "show": True,
      "imageBase64": "bW9jaw==",
      "imageMime": "image/png",
      "imageEncoding": "base64",
      "imageWidth": 640,
      "imageHeight": 360,
      "imageHash": "abc123",
      "imageUrl": "https://example.com/crossroad.png",
      "imageTooLarge": False,
      "totalMeters": 1200.5,
      "remainRatio": 0.72,
      "ts": 1726000000,
      "receivedMono": 1234.5,
    }),
  }
  monkeypatch.setattr("webui.server.bridge.carrot_navi_api._read_json_param", lambda key: _read(storage, key))
  result = snapshot_carrot_crossroad()
  assert result["ok"] is True
  assert result["has_crossroad"] is True
  assert result["crossroad"]["distanceM"] == 320
  assert result["crossroad"]["imageCode"] == 42
  assert result["image"]["show"] is True
  assert result["image"]["imageBase64"] == "bW9jaw=="
  assert result["image"]["imageWidth"] == 640


def test_navi_debug_empty():
  result = snapshot_carrot_navi_debug()
  assert result["ok"] is True
  assert result["has_debug"] is False


def test_navi_debug_with_data(monkeypatch):
  storage = {
    DEBUG_PARAM: json.dumps({
      "receivedAt": "2026-09-12T15:10:00",
      "eventTimeMs": 1234567890,
      "type": "complexCrossroad",
      "summary": {"type": "complexCrossroad", "keys": ["crossroad", "imageBase64"]},
    }),
  }
  monkeypatch.setattr("webui.server.bridge.carrot_navi_api._read_json_param", lambda key: _read(storage, key))
  result = snapshot_carrot_navi_debug()
  assert result["ok"] is True
  assert result["has_debug"] is True
  assert result["debug"]["type"] == "complexCrossroad"
  assert result["debug"]["summary"]["keys"] == ["crossroad", "imageBase64"]

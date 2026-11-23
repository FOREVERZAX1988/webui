"""Developer panel helpers (error log)."""

from __future__ import annotations

import datetime
import os
from pathlib import Path
from typing import Any


def _params():
  from openpilot.common.params import Params
  return Params()


def _error_log_path() -> Path:
  try:
    from openpilot.common.hardware import PC
    from openpilot.common.hardware.hw import Paths
    root = Paths.crash_log_root()
  except Exception:
    root = "/data/crash"
  return Path(root) / "error.log"


def developer_error_log() -> dict[str, Any]:
  path = _error_log_path()
  if os.environ.get("WEBUI_DEV_PC") == "1":
    return {
      "ok": True,
      "exists": False,
      "html": "<p>No error log on PC preview.</p>",
      "dev_pc": True,
    }
  try:
    if not path.is_file():
      return {"ok": True, "exists": False, "html": "<p>No error log found.</p>"}
    mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    header = f"<b>{mtime.strftime('%d-%b-%Y %H:%M:%S').upper()}</b><br><br>"
    try:
      body = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
      body = str(exc)
    escaped = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return {"ok": True, "exists": True, "html": header + f"<pre style='white-space:pre-wrap'>{escaped}</pre>"}
  except Exception as exc:
    return {"ok": False, "error": str(exc)}


def developer_delete_error_log() -> dict[str, Any]:
  path = _error_log_path()
  try:
    if path.is_file():
      path.unlink()
    return {"ok": True}
  except Exception as exc:
    return {"ok": False, "error": str(exc)}


def tailscale_state() -> dict[str, Any]:
  """Tailscale pairing state for the Developer panel QR row.

  Reads the TailscaleState param written by AGNOS's tailscale_manager
  ("pairing|<url>" / "joined|<name>|<ip>" / "error|<msg>") and renders the
  pairing URL as a QR PNG data URL, mirroring the Big GUI TailscaleDialog.
  """
  if os.environ.get("WEBUI_DEV_PC") == "1":
    return {"ok": True, "status": "", "url": "", "ip": "", "qr_data_url": "", "dev_pc": True}
  try:
    raw = _params().get("TailscaleState")
  except Exception as exc:
    return {"ok": False, "error": str(exc)}
  value = str(raw or "").strip()
  status, url, name, ip, message = "", "", "", "", ""
  parts = value.split("|")
  head = parts[0] if parts else ""
  if head == "pairing" and len(parts) >= 2:
    status, url = "pairing", parts[1]
  elif head == "joined" and len(parts) >= 3:
    status, name, ip = "joined", parts[1], parts[2]
  elif head == "error":
    status, message = "error", "|".join(parts[1:])
  elif value:
    status, message = head, value

  qr = ""
  if url:
    try:
      from webui.server.bridge.qr_data_url import qr_data_url
      qr = qr_data_url(url)
    except Exception:
      qr = ""
  return {"ok": True, "status": status, "url": url, "name": name, "ip": ip,
          "message": message, "qr_data_url": qr}


def agent_password_reset() -> dict[str, Any]:
  """Regenerate the AI agent web login password (AgentPassword param)."""
  try:
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(16))
    _params().put("AgentPassword", password, block=True)
    return {"ok": True, "action": "agent_password_reset", "password": password}
  except Exception as exc:
    return {"ok": False, "action": "agent_password_reset", "error": str(exc)}

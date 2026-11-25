import time
from openpilot.common.params import Params
from openpilot.selfdrive.ui.lib.api_helpers import get_token
from openpilot.common.api import api_get

p = Params()
d = p.get("DongleId")
tok = get_token(d)
for i in range(6):
  r = api_get(f"v1.1/devices/{d}/stats", access_token=tok, timeout=10)
  print(i, "status:", r.status_code, r.text[:80])
  time.sleep(1)
# 换一个端点对比：v1/device/ (老端点)
for ep in (f"v1/device/{d}", f"v1.1/me/", "v1.1/devices/"):
  try:
    r = api_get(ep, access_token=tok, timeout=10)
    print(ep, "->", r.status_code, r.text[:100])
  except Exception as e:
    print(ep, "EXC", e)

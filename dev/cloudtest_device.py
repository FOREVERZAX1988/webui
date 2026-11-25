import sys
import webui.server.bridge.trips_api as ta
print("trips_api file:", ta.__file__)
from webui.server.bridge.trips_api import trips_stats
r = trips_stats("cloud")
print("ok:", r["ok"], "error:", r.get("error"))

# 再直接对比手工链路
from openpilot.common.params import Params
from openpilot.selfdrive.ui.lib.api_helpers import get_token
from openpilot.common.api import api_get
import openpilot.common.api.comma_connect as cc
print("API_HOST:", cc.API_HOST)
import jwt as pyjwt
print("jwt lib:", pyjwt.__file__)
import requests as rq
print("requests:", rq.__version__, rq.__file__)
p = Params()
d = p.get("DongleId")
print("dongle:", d)
tok = get_token(d)
r2 = api_get(f"v1.1/devices/{d}/stats", access_token=tok, timeout=10)
print("manual status:", r2.status_code, r2.text[:150])

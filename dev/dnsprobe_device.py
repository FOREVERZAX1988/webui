import socket
import requests

ips = set()
for _ in range(5):
  try:
    infos = socket.getaddrinfo("api.commadotai.com", 443)
    for i in infos:
      ips.add(i[4][0])
  except Exception as e:
    print("dns exc", e)
print("resolved IPs:", ips)

for ip in ips:
  try:
    r = requests.get(
      f"https://api.commadotai.com/v1.1/devices/x/stats",
      timeout=10,
      headers={"Host": "api.commadotai.com"},
      proxies={"http": None, "https": None},
    )
    print(ip, "->", r.status_code, r.text[:80])
  except Exception as e:
    print(ip, "EXC", type(e).__name__, str(e)[:120])

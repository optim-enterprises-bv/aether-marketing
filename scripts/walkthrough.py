#!/usr/bin/env python3
"""Capture a walkthrough of the live Aether UI over CDP."""
import base64
import json
import pathlib
import time

import requests
import websocket

BASE = "http://127.0.0.1:18080"
OUT = pathlib.Path("/tmp/claude-1000/-home-dingo/8fa87e8a-7333-473f-918d-8297ebd71765/scratchpad/walk")
OUT.mkdir(exist_ok=True)
USER, PW = "admin", "je-@QcKHJB3zUT+9-423Dut!"

tabs = requests.get("http://127.0.0.1:9222/json").json()
page = next(t for t in tabs if t["type"] == "page")
ws = websocket.create_connection(page["webSocketDebuggerUrl"], suppress_origin=True, timeout=60)
_id = [0]


def cmd(method, **p):
    _id[0] += 1
    ws.send(json.dumps({"id": _id[0], "method": method, "params": p}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == _id[0]:
            if "error" in m:
                raise RuntimeError(f"{method}: {m['error']}")
            return m.get("result", {})


def js(e):
    return cmd("Runtime.evaluate", expression=e, returnByValue=True).get("result", {}).get("value")


def shot(n):
    p = OUT / f"{n}.png"
    p.write_bytes(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))
    return p


cmd("Page.enable")
cmd("Runtime.enable")
cmd("Emulation.setDeviceMetricsOverride", width=1600, height=1000, deviceScaleFactor=1, mobile=False)

# ── login ───────────────────────────────────────────────────────────
cmd("Page.navigate", url=BASE + "/login")
time.sleep(4)
js("""(() => {
  const set=(el,v)=>{const p=Object.getPrototypeOf(el);
    Object.getOwnPropertyDescriptor(p,'value').set.call(el,v);
    el.dispatchEvent(new Event('input',{bubbles:true}));
    el.dispatchEvent(new Event('change',{bubbles:true}));};
  const i=[...document.querySelectorAll('input')];
  set(i.find(x=>x.type!=='password'), %s); set(i.find(x=>x.type==='password'), %s);
})()""" % (json.dumps(USER), json.dumps(PW)))
time.sleep(1)
js("""[...document.querySelectorAll('button,[type=submit]')].find(x=>/sign|log|enter/i.test(x.innerText||''))?.click()""")
time.sleep(6)
print("logged in ->", js("location.href"))

# ── walk ────────────────────────────────────────────────────────────
STOPS = [
    ("/dashboard", "dashboard", 5),
    ("/devices", "devices", 5),
    ("/topology", "topology", 5),
    ("/events", "events", 4),
    ("/analytics", "analytics", 4),
    ("/pki", "pki", 4),
    ("/tmf", "tmf", 4),
    ("/billing", "billing", 4),
]
seen = []
for route, name, wait in STOPS:
    cmd("Page.navigate", url=BASE + route)
    time.sleep(wait)
    txt = (js("document.body.innerText") or "").strip()
    p = shot(name)
    empty = len(txt) < 400
    seen.append((name, route, p.stat().st_size // 1024, "SPARSE" if empty else "ok"))
    print(f"  {name:10} {route:14} {p.stat().st_size//1024:4} KB  {'SPARSE' if empty else 'ok'}")

# ── device detail: click the first row on /devices ──────────────────
cmd("Page.navigate", url=BASE + "/devices")
time.sleep(5)
clicked = js("""(() => {
  const r = document.querySelector('tbody tr, [role=row]:nth-child(2), .device-row');
  if (r) { r.click(); return r.innerText.slice(0,60); } return null;
})()""")
time.sleep(5)
p = shot("device-detail")
print(f"  device-detail  clicked={clicked!r}  {p.stat().st_size//1024} KB  url={js('location.href')}")

print("\nframes:", len(list(OUT.glob("*.png"))))
ws.close()

#!/usr/bin/env python3
"""A-track LinkedIn document ad — 6 square slides, converged access story."""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

W = H = 720.0
M = 64.0

BG     = HexColor("#0B0F14")
CARD   = HexColor("#111827")
LINE   = HexColor("#1F2937")
TXT    = HexColor("#F0F4F8")
SEC    = HexColor("#9CA3AF")
MUT    = HexColor("#6B7280")
CYAN   = HexColor("#22D3EE")
BLUE   = HexColor("#0EA5E9")
VIOLET = HexColor("#8B5CF6")
EMER   = HexColor("#10B981")
AMBER  = HexColor("#F59E0B")
ROSE   = HexColor("#F43F5E")
PINK   = HexColor("#F472B6")
LIME   = HexColor("#A3E635")

B, R, Mo = "Helvetica-Bold", "Helvetica", "Courier-Bold"
c = canvas.Canvas("aether-converged-access.pdf", pagesize=(W, H))


def bg():
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def chrome(n, total=7):
    c.setFont(Mo, 8)
    c.setFillColor(MUT)
    c.drawString(M, 34, "AETHER-IO.COM")
    c.drawRightString(W - M, 34, f"{n} / {total}")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(M, 52, W - M, 52)


def eyebrow(y, text, col=CYAN):
    c.setFont(Mo, 9)
    c.setFillColor(col)
    c.drawString(M, y, text.upper())
    return y - 34


def heading(y, lines, size=40, lead=46, col=TXT):
    c.setFont(B, size)
    for ln in lines:
        if ln.startswith("~"):
            c.setFillColor(CYAN); ln = ln[1:]
        else:
            c.setFillColor(col)
        c.drawString(M, y, ln)
        y -= lead
    return y


def body(y, text, size=13.5, lead=21, col=SEC, width=None, font=R):
    width = width or (W - 2 * M)
    c.setFont(font, size)
    c.setFillColor(col)
    for ln in simpleSplit(text, font, size, width):
        c.drawString(M, y, ln)
        y -= lead
    return y


def rule(y, col=LINE):
    c.setStrokeColor(col); c.setLineWidth(0.5)
    c.line(M, y, W - M, y)
    return y - 26


# ── 1 · cover ────────────────────────────────────────────────────────
bg()
c.setFillColor(CYAN); c.rect(M, H - 150, 54, 4, stroke=0, fill=1)
y = heading(H - 250, ["Two networks.", "~One control plane."], 46, 56)
y = body(y - 14, "Fixed access and mobile access are managed by two disjoint "
                 "toolchains, two data models and two on-call rotations. "
                 "Aether puts them behind one.", 15, 24)
y -= 26
c.setFont(Mo, 10); c.setFillColor(MUT)
c.drawString(M, y, "10 PROTOCOLS  ·  ONE BINARY  ·  OPEN AGENT  ·  MANAGED PLATFORM")
chrome(1); c.showPage()

# ── 2 · the problem ──────────────────────────────────────────────────
bg()
y = eyebrow(H - 92, "The problem", ROSE)
y = heading(y, ["The access network is", "~managed twice."], 36, 44)
y = body(y - 6, "Every operator runs both of these. Almost nobody runs them "
                "from one place.", 13.5, 21)
y -= 26

cols = [
    ("CPE / WiFi", CYAN, ["uCentral · TIP OpenWiFi", "TR-369 / USP", "WRP · RDK-B",
                          "IEEE 1905.1 EasyMesh", "OpenSync"], "Broadband team"),
    ("Transport / RAN", VIOLET, ["NETCONF + YANG", "SNMP v1/v2c/v3", "gNMI streaming",
                                 "O-RAN A1 policy", "VES event collector"], "RAN + transport team"),
]
cw, gap = (W - 2 * M - 24) / 2, 24
top, ch = y, 258
for i, (title, col, items, owner) in enumerate(cols):
    x = M + i * (cw + gap)
    c.setFillColor(CARD); c.setStrokeColor(LINE); c.setLineWidth(1)
    c.roundRect(x, top - ch, cw, ch, 10, stroke=1, fill=1)
    c.setFont(B, 15); c.setFillColor(col)
    c.drawString(x + 20, top - 34, title)
    c.setFont(R, 11.5); c.setFillColor(SEC)
    yy = top - 62
    for it in items:
        c.drawString(x + 20, yy, "· " + it); yy -= 21
    c.setStrokeColor(LINE); c.line(x + 20, yy - 4, x + cw - 20, yy - 4)
    c.setFont(Mo, 8.5); c.setFillColor(MUT)
    c.drawString(x + 20, yy - 24, owner.upper())

y = top - ch - 34
c.setFont(B, 14); c.setFillColor(TXT)
c.drawString(M, y, "When a subscriber says “my connection is bad” —")
c.setFont(R, 14); c.setFillColor(SEC)
c.drawString(M, y - 24, "no single system can see the home, the backhaul and the radio.")
chrome(2); c.showPage()

# ── 3 · ten protocols ────────────────────────────────────────────────
bg()
y = eyebrow(H - 92, "Protocol coverage", CYAN)
y = heading(y, ["Ten protocols.", "~One binary."], 36, 44)
y -= 6

protos = [
    ("uCentral / TIP",  "WebSocket + JSON · OpenWiFi, OpenWrt",        CYAN),
    ("TR-369 / USP",    "WebSocket + MQTT · protobuf · QSDK, prplOS",  BLUE),
    ("WRP / Xmidt",     "RDK-B, zero-install via Parodus",             VIOLET),
    ("IEEE 1905.1",     "EtherType 0x893a · CMDU · EasyMesh R1–R5", PINK),
    ("OpenSync",        "MQTT · Plume migration path",                 AMBER),
    ("MQTT",            "3.1 / 5.0 clustered broker · USP MTP",        EMER),
    ("NETCONF / YANG",  "SSH + XML · RFC 6241 / 6242",                 ROSE),
    ("SNMP",            "v1 / v2c / v3 · polling + traps",             LIME),
    ("gNMI",            "gRPC + protobuf · OpenConfig telemetry",      PINK),
    ("O-RAN A1 / VES",  "A1 policy → Near-RT RIC · VES collector", AMBER),
]
yy = y
for i, (name, desc, col) in enumerate(protos):
    c.setFillColor(col); c.rect(M, yy - 3, 3, 15, stroke=0, fill=1)
    c.setFont(B, 12.5); c.setFillColor(TXT)
    c.drawString(M + 16, yy, name)
    c.setFont(R, 11); c.setFillColor(MUT)
    c.drawString(M + 186, yy, desc)
    yy -= 30
    if i == 5:
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        c.line(M, yy + 12, W - M, yy + 12)
        yy -= 8
c.setFont(Mo, 9); c.setFillColor(MUT)
c.drawString(M, yy - 4, "ABOVE THE LINE: CPE.   BELOW: TRANSPORT, BACKHAUL AND RAN.")
chrome(3); c.showPage()

# ── 4 · what we are / are not ────────────────────────────────────────
bg()
y = eyebrow(H - 88, "Precision", VIOLET)
y = heading(y, ["Aether is not a RIC.", "~Here is what it is."], 32, 40)
y -= 4

bands = [
    ("IS", EMER, ["A1 client — deliver, withdraw, fetch and status policy",
                  "VES collector — events into ONAP-style OSS",
                  "Device.Cellular — IMEI, IMSI, RSRP, RSRQ, SINR on FWA CPE",
                  "One data model across CPE, transport and RAN"]),
    ("ON THE ROADMAP", AMBER, ["O1 interface — the NETCONF/YANG transport is already in place",
                               "Non-RT RIC / rApp runtime over R1",
                               "STOMP and CoAP message transports"]),
    ("IS NOT", ROSE, ["A Near-RT RIC, or E2 termination",
                      "An xApp hosting platform",
                      "A replacement for your RAN vendor's EMS"]),
]
for title, col, items in bands:
    c.setFont(Mo, 9.5); c.setFillColor(col)
    c.drawString(M, y, title)
    y -= 21
    for it in items:
        c.setFillColor(col); c.setFont(R, 12)
        c.drawString(M, y, "—")
        c.setFillColor(SEC)
        c.drawString(M + 18, y, it)
        y -= 20
    y -= 14

y = rule(y + 6)
y = body(y, "The hard part was never A1. It was a data model where a TR-181 "
            "parameter from an OpenWrt box and a gNMI subscription from an "
            "aggregation switch are both first-class.", 12, 19, MUT)
chrome(4); c.showPage()

# ── 5 · the open agent ───────────────────────────────────────────────
bg()
y = eyebrow(H - 92, "Open source", CYAN)
y = heading(y, ["ac-client.", "~Download. Install. Sign up."], 34, 42)
y = body(y - 6, "The agent is open source under BSD 3-Clause. The platform it "
                "reports to is a managed service. Three commands and the router "
                "is under management.", 13, 21)
y -= 24

c.setFillColor(CARD); c.setStrokeColor(LINE); c.setLineWidth(1)
c.roundRect(M, y - 78, W - 2 * M, 74, 8, stroke=1, fill=1)
c.setFont(Mo, 11); c.setFillColor(CYAN)
c.drawString(M + 20, y - 26, "opkg install ac-client luci-app-aclient")
c.setFillColor(MUT)
c.drawString(M + 20, y - 46, "uci set optimacs.@config[0].claim_token='...'")
c.drawString(M + 20, y - 66, "/etc/init.d/ac-client start")
y -= 104

feats = [("TR-369 / USP 1.3", "TP-469 conformance tested", CYAN),
         ("Post-quantum mTLS", "X25519 + ML-KEM-768, always on", VIOLET),
         ("UCI-backed TR-181", "47 backend operations", EMER),
         ("WiFi 7 + Cellular", "EHT modes and Device.Cellular", AMBER)]
for name, desc, col in feats:
    c.setFillColor(col); c.rect(M, y - 3, 3, 14, stroke=0, fill=1)
    c.setFont(B, 12.5); c.setFillColor(TXT); c.drawString(M + 16, y, name)
    c.setFont(R, 11.5); c.setFillColor(MUT); c.drawString(M + 210, y, desc)
    y -= 27

y = rule(y - 2)
c.setFont(R, 12.5); c.setFillColor(SEC)
c.drawString(M, y, "1,500+ OpenWrt router models. No custom firmware image.")
chrome(5); c.showPage()

# ── 6 · how it deploys ───────────────────────────────────────────────
bg()
y = eyebrow(H - 92, "Deployment", EMER)
y = heading(y, ["Meet the device", "~where it is."], 36, 44)
y = body(y - 6, "No reflash. No certification cycle. No truck roll.", 13.5, 21)
y -= 28

rows = [
    ("RDK-B",    "Terminates the Parodus/WRP session already running.\nNo firmware change.", EMER),
    ("OpenWrt",  "opkg package install. 30k+ router models.", CYAN),
    ("QSDK",     "Agent wrapping cfg80211tool and qca-hostapd.", BLUE),
    ("prplOS",   "Speaks the TR-181 data model bus already present.", VIOLET),
    ("OpenWiFi", "Native uCentral client.", AMBER),
    ("Aggregation gear", "NETCONF or gNMI. SNMP for anything older.", ROSE),
]
for name, desc, col in rows:
    c.setFillColor(col); c.circle(M + 4, y + 4, 3.5, stroke=0, fill=1)
    c.setFont(B, 13); c.setFillColor(TXT)
    c.drawString(M + 20, y, name)
    c.setFont(R, 11.5); c.setFillColor(MUT)
    dy = y - 17
    for ln in desc.split("\n"):
        c.drawString(M + 20, dy, ln); dy -= 16
    y = dy - 14

y = rule(y + 6)
c.setFont(B, 13); c.setFillColor(TXT)
c.drawString(M, y, "Config changes ship as JSON Patch (RFC 6902)")
c.setFont(R, 13); c.setFillColor(SEC)
c.drawString(M, y - 22, "~200 bytes per update, not a ~50 KB full-config push.")
chrome(6); c.showPage()

# ── 7 · CTA ──────────────────────────────────────────────────────────
bg()
c.setFillColor(VIOLET); c.rect(M, H - 150, 54, 4, stroke=0, fill=1)
y = heading(H - 236, ["Ten protocols.", "~One control plane."], 40, 50)
y = body(y - 8, "Built for a messy access network. Multiple CPE silicon vendors, a "
                "platform inherited from an acquisition, aggregation gear still on "
                "SNMP, and fixed wireless CPE nobody has a dashboard for.",
         13.5, 22)
y -= 24
for t in ["$0.30 / device / month at volume — no per-device AI tax",
          "Open source agent, managed platform, EU / US data residency",
          "Self-hosting licensed on Enterprise"]:
    c.setFillColor(CYAN); c.drawString(M, y, "—")
    c.setFont(R, 13); c.setFillColor(SEC); c.drawString(M + 20, y, t)
    y -= 24

y -= 16
c.setFillColor(CARD); c.setStrokeColor(CYAN); c.setLineWidth(1)
c.roundRect(M, y - 78, W - 2 * M, 74, 10, stroke=1, fill=1)
c.setFont(B, 16); c.setFillColor(TXT)
c.drawString(M + 24, y - 32, "aether-io.com")
c.setFont(R, 12); c.setFillColor(SEC)
c.drawString(M + 24, y - 54, "Running today · aether-io.com/pricing")
c.setFont(Mo, 9); c.setFillColor(MUT)
c.drawString(M, y - 108, "OPTIM ENTERPRISES BV")
chrome(7); c.showPage()

c.save()
print("wrote aether-converged-access.pdf")

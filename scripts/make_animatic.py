#!/usr/bin/env python3
"""Animatic for the B3 demo storyboard — timing + caption reference, NOT a demo.

Renders one frame per shot at 1080x1080 with the burned-in caption exactly as
specified in docs/demo-video-storyboard.md, so pacing and caption legibility can
be checked before anyone opens OBS.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

W = H = 1080.0
BG = HexColor("#0B0F14")
CARD = HexColor("#111827")
LINE = HexColor("#1F2937")
TXT = HexColor("#F0F4F8")
SEC = HexColor("#9CA3AF")
MUT = HexColor("#4B5563")
CYAN = HexColor("#22D3EE")
AMBER = HexColor("#F59E0B")

B, R, Mo = "Helvetica-Bold", "Helvetica", "Courier-Bold"

# (seconds, screen description, caption lines)
SHOTS = [
    (5, "Cold open — fleet overview, already loaded.\nSlow 4% push-in. No login, no landing page.",
     ["One control plane. Every device."]),
    (9, "Device list. Slow scroll, ~1 row / 250 ms.\nPause 1 s where RDK-B and OpenWrt sit adjacent.",
     ["OpenWrt, RDK-B, QSDK, OpenWiFi, prplOS.", "One list. No per-platform silo."]),
    (10, "Click one subscriber. Detail view:\nmesh topology, clients, signal. Replay a steering event.",
     ["One subscriber. Mesh topology, clients, RF — live."]),
    (12, "THE MONEY SHOT. New IP camera joins.\nArgus resolves vendor + type. Aegis applies IoT policy.",
     ["New device joins. Fingerprinted before it finishes associating.",
      "DHCP options + mDNS + OUI → policy applied automatically."]),
    (10, "Change one setting (SSID rename).\nCut to the JSON Patch body if the UI does not show it.",
     ["Config ships as a JSON Patch. ~200 bytes, not a ~50 KB push."]),
    (9, "Static end card. No animation. Hold 4 s.\nTight loop back to shot 1 — LinkedIn autoplays on repeat.",
     ["Aether", "Running today · aether-io.com"]),
]

c = canvas.Canvas("animatic.pdf", pagesize=(W, H))
t0 = 0
for i, (dur, screen, caps) in enumerate(SHOTS, 1):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # shot chrome
    c.setFont(Mo, 15)
    c.setFillColor(CYAN)
    c.drawString(64, H - 74, f"SHOT {i}")
    c.setFillColor(MUT)
    c.drawRightString(W - 64, H - 74, f"{t0//60}:{t0%60:02d} – {(t0+dur)//60}:{(t0+dur)%60:02d}   ({dur}s)")
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(64, H - 96, W - 64, H - 96)

    # placeholder frame — this is where the screen recording goes
    c.setFillColor(CARD)
    c.setStrokeColor(LINE)
    c.roundRect(64, 300, W - 128, 480, 14, stroke=1, fill=1)
    c.setFont(Mo, 13)
    c.setFillColor(AMBER)
    c.drawString(96, 736, "SCREEN RECORDING GOES HERE")
    c.setFont(R, 19)
    c.setFillColor(SEC)
    y = 690
    for para in screen.split("\n"):
        for ln in simpleSplit(para, R, 19, W - 192):
            c.drawString(96, y, ln)
            y -= 28

    # caption bar, as it will be burned in
    bar_h = 60 + 46 * (len(caps) - 1)
    c.setFillColor(HexColor("#0B0F14"))
    c.rect(0, 150, W, bar_h, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.line(0, 150 + bar_h, W, 150 + bar_h)
    c.setFont(B, 34)
    yy = 150 + bar_h - 46
    for k, cap in enumerate(caps):
        c.setFillColor(TXT if (i != 6 or k == 0) else SEC)
        if i == 6 and k == 0:
            c.setFont(B, 44)
        c.drawCentredString(W / 2, yy, cap)
        c.setFont(B, 34)
        yy -= 46

    c.setFont(Mo, 12)
    c.setFillColor(MUT)
    c.drawCentredString(W / 2, 90, "ANIMATIC — TIMING AND CAPTION REFERENCE, NOT THE DEMO")
    c.showPage()
    t0 += dur

c.save()
print(f"animatic.pdf — {len(SHOTS)} shots, {t0}s total")

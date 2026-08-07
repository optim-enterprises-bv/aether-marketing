# Demo video — storyboard (post B3)

A 55-second native LinkedIn video recorded against `gw.aether-io.com`.
Accompanying post copy lives in `linkedin-playbook.md` under **B3**.

An A-track variant (O-RAN / convergence) is at the bottom — same shoot,
different shot 5 and end card.

---

## Specs

| | |
|---|---|
| Aspect | **1:1 square** (1080×1080). Squares take ~40% more feed height on mobile than 16:9 |
| Length | **50–58s.** Under 60 keeps it in-feed rather than treated as long-form |
| Format | MP4, H.264, 30 fps, ~10–12 Mbps |
| Audio | **None.** No music, no VO — most of the feed watches muted, and silence removes a production dependency |
| Captions | **Burned in.** Not an SRT. LinkedIn's auto-captions won't fire without audio |
| Caption style | Bottom third, Inter/Helvetica Bold 34–38 px, white on a 70%-opacity `#0B0F14` bar, 2 lines max |

Capture at 2560×1440, then crop to a 1440×1440 square centred on the content
area, then downscale to 1080. Recording square natively makes the dashboard
layout cramped.

---

## Pre-flight — do this before you hit record

The lab is currently a working development environment, not a demo
environment. Three things will show up on camera if you don't fix them first.

1. **Seed a believable fleet.** A demo with 4 devices reads as a prototype.
   Aim for 40+ devices with a realistic mix — OpenWrt, RDK-B, QSDK, OpenWiFi,
   prplOS — and plausible names, not `test-device-01`.
2. **Clear the failing USP agent.** `agent_id: unknown:f9050d47-…` has been
   failing to decode a Record every 30 seconds. If that surfaces anywhere in
   the UI as an error badge or a red device, it's the only thing anyone will
   look at.
3. **Warm the UI first.** Telemetry inserts are currently taking 1.5–8s. Click
   through the exact path once before recording so caches are warm, and be
   ready to cut around any spinner. If a view can't be made to feel instant,
   cut it from the video — a laggy demo is worse than a shorter one.

Also: clean browser profile, no bookmarks bar, no extensions, no notifications,
dark mode, `Cmd/Ctrl +` to a comfortable zoom so text survives the downscale.
Move the cursor slowly and deliberately — fast mouse movement looks nervous.

---

## Shot list

### 1 · Cold open — the fleet `0:00 – 0:05`

Fleet overview, already loaded. **No login, no landing page.** Start on data.

Slow push-in (subtle Ken Burns, ~4% over 5s) on the fleet map or device grid.

> **Caption:** One control plane. Every device.

The first 2 seconds decide whether anyone keeps watching. It must be
immediately obvious this is a real system with real devices in it.

---

### 2 · The mixed fleet `0:05 – 0:14`

Device list. Scroll slowly — roughly one row per 250 ms. The platform column
must be legible: OpenWrt, RDK-B, QSDK, OpenWiFi, prplOS all visible in one
viewport.

Pause the scroll for ~1s on a row where an RDK-B and an OpenWrt device sit
adjacent. That adjacency is the whole product.

> **Caption:** OpenWrt, RDK-B, QSDK, OpenWiFi, prplOS.
> **Caption:** One list. No per-platform silo.

---

### 3 · Drill into a subscriber `0:14 – 0:24`

Click one subscriber. Land on their detail view — mesh topology, connected
clients, signal.

If you have a steering event you can trigger or replay, do it here and let the
topology redraw on camera. A live state change is worth more than any static
view.

> **Caption:** One subscriber. Mesh topology, clients, RF — live.

---

### 4 · Argus classifies an unknown device `0:24 – 0:36`

**The money shot.** Bring a new IoT device onto the network — an IP camera is
ideal, it's a device type operators recognise as a support burden.

Show, in sequence:
1. Device appears as unknown
2. Argus resolves it — vendor and device type — from DHCP options, mDNS and OUI
3. Aegis places it on the IoT policy
4. No operator action anywhere in that chain

If this can't be made to happen live and reliably, record it separately and cut
to it. Do not fake it — but do rehearse it.

> **Caption:** New device joins. Fingerprinted before it finishes associating.
> **Caption:** DHCP options + mDNS + OUI → policy applied automatically.

---

### 5 · The config push `0:36 – 0:46`

Change one setting — an SSID rename is the clearest. Show the change landing on
the device.

If the UI exposes the delta payload, show it. If not, cut to a terminal with the
JSON Patch body visible — a `[{"op":"replace","path":"/ssid",…}]` at ~200 bytes
next to the size of the full config is the most persuasive frame in the video
for a technical audience.

> **Caption:** Config ships as a JSON Patch. ~200 bytes, not a ~50 KB push.

**Do not put a latency number on screen.** That claim was pulled from the site
and hasn't been measured.

---

### 6 · End card `0:46 – 0:55`

Cut to a static card. Brand background `#0B0F14`, cyan rule, no animation.

```
Aether

Running today · Early access
aether-io.com
```

Hold 4 seconds. Long enough to read, short enough not to lose the loop —
LinkedIn autoplays video on repeat, and a tight loop back to shot 1 measurably
increases watch time.

---

## Honesty line

The post copy ends with *"Still early. Still ugly in places. But it's real."*

Keep it. Engineers discount polished demos automatically; an admitted rough
edge is what makes the rest credible. If something visibly glitches during a
take and it isn't an error state, consider keeping it.

---

## A-track variant (O-RAN / convergence)

Same shoot, two changes. Use this one if you lead with Track A.

**Replace shot 5** with the protocol breadth reveal `0:36 – 0:46`:

Cut to a view — device list filtered by protocol, or the protocol matrix —
where CPE and transport/RAN devices appear in the same table. Scroll so
uCentral, TR-369, NETCONF, SNMP, gNMI and O-RAN A1 are all visible.

> **Caption:** The same control plane holds the CPE fleet…
> **Caption:** …and NETCONF, SNMP, gNMI and O-RAN A1 for transport and RAN.

**Replace the end card:**

```
Aether

Ten protocols. One binary.
aether-io.com
```

**A-track post copy:**

> 45 seconds: an OpenWrt router in someone's living room and an aggregation
> switch speaking gNMI, in the same device list.
>
> Watch the fourth row. Argus fingerprints a camera from DHCP options and mDNS
> before it finishes associating, and Aegis puts it on the IoT policy — no
> operator action.
>
> Then the filter changes and the same table shows NETCONF, SNMP and O-RAN A1
> endpoints. Same control plane, same data model.
>
> Not a RIC. An A1 client and a VES collector that happens to also run your
> CPE fleet.
>
> Still early. Still ugly in places. But it's real.

---

## Tooling

- **Capture:** OBS (scene = single browser window, 2560×1440 canvas), or
  `wf-recorder` / `kooha` on Wayland.
- **Edit:** Kdenlive or DaVinci Resolve. Both handle burned-in captions fine.
- **Captions:** add as title clips, not filters — easier to time and restyle.
- **Export:** H.264, 30 fps, CRF 18–20, 1080×1080, no audio track at all
  (an empty audio track can trip LinkedIn's processing).

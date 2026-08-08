# Aether — go-to-market playbook

Four tracks. **Track A (O-RAN / convergence) leads on LinkedIn.** Track B (WiFi
economics) is the commercial follow-on. **Track C (OpenWrt / bottom-up) does not
run on LinkedIn at all** — it's the only track with a same-day feedback loop, and
it lives where the users actually are. **Track D (OEM/ODM firmware)** sells a
different thing entirely — engineering, not subscriptions — to device makers.

## Positioning in one line

> **Open OpenWrt agent. Managed platform.**
> `ac-client` — the **OpenWrt** USP/TR-369 package — is open source under BSD
> 3-Clause. Download, install, sign up.
> QSDK, prplOS and RDK-B run their own native agents; Aether speaks to those
> directly, nothing to install. The platform itself is proprietary.

## Company context — use it, it's the strongest card

Aether reads like a new product from an unknown company. It isn't, and every
track below is weaker for not saying so.

| Asset | Why it matters |
|---|---|
| **5M+ devices under management worldwide** via the global ACS | The most persuasive fact available. An operator's first question is "can you handle our fleet" — this answers it before it's asked |
| **Firmware is an existing business** | OpenWRT, OpenWiFi, wlan-ap, RDK-B, QSDK, plus camera and IoT firmware on embedded Linux |
| **A shipping NVR product** | `nvr.optimcloud.com`, nvr-server 2.0.0 — camera management, not a slideware adjacency |
| **Track record to 2022** | APClient, APConfig, wlan-cloud-ucentral-deploy, the OpenWiFi repos |
| **Optim Enterprises BV** — sovereign IaaS, NVR, LLM inference, eCommerce, global ACS | Aether is a new product from an operating company, not a startup's first swing |

**Lead with this in any first contact.** "We already manage 5M+ devices, and we
write the firmware and the NVR underneath them — Aether is the platform we built
to replace the seven stacks in the middle" is a fundamentally different opening
from "we built a thing."

Reconcile the number first: optimcloud.com currently says 4.21M in three places.
Pick the real figure and pair it with *since when* and *how many operators* — a
bare number invites doubt, an anchored one doesn't.

Post from a **personal profile**, not the company page — roughly 5–10x the
organic reach. Mechanics for every LinkedIn post below:

- **No links in the post body.** Link goes in the first comment; say "link in comments."
- Tue–Thu, **08:00 CET**. Catches EU operators mid-morning, US East Coast pre-work.
- First two lines are all that shows before "…see more."
- Reply to every comment in the first hour; your replies count as engagement.
- Get 5 people to **comment** (not react) in the first hour. Comments outweigh reactions.

---

## Claims discipline

Written to survive a hostile RAN engineer in the comments. Keep it that way.

### Safe — verified in the codebase

| Claim | Evidence |
|---|---|
| 10 protocols in one binary | `crates/` — ucentraljson, usp, wrp, ieee1905, opensync, MQTT, netconf, snmp, gnmi, oran |
| NETCONF/YANG, RFC 6241/6242 | `crates/netconf` — framing, rpc, session |
| SNMP v1/v2c/v3, polling + traps | `crates/snmp` |
| gNMI streaming telemetry | `crates/gnmi` |
| **O-RAN O1 over real NETCONF** | `crates/oran/lib.rs` — `/api/v1/oran/nodes/:serial/config` get-config/edit-config; verified against netopeer2 in `proto-sims` |
| **VES 7 collector** | `/eventListener/v7` — the standard O-RAN/ONAP path |
| **Federated ML** | `crates/prometheus-engine/src/federated/` — `aggregator.rs`, `round.rs` |
| **Live protocol test targets in-cluster** | `proto-sims` ns: O-RAN-SC a1-simulator 2.5.0, Nokia SR Linux (gNMI), sysrepo/netopeer2, snmpsim, VES sink |
| **O-RAN A1 full policy lifecycle** | `crates/oran/a1_client.rs` — `deliver`, `withdraw`, `fetch_policy`, `list_policy_types`, `fetch_status`, `upsert_status` |
| **VES collector** | `crates/oran/ves.rs` |
| **Device.Cellular on OpenWrt CPE** | `ac-client src/usp/dm/misc.rs` — IMEI, IMSI, ICCID, RSRP, RSRQ, SINR via ModemManager |
| TMF621/632/638/678 | `crates/tmf-api` |
| Post-quantum mTLS, X25519 + ML-KEM-768 | `rustls-post-quantum`, always on, no toggle |
| RDK-B zero-install via Parodus | `crates/proto-wrp`, `crates/parodus2ccsp` |
| TR-369 / USP 1.3, TP-469 tested | ac-client — TP-469 report, 25 OB-USP-Agent instances |
| ac-client is **BSD 3-Clause**, **OpenWrt only** | repo `LICENSE`; README is "USP Agent for OpenWrt Access Points"; zero QSDK/RDK-B/prplOS references in source |
| QSDK / prplOS / RDK-B need **no Aether agent** | They run their own — Parodus on RDK-B, the TR-181 bus on prplOS. Aether terminates what is already there |
| 47 UCI backend operations, WiFi 7 EHT | ac-client README |
| ~1,500+ OpenWrt router models | OpenWrt Table of Hardware, current stable |
| **IoT: MQTT ingest + LwM2M** | `connection-manager/iot_mqtt.rs` 253 L, `lwm2m.rs` 521 L — ADR-005 Accepted. ONVIF/Matter not built |
| **All 4 USP MTPs terminate on the platform** | `crates/connection-manager/uspcoap.rs` (249 L), `uspstomp.rs` (398 L), 6 tests, wired into `Protocol` enum |
| JSON Patch delta, ~200 B vs ~50 KB | RFC 6902 — property of the format, not a benchmark |
| $0.30 / $0.50 / $5 pricing | Published |
| **5M+ devices under management** | Existing global ACS fleet — not the Aether dev instance, which has 0 devices and 3.4k telemetry rows |
| **Firmware across OpenWRT, OpenWiFi, wlan-ap, RDK-B, QSDK, camera + IoT/embedded Linux** | optimcloud.com Engineering; an existing line of business |
| **NVR product shipping** | `nvr.optimcloud.com`, nvr-server 2.0.0 running in cluster |
| QSDK on-device translation is **obuspa** against the QCA HAL | `crates/platform/src/qsdk.rs` doc comment; our part is server-side config rendering + TR-181 params |
| `cfg80211tool` / `qca-hostapd` are **Qualcomm's**, ship with QSDK | 0 references anywhere in our tree |

### Do NOT claim

- ❌ `200k+ concurrent connections` — never load-tested
- ❌ **`Aether Home app`** — no codebase. The $5/home tier sells it.
- ⚠️ **`Aether Ops mobile terminal`** — the app exists (Expo, Phase 1: login,
  device list, detail, reboot) but has **no RTTY terminal**, which the name
  implies. Say "Aether Ops app (early access)", not "mobile terminal".
- ❌ `<1ms config delta delivery` — never measured
- ⚠️ `distributed SQL` — **supported, not deployed here.** sqlx is built on the PostgreSQL wire protocol (`features = ["postgres"]`), so CockroachDB is a deployment choice rather than a code change. Say "deploys against PostgreSQL or CockroachDB", not "we run CockroachDB", until a CRDB deployment is tested.
- ⚠️ `event streaming` — **the capability is real**: `crates/pheme` (pub/sub, webhooks, delivery), `crates/audit` (immutable journal + rollback), `crates/events` (SSE), over a 3-node EMQX MQTT 5.0 cluster. What does not exist is a Kafka/Redpanda log. Describe the pipeline, don't name Kafka.
- ❌ Any SLA as a current term — 99.9/99.99% are GA commitments
- ❌ **`Apache-2.0`** — the repo is BSD 3-Clause. Apache adds a patent grant BSD-3 lacks; if you want that, relicence first, then say it.
- ⚠️ **`4 MTPs`** — true of the **platform** (all four terminate). NOT true of **ac-client**, which is WebSocket + MQTT only. Always say which side you mean.
- ❌ **`30k+ router models`** — off by an order of magnitude.
- ❌ **"Aether is open source"** — only `ac-client` is, and only on OpenWrt.
- ❌ **"the device agent is open source"** — `ac-client` is the **OpenWrt** package and it is open. Other platforms do not run an Aether agent at all. Say "the OpenWrt agent", never "the agent".
- ❌ **"Self-hosted"** as a headline — it's licensed on Enterprise only.
- ❌ **"Aether is a RIC"** — it speaks A1 and emits VES. Not the same thing.
- ❌ **`cfg80211tool` / `qca-hostapd` as ours** — Qualcomm ships both with QSDK.
- ❌ **camera / PTZ / RTSP in `ac-client`** — removed in `c64a286`. That work lives in **nvr-server** now. MQTT video streaming and MQTT PTZ control were real (`0321664`, `a793c19`) but verify they are in nvr-server 2.0.0 before claiming them.
- ⚠️ **`AS207819`** — RIPE RDAP resolves it to NOVAMETRO OU, not Optim Enterprises. It's on optimcloud.com and staying there by decision; just don't repeat it in a post without knowing the arrangement, because peering people check ASNs reflexively.

**Benchmark rule:** post the hardware and duration with any number, or don't post
the number. Fix the telemetry write batching before publishing throughput figures.

---

# Track A — O-RAN / convergence (LinkedIn lead)

Fixed and mobile access run on two disjoint toolchains. Nobody has put them
behind one control plane. No WiFi vendor can follow — it's outside their category.

## A1 — The convergence problem (no product mention)

> Most operators run two completely separate management worlds and pretend
> they're one network.
>
> The CPE fleet lives in a WiFi cloud — uCentral, TR-369, maybe Plume or Mist.
> Managed by the broadband team.
>
> Transport and RAN live somewhere else entirely — NETCONF and YANG on the
> aggregation gear, SNMP on whatever's too old for that, gNMI if someone
> modernised, A1 policies into a Near-RT RIC if there's a RAN team with budget.
>
> And fixed wireless CPE usually has no dashboard at all.
>
> Two toolchains. Two data models. Two on-call rotations. When a subscriber says
> their connection is bad, nobody can say whether the problem is in the home, the
> backhaul, or the radio — because no single system sees all three.
>
> I keep hearing "converged access" in vendor decks. I have yet to see anyone
> ship a control plane that actually spans it.
>
> Is anyone running fixed and mobile access from one system? Genuinely asking.

## A2 — What we built

> We manage over 5 million devices. Aether is the platform we built to replace
> the seven stacks underneath that.
>
> Ten protocols in one binary, because the alternative was ten integrations.
>
> CPE side: uCentral, TR-369/USP, WRP for RDK-B, IEEE 1905.1 for EasyMesh,
> OpenSync, MQTT.
>
> Transport and RAN side: NETCONF with YANG models, SNMP for everything too old
> to speak anything better, gNMI for streaming telemetry, and O-RAN A1 plus VES.
>
> One process. One normalized event stream. An OpenWrt router in a living room
> and an A1 policy toward a Near-RT RIC land in the same pipeline.
>
> Rust. The OpenWrt agent is open source; the platform is a managed service
> with EU and US data residency.
>
> We also write the firmware — OpenWRT, OpenWiFi, wlan-ap, RDK-B, QSDK, plus
> camera and IoT — which is why the protocol coverage looks the way it does.
> We've had to live with all of it.
>
> Architecture write-up in the comments.

## A3 — The precision post (the credibility one)

> Let me be exact, because O-RAN rewards precision and punishes marketing.
>
> **Aether is not a RIC.**
>
> What it is: an A1 client and a VES collector. It runs the full A1 policy
> lifecycle against a Near-RT RIC — deliver, withdraw, fetch, enumerate policy
> types, track status — and emits VES events into an ONAP-style OSS. That's the
> integration surface, and it's deliberately narrow.
>
> What that buys you isn't "we do RAN optimization." It's that the same system
> holding your CPE telemetry can act on RAN policy and report into the same OSS
> your RAN already reports into. Correlation happens in one place instead of in a
> spreadsheet.
>
> Want an xApp platform? We are not that. Anyone telling you their WiFi cloud is
> a RIC is selling you something.
>
> The hard part was never A1. It was a data model where a TR-181 parameter from
> an OpenWrt box and a gNMI subscription from an aggregation switch are both
> first-class.
>
> Tell me where this framing is wrong — I'd rather hear it here than in a deployment.

## A4 — Fixed wireless, the segment nobody manages

> Every operator I talk to has a growing FWA base and no real way to manage it.
>
> The CPE is an LTE or 5G router. It's in a subscriber's window. Its performance
> depends entirely on radio conditions you can't see from a WiFi dashboard.
>
> So when the customer calls, the answer is a truck roll and someone with a
> signal meter.
>
> ac-client reads the modem through ModemManager and exposes it in the standard
> TR-181 data model — Device.Cellular. IMEI, IMSI, ICCID, and live RSRP, RSRQ and
> SINR, alongside the WiFi telemetry from the same box.
>
> Same agent. Same data model. Same dashboard as the fixed-line fleet.
>
> You can finally answer "is it the radio or the router?" without dispatching anyone.
>
> How are you monitoring FWA CPE today? I suspect the honest answer for most is
> "we aren't."

## A5 — RDK-B zero-install

> The hardest part of managing an RDK-B fleet isn't the protocol. It's that
> touching the firmware means a certification cycle.
>
> So we didn't touch it.
>
> RDK-B gateways already run Parodus, speaking WRP to Xmidt. Aether terminates
> that connection directly — no new agent, no firmware change, no cert cycle, no
> truck roll. We bridge into CcspHalExtFetch for the data model and the gateway
> doesn't know anything changed.
>
> Comcast, Cox and Charter CPE work on day one.
>
> Same principle everywhere. OpenWrt gets an opkg install. QSDK gets an agent
> wrapping cfg80211tool and qca-hostapd. prplOS talks to the TR-181 bus already
> there. Aggregation gear gets NETCONF or gNMI, and anything older gets SNMP.
>
> Meet the device where it is. The alternative is asking an operator to reflash a
> million gateways, which is the same as asking them to say no.
>
> We also build RDK-B and QSDK firmware commercially, which is how we learned
> that lesson the expensive way.

## A6 — Post-quantum TLS (contrarian)

> We put post-quantum TLS on CPE and I want to explain why that isn't a gimmick.
>
> X25519 + ML-KEM-768 hybrid, NIST FIPS 203. Always on. No config toggle.
>
> The argument against: nobody's breaking your router's key exchange with a
> quantum computer this decade.
>
> The argument for: a router deployed in 2027 is still in a living room in 2037.
> Harvest-now-decrypt-later is a real threat model for a device with a ten-year
> field life whose management channel carries config, credentials and telemetry.
> You cannot retrofit this across a deployed fleet.
>
> Every other management platform I'm aware of ships classical TLS only. In ten
> years that's a fleet-wide migration nobody budgeted for.
>
> Cost to us was a slightly larger handshake.
>
> Disagree? I'd genuinely like to hear the case against.

## A7 — The close

> Aether is running today. Ten protocols, one control plane, from the CPE in the
> home out to O-RAN A1.
>
> Built by a team already managing 5M+ devices, who also write the firmware
> underneath them.
>
> $0.30 per device per month at volume. No per-device AI tax, no separate charge
> for RF optimization or IoT fingerprinting.
>
> The device agent is open source — install it on an OpenWrt box this afternoon
> and see the device appear. The platform is a managed service with EU and US
> data residency; self-hosting is licensed for operators who need it.
>
> Built for a messy access network: multiple CPE silicon vendors, a platform
> inherited from an acquisition, aggregation gear still on SNMP, and fixed
> wireless CPE nobody has a dashboard for.
>
> Pricing and docs in the comments.

---

# Track B — WiFi economics (LinkedIn, secondary)

Stronger commercial argument, weaker credibility argument — every open-source
challenger has made the "stop paying the SaaS tax" case. Runs after Track A.

| Subscribers | Plume/Mist at ~$3/device | Aether at $0.30 | Annual delta |
|---|---|---|---|
| 100k | $3.6M/yr | $360k/yr | **$3.2M** |
| 333k | $12M/yr | $1.2M/yr | **$10.8M** |
| 1M | $36M/yr | $3.6M/yr | **$32.4M** |

**B1 — The money post.** 300k subscribers ≈ $900k/month for WiFi management
software. RF optimization is a control loop over channel and power;
fingerprinting is DHCP options and OUI lookups. Well-understood engineering, not
a moat — what it is, is a business model that depends on operators having no
alternative. *Ask: what do you actually pay per device?*

**B2 — Seven stacks.** uCentral, TR-369, WRP/Parodus, OpenSync, IEEE 1905.1, one
management stack per silicon vendor. Seven integration teams, no single fleet
view. Hermes, Meridian, Prometheus — yes, Greek gods, it made the architecture
arguments easier to have.

**B3 — The demo.** Native video. See `demo-video-storyboard.md`.

**B4 — Privacy and residency.** Every per-device WiFi SaaS ships subscriber
telemetry to the vendor's cloud. Aether keeps subscriber PII in a separate vault
from the telemetry store with a GDPR data-access API, and offers EU and US
residency. For operators who need it, self-hosting is licensed on Enterprise.

**B5 — The open agent.** *(rewritten — the old version claimed Apache-2.0)*

> Our OpenWrt agent is open source. The platform isn't. That split is deliberate,
> and I want to be precise about where the line falls.
>
> `ac-client` is BSD 3-Clause and OpenWrt-specific. It implements TR-369/USP 1.3,
> it's been tested against the Broadband Forum's TP-469 suite, it drives real
> OpenWrt config through UCI, and it does post-quantum mTLS by default.
>
>
> The other platforms don't run our agent at all. QSDK, prplOS and RDK-B already
> have their own — Parodus on RDK-B, the TR-181 bus on prplOS — and we terminate
> what's already there rather than asking anyone to install something.
>
> The reasoning is simple. If you're going to put an agent on a million devices
> in people's homes, running as root, you should be able to read what it does.
> And if we ever become a company you don't want to deal with, the thing on your
> subscribers' hardware shouldn't be what traps you.
>
> The platform you pay for. The thing in the subscriber's living room you can
> audit, fork, and package yourself.
>
> Repo in the comments.

**B6 — Reuse A7.** Don't write a second close.

---

# Track C — OpenWrt / bottom-up (NOT LinkedIn)

**This is the only track with a same-day feedback loop.** A carrier deal is an
18-month sales cycle. An OpenWrt user installs tonight and tells you what broke
by morning. `ac-client` is the wedge and the open licence is what makes it possible.

Home subscribers are not on LinkedIn. Nothing in Track A or B reaches them.

## Channels

| Where | How to show up |
|---|---|
| **OpenWrt Forum** | A build thread for `ac-client`. Answer questions, don't pitch. Highest-value venue and the hardest to fake. |
| **r/openwrt** | Same content, shorter. Expect scepticism about the managed backend — answer it head-on. |
| **r/homelab, r/selfhosted** | The FWA/cellular angle plays well here; so does "one dashboard for every router in the house." |
| **Hacker News** | *Show HN: an open source TR-369/USP agent for OpenWrt.* Post the repo, not the marketing site. |
| **GitHub** | The repo must look alive — real issues, real commits, a README that works. This is what everyone checks first. |
| **YouTube** | Network-adjacent channels. A 10-minute "manage every router in your house" walkthrough outperforms any written post. |

## The tension to manage

The OpenWrt community is culturally open-source to its core. A closed-source
*platform* behind an open agent will get questioned — repeatedly, and fairly.

Have a straight answer ready and lead with it rather than waiting to be asked:
the agent is BSD 3-Clause and always will be, the platform is how the work gets
paid for, and nothing about the agent forces you to use the platform.

Do not:
- Open a thread with pricing
- Use the word "solution"
- Argue with the licence question — concede it and move on
- Astroturf. It will be spotted, and the OpenWrt forum has a long memory.

## The funnel

`opkg install` → `claim_token` → device appears → they hit the free tier ceiling
→ they pay. Make sure the first three steps work with zero support contact,
because nobody in this audience will email you.

---

# Track D — OEM / ODM firmware (LinkedIn, own audience)

A separate business and a separate buyer. Device makers don't buy a per-device
subscription; they buy engineering. This track sells firmware work, and Aether
follows as the management layer rather than leading.

## What's being sold

Agent implementation, platform HALs and **full firmware builds** across OpenWRT,
OpenWiFi, wlan-ap, RDK-B and QSDK, plus camera and IoT firmware on embedded
Linux. Priced per device. An existing line of business, not a capability claim —
which is the whole advantage.

## Why it converts

An ODM building a gateway has to solve firmware, management and cloud
separately, usually with three vendors and three integration timelines. You do
all three, and the management platform is already built.

Two differentiators most firmware shops can't match:

- **RDK-B and QSDK.** Most shops are OpenWRT-only. RDK-B is where an ODM assumes
  they're stuck with the silicon vendor.
- **Camera and IoT.** A shipping NVR product at `nvr.optimcloud.com`, not a
  claim — including video and PTZ control over MQTT rather than a separate
  streaming stack.

## D1 — The build-vs-buy post

> An ODM quoted a customer 14 months to get a gateway to market. Nine of those
> were firmware and cloud integration, not hardware.
>
> The hardware was done. What wasn't: a management agent, a HAL mapping the
> chipset's proprietary parameters to something standard, a TR-069 or TR-369
> story, and a cloud to point it at.
>
> Four separate problems, usually four separate vendors, and each discovers the
> others' assumptions late.
>
> We do firmware for OpenWRT, OpenWiFi, wlan-ap, RDK-B and QSDK, plus camera and
> IoT firmware on embedded Linux — and the management platform the devices
> report to is ours as well.
>
> One accountability line instead of four.
>
> ODMs and OEMs: what actually blows your schedules? My money's on the
> integration between two vendors who each thought the other owned it.

## D2 — The RDK-B post

> Most firmware shops will take your OpenWRT work and pass on RDK-B.
>
> Which is a problem, because if you're building for a North American MSO, RDK-B
> is what they'll ask for.
>
> We do both, plus QSDK, wlan-ap and OpenWiFi — and camera and IoT firmware on
> embedded Linux. The same team that writes the firmware writes the management
> agent and runs the platform it reports to, so when the CPE misbehaves in the
> field there's no argument about whose bug it is.
>
> Priced per device, so it scales with your volume rather than your schedule.

## Channels

Almost none of this is a feed post. It's targeted outreach.

| Where | How |
|---|---|
| **LinkedIn Sales Navigator** | Titles: VP Engineering, Director of Firmware, Head of Product (CPE), Program Manager – Gateways, at ODMs and OEMs |
| **Direct DM** | Reference their specific product line. A considered purchase; 20 good messages beat any campaign |
| **Broadband Forum / prpl** | ODMs attend for certification reasons. Same rooms as Track A, different conversation |
| **Trade events** | ANGA COM, Network X, MWC — but ODM conversations happen in meeting rooms, not on the floor |

## Targeting

**Companies:** Taiwanese and Chinese ODMs (Arcadyan, Askey, Sercomm, Gemtek,
CIG, Tozed), silicon-adjacent integrators, regional OEMs building
operator-branded CPE, and camera/IoT ODMs for the NVR side.

**The question that qualifies fastest:** *"Which platforms are you expected to
support, and which one are you currently outsourcing?"*

---

## Targeting (LinkedIn tracks only)

### Track A — O-RAN / convergence
**Titles:** Head of RAN Engineering, Director of Network Architecture, CTO
(challenger MNO), Head of OSS, Principal Engineer – Transport, Director of
Network Automation, Head of Fixed Wireless.
**Communities:** O-RAN ALLIANCE, TIP (OpenRAN + OpenWiFi), LF Networking / ONAP,
Broadband Forum.
**Events:** MWC Barcelona, O-RAN ALLIANCE plugfests, Brooklyn 6G Summit, Network X.

### Track B — WiFi economics
**Titles:** VP/Director of Network Engineering, Head of Broadband, CTO (regional
ISP), Director of CPE/Devices, Head of Managed WiFi, PM – Residential Broadband.
**Communities:** TIP OpenWiFi, prpl Foundation, RDK Management, WISPA.
**Events:** ANGA COM (Cologne — highest-value room for a Dutch company), Fiber
Connect, WISPAMERICA, Network X.

### Track D — OEM / ODM
See the track above; it has its own targeting section.

### The multiplier
Both LinkedIn audiences together are ~5,000 people globally. Small enough to
reach by hand: **15 min/day of substantive commenting** on O-RAN ALLIANCE, TIP,
prpl and Broadband Forum posts beats everything else including paid, and **30
individual DMs** referencing specific deployments beats 300 templated ones.

**Profile first.** Headline: `Building Aether — converged access network
management | Founder, Optim Enterprises`. Featured: demo video, architecture
write-up, `ac-client` repo. Banner: the protocol matrix.

### Paid
Hold until organic shows which hook lands. Then **thought-leader ads** promoting
A3 or A4, and **document ads** using `assets/aether-converged-access.pdf`.
€3–5k over six weeks. Expect €10–20 CPC and accept it — you need a few hundred
right clicks, not volume.

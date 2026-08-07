# Aether — LinkedIn playbook

Two post sequences. **Track A (O-RAN / convergence) is the lead.** Track B (WiFi
economics) is the fallback and the follow-on — it argues a case buyers have
already heard from every open-source challenger, so it lands harder once
Track A has established that Aether is technically unusual.

Post from a **personal profile**, not the company page. Personal posts get
roughly 5–10x the organic reach; the company page is where people land to
check you're real.

Mechanics that apply to every post below:

- **No links in the post body.** LinkedIn suppresses them. Put the link in the
  first comment and write "link in comments."
- Tue–Thu, **08:00 CET** — catches EU operators mid-morning and US East Coast
  before work.
- First two lines are all that shows before "…see more". They do 90% of the work.
- Reply to every comment inside the first hour; your replies count as engagement.
- Ask 5 people to **comment** (not react) in the first hour. Comments are
  weighted far above reactions.

---

## Claims discipline

Everything below is written to be defensible against a hostile RAN engineer in
the comments. Keep it that way.

**Safe to claim — verified in the codebase:**

| Claim | Evidence |
|---|---|
| 10 protocols in one binary | `crates/` — ucentraljson, usp, wrp, ieee1905, opensync, MQTT, netconf, snmp, gnmi, oran |
| NETCONF/YANG, RFC 6241/6242 framing | `crates/netconf` — framing, rpc, session |
| SNMP v1/v2c/v3, polling + traps | `crates/snmp` |
| gNMI streaming telemetry | `crates/gnmi` |
| O-RAN A1 client + VES collector | `crates/oran` — `a1_client.rs`, `ves.rs` |
| TMF621/632/638/678 | `crates/tmf-api` |
| Post-quantum TLS, X25519 + ML-KEM-768 | FIPS 203 hybrid |
| RDK-B zero-install via Parodus/WRP | `crates/proto-wrp`, `crates/parodus2ccsp` |
| Config delta as JSON Patch, ~200 B vs ~50 KB | RFC 6902 — a property of the format, not a benchmark |
| $0.30 / $0.50 / device / month | Published pricing |

**Do NOT claim — pulled from the site for good reason:**

- ❌ `200k+ concurrent connections` — never load-tested at that scale
- ❌ `<1ms config delta delivery` — never measured
- ❌ `CockroachDB` / `distributed SQL` / `horizontal scale` — it's PostgreSQL + sqlx
- ❌ `distributed event streaming` — there is no Kafka/Redpanda tier yet
- ❌ Federated ML as shipping — it's roadmap
- ❌ Any SLA as a current term — 99.9/99.99% are GA commitments
- ❌ **"Aether is a RIC."** It speaks A1 and emits VES. That is not the same
  thing, and RAN engineers will take the post apart over it. Precision here is
  the entire credibility play.

**Benchmark rule:** if you post a number, post the hardware and the duration
alongside it, or don't post it. Right now telemetry writes are the bottleneck —
fix the batching before you publish any throughput figure.

---

# Track A — O-RAN / convergence (lead sequence)

The argument: fixed access and mobile access are managed by two disjoint
toolchains and two org charts, and nobody has put them behind one control
plane. Aether has, and no WiFi vendor can follow — it's outside their category.

## A1 — The convergence problem (no product mention)

> Most operators run two completely separate management worlds and pretend
> they're one network.
>
> The CPE fleet lives in a WiFi cloud — uCentral, TR-369, maybe Plume or Mist.
> Managed by the broadband team.
>
> The transport and RAN live somewhere else entirely — NETCONF and YANG on the
> aggregation gear, SNMP on whatever's too old for that, gNMI if someone
> modernised, A1 policies into a Near-RT RIC if there's a RAN team with budget.
>
> Two toolchains. Two data models. Two on-call rotations. And when a subscriber
> complains their connection is bad, nobody can answer whether the problem is in
> the home, the backhaul, or the radio — because no single system sees all three.
>
> I keep hearing "converged access" in vendor decks. I have yet to see anyone
> ship a control plane that actually spans it.
>
> Is anyone here running fixed and mobile access from one system? Genuinely
> asking — I'd like to know if I'm wrong about this.

No product. No link. This post's only job is to find the audience and start
the argument.

## A2 — What we built

> We spent the last stretch building a control plane that speaks ten protocols
> in one binary, because the alternative was ten integrations.
>
> The wireless CPE side: uCentral, TR-369/USP, WRP for RDK-B, IEEE 1905.1 for
> EasyMesh, OpenSync, MQTT.
>
> The transport and RAN side: NETCONF with YANG models, SNMP for everything too
> old to speak anything better, gNMI for streaming telemetry, and O-RAN A1 plus
> VES.
>
> One process. One normalized event stream. An OpenWrt router in a living room
> and an A1 policy toward a Near-RT RIC land in the same pipeline.
>
> It's called Aether. Written in Rust, open agent, self-hostable on your own
> Kubernetes. Running today, in early access, hardening for scale.
>
> Architecture write-up in the comments.

## A3 — The precision post (this is the credibility one)

> Let me be exact about something, because the O-RAN space rewards precision and
> punishes marketing.
>
> **Aether is not a RIC.**
>
> What it is: an A1 client and a VES collector. It can push policy toward a
> Near-RT RIC over A1, and it can emit VES events into an ONAP-style OSS. That's
> the integration surface, and it's deliberately narrow.
>
> What that buys you is not "we do RAN optimization." It's that the same system
> holding your CPE telemetry can act on RAN policy and report into the same OSS
> your RAN already reports into. The correlation happens in one place instead of
> in a spreadsheet.
>
> If you want an xApp platform, we are not that, and anyone telling you their
> WiFi cloud is a RIC is selling you something.
>
> The genuinely hard part wasn't A1. It was making a normalized data model that
> a TR-181 parameter from an OpenWrt box and a gNMI subscription from an
> aggregation switch both fit into without one of them being second-class.
>
> Happy to be told where this framing is wrong — I'd rather find out here than
> in a deployment.

Explicitly disclaiming the bigger claim is what makes the smaller one credible.
This is the post that gets shared into RAN engineering Slacks.

## A4 — RDK-B zero-install (operator reality)

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
> Same principle everywhere else. OpenWrt gets an opkg install. QSDK gets an
> agent wrapping cfg80211tool and qca-hostapd. prplOS talks to the TR-181 bus
> that's already there. OpenWiFi speaks uCentral natively. Aggregation gear gets
> NETCONF or gNMI, and anything older gets SNMP.
>
> Meet the device where it is. The alternative is asking an operator to reflash
> a million gateways, which is the same as asking them to say no.
>
> Operators — what actually blocked your last management platform migration?
> I'd bet firmware certification is top three.

## A5 — Post-quantum TLS (the contrarian teardown)

> We put post-quantum TLS on CPE and I want to explain why that isn't a gimmick.
>
> X25519 + ML-KEM-768 hybrid, NIST FIPS 203.
>
> The argument against: nobody is breaking your router's key exchange with a
> quantum computer this decade.
>
> The argument for: a router deployed in 2027 is still in a living room in 2037.
> Harvest-now-decrypt-later is a real threat model for a device with a ten-year
> field life whose management channel carries config, credentials and telemetry.
> You cannot retrofit this across a deployed fleet — you'd have to touch every
> device.
>
> Every other management platform I'm aware of ships classical TLS only. In ten
> years that's a fleet-wide migration nobody has budgeted for.
>
> The cost to us was a slightly larger handshake. That seemed like a good trade.
>
> Disagree? I'd genuinely like to hear the case against.

Inviting disagreement is the single most reliable comment driver on technical
LinkedIn.

## A6 — The ask

> We're taking a small number of design partners into Aether early access.
>
> Best fit: an operator with a genuinely messy access network. Multiple CPE
> silicon vendors, at least one platform inherited from an acquisition, some
> aggregation gear still on SNMP, and ideally a RAN team you'd like to stop
> emailing spreadsheets to.
>
> What you get: founding-partner pricing locked for the life of the contract,
> direct input on roadmap priority, our engineering time on your specific mix.
>
> What we get: real-world protocol edge cases we can't invent in a lab.
>
> Roughly 50k–500k subscribers is the sweet spot. Below that the migration
> doesn't pay for itself; above that you need BSS/OSS work that's further out.
>
> Not a sales process. DM me and I'll show you the platform and tell you
> honestly what doesn't work yet.
>
> Link in comments.

---

# Track B — WiFi economics (secondary sequence)

Run this **after** Track A, or in parallel on a slower cadence. It's a stronger
commercial argument but a weaker credibility argument — every open-source
challenger has made the "stop paying the SaaS tax" case, so it reads as
familiar until you've shown you can actually build.

The core asset is the arithmetic:

| Subscribers | Plume/Mist at ~$3/device | Aether Pro at $0.30 | Annual delta |
|---|---|---|---|
| 100k | $3.6M/yr | $360k/yr | **$3.2M** |
| 333k | $12M/yr | $1.2M/yr | **$10.8M** |
| 1M | $36M/yr | $3.6M/yr | **$32.4M** |

## B1 — The money post (no product mention)

> A regional ISP with 300,000 subscribers pays roughly $900,000 a month for WiFi
> management software.
>
> Not for the routers. For the software that manages them.
>
> $3 per device per month for RF optimization and IoT fingerprinting, billed
> forever, running on someone else's cloud, over subscriber data that never
> leaves your network in any other context.
>
> The industry has quietly accepted that this is just what things cost.
>
> I don't think it is. The RF optimization is a control loop over channel and
> power. The fingerprinting is DHCP options and OUI lookups against a database.
> This is well-understood engineering, not a moat.
>
> What it *is* is a business model that depends on operators not having an open
> alternative.
>
> Curious what operators here actually pay per device — and whether anyone has
> tried bringing it in-house.

## B2 — The seven stacks post

> Last year I started counting how many separate systems an operator needs to
> manage a mixed CPE fleet.
>
> uCentral for the OpenWiFi APs. TR-369/USP for the OpenWrt routers. WRP and
> Parodus for the RDK-B gateways. OpenSync for anything Plume-adjacent. IEEE
> 1905.1 for the mesh. A different management stack per silicon vendor.
>
> Seven stacks. Seven integration teams. No single view of the fleet.
>
> So we built one control plane that speaks all of them natively and normalizes
> everything into a single event stream.
>
> The protocol router is called Hermes, because it's a translator. The mesh
> layer is Meridian. The RF engine is Prometheus. Yes, Greek gods. It made the
> architecture arguments easier to have.
>
> Running today, in early access. Link in comments.

## B3 — The demo

Native video, 45–60s, screen recording of `gw.aether-io.com`. Captions burned
in — most of the feed watches muted. Show: fleet map → drill into one subscriber
→ mesh topology with a steering event → Argus classifying an unknown IoT device
→ a config change landing.

> 45 seconds: a mixed fleet of OpenWrt, RDK-B and QSDK devices in one pane of glass.
>
> Watch the third device. Argus fingerprints it from DHCP options and mDNS
> before it finishes associating, classifies it as an IP camera, and Aegis puts
> it on the IoT policy — no operator action.
>
> The config push at the end is a JSON Patch delta. About 200 bytes, against the
> ~50 KB full config most platforms ship on every change.
>
> Still early. Still ugly in places. But it's real.

"Still ugly in places" is not weakness — it's the line that makes engineers
trust the rest.

## B4 — The privacy / data residency post

> Every per-device WiFi SaaS has the same architecture: your subscribers'
> telemetry goes to the vendor's cloud, and the intelligence comes back.
>
> For an EU operator that's a GDPR conversation every single time. For anyone
> else it's a dependency you can't audit.
>
> We built Aether to run on your infrastructure. Subscriber PII sits in a
> separate vault from the telemetry store, with a GDPR data-access API on top,
> and the whole thing self-hosts on your own Kubernetes via Helm.
>
> The RF optimization runs where your data already is. Nothing has to leave.
>
> That's not a feature we added for compliance. It's the reason the architecture
> looks the way it does.

## B5 — The open source post

> The device agent is Apache-2.0. Not open-core, not source-available, not
> "open" with a commercial licence bolted on.
>
> `ac-client` — installs as an opkg package on OpenWrt, speaks TR-369/USP to
> whatever backend you point it at.
>
> The reasoning is simple. If you're going to put an agent on a million devices
> in people's homes, you should be able to read what it does. And if we ever
> become a company you don't want to deal with, the agent shouldn't be the thing
> that traps you.
>
> The platform is commercial. The thing on your subscribers' hardware isn't.
>
> Repo in the comments.

## B6 — The ask

Reuse **A6**. Don't write a second one — a second "we're taking design
partners" post inside a few weeks reads as desperation.

---

## Targeting

The two tracks reach **different rooms**. Don't blend them.

### Track A — O-RAN / convergence

**Titles:** Head of RAN Engineering, Director of Network Architecture, CTO
(regional/challenger MNO), Head of OSS, Principal Engineer – Transport, Director
of Network Automation.

**Communities:** O-RAN ALLIANCE, Telecom Infra Project (OpenRAN + OpenWiFi
project groups), Linux Foundation Networking / ONAP, Broadband Forum.

**Events:** MWC Barcelona, O-RAN ALLIANCE plugfests, Brooklyn 6G Summit, Network
X, Small Cells World Summit.

### Track B — WiFi economics

**Titles:** VP/Director of Network Engineering, Head of Broadband, CTO (regional
ISP), Director of CPE/Devices, Head of Managed WiFi, PM – Residential Broadband.

**Communities:** TIP OpenWiFi, prpl Foundation, RDK Management, WISPA.

**Events:** ANGA COM (Cologne — you're a Dutch company, this is your highest-value
room), Fiber Connect, WISPAMERICA, Network X.

### The unglamorous multiplier

Both audiences together are maybe 5,000 people globally. That's small enough to
reach by hand:

- **15 min/day commenting substantively** on posts from O-RAN ALLIANCE, TIP,
  prpl, Broadband Forum and operator engineering leaders. Not "great post" —
  actual technical contribution. For a niche this size this beats everything
  else, including paid.
- **30 individual DMs**, no template, referencing their specific deployment.
- **Fix the profile first.** Headline: `Building Aether — open, converged access
  network management | Founder, Optim Enterprises`. Featured section: demo
  video, architecture write-up, `ac-client` repo. Banner: the protocol matrix.

### Paid

Hold until organic tells you which hook lands. Then:

- **Thought-leader ads** promoting A1 or A3 — consistently 2–3x standard
  sponsored content in technical B2B.
- **Document ads** with a 6-page "Converged access management: what it costs to
  run two toolchains" PDF.
- €3–5k over six weeks is plenty. Expect €10–20 CPC and accept it; you need a
  few hundred right clicks, not volume.

### What LinkedIn won't do

It reaches buyers; it doesn't build the technical credibility that makes them
believe you can ship. That comes from being present in the O-RAN and OpenWiFi
communities, and from **`ac-client` on GitHub looking alive** — real commits,
real issues, real docs. An operator evaluating an early-access platform from an
unknown Dutch company will look at the repo before the deck.

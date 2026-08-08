# MASTER_PLAN vs. what is actually built

Analysis of `MASTER_PLAN.md` (147 checkboxes, **0 ticked**) against the codebase,
the ADRs, and the running cluster. The plan was written up front and never
updated; almost everything in it now exists, and a substantial amount exists
that was never planned.

**Codebase:** 35,373 lines of Rust · 222 files · 44 crates · 30 migrations ·
26 UI pages · 5 ADRs · 10 design/plan docs.

---

## Headline

The plan projected **20 months to GA**. Measured by deliverables rather than
calendar, **Phases 0–7 are substantially complete** and Phase 8 is partial. The
marketing site was, until this pass, describing a subset of what ships.

---

## Phase-by-phase

| Phase | Plan | Status | Evidence |
|---|---|---|---|
| **0** Foundation | workspace, CI, Docker, Helm, `core`, multi-tenancy | **Built** | `core` 607 L, 30 migrations, `tenant_id` in 24 crates, Helm + Dockerfile present |
| **1** Protocol & connection | 4 proto codecs, IEEE1905, connection-manager, routing, PKI | **Built** | `connection-manager` **6,149 L** (largest crate), `pki` 1,440 L, `ieee1905` 489 L, `routing` 156 L |
| **2** OpenWiFi services port | owgw/owsec/owfms/owprov/owanalytics/owsub/owls, RBAC, delta | **Built** | `owgw` 2,369 L + 6 sibling crates, `rbac` 771 L, `delta` 317 L (JSON Patch) |
| **3** Xmidt + RDK-B | WRP codec, tr1d1um, parodus2ccsp, WRP↔USP bridge | **Built** | `proto-wrp` 480 L, `tr1d1um` 415 L, `parodus2ccsp` 211 L |
| **4** QSDK + prplOS | platform adapters, EasyMesh, DataElements | **Built** | `platform` 754 L (`qsdk.rs`, `prplos.rs`, `rdkb.rs`, `openwrt.rs`, `opensync.rs`), `easymesh` 920 L |
| **5** Mesh + Prometheus AI | topology, steering, channels, backhaul, 5 ML modules, **FedAvg** | **Built** | `meridian` 516 L; `prometheus-engine` 1,058 L with `channel_optimizer.rs`, `steering_predictor.rs`, `anomaly_detector.rs`, `failure_predictor.rs`, `sense.rs`, **`federated/aggregator.rs` + `round.rs`** — every module the plan named |
| **6** Business + subscriber | billing, TMF, GDPR/PII, subscriber portal, white-label | **Built** | `billing` 1,047 L (`airwallex.rs`, `invoices.rs`, `metering.rs`, `subscriptions.rs`), `tmf-api` 514 L, `gdpr` 364 L, `owsub` (`accounts.rs`, `portal.rs`) |
| **7** Argus + Aegis + OpenSync | fingerprinting, DNS filtering, OpenSync port | **Built** | `argus` 897 L (`classifier.rs`, `dhcp.rs`, `mdns.rs`, `oui.rs`, `inference.rs`), `aegis` 506 L (`blocklist.rs`, `policy.rs`, `resolver.rs`, `schedule.rs`), `proto-opensync` 685 L incl. `ovsdb.rs` |
| **8** Embedded agent + GA | agent, GA hardening | **Partial** | `agent` 688 L is a **test harness**, not a shipped package. GA hardening outstanding — see Gaps |

---

## Built but never planned — 16 crates

None of these appear in `MASTER_PLAN.md` §5:

`netconf` · `snmp` · `gnmi` · `oran` · `platform` · `provisioning` · `retention`
· `configs` · `subscriber-configs` · `rbac` · `events` · `agent` · `tr1d1um` ·
`parodus2ccsp` · `integration-tests` · `prometheus-engine` *(planned as
`prometheus`)*

The first four are the significant ones — they move the product from WiFi CPE
management into converged access, and none were in the original scope.

---

## ADR-003 — executed, and it matters

`ADR-003` (Accepted, 2026-08-07) recorded that `gnmi` and `snmp` were **stubs
returning synthetic data**, `netconf` had a `<stub/>` fallback, and `oran`
self-described as "stubs suitable for integration testing." Its directive:

> No protocol adapter may return a stub/synthetic payload on a path reachable in
> production. If a real client cannot be built, the API must return an explicit
> error, never fabricated data.

**Verified done:**

- No `stub*.rs` files remain; no `"stub"` / `<stub/>` markers anywhere in `crates/*/src`
- `snmp` 1,759 L on `rasn` + `rasn-snmp` + `cfb-mode` — real v3 USM crypto
- `gnmi` 1,111 L on `tonic` 0.12 + `rustls` — real gRPC/TLS
- `netconf` 1,124 L on `russh` + `quick-xml`
- `oran` 1,460 L — A1 over `reqwest`, O1 over real NETCONF, VES 7

**And the live-test gates are running.** Namespace `proto-sims`:

| Simulator | Image |
|---|---|
| A1 | `nexus3.o-ran-sc.org/o-ran-sc/a1-simulator:2.5.0` |
| gNMI | `ghcr.io/nokia/srlinux:latest` |
| NETCONF | `sysrepo/sysrepo-netopeer2:latest` |
| SNMP | `polinux/snmpd:alpine` |
| VES | `mendhak/http-https-echo:31` |

Using the official O-RAN-SC simulator and a real Nokia network OS as targets is
a stronger conformance story than the plan asked for.

---

## Marketing claims this analysis corrected

Three things were described as roadmap that already ship. All were my error —
each came from grepping for a *technology* rather than checking the *capability*.

| Claim | Was | Is |
|---|---|---|
| **O-RAN O1** | "roadmap — NETCONF transport already in place" | **Built.** `/api/v1/oran/nodes/:serial/config` does get-config/edit-config over real NETCONF, verified against netopeer2 |
| **Federated ML** | marked `Roadmap` in the comparison table | **Built.** `prometheus-engine/src/federated/{aggregator,round}.rs` |
| **Distributed SQL** | "on the roadmap" | **Deployment choice.** `sqlx` on `features = ["postgres"]`; CockroachDB is Postgres-wire compatible |
| **Event streaming** | "dedicated tier on the roadmap" | **Built.** `pheme` (pub/sub, webhooks) + `audit` (immutable journal + rollback) + `events` (SSE) over 3-node EMQX |

---

## Genuine gaps — accurate to call roadmap

- **Near-RT RIC / E2 termination / xApp runtime.** Not built and shouldn't be —
  see `e2-phase1-scope.md`.
- **IoT device management.** *Updated:* ADR-005 is now **Accepted** — generic
  MQTT ingest (`iot_mqtt.rs`, `Protocol::MqttIot`) and LwM2M (`lwm2m.rs`,
  Registration/Update/Deregister/Notify) both ship. **ONVIF and Matter remain.**
- **STOMP / CoAP in `ac-client`.** The platform terminates all four USP MTPs
  (`02c5f35`); the OpenWrt agent is still WebSocket + MQTT.
- **Kafka/Redpanda log.** Planned in `MASTER_PLAN` §10; not deployed. The
  pipeline is covered another way — describe the capability, don't name Kafka.
- **Phase 8 GA hardening.** The real one. `20c3d93` landed batched writes and is
  deployed, but measured over 30 min the gate is **still unmet**: `device_telemetry`
  inserts median 2.81 s / max 3.97 s, and the heartbeat `UPDATE`s are now worse
  (`gnmi_devices` max 4.61 s). `rows_affected` is 3, not 500 — the batcher flushes
  on a timer with an empty buffer in this lab, so the path is untested. The
  remainder is the storage tier: shared `pg-shared` on single-replica LINSTOR.
  **No throughput figure is publishable until this clears.**
- **Mobile.** *Updated:* Aether **Ops** started (`c5da739`) — Expo 51,
  ~1,304 L TS: login, device list with search/filter, detail, single reboot.
  Absent: MFA, RTTY terminal, bulk ops, push notifications, topology map.
  **Aether Home has no codebase** and is what the $5/home tier leads with.

---

## Recommendation

**Update `MASTER_PLAN.md`.** 147 unticked boxes against a largely finished
product is actively misleading — it was the source of three wrong claims on the
public site. Either tick it, or replace §7 with a `/status` page generated from
reality.

**The ADRs are the reliable record**, not the plan. ADR-003 in particular
describes work that was scoped and completed inside two days, and its
"no synthetic data" directive is the right standard for public claims too.

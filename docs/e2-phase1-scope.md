# E2 termination — Phase 1 scope

Answers the question "what would it take to fulfil what the deck says we're
not?" The short version: **Phase 1 needs no edge component at all**, because
latency only binds once you're closing a control loop.

Current public position (`docs/assets/aether-converged-access.pdf`, slide 4):

- **IS** — A1 client, VES collector, `Device.Cellular`, one data model
- **ON THE ROADMAP** — O1 (NETCONF/YANG transport already in place), Non-RT RIC
  and rApp runtime over R1, STOMP/CoAP *(landed — see below)*
- **IS NOT** — a Near-RT RIC. No E2 termination, and so no xApp runtime.

Phase 1 moves E2 termination from the third bucket to the first without
touching the Near-RT RIC claim.

---

## Why Phase 1 doesn't need an edge component

| | Phase 1 (KPM, read) | Phase 2 (RC, control) |
|---|---|---|
| Traffic | Periodic measurement reports, 100ms–seconds | RIC Control Request/Ack |
| Anything waiting on us? | No | Yes — 10ms–1s budget |
| Deployment | **Cloud, alongside the rest of Aether** | Edge, co-located with CU/DU |
| Claim it earns | "We terminate E2 and ingest RAN KPIs" | "We close a RAN control loop" |

Phase 2 is where the client becomes necessary — and it isn't thin. It has to
hold the control logic locally, which means **the edge component essentially is
the Near-RT RIC**. That's a second product, not a feature.

---

## What Phase 1 needs

| Piece | Reuse | Notes |
|---|---|---|
| **E2AP over SCTP** | `rasn` 0.28 — already in tree for `crates/snmp` | E2AP is ASN.1 **APER**, which `rasn` supports. Biggest single item, but the codec dependency and in-house familiarity already exist |
| **SCTP transport** | socket work in `crates/ieee1905` | Linux kernel SCTP. Different from raw-ethernet CMDU work, but the muscle is there |
| **Procedures** | — | E2 Setup Request/Response/Failure, RIC Subscription Request/Response/Failure/Delete, RIC Indication, E2 Node Configuration Update, Reset |
| **E2SM-KPM v3** | — | Read-only measurement reporting. The whole of Phase 1's value |
| **Ingest** | existing telemetry pipeline | KPM reports land in the same normalized event stream as CPE telemetry — this is the actual product differentiator |
| **State** | Redis, already a workspace dep | Subscription and E2 node state |

**Not in Phase 1:** E2SM-RC, xApp runtime/SDK, A1 termination, conflict
mitigation, edge deployment.

---

## Where this dies if it dies

**Not in the protocol — in E2 node interop.** Every CU/DU vendor implements E2
slightly differently, and that is what kills RIC projects.

Test order, before assuming anything:

1. **FlexRIC** (Eurecom) — deliberately lightweight, fastest signal
2. **O-RAN SC** reference Near-RT RIC — what everyone benchmarks against
3. **srsRAN** or **OAI** as E2 nodes

If a subscription won't hold against those, vendor gear will be worse.

---

## Recommendation

**Do Phase 1.** Bounded, reuses the codec, the telemetry pipeline and the data
model, needs no new deployment topology, and converts "Aether is not a RIC" from
a limitation into a scope statement.

**Treat Phase 2 as a decision, not a continuation.** Only take it with a partner
who has real E2 nodes to test against — otherwise you're building control logic
against a specification instead of a network.

**Don't do Phase 3.** xApp hosting puts you against Juniper, Nokia, Samsung and
VMware with no structural advantage, against an open-source reference
implementation everyone benchmarks to.

---

## Claims discipline

Say nothing publicly about E2 until Phase 1 terminates a subscription against
FlexRIC or the OSC RIC. Then the claim is exactly:

> Aether terminates E2 and ingests E2SM-KPM measurement reports into the same
> pipeline as CPE telemetry. It is not a Near-RT RIC and hosts no xApps.

That sentence is defensible in a hostile comment thread. Anything looser isn't.

---

## Precedent: STOMP and CoAP

Landed in `02c5f35` — `crates/connection-manager/uspcoap.rs` (249 L, 2 tests),
`uspstomp.rs` (398 L, 4 tests), both wired into the `Protocol` enum. The site
moved from "2 MTPs, STOMP and CoAP on the roadmap" to "all 4 USP MTPs" the same
day, and the agent claim stayed at 2 because `ac-client` didn't change.

Same discipline applies here: ship it, test it, then claim it — and scope the
claim to the side that actually has it.

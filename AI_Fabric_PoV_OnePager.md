# AI as a Platform Fabric

**Point of View — Executive Summary**
*Build flows — data to insights to action — with AI embedded. Not a place you go to use AI.*

---

> **The one idea:** People don't come to the platform for AI alone — they come to build flows with AI embedded. The platform should be measured not by whether it offers a place to build agents, but by whether **every functional owner can embed AI safely and consistently inside their own flows**.

---

## Why this matters now

- As the platform serves external customers, AI built as standalone surfaces means every customer-facing flow reimplements model access, grounding, guardrails, and audit — **inconsistent governance exposed to customers**.
- A fabric lets us promise one thing that separate AI surfaces never can: **every AI-touched flow grounds, governs, and audits the same way, everywhere**.

## What the AI Fabric is

Shared, governed services every flow consumes instead of rebuilding:

| Service | What it provides |
| --- | --- |
| Model Gateway | Governed model access, routing, cost, policy |
| Tool / MCP Gateway | Governed, discoverable tool & system access |
| Context Layer | Entitlement-aware grounding (lineage, metrics, ontology) |
| Memory Layer | Governed, scoped, auditable memory |
| Evals + Observability | Release-gating evals; end-to-end traces |
| Guardrails / Policy | Ambient enforcement at the gateway, default-on |
| Agent Runtime | Reusable patterns; deterministic, auditable paths |

## Why fabric is the right architecture

- **Consistency as a product promise.** Every AI-touched flow grounds, governs, and audits the same way — governance that is **unavoidable, not merely available**. Non-negotiable once external customers in regulated domains share the platform.
- **Teams should never rebuild the substrate.** No flow should re-implement memory, context retrieval, guardrails, or evals. The fabric provides them as shared, ambient gateway services, inherited by default.
- **Probabilistic at the edge, deterministic underneath.** The model proposes; policy, effects, and audit stay deterministic and typed — adaptable **and** auditable, drawn once in the fabric, not re-drawn per flow.
- **Delivered through the SDK.** The active push to converge at the SDK is correct — the fabric is delivered through it. The question is not whether to converge, but **what the SDK fronts**: a governed runtime client, not thin model wrappers.

## We will know it worked when

- A new flow embeds AI without building its own model access, retrieval, memory, evals, or guardrails.
- Any flow's grounding, policy, and effects are traced and audited the same way, regardless of domain.
- An external customer can be shown that every AI-touched flow grounds, governs, and audits identically.

---

> Not AI as a destination. Not AI as a functional silo. Not AI as wrappers behind an SDK.
>
> **AI as a composable, governed, observable fabric woven into every flow the platform exists to build.**

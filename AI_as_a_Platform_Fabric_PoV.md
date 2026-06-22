# AI as a Platform Fabric

**Point of View — Strategy Position Paper**
*The platform exists to build end-to-end flows — data to insights to action — with AI embedded in the flow.*

Status: Draft for leadership review

---

## Executive Summary

People do not come to the platform for AI alone. They come to build end-to-end flows — data to insights to action — and they want AI **embedded in those flows**, not bolted on beside them. The standalone need ("give me a place to build an agent") is already met by AI experiences across the enterprise. The platform's reason to exist is the flow, and AI's job is to make that flow more intelligent at every step.

This reframes what AI should be on the platform. AI is not a functional capability sitting next to Data, Insights, and Solutions. It is the **technical fabric those functional capabilities weave AI into** — a shared, governed substrate of model access, context, memory, evaluation, observability, guardrails, and reusable runtime that every functional owner consumes through standard SDKs and plugins.

> **THE LINE TO LEAD WITH**
>
> **AI is a fabric, not a destination.**
>
> The platform is not measured by whether it offers a place to build agents. It is measured by whether **every functional owner can embed AI safely and consistently inside their own flows**.
>
> They do it through shared, governed fabric services — using the SDK and plugin tooling they already build with — while keeping the experience anchored in their domain.

The strategic goal is a shared **AI Fabric**: model gateways, tool/MCP gateways, a context layer, a governed memory layer, evaluation infrastructure, first-class observability, a policy and guardrail layer, a capability registry, and a reusable agent runtime. The fabric lets many flows and agentic workflows be composed consistently, instead of accreting one-off implementations that each reinvent access, grounding, evaluation, and tracing.

**Why now.** As the platform is positioned to serve external customers, the cost of getting this wrong compounds. AI built as a standalone surface forces every customer-facing experience to reimplement model access, grounding, guardrails, and audit — producing inconsistent governance exposed directly to customers. A fabric is what lets the platform promise that **every AI-touched flow grounds, governs, and audits the same way, everywhere** — a promise a collection of separate AI surfaces cannot make.

---

## Core Position

The platform should not be measured by whether it provides a place to build agents. It should be measured by whether it gives **every functional owner the primitives to embed AI safely and consistently inside their own flows**.

A **data owner** should use AI grounded in lineage, contracts, quality signals, and metadata. An **insights owner** should use AI grounded in metrics, dashboards, anomalies, and business definitions. An **analytics owner** should use AI grounded in experiments, model runs, features, and diagnostics.

In this model, functional owners do not rebuild their domain inside a generic agent surface. They consume the **AI Fabric through SDKs, plugins, and platform-native extension points** — while keeping the user experience anchored in their domain.

> **THE ANALOGY**
>
> Cloud did not win as a "data center you visited". It won as a **fabric** — compute, storage, identity, networking, observability — that every team composed against, in their own context.
>
> Kubernetes did not win as an "orchestration app". It won as a **control plane** everything else built on.
>
> Platform AI is the same shape. The value is the fabric and the control plane, not a surface you navigate to.

---

## Why AI Belongs in the Fabric, Not Beside the Flow

Three forces make the fabric the correct architecture rather than a stylistic preference.

### 1. The platform's value is the flow, not AI in isolation

A user assembling a data-to-insights-to-action flow wants AI to help **at each step within that flow**: interpret the data, explain the metric, propose the next action. The moment AI lives in a separate surface, the user must leave the flow, reframe their problem in a generic agent builder, and stitch the result back in. That friction is the tax a standalone AI surface imposes. Embedding AI through the fabric removes it — AI shows up where the work already is.

### 2. AI operates on a different substrate than functional code

Functional capabilities and developer tooling operate over deterministic code and build artifacts. AI operates over **probabilistic inference, live enterprise context, entitlements, and irreversible effects on data and decisions**. That substrate needs primitives functional capabilities do not already have: entitlement-aware context, evaluation as a release gate, input/output guardrails, and traceable, auditable effects. A plugin SDK alone cannot supply these — they are runtime services the SDK must front.

### 3. External customers make consistency a product promise, not a convenience

When the platform serves external customers, every AI-touched surface is one a customer sees. If each carries its own model access, grounding, guardrails, and audit, the customer experiences **inconsistent governance and unprovable auditability** — a serious problem in regulated contexts. A fabric makes governance, grounding, and audit **uniform and provable across every flow**. This is a product-and-trust argument, and it is the strongest reason the fabric is not optional.

---

## Converging at the SDK Is Correct — What the SDK Must Front

There is an active and correct push to converge at the **SDK and plugin layer** and align with existing build tooling. The fabric does not oppose this — **it is delivered through it**. Weaving AI into a data-to-insights flow via the SDK **is** the fabric thesis in practice. The convergence ask and the fabric are the same direction described from two ends.

The decision that actually matters is not **whether** to converge at the SDK, but **what the SDK fronts**. The SDK should not distribute thin model wrappers. It should distribute a **governed runtime client** — the functional owner's entry point into the fabric.

| The SDK should NOT be… | The SDK SHOULD be… |
| --- | --- |
| A bag of direct model-API wrappers | A client to the model gateway (routing, cost, policy, fallback) |
| Per-team, ad-hoc retrieval helpers | A client to the shared context layer, entitlement-aware |
| Optional, after-the-fact logging | Automatic trace propagation and eval hooks |
| Guardrails each team re-implements | Ambient gateway enforcement, inherited automatically; tune exceptions only |

Framed this way, the SDK push becomes the fabric's **distribution mechanism**. Functional owners weave AI in with the tooling they already use; the fabric ensures every flow they build inherits grounding, governance, evaluation, and observability by default.

---

## The AI Fabric: Shared Services

The fabric is a set of shared services every flow consumes rather than rebuilds. Nine components, each with a clear contract and a real-world reference shape.

### 1. Model Gateway

A centralized, governed model-access layer across providers: authentication, authorization, routing, fallback, cost controls, rate limits, model policy, and usage tracking — while preserving the operational detail flows need (latency, token accounting, provider attribution).

**Reference shape:** an OpenAI-compatible gateway (LiteLLM, Portkey, Kong AI Gateway, or a Vertex/Bedrock-fronted proxy) so flow code targets one stable interface and the enterprise keeps a single control and observability point. Semantic routing (e.g. vLLM Semantic Router) can direct requests to the right model tier by intent and cost.

**Anti-goal:** abstracting model access so far that a flow can't see which model answered, at what cost, with what latency.

### 2. Tool and MCP Gateway

A governed gateway exposing enterprise tools, systems, APIs, and MCP servers to flows in a controlled, reusable way: policy enforcement, authn/authz, tool discovery, invocation logging, protocol mediation, and runtime visibility.

**Reference shape:** MCP has become the de-facto tool interface across Anthropic, OpenAI, and Google tooling. A gateway in front of many MCP servers — with a registry, per-tool scopes, and audit — turns ad-hoc connections into a governed catalog. The goal is not merely connecting agents to tools; it is making tool access discoverable, governed, and observable.

### 3. Registry and Capability Catalog

A registry for tools, agents, prompts, workflows, models, and reusable components — plus the metadata that makes them governable: ownership, lifecycle state, version, certification status, access policy, domain context, tool contracts, expected behavior, eval status, and operational readiness.

**Reference shape:** a "service catalog for AI capabilities" (Backstage-style) plus a model registry (MLflow, Vertex Model Registry). This is the control plane for reuse and governance; without it, reuse is tribal knowledge.

### 4. Context Layer

Enterprise AI is only as good as the context it can safely assemble. A standard context layer retrieves, assembles, ranks, and governs context across data, knowledge, metadata, business definitions, policies, lineage, prior interactions, and workflow state — reusable across flows instead of each team rebuilding retrieval and grounding.

**Reference shape:** hybrid retrieval (vector + structured + semantic) grounded in an ontology/knowledge layer (e.g. OWL with an Ontop-style mapping over physical tables), with access policy applied at retrieval time so a flow never assembles context its caller isn't entitled to see.

### 5. Memory Layer

Distinguish session, workflow, user-preference, domain, and long-term institutional memory. Memory must be governed, permission-aware, explainable, and auditable — with ownership, retention, and access boundaries. It is not an unbounded chat-history store.

**Reference shape:** a typed memory service with scoped namespaces and per-scope retention, so flows get more useful over time without becoming opaque or leaking context across tenants and entitlements — a hard requirement once external customers share the platform.

### 6. Evaluation Framework

Capabilities must not reach production on the strength of a demo. The fabric provides evaluation for prompts, agents, tools, workflows, retrieval quality, reasoning quality, task completion, safety, latency, cost, and regression — wired into delivery the way unit tests wire into CI/CD.

**Reference shape:** offline eval suites plus online evals on sampled production traffic, gated in CI (Langfuse or Braintrust datasets, promptfoo-style assertions). Especially load-bearing for reusable flows and regulated domains where consistency is the product.

### 7. First-Class Observability

Observability is a platform requirement, not an afterthought. Traces span user request, plan, model calls, tool calls, context retrieval, memory access, policy decisions, errors, latency, cost, and output quality — with replay, audit, root-cause analysis, and usage analytics.

**Reference shape:** OpenTelemetry-based tracing with LLM semantics, surfaced in an LLM-observability tool (Langfuse, Arize Phoenix, LangSmith). Without it, AI-embedded flows are undebuggable, ungovernable, and untrustworthy.

### 8. Guardrails and Policy Layer

Enforcement is **ambient and transparent**, applied automatically at the gateway — not a feature flows opt into. Data access, tool access, model usage, sensitive-information handling, output constraints, and human-in-the-loop gates are enforced by default for every request that traverses the fabric. Functional owners do not configure guardrails to get them; they get them by going through the gateway. The model is **InfoSec and DLP controls**: enforced by default, invisible in the happy path, and surfaced only when a request trips a rule or an exception must be filed.

What **is** configurable is the exception, not the enforcement. Thresholds and sensitivity — redaction strictness, allowed tool scopes, approval-gate triggers, domain-specific rules — can be tuned per flow where a domain genuinely needs it, through an explicit, auditable override. Baseline protection is never something a flow can silently skip; it is the default state of the fabric.

**Reference shape:** a policy decision point (OPA-style) evaluated inline at the model and tool gateways, plus input/output guardrails (PII detection and redaction via Presidio or GLiNER-based NER, jailbreak and toxicity filters, schema and grounding checks) running as gateway middleware. Per-flow tuning is a declarative override against a secure default, not a bespoke implementation.

**Why this matters for external customers:** if policy is enforced at the gateway rather than configured per flow, it cannot be inconsistent, forgotten, or bypassed. That is a far stronger guarantee than "every team calls the same service" — it is the difference between governance that is available and governance that is **unavoidable**.

### 9. Reusable Agent Runtime and Framework

Strong architectural primitives — planning, tool use, context management, memory integration, eval hooks, observability hooks, policy enforcement, deterministic execution paths, domain grounding — without forcing every problem into one generic universal agent.

**Reference shape:** typed, structured agent frameworks (PydanticAI for type-safe structured agents; LangGraph where explicit graph state, checkpointing, and human-in-the-loop are needed) over the shared gateways and services. Teams build flows fast while inheriting consistency, control, and enterprise-grade behavior.

---

## Architectural Principle: Determinism by Boundary

The fabric encodes one core stance: keep the **probabilistic components at the boundary**, and keep **policy, effect, and record layers deterministic** underneath, with rigorously typed interfaces between them.

- **Boundary (probabilistic):** the model interprets intent, drafts plans, proposes tool calls, synthesizes language.
- **Policy (deterministic):** entitlements, guardrails, approval gates, and human-in-the-loop decide what is allowed to happen — enforced ambiently at the gateway, not configured per flow.
- **Effect (deterministic):** tool invocations and system mutations run through governed, typed contracts — not free-form model output.
- **Record (deterministic):** every decision, call, and output is traced, evaluated, and auditable.

This is why **chat is an interface pattern, not the architecture**. Most flows require structured execution, deterministic steps, approval gates, workflow state, and system integration. A neuro-symbolic shape — LLM flexibility at the edge, deterministic control underneath — gives both adaptability and auditability.

---

## Relationship to Current Initiatives

Two in-flight initiatives are complementary but distinct. They converge at the fabric, not at the user experience.

### Analytics Orchestrator Agent

A domain experience that simplifies analytical and ML workflows — XGBoost runs, next-best-action analysis, LSA, model diagnostics, experiment support. It embeds AI into the analytics flow, which is exactly right. **It should not build its own model access, memory, tool registry, retrieval, evals, or observability** — it should consume those from the fabric.

### ACT Agent Framework

A neuro-symbolic foundation for governed, auditable agents that combine LLM flexibility with deterministic reasoning, symbolic world models, explicit constraints, tool orchestration, and auditable execution. It is the platform's **agent runtime foundation** — enabling teams to build consistently without collapsing every flow into one universal surface.

> **HOW THEY COMPOSE**
>
> - The **AI Fabric** provides gateways, context, memory, evals, observability, policy, and registry.
> - The **ACT Agent Framework** provides the common runtime and neuro-symbolic patterns on top of the fabric.
> - The **Analytics Orchestrator** is one domain flow built on that framework and fabric — the template for every future domain experience.

---

## Failure Tests: How We Will Know the Fabric Is Going Wrong

Each of these is a signal that the platform has drifted from fabric to silo. Treat them as tripwires, not preferences.

- **A functional owner has to leave their domain to use AI.** If embedding AI means reframing the problem in a generic agent surface and stitching the result back, the fabric has failed its one job.
- **Two flows ground, govern, or audit AI differently.** Divergent model access, retrieval, or guardrails across flows means consistency is no longer provable — fatal once external customers are on the platform.
- **The SDK fronts thin model wrappers instead of the governed fabric.** Converging at the SDK is right; converging on wrappers wastes the convergence and reintroduces the fragmentation it was meant to remove.
- **A team re-implements memory, context, evals, or observability.** Anything rebuilt per flow is something the fabric should have provided. Duplication here is the leading indicator of silo drift.
- **Chat becomes the architecture.** If structured execution, approval gates, and auditable paths are getting bent to fit a chat surface, the interface has been mistaken for the substrate.

---

## Recommended Direction: Three Layers

Organize AI around three layers, bottom to top.

### Layer 1 — Shared AI Fabric (foundational, common to the platform)

Model gateway, MCP/tool gateway, registry, context layer, memory layer, evals, observability, guardrails/policy, and reusable runtime services. Built once. Consumed everywhere — through the SDK.

### Layer 2 — Reusable Agent and Workflow Frameworks

Neuro-symbolic execution, deterministic orchestration, tool-use patterns, memory integration, context grounding, eval hooks, observability hooks, and deployment templates. Accelerates delivery without flattening every use case into one experience.

### Layer 3 — AI Embedded in Functional Flows

AI appears inside the work — Data, Insights, Analytics, Solutions, Identity, Knowledge — driven by the user's task and woven in by the functional owner via the SDK:

| Functional capability | What AI does, embedded in the flow |
| --- | --- |
| Data | Discovery, metadata generation, data-quality explanation, lineage reasoning, contract authoring |
| Insights | Conversational BI, dashboard summarization, metric explanation, anomaly interpretation |
| Analytics | Model-workflow orchestration, experiment analysis, feature selection, diagnostics, recommendations |
| Solutions | ETL generation, workflow automation, operational agents, solution assembly |
| Identity | Entity resolution, matching explanation, identity-graph exploration, risk-aware workflows |
| Knowledge | Ontology reasoning, taxonomy management, semantic search, domain-grounded Q&A |

Note what is **not** a layer here: a standalone place users go to build AI. Studio-style agent-building experiences exist across the enterprise and can themselves consume this fabric — but the platform's value is the embedded flow, and that is where this model concentrates it.

---

## Operating Principles

1. The platform exists for flows with AI embedded, not for AI as a standalone destination.
2. AI is a horizontal technical fabric, consumed by functional capabilities — not a functional capability itself.
3. Functional owners weave AI into their domains through the SDK; the SDK fronts the governed fabric, not thin wrappers.
4. Shared AI capabilities are built once and reused across flows.
5. Context, memory, evals, and observability are first-class platform services.
6. Guardrails and policy are enforced ambiently at the gateway — default-on, not opt-in; only exceptions and thresholds are configured per flow.
7. Grounding, governance, and audit are uniform and unavoidable across every flow — a requirement for external customers.
8. Chat is an interface pattern, not the architecture.
9. Prefer reusable frameworks over one-off implementations.
10. Support deterministic, auditable execution for enterprise workflows.
11. Evaluate and certify capabilities before broad reuse.

---

## Target-State Vision

An **AI-native enterprise platform** where AI is embedded across functional flows and powered by a shared fabric. Functional owners build data-to-insights-to-action flows faster because they no longer recreate model access, tool integration, memory, context, evals, observability, or guardrails — they pull them through the SDK. Flows become more intelligent because they reuse one AI foundation while staying grounded in their own domain. External customers get AI that grounds, governs, and audits the same way everywhere.

In this target state the **Analytics Orchestrator** is a worked example of AI embedded into a flow; the **neuro-symbolic agent framework** is the foundation for governed, auditable agents; and the **AI Fabric** is the shared layer that makes all of it composable and enterprise-ready.

### We will know it worked when…

- A new functional flow can embed AI **without building** any model access, retrieval, memory, eval, or guardrail of its own.
- Any flow's grounding, policy decisions, and effects can be **traced and audited the same way**, regardless of domain.
- An external customer can be **told — and shown** — that every AI-touched flow grounds, governs, and audits identically.
- Adding a new domain experience is a matter of grounding and UX, not of rebuilding the AI substrate.

---

> Not AI as a separate destination. Not AI as a functional silo. Not AI as isolated wrappers behind an SDK.
>
> **AI as a composable, governed, observable fabric, woven into every flow the platform exists to build.**

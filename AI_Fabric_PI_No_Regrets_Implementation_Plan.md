# AI Fabric: No-Regrets Implementation Plan for PI Planning

**Audience:** Product Managers, Product Owners, Platform Engineering, Architecture, Security, and use-case teams  
**Purpose:** Convert the AI Fabric implementation philosophy into a PI-planning sequence that delivers reusable enterprise primitives without committing the organization to one agent framework, SDK, or runtime.

---

## 1. PI intent

The goal of this PI is **not** to build a complete AI platform, another agent framework, or a universal SDK. The goal is to establish a small set of enterprise primitives that are valuable regardless of whether application teams use ADK, LangChain/LangGraph, OpenAI SDKs, ACT, custom Python/Java, or future frameworks.

> **PI objective:** Make the first set of enterprise AI primitives independently consumable, governed, observable, and proven through real use cases.

A successful PI leaves us with capabilities that we will still want even if the preferred agent framework changes next quarter.

### What makes work “no-regrets”

A capability belongs in this PI when it meets most of these tests:

- It solves a recurring enterprise problem rather than recreating a commodity framework abstraction.
- Multiple application teams can consume it independently.
- It can be used from more than one framework or runtime.
- It has a clear security, governance, reliability, or reuse benefit.
- It can evolve/version independently from application orchestration.
- At least one prioritized use case can prove it in the PI.

---

## 2. Recommended PI exit state

By the end of the PI, an application team should be able to assemble a solution roughly like this:

```text
Business Use Case
      |
      v
Application / Agent / Workflow
(ADK | LangGraph | OpenAI | ACT | Custom)
      |
      +------ Model Access
      +------ Guardrails / Policy
      +------ Memory / State
      +------ RAG / Retrieval
      +------ MCP / Credentials (where needed)
      |
      v
Enterprise systems, models, data and knowledge
```

The application team owns orchestration and business behavior. The platform owns reusable enterprise capabilities and the controls that must be consistent across applications.

**PI exit condition:** At least two materially different use cases consume common primitives without being forced onto the same agent abstraction or execution runtime.

---

## 3. Scope at a glance

### Commit: core PI outcomes

1. **Reference architecture and contracts** — establish boundaries, APIs, ownership, versioning, and the thin-SDK approach.
2. **Model access baseline** — harden model access as a governed inference boundary without turning it into an AI runtime.
3. **Guardrails baseline** — separate non-bypassable gateway controls from reusable guardrail services and use-case policy.
4. **Memory and state MVP** — provide a framework-neutral state primitive with enterprise identity, lifecycle, and audit controls.
5. **RAG / retrieval MVP** — provide reusable retrieval as a capability, not something hidden inside the model endpoint.
6. **Dogfood through prioritized use cases** — prove composition and feed gaps back into the platform backlog.

### Enable where required by use cases

- MCP access patterns and credential-provider integration.
- Common telemetry, evaluation hooks, cost attribution, and service-level metrics.
- Thin client libraries that reduce integration friction without defining application orchestration.

### Deliberately defer from the core PI

- A new enterprise `Agent`, `Tool`, `Chain`, or workflow abstraction.
- A universal agent runtime.
- RAG, memory, or agent execution embedded in the model endpoint.
- A new proprietary prompt/workflow DSL.
- Enterprise ontology/semantic context as a prerequisite for this PI. It remains strategic and can be introduced when a prioritized use case requires it.
- Broad migration of every existing application to the new primitives.

---

## 4. Implementation sequence

The sequence is designed to reduce architecture rework. Phases can map to iterations/sprints based on the ART cadence; they are intentionally expressed as outcomes rather than fixed dates.

### Phase 1 — Boundaries and contracts

**Primary outcome:** Teams agree on what the platform owns before expanding existing SDKs/endpoints.

**Deliver:**

- Reference architecture and ownership map.
- Capability boundaries for Model Access, Guardrails, Memory/State, RAG, MCP/Credentials, and Observability/Evaluation.
- API-first contracts and versioning expectations.
- A clear rule for mandatory gateway controls vs optional/composable services.
- Thin SDK/client principles for Java/Python as needed.
- Architecture review checklist to prevent framework duplication.

**Exit criteria:** New work can be mapped to a named capability and owner; model-gateway and SDK scope are explicit.

### Phase 2 — Establish the mandatory enterprise boundary

**Primary outcome:** Model access and enterprise-wide controls are dependable and narrow.

**Deliver:**

- Governed model access baseline.
- Guardrail enforcement points.
- Identity and entitlement propagation.
- Quota/rate/cost controls.
- Common request/response telemetry and audit context.

**Exit criteria:** A use-case team can call approved models through a stable interface and cannot bypass mandatory enterprise controls through the supported path.

### Phase 3 — Add independently consumable primitives

**Primary outcome:** Application teams can compose state and retrieval without adopting a platform-owned orchestration framework.

**Deliver:**

- Memory/State MVP.
- RAG/Retrieval MVP.
- Thin client integration patterns.
- Required MCP/Credential patterns for selected use cases.

**Exit criteria:** The primitives can be consumed directly from at least two application patterns/frameworks.

### Phase 4 — Dogfood, harden, and measure reuse

**Primary outcome:** Platform gaps are discovered from real application composition, not hypothetical framework design.

**Deliver:**

- Integrate 2–3 prioritized use cases.
- Record primitive-by-primitive gaps.
- Fix repeated integration friction at the platform layer.
- Establish SLOs/runbooks for capabilities entering production.
- Produce next-PI backlog from evidence.

**Exit criteria:** Common primitives have demonstrated reuse and the next investment decisions are backed by real integration evidence.

---

## 5. Epic 0 — Reference architecture and capability contracts

### Problem to solve

Existing AI functionality can grow organically into overlapping SDKs, gateways, runtime behavior, and framework abstractions. Without explicit boundaries, convenience features can become architecture by accident.

### PI outcome

A published implementation contract that answers: **what belongs in the Fabric, what belongs in the application, and where each capability is consumed.**

### In scope

- Reference architecture and capability ownership.
- API/service boundaries.
- Non-bypassable vs composable control model.
- Contract/versioning standards.
- Framework-neutral integration guidance.
- Thin-client packaging guidance.
- Design review checklist and anti-patterns.

### Explicitly out of scope

- Selecting one enterprise agent framework.
- Designing a new agent abstraction.
- Requiring all existing applications to migrate.

### Candidate features / backlog

- Publish logical architecture with application/runtime layer separated from Fabric primitives.
- Define model-gateway responsibilities and exclusion list.
- Define guardrail layers: enterprise invariants, reusable guardrails, use-case policy.
- Define common identity/context envelope passed across primitives.
- Define standard telemetry fields: application, use case, owner, model, policy, request correlation, cost attribution.
- Define versioning/deprecation contract for primitive APIs and clients.

### Acceptance evidence

- Architecture is reviewed by platform, security, and at least two application teams.
- Each committed PI epic maps to an explicit capability boundary.
- No committed epic requires a proprietary agent/runtime abstraction.

---

## 6. Epic 1 — Model access baseline

### Problem to solve

Application teams need secure and consistent access to enterprise-approved models, but the model endpoint should not become the place where RAG, memory, tools, workflows, and agent execution accumulate.

### PI outcome

A **boring, dependable model-access boundary** that handles enterprise inference concerns and stays out of application orchestration.

### In scope

- Authentication and workload/application identity.
- Model/provider entitlements.
- Approved model catalog / model identifiers.
- Provider abstraction where it reduces application coupling.
- Rate limits, quotas, token limits, and cost attribution.
- Required audit/telemetry.
- Mandatory enterprise safety/data-handling checks.
- Streaming and core OpenAI-compatible behavior required by target applications.
- Reliability baseline: timeouts, retries where safe, error taxonomy, health/SLOs.

### Explicitly out of scope

- RAG orchestration.
- Conversation memory.
- Agent loops or planning.
- Tool/MCP orchestration.
- Prompt workflow engine.
- Business approval flows.

### Candidate features / backlog

- Publish supported compatibility surface and known deviations.
- Add/standardize application identity and owner metadata.
- Enforce model/provider entitlements.
- Standardize usage/cost events.
- Define error model and retry semantics.
- Add policy hooks for mandatory controls.
- Establish service SLO dashboard and operational runbook.

### Acceptance evidence

- A developer can switch between at least two approved models/providers without rewriting application orchestration.
- Unsupported application semantics are not added to the gateway to unblock a single use case.
- Every supported invocation emits attributable usage/audit telemetry.
- Mandatory controls are validated through integration tests.

### PM success measures

- Time for a new application to receive approved model access.
- Percentage of model calls attributable to an application/use case/owner.
- Gateway availability and error rate.
- Number of application-specific exceptions introduced into the gateway — target should trend toward zero.

---

## 7. Epic 2 — Guardrails and policy baseline

### Problem to solve

Some controls must apply to every supported model invocation, while other policies are reusable but application-specific. Putting all guardrails into the model gateway either makes the gateway domain-aware or makes application controls impossible to evolve independently.

### PI outcome

A layered guardrail model with **mandatory enforcement for enterprise invariants** and an **independent policy/guardrail capability** for reusable application controls.

### Target model

```text
Application / Workflow
        |
        +--> Guardrail Service
        |    configurable/reusable policy
        |
        v
Model Access
        |
        +--> Mandatory enterprise controls
        |
        v
Model Provider
```

### In scope

**Gateway-enforced baseline**
- Model/provider entitlement.
- Required data-classification/provider restrictions.
- Required auditability.
- Quota/rate controls.
- Mandatory safety controls defined by enterprise policy.

**Independent guardrail service / policy layer**
- Policy evaluation API.
- Configurable input/output rule packs.
- PII/secret checks or redaction where appropriate.
- Prompt-injection / unsafe-input checks where applicable.
- Response/schema validation.
- Hooks for groundedness/citation checks when used by RAG applications.
- Policy decision telemetry.

### Explicitly out of scope

- Encoding business workflows in the model gateway.
- A universal confidence score for all use cases.
- Domain approval logic such as claims/payment thresholds inside the gateway.

### Candidate features / backlog

- Classify current guardrails into mandatory vs reusable vs use-case-specific.
- Define policy evaluation contract and policy IDs/versioning.
- Implement gateway enforcement hooks for mandatory baseline.
- Expose app-callable guardrail API/client.
- Emit allow/block/warn decisions with reason codes.
- Provide 2–3 starter policies required by dogfood applications.

### Acceptance evidence

- Mandatory controls cannot be bypassed through the supported model-access path.
- At least one application invokes additional guardrails independently of the gateway.
- Policies are versioned/configurable without a model-gateway release.
- Business-specific policy remains owned by the use-case/application team.

### PM success measures

- Policy coverage for supported model paths.
- Percentage of guardrail decisions with auditable reason/version.
- Time to add or update a reusable policy without gateway deployment.
- Number of application-specific rules embedded in the gateway — target zero.

---

## 8. Epic 3 — Memory and state MVP

### Problem to solve

Teams need durable state, but embedding memory into an agent SDK or model endpoint forces one state model and creates migration friction when orchestration frameworks change.

### PI outcome

A framework-neutral **Memory/State primitive** that applications can use directly and securely.

### In scope

- Namespaced state by application/use case/user or workload as appropriate.
- Basic read/write/query/delete semantics.
- Session/conversation state and a path for longer-lived application memory where needed.
- TTL/retention configuration.
- Access control and identity propagation.
- Encryption and audit events.
- Metadata/tags for retrieval and lifecycle management.
- Size/usage limits and operational telemetry.
- Thin Java/Python client if it materially reduces integration work.

### Explicitly out of scope

- Agent planning state machine.
- A platform-defined definition of “what an agent should remember.”
- Automatic summarization strategy for every use case.
- Hiding state behind the model endpoint.

### Candidate features / backlog

- Define state resource model and namespace rules.
- CRUD/query API.
- TTL/retention and delete semantics.
- Identity/authorization integration.
- Audit and usage metrics.
- Reference adapters/examples for two framework patterns.
- Document guidance for session state vs durable memory.

### Acceptance evidence

- Two different applications/frameworks can store and retrieve state through the same service.
- State is isolated by declared application/tenant/security context.
- Retention and deletion behavior is testable and documented.
- No agent-loop semantics are required to consume the capability.

### PM success measures

- Integration time for a new application.
- Number of applications reusing the service.
- Read/write latency and availability against agreed SLOs.
- Percentage of stored state covered by explicit retention policy.

---

## 9. Epic 4 — RAG / retrieval MVP

### Problem to solve

Each team rebuilding retrieval produces inconsistent access control, metadata handling, evidence, observability, and quality. Conversely, hiding RAG inside the model endpoint couples retrieval to inference and limits application choice.

### PI outcome

A reusable **retrieval capability** that can return trusted context/evidence to applications independently of model execution.

### In scope

- Retrieval API separated from model inference.
- Registration/configuration of supported knowledge sources/indexes needed by dogfood use cases.
- Query + metadata filters.
- Identity/entitlement-aware retrieval where source permissions require it.
- Ranked results with source/evidence metadata.
- Citation-friendly response contract.
- Retrieval telemetry: source, latency, result counts, filters, failures.
- Initial quality/evaluation hooks.
- Thin client/reference integration with at least two application patterns.

### Explicitly out of scope

- “Ingest every enterprise document” as a PI goal.
- One chunking/embedding strategy mandated for every domain.
- RAG hidden inside `/chat/completions` or equivalent gateway APIs.
- Agent orchestration or prompt construction.
- Enterprise semantic/ontology layer as a prerequisite for the MVP.

### Candidate features / backlog

- Define retrieval request/response contract.
- Define source/index registration pattern.
- Implement metadata filters and evidence contract.
- Propagate application/user authorization context.
- Add retrieval tracing and basic quality metrics.
- Build reference examples: application-controlled prompt assembly and citation rendering.
- Document when teams should use the shared retrieval service vs domain-owned retrieval.

### Acceptance evidence

- A use case can call retrieval without invoking a model.
- Retrieved results contain sufficient source metadata for citations/evidence.
- Access controls are enforced consistently for at least one governed source.
- Two use cases can reuse the same retrieval contract even if their prompt/orchestration logic differs.

### PM success measures

- Time to onboard a supported knowledge source/index.
- Retrieval latency and failure rate.
- Percentage of returned results with source/evidence metadata.
- Quality baseline for selected dogfood queries (use-case-defined, not a universal score).
- Number of duplicated retrieval implementations avoided or retired over time.

---

## 10. Epic 5 — MCP and credential normalization (enablement / use-case driven)

### Problem to solve

Applications need secure access to enterprise tools and systems. Tool connectivity becomes brittle when every agent/framework implements credential acquisition and MCP connection patterns differently.

### PI outcome

Normalize the **enterprise integration boundary** enough for selected use cases without building a proprietary tool abstraction.

### In scope

- Credential-provider pattern for workload/tool access.
- Standard MCP authentication/authorization expectations.
- Tool/server identity and ownership metadata.
- Connection patterns reusable from multiple frameworks.
- Audit/telemetry for tool invocation where the platform boundary can observe it.

### Explicitly out of scope

- Replacing MCP with an enterprise `Tool` class.
- Building an enterprise-specific tool-call DSL.
- Requiring every existing MCP server to migrate in this PI.

### Acceptance evidence

- Selected dogfood applications can call required enterprise tools without embedding long-lived credentials.
- The same MCP/server can be consumed from more than one framework/runtime pattern where practical.

---

## 11. Epic 6 — Dogfood and prove composition

### Problem to solve

A platform can appear reusable in architecture diagrams while remaining difficult to consume. The PI needs real use cases to expose missing contracts, coupling, and developer friction.

### PI outcome

Use 2–3 prioritized business use cases as **design partners**, not one-off exceptions.

### How to select dogfood use cases

Prefer a portfolio that exercises different combinations:

| Use case profile | Capabilities exercised |
|---|---|
| Knowledge / assistant use case | Model Access + Guardrails + RAG |
| Stateful workflow / copilot | Model Access + Guardrails + Memory/State |
| Action-oriented use case | Model Access + Guardrails + MCP/Credentials, optionally RAG/Memory |

The use cases do **not** need to share the same framework. In fact, using different application patterns is useful evidence that the Fabric is truly composable.

### Required planning artifact for each use case

```text
Use case:
Business outcome / KPI:
Application owner:
Framework/runtime:
Primitives consumed:
  [ ] Model Access
  [ ] Guardrails
  [ ] Memory / State
  [ ] RAG / Retrieval
  [ ] MCP / Credentials
  [ ] Evaluation / Observability
Known gaps:
Platform capability requested:
Is the request reusable across multiple use cases? Yes / No
Production readiness target:
```

### Acceptance evidence

- At least two use cases consume common primitives.
- Platform teams do not introduce use-case-specific behavior into model access to make dogfood succeed.
- Repeated integration gaps are converted into platform backlog; one-off business behavior stays with the application.
- Each use case records measurable business or delivery outcomes.

---

## 12. Cross-cutting work that should be included inside every epic

These should not become large standalone programs before the core primitives exist. Each primitive should include the minimum needed to operate responsibly.

### Identity and ownership

Every call/resource should be attributable, where applicable, to:
- application/use case,
- workload/user identity,
- owning team,
- environment,
- policy/version context.

### Observability

Each primitive should expose:
- availability/error rate,
- latency,
- usage/volume,
- major policy/failure reason codes,
- correlation IDs across primitives.

### Cost attribution

Where meaningful, capture enough metadata to allocate model, storage, retrieval, and tool usage back to an application/use case.

### Operational readiness

A primitive should not be considered production-ready without:
- owner/on-call path,
- SLO or service objective,
- runbook,
- capacity/limit documentation,
- version/deprecation approach,
- support/escalation expectations.

### Developer experience

Prefer:
- API-first capability,
- small client libraries where useful,
- examples for more than one framework,
- local/test doubles where practical,
- explicit errors and troubleshooting guidance.

Avoid making a large SDK package the only supported consumption path.

---

## 13. PI sequencing and dependency view

```text
[Reference Architecture / Contracts]
               |
               v
 [Model Access] ------> [Guardrails Baseline]
       |                       |
       +-----------+-----------+
                   |
          +--------+--------+
          |                 |
          v                 v
   [Memory / State]    [RAG / Retrieval]
          |                 |
          +--------+--------+
                   |
          [Use-case Dogfood]
                   |
                   v
        [Hardening + Next PI]

MCP/Credentials and Eval/Observability are pulled through
where required by the selected use cases.
```

### Dependency principles

- Do not wait for every primitive to be “complete” before dogfood begins.
- Do not make enterprise context/ontology a dependency for the initial platform foundations.
- Do not block model-access hardening on a new SDK design.
- Do not make RAG depend on the model gateway beyond shared identity/policy/telemetry needs.
- Do not make memory depend on a specific agent framework.

---

## 14. Suggested PI objectives and measurable evidence

These are examples PMs can adapt into formal PI objectives.

### Objective 1 — Establish AI Fabric contracts

**Outcome:** Publish and adopt capability boundaries and API contracts for committed primitives.

**Evidence:** All committed work maps to a defined primitive; architecture reviews use the same boundary rules; no new platform-owned agent abstraction is introduced.

### Objective 2 — Harden governed model access and guardrails

**Outcome:** Application teams can access approved models with consistent identity, policy, quota, audit, and telemetry controls.

**Evidence:** At least two dogfood applications use the supported model path; mandatory controls are integration-tested; usage is attributable.

### Objective 3 — Deliver composable Memory/State and RAG MVPs

**Outcome:** Applications can consume state and retrieval independently of model execution and framework choice.

**Evidence:** Each primitive is used by at least one dogfood application; across the portfolio, common contracts are reused by multiple application patterns.

### Objective 4 — Prove the Fabric through real use cases

**Outcome:** 2–3 prioritized use cases compose shared primitives and provide feedback into the platform backlog.

**Evidence:** Reusable platform gaps, one-off app requirements, developer integration effort, reliability, and business/delivery outcomes are documented.

---

## 15. What PMs should not use as success metrics

Avoid metrics that reward platform lock-in instead of business/platform value:

- “100% of teams use our AI SDK.”
- “All agents run on our runtime.”
- “Number of custom framework abstractions created.”
- “Number of features added to the gateway.”
- “Number of use cases migrated” without evidence of reuse, quality, or reduced delivery effort.

Prefer:

- Time to first governed model call.
- Time to integrate a reusable primitive.
- Number of independent applications reusing the same capability contract.
- Reduction in duplicate implementations.
- Percentage of calls/resources with ownership, policy, and audit context.
- Reliability and operational readiness of each primitive.
- Delivery acceleration demonstrated by dogfood use cases.

---

## 16. Decisions PMs need to lock during PI planning

1. **Which 2–3 use cases are design partners?** Pick use cases that exercise different primitive combinations.
2. **Which capabilities are committed vs enablement/stretch?** Avoid committing to every possible Fabric capability in one PI.
3. **What is the minimum production bar for each primitive?** Define SLO/support expectations up front.
4. **What current SDK/gateway features are frozen from further expansion?** Prevent parallel investment in patterns we intend to unwind.
5. **Which existing functionality can be wrapped/extracted rather than rebuilt?** Reuse before rewrite.
6. **Which policies are mandatory enterprise invariants?** Security/platform owners must make this explicit.
7. **What evidence will decide next-PI investment?** Reuse, integration friction, reliability, risk reduction, and use-case value should drive the next sequence.

---

## 17. Definition of done for a Fabric primitive

A primitive is not “done” because an API exists. For PI purposes, a capability is ready to claim as reusable when:

- It has a named product/engineering owner.
- Its responsibility and exclusions are documented.
- It has a stable/versioned API or protocol contract.
- It can be consumed independently of a proprietary agent framework.
- Authentication/authorization requirements are implemented.
- Audit/telemetry are available.
- SLO/support/runbook expectations are defined for production use.
- At least one real use case has consumed it end-to-end.
- There is a second plausible/reviewed consumer proving it is not a one-off abstraction.
- Known gaps and next-PI backlog are documented.

---

## 18. PI planning summary

**Build now:**

```text
Reference Architecture / Contracts
        +
Governed Model Access
        +
Layered Guardrails
        +
Memory / State MVP
        +
RAG / Retrieval MVP
        +
Use-case Dogfood
```

**Enable as pulled by use cases:** MCP/Credentials, evaluation/observability enhancements, and thin clients.

**Do not make the PI about:** another agent SDK, a universal runtime, a giant AI endpoint, or full enterprise-semantic convergence.

> **The PI succeeds when application teams can compose reusable enterprise capabilities to deliver outcomes faster — without the platform becoming another agent framework.**

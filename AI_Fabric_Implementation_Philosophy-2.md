# AI Fabric Implementation Philosophy

**Build enterprise primitives, not another AI framework**  
Draft | September 2026

> **Converge at the enterprise capability layer — not by forcing one SDK, one agent framework, or one runtime.**

## Purpose

Define how the AI Fabric strategy should be implemented: what the platform should own, what application teams should own, where enterprise controls belong, and which design patterns we should deliberately avoid.

## 1. Implementation thesis

The AI Fabric is not a new destination where every team must build applications in the same way. It is a set of reusable enterprise capabilities that application teams compose into business solutions using the frameworks and runtimes that best fit their use case.

> **Own enterprise primitives. Adopt commodity abstractions. Keep application composition flexible.**

- **Business outcomes first.** The platform exists to accelerate high-value use cases, not to create another general-purpose agent ecosystem.
- **Capabilities over frameworks.** Standardize model access, identity, memory, retrieval, tooling, policy, context, evaluation and observability — not Agent/Tool/Chain abstractions.
- **Convergence below the application.** AI Studio, Workbench, ACT, domain apps and future experiences can differ while consuming the same Fabric capabilities.
- **Control at enterprise boundaries.** Non-bypassable security, policy, audit and entitlement controls should be enforced centrally; use-case behavior stays with the application.
- **Dogfood through real use cases.** The first prioritized business solutions should consume the primitives and feed gaps back into the platform.

## 2. Reference implementation model

```text
BUSINESS SOLUTIONS / EXPERIENCES
Analytics | Service | Decisioning | Data Products | Domain Apps
                         |
                         v
APPLICATION COMPOSITION & RUNTIME
ADK | LangGraph | OpenAI SDK | ACT | Custom Python/Java
(Application team owns orchestration, prompts, workflow, approvals)
                         |
             compose enterprise capabilities
                         v
AI FABRIC PRIMITIVES
Model Access | MCP/Tools | Memory/State | RAG/Retrieval
Identity/Credentials | Guardrails/Policy | Enterprise Context
Evaluation | Observability | Cost/Audit
                         |
                         v
MODELS | ENTERPRISE DATA | KNOWLEDGE | SYSTEMS / APIS
```

**Key architecture rule:** the package is not the architecture. A convenience SDK may bundle clients, but each capability should remain independently consumable and independently evolvable.

## 3. Design principles

### 3.1 Solve an enterprise problem
Build when the capability addresses a problem that every application team would otherwise solve differently: secure access, identity, policy, enterprise context, governed retrieval, memory/state, observability, evaluation, cost or audit.

### 3.2 Prefer protocols and portable interfaces
Use standards such as OpenAI-compatible model APIs and MCP where they provide interoperability. Avoid proprietary abstractions when an ecosystem contract already exists.

### 3.3 Independent capabilities over a monolith
RAG, memory, guardrails, tools and model access have different lifecycles. Keep them composable rather than hiding them behind one heavy AI endpoint or runtime.

### 3.4 Opinionated at the enterprise boundary
The platform should be strict about controls that must be consistent: authentication, authorization, provider/model entitlement, data policy, audit, rate limits and required telemetry.

### 3.5 Flexible at the application boundary
Applications decide planning, prompt strategy, workflow, tool sequence, human approvals, state machines and business-specific policy.

### 3.6 No universal agent by default
Do not introduce a universal enterprise agent, router or orchestration layer simply to create consistency. Reuse capabilities underneath different application experiences instead.

## 4. Build vs. adopt decision framework

Before adding a new abstraction or platform feature, ask:

1. **Enterprise problem?** Does it solve a security, governance, integration, context, reliability, cost or operational problem unique to running AI in the enterprise?
2. **Consistency required?** Would inconsistent implementations across teams create material risk, duplicated effort or poor interoperability?
3. **Independent boundary?** Can it be consumed independently from LangChain, ADK, ACT, OpenAI SDK or custom applications?
4. **Ecosystem alternative?** If a mature framework already solves the abstraction and no enterprise value is lost, adopt rather than recreate it.

| Capability / abstraction | Default position | Rationale |
|---|---|---|
| Agent loop / planner | Adopt | Commodity application orchestration; use framework of choice. |
| Tool abstraction / decorator | Adopt / use MCP | Avoid inventing another proprietary tool contract. |
| Prompt chaining / workflow DSL | Adopt | Application concern; ecosystem evolves quickly. |
| Model access | Build / operate | Enterprise entitlement, routing, provider policy, quotas, telemetry and cost. |
| Credential / workload identity | Build / integrate | Enterprise-specific security and access boundary. |
| MCP gateway / enterprise tool access | Build / integrate | Governed discovery, auth, connectivity and audit for enterprise systems. |
| Memory / state | Build as capability | Shared persistence, identity, tenancy, lifecycle and policy concerns. |
| RAG / retrieval service | Build selectively | Shared governed retrieval patterns, ACL propagation, citations and observability. |
| Guardrails / policy | Both | Independent policy capability plus mandatory gateway enforcement for enterprise invariants. |
| Evaluation / observability | Build / integrate | Cross-application quality, traceability, operations and cost control. |
| Enterprise context / semantics | Build strategically | Enterprise-specific business meaning; independent from any one agent framework. |

## 5. Keep the model-access boundary intentionally narrow

The OpenAI-compatible endpoint is valuable as a familiar, governed model-access contract. It becomes harmful when convenience causes it to absorb application semantics.

**Belongs in model access:** authentication, model/provider entitlement, routing, rate limits and quotas, non-bypassable data/provider policy, required audit/usage/cost telemetry, mandatory baseline safety controls.

**Usually stays outside:** RAG orchestration, long-lived memory, agent planning, tool sequencing, prompt chains, human approvals, business rules and application-specific evaluation.

> If the endpoint owns all of these, it is no longer a model gateway; it has become a proprietary AI application runtime.

## 6. Guardrails: independent capability + mandatory enforcement

Use layered enforcement:

- **Enterprise invariants — gateway/control plane:** model/provider restrictions, sensitive-data rules, mandatory logging, quotas, baseline safety.
- **Reusable AI guardrails — independent service:** PII detection/redaction, prompt-injection checks, groundedness, content classification, response/schema validation.
- **Use-case policy — application:** human approvals, domain thresholds, tool sequence, confidence rules and business-specific response constraints.

## 7. SDK philosophy: thin clients over Fabric capabilities

An enterprise SDK can reduce friction, but it should not define a new AI programming model.

```text
GOOD
enterprise-model-client
enterprise-memory-client
enterprise-rag-client
enterprise-mcp-client
enterprise-guardrail-client
enterprise-credential-provider
enterprise-eval-client

OPTIONAL convenience package:
enterprise-ai-clients = supported bundle of the above clients

AVOID
EnterpriseAgent + EnterpriseTool + EnterpriseChain + EnterpriseWorkflow
+ proprietary runtime semantics
```

## 8. Patterns to deliberately avoid

- **Build “our LangChain.”** Duplicates commodity abstractions, creates internal lock-in and forces platform teams to chase framework parity.
- **Put everything behind the model endpoint.** Couples unrelated lifecycles and turns the gateway into the application runtime.
- **Universal enterprise agent/router.** Flattens domain differences and centralizes application semantics.
- **Custom tool contract instead of MCP.** Reduces portability and creates another integration ecosystem.
- **Bundled RAG/memory inside the SDK.** Forces one retrieval/state pattern across diverse use cases.
- **Platform features without a target use case.** Produces abstractions without evidence of reusable enterprise value.

## 9. What composition looks like in practice

| Use case | Composition example |
|---|---|
| Analytics Orchestrator | Framework/runtime + Model Access + Code/Tools + Memory/State + Guardrails + Evaluation/Observability |
| Service / domain copilot | Framework/runtime + Model Access + RAG + Enterprise Context + MCP/Tools + Guardrails |
| Deterministic decision workflow | Application workflow + Model Access only where ambiguity exists + Enterprise Context + Policy + Audit |
| Simple summarization API | Model Access + baseline gateway controls; no requirement to adopt memory, RAG or an agent runtime |

## 10. No-regrets implementation sequence

1. **Publish the reference architecture and boundaries.** Make ownership explicit.
2. **Harden model access without expanding it into a runtime.** Clarify non-bypassable controls and simplify the access path.
3. **Establish guardrails as a layered capability.** Separate gateway policy, reusable guardrails and use-case policy.
4. **Stand up memory/state and RAG as independent services/interfaces.** No framework dependency.
5. **Normalize MCP and credential access patterns.** Make secure enterprise tool access easy to consume.
6. **Dogfood with prioritized use cases.** Map each use case to the primitives it consumes and feed gaps back into the Fabric.
7. **Add enterprise context deliberately.** Strategic, but it need not block the initial PI foundations.

> **Success is not “all teams use our SDK.” Success is: teams deliver business outcomes faster because enterprise AI capabilities are reusable, governed, composable and easy to consume.**

## 11. Design review questions

- What enterprise problem is this capability solving?
- Why must the platform own this instead of adopting an ecosystem abstraction?
- Can an application consume it independently from our preferred SDK/framework?
- Does this belong in the model-access boundary, or are we adding application semantics to the gateway?
- Which controls must be non-bypassable, and which belong to the use case?
- Can the capability evolve and version independently?
- Which prioritized use case will dogfood it and prove reuse?
- What do we stop building if we invest in this?

## 12. Implementation philosophy in one page

| Dimension | Position |
|---|---|
| Strategy | AI is a Fabric that enables business solutions; it is not another application destination. |
| Product model | Reusable enterprise primitives consumed by many experiences. |
| Convergence point | Capability layer — not one SDK, one framework or one agent runtime. |
| Platform ownership | Identity, model access, credentials, MCP, memory/state, RAG, guardrails, context, evaluation, observability, audit/cost. |
| Application ownership | Orchestration, prompts, planning, workflow, business rules, approvals and domain-specific behavior. |
| SDK stance | Thin, framework-neutral clients over independent capabilities. |
| Gateway stance | Narrow, governed model-access boundary; do not hide RAG, memory or agent execution inside it. |
| Guardrails stance | Independent policy capability plus mandatory enforcement of enterprise invariants. |
| Build test | Build where enterprise value/control exists; adopt commodity AI abstractions. |
| Delivery model | Dogfood primitives through prioritized use cases and refine from evidence. |

> **Opinionated at enterprise boundaries. Composable at the application boundary.**

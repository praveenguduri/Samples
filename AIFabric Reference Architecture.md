On this page

- [Overview](#overview)
- [Design principles](#principles)
- [Architecture layers](#layers)
- [Experience and ingress](#experience)
- [Runtime](#runtime)
- [Agent capabilities](#capabilities)
- [Gateways](#gateways)
- [Control plane](#control)
- [Cross-layer concerns](#cross)
- [Assurance](#assurance)
- [Build](#build)
- [Human-in-the-loop and feedback](#hitl)
- [Catalog](#catalog)
- [Factories](#factories)
- [Agent factory: harness templates](#templates)
- [Developer experience](#devex)
- [Reference request flow](#flow)
- [Architecture decisions](#decisions)
- [Standards](#standards)
- [Industry comparables](#comparables)

AIFabric › Architecture › Reference architecture

# AIFabric reference architecture for enterprise agents

Version 0.4 · October 2026 · Status: draft for review

AIFabric is the enterprise platform for building, running and governing AI agents. This page describes the reference architecture: the layers of the platform, the modular services in each layer, and how they work together.

The architecture is built on one position. Teams own their agent's reasoning loop and can use any supported framework. The platform owns the controls that must hold for every agent: identity, authorization, content safety, cost, audit and evaluation. These controls are enforced at the gateways (model, MCP and agent), outside agent code, so they apply whether or not a developer remembers to call them.

Each service has its own API and can be adopted independently. A team can start with only the model gateway and tracing, and add other services as its agents mature.

Must have Good to have Optional

**Build**

Fabric SDKFramework adaptersAgent factoryTool factorySkill factoryEval dataset factoryPattern libraryModel factoryPlanners

**Experience and ingress**

SurfacesAgent API and A2ATriggers

**Assurance**

ObservabilityAuditEvaluationFeedback

**Runtime**

Agent RuntimeSandboxMCP Server Hosting

**Agent capabilities**

MemoryContextRetrievalKnowledge

**Gateways**

Model GatewayMCP GatewayAgent Gateway

**Control plane (called inline by every gateway)**

CatalogIdentityPolicyGuardrailsApprovalsFinOps

Figure 1. AIFabric layers and services, by priority. Must-have services form the minimum governed platform; good-to-have services are added as agents need them; optional services are added only for specific use cases. Models, MCP servers, other agents and enterprise systems sit behind the gateways and are reached only through them.

## Design principles

- **Enforce at the gateway, not in the agent** – Policy, guardrails, budgets and audit run in the gateways. SDK helpers make the right path easy, but the gateways guarantee the outcome.
- **Every agent is a principal** – Each agent has its own workload identity and a named owner. Calls made for a user act on behalf of that user. Tokens are never passed through to downstream systems.
- **Modular and independently adoptable** – Each service has its own API, owner team and service-level objectives.
- **Framework-native** – The platform plugs into the extension points of LangGraph, ADK and similar frameworks. It does not introduce a competing agent runtime.
- **One catalog** – Agents, MCP servers, tools, skills, prompts and models are recorded in one governed catalog with versions and owners.
- **Durable by default** – Agent runs survive restarts. Long waits, retries and human approvals are platform features.
- **Observable from the first call** – Every hop emits an OpenTelemetry span and an audit record. Production traces feed evaluation.

## Architecture layers

The platform is organized into five layers. Requests enter at the experience and ingress layer and leave the platform only through the gateway layer. The control plane sits beneath the gateways and is called inline on every request.

### Experience and ingress layer

This layer is where work reaches an agent, from people, from other systems or from other agents.

- **Surfaces** – A reference chat interface and connectors for Microsoft Teams and Slack. Supports streaming responses, citations, approval cards and an approver inbox, so teams do not each build their own front end.
- **Agent API and A2A** – A stable endpoint for each agent version. Supports synchronous and streaming calls and the full task lifecycle (submit, stream, cancel, resume). Publishes signed A2A Agent Cards generated from the catalog.
- **Triggers** – Starts agent runs from webhooks, message queues and schedules, with ordering, retries and dead-letter handling. Runs started by triggers use the agent's own identity.

### Runtime layer

This layer runs agents and the internal tools they use. It hosts the team's harness but does not own the reasoning loop.

- **Agent Runtime** – Managed hosting for agents built with any supported framework. Provides per-session isolation, session routing, scale to zero, timeouts and cancellation, checkpoint storage and durable execution for long waits. Injects the agent's identity at start-up, so agent code holds no secrets.
- **Sandbox** – Isolated environments in which agents run generated code or operate a headless browser. Uses microVM or gVisor isolation with warm pools. Network egress is controlled by Policy.
- **MCP Server Hosting** – A deployment harness for internal MCP servers. Packages a server from a template, runs it with its own workload identity, and registers it in the catalog behind the MCP Gateway. Externally hosted servers can also be registered and pass the same catalog review.

### Agent capabilities layer

This layer gives agents knowledge and memory. Its services are distinguished by who writes the data and how long it is kept.

- **Memory** – Stores what agents learn about users and tasks: session memory within a run, episodic memory across runs, and a persistent store shared across applications. Includes retention and deletion controls. Memory is separate from run checkpoints, which hold the state needed to resume a run.
- **Retrieval** – Managed retrieval-augmented generation over enterprise documents and data. Provides connectors, chunking, embedding, hybrid search and reranking. Enforces source access controls at query time and returns citations.
- **Knowledge** – The ontology registry, managed graph databases and pre-built organizational graphs. Provides shared definitions so that agents interpret enterprise terms consistently.
- **Context** – A composition service that assembles context for an agent step from Memory, Retrieval and Knowledge. Resolves entities against the ontology, filters results by the acting user's entitlements and fits the result to a token budget. Context does not store data of its own.

### Gateway layer

The gateways are the only paths from agents to models, tools and other agents. They are stateless enforcement points that call the control plane on every request.

- **Model Gateway** – Routes model calls to approved models, with fallback and retries. Applies per-agent, per-team and per-run budgets and rate limits. Offers optional exact and semantic caching. Calls Guardrails inline on prompts and responses. Exposes OpenAI-compatible and Anthropic-compatible APIs.
- **MCP Gateway** – The broker for every tool call. Agents connect to one MCP endpoint; the gateway federates the approved MCP servers behind it and wraps REST and gRPC services as MCP tools. On every call it checks the catalog, calls Policy and Guardrails, performs token exchange so that each server receives a scoped token, and writes an audit record. Offers semantic tool search so agents are not given hundreds of tool definitions.
- **Agent Gateway** – The broker for agent-to-agent calls over A2A. Resolves target agents from the catalog, verifies signed Agent Cards, calls Policy to decide which agents may call which, propagates delegated user context, and enforces timeouts and call-depth limits to prevent loops between agents.

### Control plane

The control plane holds the platform's shared governance services. Both gateways call these services inline, so the same rules apply to model calls and tool calls.

- **Catalog** – The system of record for everything agents are or use: agents, MCP servers and tools, skills, prompts, model routes, templates and patterns. Holds versions, owners, lifecycle state, risk tier and dependencies, and runs the approval workflow. Gateways, Identity, Policy and the Agent Runtime all read it. See [Catalog](#catalog).
- **Identity** – Issues a workload identity to each agent and ties it to an owner. Supports OAuth on-behalf-of flows and RFC 8693 token exchange, and keeps credentials in a vault that agent code cannot read. Manages the agent lifecycle, including access reviews and deprovisioning.
- **Policy** – Decides whether an agent may perform an action for a user with given arguments. Policies are written in Cedar or OPA, versioned and tested. Decisions are allow, deny, require approval or redact.
- **Guardrails** – Inspects content: content safety, prompt-injection detection, and PII redaction before data leaves the platform with reinsertion when results return.
- **Approvals** – Manages human-in-the-loop decisions. Receives requests raised by Policy or by the framework's own interrupt, routes them to approvers with SLAs and escalation, and resumes the paused run through the Agent Runtime. Approvers can approve, reject, or edit the proposed action before it runs. See [Human-in-the-loop and feedback](#hitl).
- **FinOps** – Manages budgets and quotas by agent, team and run, provides a kill switch for runaway loops, and produces showback and chargeback reports.

**Note**Guardrails and Policy are separate services. Guardrails inspect what is said; Policy decides what an agent may do. They change at different rates and are usually owned by different teams.

## Cross-layer concerns

### Assurance

- **Observability** – Collects traces and metrics for every agent using the OpenTelemetry GenAI semantic conventions (`invoke_agent`, `chat`, `execute_tool`, `plan`). Provides latency, error, token and cost dashboards, and samples and redacts trace content.
- **Audit** – An immutable, append-only record of every model call, tool call, approval and data access, stamped with the agent, the user and the policy decision. Records lineage from source data to answer. Kept separately from sampled debug traces and exported to the SIEM.
- **Evaluation** – Maintains versioned evaluation datasets per agent, gates releases in CI when prompts, models or tools change, scores sampled production traces with LLM judges, and queues cases for human review. Failures are added back to the datasets.
- **Feedback** – Captures feedback on agent behaviour from every channel and links it to the trace that produced it: user ratings and corrections in Surfaces, approver decisions and edits from Approvals, reviewer labels from evaluation queues, and outcome signals from downstream systems. Routes feedback to evaluation datasets, review queues and agent owners.

### Build

- **Fabric SDK** – A Python-first library that supplies endpoints, credentials, telemetry and storage backends. It returns framework-native objects only. See [Developer experience](#devex).
- **Framework adapters** – Implementations of framework extension points backed by platform services, such as a LangGraph `BaseStore` and ADK `SessionService` and `MemoryService`.
- **Factories** – Build pipelines that produce Catalog entries: the agent factory (harness templates), tool factory, skill factory, eval dataset factory and, optionally, a model factory. See [Factories](#factories).
- **Pattern library** – A small set of versioned reasoning patterns (ReAct, plan-and-execute, router) that return compiled LangGraph graphs.
- **Planners (optional)** – Planning delivered as libraries and tools rather than a central service: Agent Skills as the default format for planning know-how, a deterministic rules guard generalized from SOAR, and HTN decomposition as an MCP tool for procedure-heavy domains.

## Human-in-the-loop and feedback

People take part in agent work in two ways. During a run, they approve, correct or take over an agent's actions. After a run, their feedback is used to improve the agent. AIFabric provides both as platform features, so individual agents do not build their own.

### In-run interactions

All in-run interactions use the same mechanism. The agent's graph pauses with the framework's own interrupt, the Agent Runtime holds the session durably without holding compute, and the run resumes when a person responds through Surfaces or the approver inbox.

| Interaction | Raised by | Person's options | Example |
| --- | --- | --- | --- |
| Approval | Policy returns `require_approval` at a gateway | Approve, reject, or edit the action and approve | Refund above threshold |
| Clarification | The agent, when input is ambiguous or missing | Answer the question | "Which of the two orders should be refunded?" |
| Review | The agent or template, before output is released | Accept, edit, or send back with comments | Draft customer letter |
| Escalation | The agent, a timeout, low confidence, or repeated failure | Take over the task, or return it with guidance | Complaint the agent cannot resolve |

Each interaction has an assignee, an SLA and an escalation path, which are configured per agent in the catalog. A request that passes its SLA is escalated or, for approvals, rejected by default. Every decision, including any edit a person makes, is written to Audit and sent to Feedback.

### Feedback loop

Feedback connects production use to agent improvement:

1. **Capture** – Feedback records user ratings and corrections, approver decisions and edits, reviewer labels and downstream outcomes, each linked to its trace ID.
2. **Triage** – Negative feedback and edited approvals are queued for the agent owner. Patterns across agents, such as a tool that is often misused, are reported to the platform team.
3. **Curate** – Reviewed cases are added to the agent's evaluation dataset as new test cases with expected outcomes.
4. **Improve** – The owner changes prompts, skills, tools or policies. Changes are versioned in the catalog.
5. **Verify** – The evaluation gate in CI runs the updated dataset before release. Online evaluation then confirms the change in production.

**Note**Feedback improves agents through versioned changes that pass evaluation. It does not change agent behaviour directly at run time, except through Memory, where users can correct facts about themselves.

## Catalog

The Catalog is the system of record for everything agents are or use. It answers which artifacts exist, which versions are approved, who owns them and which agents depend on them. It does not build artifacts; the [factories](#factories) do, and submit them to the Catalog for approval.

### Entry types

- **Agents** – Each agent version, with its topology, owner and dependencies.
- **MCP servers and tools** – Servers and the tools they expose, each tool marked read-only or write.
- **Skills** – Agent Skills packages (SKILL.md and bundled scripts).
- **Prompts** – Versioned system prompts and instructions.
- **Model routes** – Approved models and the route names agents use at the Model Gateway.
- **Templates and patterns** – Harness templates and pattern library versions, so the platform knows which agents were built from which version.

### Common fields

| Field | Description |
| --- | --- |
| ID, type, version | Stable identifier and semantic version |
| Owner | Owning team and on-call contact |
| Lifecycle state | Draft, in review, approved, deprecated or retired |
| Risk tier | Sets the depth of review and is used as a Policy input |
| Data classification | Highest classification of data the artifact can read or return |
| Dependencies | For agents: the tools, skills, prompts and model routes used, with pinned versions |
| Evidence | Evaluation results, scan results, signature and the factory build that produced it |
| Governance defaults | Budget, approval rules, SLAs and assignees that apply at run time |

### Lifecycle and approval

Entries move from draft to in review to approved, and later to deprecated and retired. The review required depends on the risk tier. A read-only skill can be approved automatically when its factory checks pass. A write tool that moves money requires security and owner review. Deprecation notifies the owners of every dependent agent.

### Consumers

- **Gateways** – Allow only approved entries at the versions an agent has pinned.
- **Identity** – Issues an agent's workload identity when its entry is approved and revokes it at retirement.
- **Policy** – Uses risk tier, data classification and read/write marking as policy attributes.
- **Agent Runtime** – Deploys only approved agent versions.
- **Developer portal** – Lists entries for discovery and reuse.
- **Protocol projections** – The MCP Registry–compatible subregistry, A2A Agent Cards and the skills index are generated from the Catalog.

### Dependency graph

Because agents pin their dependencies, the Catalog can show the impact of a change before it is made, for example which agents are affected if a tool is deprecated or a model route is withdrawn.

### Skills at run time

An agent is given the names and descriptions of the approved skills it is allowed to use, filtered by the Catalog and Policy. It loads a skill's full content only when needed; the Catalog serves it as an MCP resource. Production agents pin skill versions in their Catalog entry. Usage and Feedback data are returned to the skill's owner.

## Factories

Factories are the build pipelines that produce Catalog entries. Every entry type has a factory, and all factories run on one shared pipeline with type-specific checks. As a result, every artifact reaches the Catalog with the same kind of evidence: who built it, what it was tested against, its scan results and its signature.

### Shared pipeline

1. **Author** – Start from a template, or generate a draft from existing material.
2. **Validate** – Check structure, schemas and declared dependencies.
3. **Scan** – Check for prompt-injection and exfiltration content, and run static analysis on code.
4. **Evaluate** – Run the artifact's test cases and evaluation dataset.
5. **Sign** – Sign the artifact and record the build provenance.
6. **Submit** – Register the artifact in the Catalog for review at its risk tier.

### Factory types

| Factory | Input | Produces | Type-specific checks | Priority |
| --- | --- | --- | --- | --- |
| Agent factory | A harness template and a pattern | An agent service and its Catalog entry | Unit tests, evaluation gate, declared dependencies | Must have |
| Tool factory | OpenAPI spec, gRPC definition, database schema or existing API | An MCP server deployed through MCP Server Hosting | Tool schema quality, read/write marking, risk tier, contract tests | Must have |
| Skill factory | SOPs, runbooks, code, expert-written drafts | Skill packages (SKILL.md and scripts) | Injection and exfiltration scan, trigger accuracy, outcome tests | Good to have |
| Eval dataset factory | Documents, production traces, Feedback, expert labels | Versioned evaluation datasets | Label review, PII removal, coverage of known failure modes | Good to have |
| Model factory | Base models and training data | Fine-tuned or distilled model routes | Model evaluation, safety tests, data lineage | Optional |

Prompts are versioned and evaluated inside the agent and skill factories rather than through a factory of their own.

**Note**The tool factory usually delivers the most value first. Most agent capability comes from good tools over existing enterprise APIs, and generating MCP servers from OpenAPI specs with read/write marking and risk tiers is the fastest way to make the platform useful.

Two pipelines resemble factories but are owned elsewhere. Knowledge ingestion (connectors, chunking, index and graph builds) runs continuously on live data and belongs to the Retrieval and Knowledge services. Policy-as-code is owned by the security team with the Policy service.

## Agent factory: harness templates

Most enterprise agents fit a few common topologies, in the same way most services fit a few service templates. AIFabric codifies these topologies as harness templates. A template scaffolds the complete agent service: harness code, ingress wiring, catalog entry, identity and policy defaults, evaluation skeleton, CI pipeline and dashboards.

### Agent topologies

| Template | Equivalent service topology | Ingress | Identity | Typical characteristics |
| --- | --- | --- | --- | --- |
| Conversational assistant | Web application | Surfaces | User, on-behalf-of | Streaming, context and tools, citations |
| Business-capability agent | API service | Agent API, A2A | Caller's delegation | Task in, structured result out |
| Event-driven agent | Event processor | Triggers (queue, webhook) | Agent's own | Background, approvals, durable |
| Workflow or document agent | Batch pipeline | Schedule or event | Agent's own | Long-running, checkpointed |
| Insight agent | Data dashboard | Surfaces or schedule | User, on-behalf-of | Retrieval and sandboxed analysis, charts |

The template sets the topology of the agent. The pattern library sets its reasoning shape. Most agents are one combination of the two, for example an event-driven agent that uses plan-and-execute.

### Template tooling

Templates are built with [Copier](https://copier.readthedocs.io/) and offered through the developer portal. Copier is chosen because it can apply template changes to repositories that were already generated (`copier update`), which limits drift.

```
fabric-agent-event/
├── copier.yml
└── {{agent_name}}/
    ├── agent/graph.py.jinja       # build_graph() using fabric.patterns.{{pattern}}
    ├── agent/main.py.jinja        # trigger handler → graph.ainvoke
    ├── catalog.yaml.jinja         # owner, tools, model route, budget, policy set
    ├── evals/golden.jsonl         # dataset skeleton
    ├── tests/test_graph.py.jinja
    ├── pyproject.toml.jinja       # pins fabric-sdk and fabric-patterns
    └── .github/workflows/ci.yml   # tests, evaluation gate, deploy
```

```
# copier.yml
agent_name: { type: str }
owner_team: { type: str }
pattern:
  type: str
  choices: [react, plan_execute, router]
trigger:
  type: str
  choices: [kafka, webhook, schedule]
tools: { type: str, help: "Catalog tool IDs, comma-separated" }
_tasks:
  - "fabric catalog register catalog.yaml"   # creates identity and default policies
```

### Keeping templates current

- **Thin templates** – Templates contain wiring and configuration only. Reasoning logic lives in versioned packages (`fabric-patterns`, framework adapters) that are upgraded as normal dependencies.
- **Governance in the catalog** – Policy, budget and identity defaults are held in the catalog entry rather than in code, so the platform team can change them without editing each repository.
- **Template updates** – Structural changes are released as new template versions and applied with `copier update`.

## Developer experience

Teams write ordinary LangGraph or ADK code. The Fabric SDK supplies endpoints, credentials, telemetry and storage backends at the extension points those frameworks already define.

**SDK rule**Fabric returns framework-native objects, never Fabric-native ones. If a team removes `import fabric` and supplies the URLs and credentials directly, the agent still runs. It loses only managed identity, memory and tracing.

### Development tiers

| Tier | Who uses it | What the team writes | Result |
| --- | --- | --- | --- |
| Pro-code | Teams with complex agents | Their own LangGraph or ADK graph | Native framework code with Fabric backends |
| Assembled | Most teams | Harness template plus a pattern from the library | A compiled LangGraph graph the team can extend |
| Declarative | Simple agents, low-code builders | Template parameters only | The same template output, generated from a spec |

### Example: LangGraph

```
import httpx
from fabric import Fabric
from fabric.langgraph import FabricStore      # implements LangGraph's BaseStore

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

fx = Fabric(agent="refunds-agent")   # reads identity and endpoints injected by Runtime
fx.instrument()                      # OpenTelemetry GenAI auto-instrumentation

# Model: a standard LangChain chat model pointed at the Model Gateway
llm = ChatOpenAI(
    model="default-reasoning",                          # gateway route name
    base_url=fx.endpoints.models,
    http_async_client=httpx.AsyncClient(auth=fx.auth),  # agent identity and user context
)

# Tools: a standard MCP client pointed at the MCP Gateway
mcp = MultiServerMCPClient({
    name: {"url": fx.endpoints.mcp(name), "transport": "streamable_http", "auth": fx.auth}
    for name in ("crm", "refunds")
})

async def main():
    tools = await mcp.get_tools()
    async with AsyncPostgresSaver.from_conn_string(fx.endpoints.checkpoints) as checkpointer:
        graph = build_graph(llm, tools).compile(   # the team's own LangGraph code
            checkpointer=checkpointer,             # standard saver on platform Postgres
            store=FabricStore(fx),                 # Fabric Memory behind BaseStore
        )
        await graph.ainvoke(
            {"messages": [("user", "Refund order 8841")]},
            config={"configurable": {"thread_id": fx.session_id}},
        )

# Approvals need no Fabric API. When Policy returns require_approval, the tool node
# calls LangGraph's interrupt(). Surfaces later resumes the run with
# Command(resume=...) on the same thread_id.
```

### Example: Google ADK

```
from fabric import Fabric
from fabric.adk import FabricSessionService, FabricMemoryService  # ADK base classes
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.adk.runners import Runner

fx = Fabric(agent="refunds-agent")
fx.instrument()

agent = LlmAgent(
    name="refunds_agent",
    model=LiteLlm(model="openai/default-reasoning", api_base=fx.endpoints.models,
                  extra_headers=fx.headers()),
    tools=[McpToolset(connection_params=StreamableHTTPConnectionParams(
        url=fx.endpoints.mcp("refunds"), headers=fx.headers()))],
)

runner = Runner(agent=agent, app_name="refunds",
                session_service=FabricSessionService(fx),   # Fabric Runtime sessions
                memory_service=FabricMemoryService(fx))     # Fabric Memory
```

### SDK surface

| Element | Description | Framework contract |
| --- | --- | --- |
| `fx.endpoints` | URLs and connection strings for the gateways, MCP servers and checkpoint database | Plain strings |
| `fx.auth` | Attaches the agent's token and the user's delegated context, and refreshes them | `httpx.Auth` |
| `fx.headers()` | The same credentials as headers, for frameworks that take headers | Dictionary |
| `FabricStore` | Fabric Memory for LangGraph | `BaseStore` |
| `FabricSessionService`, `FabricMemoryService` | Fabric Runtime sessions and Fabric Memory for ADK | ADK base classes |
| `fabric.patterns` | Versioned reasoning patterns | Compiled LangGraph graph |
| `fx.instrument()` | Registers OpenTelemetry GenAI instrumentors | OpenTelemetry |

### Anti-patterns

The following indicate that the SDK is becoming a competing framework rather than a platform client:

- A Fabric agent loop or runtime that does not compile to LangGraph or ADK
- A Fabric chat-model wrapper in place of the framework's model classes
- A Fabric tool decorator or tool-calling format
- A Fabric approval API that duplicates the framework's interrupt mechanism
- Prompt templating or chain composition that duplicates the framework's

## Reference request flow

The following steps show how services act on one request. A user in Microsoft Teams asks a refunds agent to issue a refund above the automatic approval threshold.

1. **Surfaces** receives the message with the user's single sign-on session. The **Agent API** resolves the agent in the **Catalog** and confirms it is approved for this channel.
2. The **Agent Runtime** starts or resumes a session, loads the last checkpoint and injects the agent's identity. The user's token is not exposed to agent code.
3. The agent requests customer context. **Context** retrieves it from **Memory**, **Retrieval** and **Knowledge**, filters it by the user's entitlements and fits it to a token budget.
4. The agent calls the model through the **Model Gateway**. **Guardrails** redacts PII and checks for prompt injection, **FinOps** checks the run and team budgets, and the gateway routes the call to an approved model.
5. The agent calls `refunds.issue` through the **MCP Gateway**. **Policy** evaluates the agent, user, tool and arguments, and returns `require_approval`.
6. The agent's graph interrupts. **Approvals** sends an approval card to the approver, and the **Agent Runtime** pauses the session durably without holding compute.
7. After approval, the run resumes. **Identity** exchanges the user's token for a scoped downstream token, the tool runs, and PII is reinserted in the response.
8. Each step emits a span to **Observability** and a record to **Audit**. A sample of the trace is sent to **Evaluation** for online scoring. If the approver edited the refund amount, the edit is recorded in **Feedback** for the agent owner to review.

## Architecture decisions

| Decision | Rationale |
| --- | --- |
| Guardrails and Policy are shared services called by every gateway | Model calls, tool calls and agent calls need the same checks. One service gives one rule set and one audit trail. |
| Separate MCP Gateway and Agent Gateway | Tool calls and agent-to-agent calls have different protocols, scaling profiles and risks (agent loops, call depth). Both call the same control plane. |
| Feedback is a platform service, not per-agent code | Feedback from every channel is tied to trace IDs and flows into the same evaluation datasets, so improvement is measurable across agents. |
| One catalog instead of separate agent, MCP, skill and tool registries | Separate registries drift apart and lose ownership data. Protocol-specific views are generated from the one catalog. |
| The Agent Runtime runs agents; the gateways route calls | Keeps gateways stateless and easy to scale. Sessions, isolation and checkpoints have one owner. |
| Context composes data and does not store it | Avoids a fourth copy of enterprise data and keeps entitlement filtering in one place. |
| Checkpoints and memory are separate | Run state and learned knowledge have different retention, privacy and access requirements. |
| Model registry and model gateway are separate | Approved models are catalog data with an approval workflow. Routing and cost are gateway behaviour. |
| Planners are libraries, not a hosted Planner API | Planning is tightly coupled to each agent's loop. No major platform offers planning as a central service. |
| Catalog records artifacts; factories build them | Keeps the system of record separate from build tooling, so new factories can be added without changing the Catalog. |
| All factories share one pipeline | Every Catalog entry arrives with the same evidence: provenance, tests, scans and signature. |
| Harness templates use Copier | Copier can update repositories already generated from a template, which limits drift. |

## Standards

| Standard | Use | Services |
| --- | --- | --- |
| Model Context Protocol (2025-11-25) | Tool and resource access. MCP servers are OAuth 2.1 resource servers; token passthrough is not allowed. | MCP Gateway, MCP Server Hosting, Catalog, Context |
| MCP Registry schema | Private subregistry of approved MCP servers | Catalog |
| Agent2Agent (A2A) v1.0 | Agent-to-agent calls and signed Agent Cards | Agent API, Agent Gateway |
| OpenTelemetry GenAI semantic conventions | Agent, model, tool and plan spans. Pin the convention version, as it is still in development. | Observability, SDK, gateways |
| Agent Skills (SKILL.md) | Packaged procedures and knowledge | Catalog, Planners |
| OAuth 2.0 on-behalf-of, RFC 8693, RFC 8707 | Delegated user access and scoped downstream tokens | Identity, MCP Gateway, Agent Gateway |
| SPIFFE, OIDC | Workload identity for each agent | Identity, Agent Runtime |
| Cedar, OPA | Authorization policy as code | Policy |

## Industry comparables

The following table maps AIFabric services to the closest equivalents in public platforms, for orientation. Several of these vendor features were in preview in 2026.

| AIFabric service | AWS Bedrock AgentCore | Google Gemini Enterprise Agent Platform | Microsoft Foundry |
| --- | --- | --- | --- |
| Agent Runtime | Runtime | Agent Runtime | Hosted agents |
| MCP Gateway | Gateway | Agent Gateway (MCP traffic) | Foundry tools, API Management MCP |
| Agent Gateway | — | Agent Gateway (A2A traffic) | Foundry connected agents |
| Identity | Identity | Agent Identity | Entra Agent ID |
| Policy | Policy (Cedar) | IAM policies at Agent Gateway | Entra and Azure Policy |
| Catalog | — | Agent Registry | Agent 365 registry |
| Memory | Memory | Memory Bank, Sessions | Agent memory |
| Sandbox | Code Interpreter, Browser | Agent Sandbox (GKE) | Session sandbox |
| Observability | Observability | Cloud Trace | Foundry tracing |
| Evaluation | Evaluations | Gen AI evaluation | Foundry evaluation |
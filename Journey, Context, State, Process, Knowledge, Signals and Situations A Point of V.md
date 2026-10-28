# Journey, Context, State, Process, Knowledge, Signals and Situations: A Point of View

Oct 28, 2026 · @Praveen · Draft for review

## Summary

Every enterprise AI journey reasons over the same seven concepts, and we should define them once. Three are modelled stores, each with one owner: **Knowledge** (what applies), **State** (what is true for the member, and since when) and **Process** (where the work is, and which clock is running). Two describe how truth moves: **Signals** bring facts in, and **Situations** announce the changes that matter.

**Context** is not a fourth store. It is a governed read contract that composes the others for one member, one purpose and one moment. The **Journey** is the anchor: the only object that touches all three stores.

The positions this document takes:

- The layer provides; journeys decide.
- The layer is derived and rebuildable. Source systems and journeys remain the systems of record.
- Ask yourself about your own work; ask the layer about everyone else's.
- Facts enter only as signals. Agents never write facts.
- Decision traces are first-class and stored once. Any graph of them is a projection, not a second store.
- Recommendations are not decisions, and precedent is not member truth.
- Time is regulated: clocks start when the organization receives a request, not when we ingest it.

## Why these terms need fixing now

We agree we need a common context layer built on signals and state. The risk now is vocabulary: familiar terms each answer a narrower question than the layer must, and a design built on the wrong one inherits its gaps.

| Term often used | What it actually answers | Why it is not the layer |
| --- | --- | --- |
| Knowledge graph / semantic layer | What applies, and how things relate | No member state, no time per member, no permissions |
| Member 360 / master data | Who this person is across systems | Identity, not what is true over time or what is in flight |
| Feature store | What a model needs to score | Precomputed features; signals come first, features are downstream |
| Context graph | Why something was decided | Becomes a second record of decisions if built as its own store |
| "Approved" (one status field) | The state of the entity | Hides the process: the notice and its clock may still be open |

The cost of leaving this vague: each journey builds its own integrations, answers differ by audience, and no one can reproduce what an agent saw when a decision is audited or appealed.

## The seven concepts at a glance

Each concept answers one question and has one owner. Only Journey and Process are systems of record inside our architecture; the rest are derived or computed.

| Concept | Definition | Question it answers | Time | Owner | System of record? |
| --- | --- | --- | --- | --- | --- |
| Journey | A member-scoped unit of goal-directed work, with an owner and an outcome | What are we trying to achieve for this member, and is it done? | Opened by a situation or request, closed by an outcome | Journey Intelligence Platform | Yes, for the work |
| Knowledge | Versioned, member-independent facts, rules and relationships | What applies, as of a given date? | Valid time: effective and end dates per version | Policy, benefits, clinical policy and quality owners | Policy library and benefits configuration are; the graph is a projection |
| Signal | A typed, scoped, timestamped fact from a named source | What just happened, where did it come from, and when? | Occurred, received by the organization, recorded by us | SignalHub | No; the source system is |
| State | The reconciled record of what is true about a member (and related provider and place scopes) | What is true now, or as of a moment, since when, and how did we learn it? | Bitemporal: when it was true, and when we learned it | StateHub | No; derived and rebuildable |
| Situation | A change in state that matters to work, detected by a versioned rule | What changed that someone may need to act on? | Detected at; active, resolved or obsolete | StateHub (rules governed like knowledge) | No; derived |
| Process | How work moves: the model, the live instance and the event log | Where is the work, who owns it, what is next, and which clock is running? | Clocks, timers, milestones | Journeys | Yes, for the work |
| Context | A permitted, purpose-shaped, point-in-time composition of the above | What does this consumer need now, and may it see it? | Pinned by a context token | Context Hub | No; computed, never stored |

**The boundary test for any data item.** If it is true whichever member you ask about, it is Knowledge. If it is true about a member whether or not any work is happening, it is State. If it exists only because someone is doing work, it is Process. If it exists only because a consumer asked a question, it is Context.

## Journey: the anchor

The journey is the unit of value and the only object that touches all three stores. It pins Knowledge, reads State through context, and owns Process.

**What it is.** A member-scoped unit of goal-directed work, with an owner, a goal and an outcome. Kinds include a prior authorization request, an inpatient stay under review, a care program episode, a member conversation and a care gap. A journey may also be scoped to a case and a provider.

**How it relates to each store.**

- **Knowledge:** pins the versions in force for its work (policy, criteria, measure specification, clock rule), usually as of when the request was received.
- **State:** reads it through the Context Hub and changes it only by emitting signals, never by writing facts.
- **Process:** owns it outright: tasks, waits, timers, milestones, case decisions and outcomes.

**Lifecycle.** A situation or a request opens a journey; an outcome closes it. While open, it publishes a small set of work signals so other journeys can see what is in flight.

**Member-rooted.** The member is the primary key. Cases, journeys, providers and places are scopes on that member, so every journey sees the same person.

**What the journey owns, and what it does not.**

- Owns: decisions (its system is their system of record), recommendations in its audit trail, and relevance: it ranks, times, words and acts.
- Does not own: facts about the member, or other journeys' work.

## Knowledge: what applies, versioned

Knowledge is member-independent and versioned. It answers "what applies, as of this date?" and is served by `what_applies`, which returns no member data.

**What it holds.**

- Plans, products, benefits and cost-share structures
- Prior authorization rules and the services they govern
- Coverage criteria: national and local coverage determinations, licensed criteria, internal policy
- Code systems for services, diagnoses, labs and drugs
- Quality measure specifications and value sets
- Network rules
- Clock rules: which regulatory timeframe applies, by line of business, urgency and service type

**Properties every item needs.**

- **Valid-time versions:** effective and end dates, and what each version supersedes.
- **Provenance:** the source and the approval behind it, such as a utilization management committee review.
- **Pinning:** every context token and every decision trace records the versions it used, so an auditor can ask which rule applied on a given date.
- **Executable where possible:** rules and criteria held as computable artifacts (FHIR resources, CQL, decision tables) rather than documents only.

**System of record.** The policy library, benefits configuration and licensed criteria. The semantic layer or knowledge graph is a projection over them for retrieval and traversal.

**Boundary.** A knowledge graph is one input to context, not the context layer. It has no member state, no member timeline and no purpose-based permissions.

## Signals: typed facts arriving from sources

A signal is the only way a fact enters the layer. It is typed, scoped and timestamped, and it names its source. Corrections arrive as new signals; nothing is overwritten.

**The envelope.**

| Field | What it carries |
| --- | --- |
| Type | A registered signal type, with its lifecycle: active, updated, cancelled, expired |
| Scope | Member, and optionally case, provider or place |
| Source | The named system or person that produced it |
| Occurred at | When it happened in the world |
| Received at | When the organization received it; regulatory clocks start here |
| Recorded at | When we ingested it |
| Identity | Stable signal id plus revision, so retries are idempotent |
| Sensitivity | Category tags, such as substance-use or behavioral health, carried to anything derived from it |

**Four families.**

- **Events:** something happened, such as an admission, a claim, a lab result or a discharge.
- **Decisions:** a committed decision with its trace (below).
- **Work signals:** what journeys publish about their work: opened, owner, status, due time and clock, pended, decided, notified, commitment made, closed.
- **Place signals:** facility alerts and outages, with no member data.

**The decision trace.** A decision signal carries the outcome and why: the reason (a specific denial reason when adverse), criteria met and not met, evidence cited, policy and criteria versions, an exception or override flag with its approver, who decided, whether AI assisted, a reference to the recommendation and its disposition (accepted, modified, rejected), and when it was received, decided and notified.

**Rules.** Signals are processed in order per member. Only the validation path turns signals into state. Agents never emit facts. Later, the same signals feed the feature store.

## State: what is true for the member, since when

State is the reconciled, bitemporal record of what is true about a member. It is derived from sources and rebuildable from the change log plus baselines, so it is never the system of record.

**How it is built.** A baseline from the member data system (each refresh kept with its version and cutoff), plus validated signals, written to an append-only change log. The current state is a projection over that log. Validation asks whether a signal is already known, newer or older, a correction, plausible for this member, and, for decisions, allowed and not in conflict. Implausible or conflicting signals go to a review queue for people. A new baseline retires, carries forward or flags items; it never overwrites silently.

**Every item carries:**

- Its value and its source
- When it was true (valid time) and when we learned it (record time)
- Its kind: observed, reported, extracted, derived or estimated, with the model or rule version for anything derived
- Freshness, so stale items are visible as stale
- The sensitivity it inherits from its inputs

**Gaps are values.** "No qualifying record received" is stated, never "not done". Outstanding and stale are values too.

**Scopes.** The member is the primary scope. Provider-scoped state (such as gold-card exemptions and network status) and place-scoped state (such as facility alerts) are first-class partitions in the same log, because they change what applies to a member.

**What is in State and what is not.**

- In: member facts, decision traces (what was decided and why), and a coarse, read-only projection of work in flight across journeys.
- Not in: recommendations, cross-member precedent and agent memory.

**Served by** `what_is_true_now`, `what_was_decided` and `what_changed(since)`, plus as-of replay of any past moment.

**Not master data.** Member 360 and master data answer who the member is. State answers what is true about them over time.

## Situations: changes that matter

A situation is a change in state that matters to work. A versioned rule detects it, and the layer publishes it once to every journey that subscribes. Situations are how the layer is aware, not just queryable: context is pull, awareness is push.

**What a situation carries.** The rule and rule version that detected it, the state items that triggered it, the member and scope, and its lifecycle: active, resolved or obsolete.

**Typical kinds.** A decision reached; a clock at risk; a gap opened or closed; a trajectory turned; an admission or discharge; a coverage change; a commitment coming due.

**What a situation does.**

- Starts journey work ("admission needs review") and closes it when resolved ("discharged").
- Reaches every subscribed journey in the same form, so programs act on the same facts.
- Says what changed and why it matters. It does not prescribe an action; consumers decide whether and how to act.

**Governance.** Situation rules are policy in disguise. Without owners, versions and tests, they become an untested shadow policy engine. They are governed like Knowledge, and every rule change is tested with as-of replay before release.

## Process: where the work is and which clock is running

Process is how work moves: who owns it, what is allowed next, what is waiting, and which clock is running. Journeys own it and are its system of record. The layer only reads a coarse projection of it.

**Three layers of process.**

- **Model:** the allowed steps and transitions. Review and appeals work is case-shaped (event-driven, knowledge workers in control); intake, notices and outreach are flow-shaped; criteria and clock selection are decision tables.
- **Instance:** this piece of work, now.
- **Event log:** what actually happened, step by step.

**Entity state is not process state.** An authorization can be approved while the notice task and its clock are still open. Keep them as separate fields, and never answer "approved" without the open work beside it.

**A decision is several steps.** Determination, notification and effectuation, with pend, request-for-information and extension events between them. Each carries its own clock and failure consequence. In Medicare Advantage, for example, a standard decision on a prior-authorized item is due no later than 7 calendar days after receiving the request, and a missed notice is itself an adverse determination ([42 CFR 422.568](https://www.law.cornell.edu/cfr/text/42/422.568)).

**Regulatory clocks span all three stores.** The rule comes from Knowledge, the start time from State (received at), and the life of the clock from Process.

**People decide where it counts.** Agents assist: they summarize, map evidence to criteria and draft. An accountable clinician makes any adverse determination. Agent proposals are recorded as recommendations in the journey's audit trail, with their disposition, and linked to the decision by reference.

**What the layer sees.** Journeys publish coarse work signals, and the layer keeps a read-only projection for cross-journey visibility. The rule: ask yourself about your own work; ask the layer about everyone else's. The projection must stay summary-level, or it becomes a second workflow engine.

**Mineable by design.** If each work signal links to every object it touches (member, case, authorization, provider, notice), the event log supports object-centric process mining for timeliness and rework analysis without a separate pipeline.

## Context: the governed read contract

Context is a contract, not a store. It is a permitted, purpose-shaped, point-in-time composition of Knowledge, State, work in flight and situations, assembled for one member, one purpose and one moment, then discarded.

**The request.** The consumer brings who is asking (the agent's identity and the delegated user), the purpose, the relationship to the member and the question. The hub uses these to decide what is permitted and what answers the question. The live details of a conversation stay with the consumer.

**The typed questions.**

| Question | Composes | Member data? |
| --- | --- | --- |
| `what_applies` | Knowledge, resolved to a plan and date | No |
| `what_is_true_now` | State, plus work in flight across journeys | Yes |
| `what_was_decided` | Decision traces | Yes |
| `what_changed(since)` | Changes and situations since a moment | Yes |
| `what_changed_in_place` | Place-scoped state, such as facility alerts | No |

**Every answer carries** its sources with both timestamps, each item's kind, its freshness, gaps stated as values, and a summary first with evidence on request, sized to a budget.

**The context token** pins the as-of moment and the knowledge versions in effect. Parallel agents and retries see the same case, and any answer can be replayed. It is not a credential.

**Access.** Role, plus purpose, plus relationship to the member, under minimum necessary. Sensitive categories are segmented, and derived items inherit the restrictions of their inputs. Every call goes through the gateway, identified, authorized and traced.

**Where the line sits.** The hub selects the permitted facts that answer the typed question. The journey decides what matters: it ranks, times, words and acts. The hub never recommends an action.

**On "context graph".** We do not build it as a component. The decisions, policies, exceptions and evidence it describes already live in the change log; a decision-trace view over that log can be projected when a consumer needs to traverse it.

## Relationship spine

&#91;embedded content: relationship spine · 3 stores, 1 contract, 1 feedback loop\]

Facts arrive as signals and become state. Context composes knowledge and state for the journey, and situations open and close its work. The journey owns its process and sends decisions and work back as signals, which is how other journeys learn what is in flight.

The same spine as relationships:

```text
Member ─has→ Coverage ─in→ Plan ─offers→ Benefit ─subject to→ Rule (version) ─references→ Criteria (version)
Source ─emits→ Signal ─validated into→ State item ─about→ Member (+ case, provider, place)
State change ─detected by→ Situation (rule version) ─opens or closes→ Journey instance
Journey instance ─scoped to→ Member ─owns→ Tasks ─guarded by→ Clock (rule from Knowledge, start from State)
Agent ─reads→ Context (token: as-of moment + versions) ─composed from→ Knowledge + State + Situations
Agent ─proposes→ Recommendation ─reviewed by→ Person ─commits→ Decision ─emitted as→ Decision signal → State
```

## Boundaries and principles

Ten rules keep the layer from becoming a second system of record or a hidden decision engine.

1. **Member-rooted.** The member is the key; case, journey, provider and place are scopes.
2. **Derived, never the record.** Sources and journeys remain systems of record; the layer can be rebuilt from them.
3. **The layer provides; journeys decide.**
4. **Own work from yourself, others' work from the layer.** A journey never reads its own work back through the layer, which trails it.
5. **Facts enter only as signals.** Agents never write facts.
6. **Decision traces are stored once,** in the change log. Any graph of them is a projection.
7. **Recommendations are not decisions.** They live in the journey's audit trail, linked to the decision by reference.
8. **Precedent is not member truth.** It is governed separately and is never the sole basis for an adverse decision.
9. **Every answer is attributed, timestamped, labelled by kind and honest about gaps.**
10. **Access is role, purpose and relationship.** Restrictions travel with derived data, and clocks start at organizational receipt.

**Anti-patterns to name and refuse.**

| Anti-pattern | Why it fails | Guardrail |
| --- | --- | --- |
| A second store for decisions | Two records of a decision diverge; audit cannot say which is authoritative | A graph is a projection over the log |
| Agents writing facts | Extraction errors become member truth with no accountable author | Agents write recommendations; only validation writes state |
| Precedent leaking into member truth | Breaks individualized determinations and invites bias | Separate governed store, never an input to adverse decisions alone |
| Stale context | Accumulators, authorizations and coverage change during the day | Freshness on every item; tokens expire |
| Entity and process state in one field | "Approved" hides the open notice and its clock | Separate entity status and open work |
| Relevance centralized in the layer | The layer becomes a hidden decision engine | Typed questions return permitted facts; journeys choose |
| A knowledge graph as the context layer | No member state, no time, no permissions | Knowledge is one input to Context |
| Clocks from ingestion time | Timeliness is systematically misreported | Received at is required on every request signal |
| The work projection grows into a workflow engine | Two process stores drift | Coarse, read-only work signals only |

## Open questions

These are unresolved and should be settled during the source assessment, before the build.

- [ ] Who owns the clock rule table across lines of business: compliance, utilization management operations or the platform team?
- [ ] What shared status vocabulary maps Phoenix and Vector to one process model?
- [ ] What minimum set of work signals must each journey publish, and how stale may they be for each consumer?
- [ ] Do decision signals from the UM systems carry their reasons today, or only outcomes?
- [ ] Can fax and portal adapters capture organizational receipt time reliably?
- [ ] Does a consent or segmentation service exist today? If not, who owns sensitive-category tagging?
- [ ] Which journeys run outside the Journey Intelligence Platform, such as vendor programs and campaigns?
- [ ] Who owns situation rules, and how are they tested before release?
- [ ] Should agents ever use cross-member precedent, and under what governance?
- [ ] Is feeding the feature store part of the first release, or a later direction?

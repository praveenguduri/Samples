# AI Platform FinOps — TL;DR

> Token spend is a platform concern, not an agent concern. Enforcement lives at the proxy — no agent can bypass it.

---

## The Model

Every agent type gets a **virtual key** in LiteLLM. The key carries identity, model scope, and spend limits. Real provider API keys never leave the proxy.

```
Agent Pod  →  LiteLLM Proxy (virtual key)  →  Vertex AI / Anthropic / OpenAI
                     │
              enforces TPM · RPM · USD cap
              emits cost OTel spans
```

---

## Virtual Key Config

```yaml
- key_alias: "data-quality-agent"
  models: ["gpt-4o"]       # agent cannot call any other model
  tpm_limit: 50000          # tokens per minute
  rpm_limit: 100            # requests per minute
  max_budget: 10.0          # USD hard cap
  budget_duration: "1d"     # resets daily
  metadata:
    agent_type: "data-quality-agent"
    team: "data-platform"
```

An agent that hits its budget gets a rate-limit response. It cannot proceed. No code path around it.

---

## What You Get Per Agent

| Control | Mechanism |
|---|---|
| Model scope | Key only permits listed models — no unapproved calls |
| Token rate limit | TPM + RPM enforced at proxy, not in agent code |
| Spend cap | USD budget with configurable reset window |
| Cost attribution | Every token charge tagged with `agent_type` + `team` in OTel |
| Runaway loop protection | TPM limit bounds worst-case cost of an infinite loop |

---

## Observability

LiteLLM emits OTel spans on every request:

```
litellm.request
  agent_type:        "data-quality-agent"
  team:              "data-platform"
  model_requested:   "gpt-4o"
  model_actual:      "vertex_ai/gemini-1.5-pro"
  tokens_input:      1240
  tokens_output:     380
  cost_usd:          0.0021
  budget_remaining:  7.43
  trace_id:          "abc-123"
```

These land in **BigQuery** via Cloud Logging. Standard views:

- Daily spend by `agent_type` and `team`
- Token efficiency ratio (output / input tokens) per agent — a proxy for prompt quality
- Budget burn rate — projects overage before it hits the cap
- Model substitution savings — what routing to Vertex vs. OpenAI is saving

Grafana dashboard pulls from BigQuery. No custom instrumentation required in agent code.

---

## Suggested Limits by Agent Pattern

| Agent Pattern | TPM | RPM | Daily Cap |
|---|---|---|---|
| Batch / data quality | 50k | 100 | $10 |
| Interactive / user-facing | 20k | 200 | $5 |
| Research / external fetch | 100k | 50 | $25 |
| Tool execution | 30k | 150 | $15 |

Start conservative. Raise limits based on observed spend in BigQuery, not guesses.

---

## Cost Levers

**Model routing** — the biggest lever. Agent code says `model="gpt-4o"`, LiteLLM routes to Gemini on Vertex. Cost difference is 5–10x on equivalent tasks. Swap in config, zero agent code changes.

**Semantic caching** — LiteLLM caches responses by prompt similarity (Redis-backed). Repeated or near-identical prompts return cached responses. Effective for batch agents running similar tasks across many records.

**Context trimming** — long context is the primary cost driver. Enforce max context windows per agent type via LiteLLM's `max_input_tokens` per key. Agents that blow past limits get a clear error, not a silent large bill.

---

## What FinOps Does Not Require

- No instrumentation inside agent code
- No per-team billing dashboards to maintain
- No manual cost allocation — `team` metadata on the virtual key handles it
- No separate FinOps tooling — BigQuery + Grafana + existing OTel pipeline

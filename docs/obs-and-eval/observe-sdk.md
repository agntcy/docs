# Observability SDK

## AGNTCY Observability Data Schema

We provide the AGNTCY Observability Data Schema, an extension of OpenTelemetry (OTel) and aligned with LLM semantic conventions for generative AI systems. The schema is designed to deliver comprehensive observability for multi‑agent systems (MAS), enabling detailed monitoring, analysis, and evaluation of performance and behavior.

Its goal is to standardize telemetry across diverse agent frameworks, enriching core OTel structures with MAS‑specific concepts such as agent collaboration success rate, MAS response time, and task delegation accuracy.

For more information, see the [schema directory in the observe repository](https://github.com/agntcy/observe/tree/main/schema).

## Observe SDK

We provide a framework‑agnostic, OTel‑compliant observability SDK for multi‑agent systems. Each agent in the MAS can be instrumented by applying lightweight decorators to key functions or by using native OpenTelemetry primitives directly. The SDK exports metrics and traces using the [OpenTelemetry (OTel)](https://opentelemetry.io/) standard.

OTel is central to effective MAS observability as it provides:

- **Unified telemetry collection:** A single, vendor‑neutral API/SDK for metrics, traces, and (optionally) logs across heterogeneous agent components.
- **Consistent instrumentation & standardization:** Semantic conventions and stable APIs ensure uniform telemetry shape, enabling backend flexibility without re‑instrumentation.
- **Distributed tracing for complex workflows:** OTel’s tracing links agent spans, LLM calls, and tool interactions into an end‑to‑end execution graph—critical for understanding non‑deterministic decision paths and debugging across agent boundaries.

### Agentic Protocol Instrumentation

The Observe SDK also instruments major agent communication and coordination protocols. Currently supported: Agent‑to‑Agent (A2A), Secure Low‑latency Messaging (SLIM), and the Model Context Protocol (MCP). This yields traceability for agent‑to‑agent and agent‑to‑tool interactions within a MAS.

### End‑to‑End Trace Recomposition

A core MAS challenge is decentralization: independent autonomous agents, when instrumented in isolation, produce fragmented trace trees (one per agent). To avoid stitching telemetry manually, we leverage OTel context propagation to carry identifiers (e.g., session, user, workflow) across boundaries. This preserves causal linkage and yields a coherent, recomposed execution trace spanning all participating agents.

## Translator

In heterogeneous environments, different OTel‑compliant SDKs may emit telemetry following divergent schemas (there is no universal MAS schema standard yet). A translator layer can normalize these differences—mapping attributes, renaming fields, or redacting sensitive keys. The OpenTelemetry Collector supports this via configurable [processors](https://opentelemetry.io/docs/collector/transforming-telemetry/) that transform telemetry in transit (e.g., attribute rename, drop, redaction), enabling schema convergence without rewriting upstream code.

## Links

To get started with the Observe SDK, visit the [repository](https://github.com/agntcy/observe/).

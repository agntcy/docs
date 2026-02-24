# Evaluation

The Observe SDK emits raw telemetry (traces, metrics, and optional logs) to an OpenTelemetry (OTel) Collector. The collector exports that telemetry to a storage backend where it becomes a durable, queryable substrate. On top of this substrate we layer **evaluation**: deriving higher‑order insights (quality, efficiency, reliability, safety) from factual execution data. Two core building blocks enable this: the **API Layer** and the **Metrics Computation Engine (MCE)**.

## API Layer

The API Layer abstracts the underlying database so that we are not locked into a single storage technology. While ClickHouse is the initial implementation, the interface is intentionally narrow (session lookup, span search, metric fetch, write‑back of computed artifacts) to keep alternative backends (e.g., PostgreSQL, BigQuery, Elastic, Parquet lake) easily pluggable.

Capabilities:

- Retrieve raw session traces (for replay, graph reconstruction, diffing).
- Fetch primary metrics emitted directly by the SDK (e.g., latency histograms, token usage counters).
- Provide bounded, pagination‑friendly queries for the MCE (avoids heavy ad‑hoc joins inside the engine).
- Enforce schema normalization/translation so upstream differences (SDK versions, framework variants) do not leak into evaluator logic.

Design goals:

- **Decoupling:** Evaluation logic never embeds vendor‑specific SQL.
- **Portability:** Swap storage by implementing a small provider contract.
- **Consistency:** Uniform response envelopes (metadata + data + pagination cursor).

## Metrics Computation Engine (MCE)

The Metrics Computation Engine computes **derived** metrics at multiple aggregation levels:

- **Span level:** e.g., answer relevance for a single LLM call or tool invocation success rate.
- **Session level:** overall MAS completion status, agent collaboration success rate, delegation accuracy.
- **Population level:** metrics computed over a set of sessions, like graph determinism score.

The MCE uses a plugin architecture, making it straightforward to add new metrics.  
It was designed to be running either as a stand-alone service, exposed through a REST API; or as an embeddable SDK, integrated into a third-party data or analytics platform.

The metrics computed by the MCE can either be stored back into the database via the API Layer for longitudinal analysis, and/or returned directly to the caller for immediate consumpltion.

## Detailed Usage

For detailed usage and examples, see the [telemetry-hub repository](https://github.com/agntcy/telemetry-hub).

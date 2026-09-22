# Switching Friction & Lock-in Taxonomy

This document formalizes the mechanical vectors through which incumbents create artificial switching friction, and the architectural levers required to neutralize them.

## 1. Incumbent Lock-in Classification

Incumbent vendors sustain retention through four structural categories of friction. Every migration battlecard must identify which categories apply to the target incumbent:

### Class A: Data Egress & Storage Inertia
- **Proprietary Encoding:** Data exported in non-standard JSON blobs or obfuscated relational models requiring extensive rehydration.
- **Rate-Limited Egress:** Bulk export endpoints throttled (e.g. 5 requests/sec or strict daily export quotas).
- **Egress Bandwidth Tolls:** High marginal costs charged for moving data out of cloud storage or proprietary clusters.
- **Historical Pruning:** Incumbent imposes data loss penalties or forces deletion upon cancellation.

### Class B: SDK & API Coupling (Blast Radius)
- **High Ingestion Coupling:** Proprietary client-side SDKs embedded across dozens of microservices, web apps, or mobile clients.
- **Proprietary Query Language:** User queries, dashboards, and alerting rules locked in vendor-specific syntax (e.g. proprietary DSLs instead of standard SQL).
- **Webhook & Pipeline Inflexibility:** Inability to multiplex webhook streams or forward raw events to multiple destinations simultaneously.

### Class C: Workflow & Cognitive Friction
- **Team Retraining Overhead:** Custom analyst workflows and dashboard configurations built up over years.
- **Permission & Governance Entrenchment:** Complex RBAC models, audit logs, and directory synchronizations that enterprise IT resists recreating.
- **Organizational Inertia:** "Nobody gets fired for buying the incumbent." Risk aversion from middle management.

### Class D: Commercial & Economic Penalties
- **Seat-Tax Multiplication:** Charging per viewer or collaborator rather than for compute/usage.
- **Overage Tier Cliffs:** Steep multiplier rates (2x-5x) applied as soon as a tier ceiling is crossed by a single percent.
- **Multi-Year Minimum Commitments:** True-up clauses and renewal traps that penalize downsizing.

---

## 2. Migration Complexity Tiers

| Tier | Characteristics | Typical Cutover Window | Recommended Runbook Pattern |
| :--- | :--- | :--- | :--- |
| **Low** | Stateless API replacement, simple SDK swap, no historical state required | 1-3 days | Direct drop-in replacement with feature flag |
| **Medium** | Event streaming, client SDK migration, historical window backfill (30-90 days) | 1-2 weeks | Dual-write shadow ingestion with delta reconciliation |
| **High** | Stateful datastore, terabyte/petabyte scale, multi-region compliance, complex RBAC | 2-6 weeks | Phased shadow ingestion, snapshot bulk loading, continuous replication |

---

## 3. The 4-Stage Zero-Downtime Migration Model

Every production cutover must follow this sequence to guarantee zero data loss and eliminate downtime risk:

1. **Stage 1 (Shadow Dual-Write):** Route new writes or events to both the incumbent and the target system simultaneously. The target operates in shadow mode; production reads remain on the incumbent.
2. **Stage 2 (Historical Backfill & Translation):** Extract historical datasets using bounded parallel chunking. Execute schema transformations to normalize fields into target standards.
3. **Stage 3 (Delta Reconciliation & Parity Verification):** Compare query results, record counts, and latency percentiles across both systems. Resolve any discrepancies in transformation rules.
4. **Stage 4 (Atomic Traffic Cutover & Graceful Sunset):** Switch production read traffic to the target system via DNS, CDN, or feature flag. Keep the incumbent in passive sync for a 7-day observation buffer before account termination.

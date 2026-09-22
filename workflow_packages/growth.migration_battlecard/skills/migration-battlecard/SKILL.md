---
name: migration-battlecard
description: Build an evidence-based migration runbook, honest parity matrix, and switcher battlecard to displace an incumbent competitor.
---

# Migration Battlecard Procedure

Create an engineering-grade competitor teardown, honest architectural parity matrix, and zero-downtime cutover runbook for displacing an incumbent competitor.

This workflow is designed like an industrial engineering process: transforming unstructured product documentation and competitive friction into a rigorous, verifiable switcher asset. It produces `reports/MIGRATION_BATTLECARD.md`.

## Inputs & Context Processing

1. **Read Project Evidence:**
   - Inspect the local workspace repository: `README.md`, package manifests, documentation, and core architecture files to understand the project's actual features, performance boundaries, and pricing model.
   - Ground all claims in verified repository evidence. Never invent capabilities that do not exist in the code or documentation.

2. **Ingest Supplied Parameters:**
   - `competitor_name`: Name of the incumbent product to displace (e.g. "Mixpanel", "Segment", "SendGrid").
   - `competitor_domain`: Incumbent web domain (e.g. "mixpanel.com").
   - `target_persona`: The target technical buyer (default: "Technical decision makers, engineering leads, and founders").
   - `core_differentiators`: Explicitly highlighted technical, architectural, or commercial advantages.
   - `known_limitations`: Documented areas where the incumbent is still superior (mandatory for technical credibility).
   - `migration_complexity`: Expected difficulty level (`low`, `medium`, `high`).

---

## Analytical Methodology

Follow the structural rules defined in `TAXONOMY.md` and the quality rubrics in `RUBRIC.md`:

### Section 1: Executive Summary & Switching Thesis
- Define the single core reason engineering teams migrate away from the incumbent (e.g. unpredicted billing spikes at scale, lack of raw SQL access, closed-source vendor lock-in).
- State the quantified payoff: typical percentage reduction in annual SaaS spend and migration timeline.

### Section 2: Incumbent Lock-in & Friction Analysis
- Classify the incumbent's friction vectors using the four classes from `TAXONOMY.md`:
  - Class A (Data Egress & Storage Inertia)
  - Class B (API & SDK Blast Radius)
  - Class C (Workflow & Cognitive Retraining Costs)
  - Class D (Commercial & Contractual Penalties)
- Explain exactly how our product neutralizes each active friction vector.

### Section 3: Honest Architectural Parity Matrix
- Construct a detailed Markdown table evaluating five core dimensions:
  1. Core Engine & Hosting Architecture
  2. Data Ingestion & Storage Ownership
  3. Feature Parity & Extensibility
  4. Developer Experience (APIs, SDKs, Local Dev)
  5. Pricing Model & Scaled Unit Economics
- **The Radical Honesty Mandate:** Under the table, include a dedicated callout block:
  `> [!NOTE] Where [Competitor] Still Holds an Advantage`
  Detail at least two areas where the incumbent has a legitimate edge (e.g. older legacy integrations, specific enterprise compliance frameworks, polished non-technical UI builders). Radical honesty establishes instant credibility with technical buyers.

### Section 4: 4-Stage Zero-Downtime Migration Runbook
- Provide step-by-step instructions for safely executing the migration without service interruption:
  - **Stage 1: Shadow Dual-Write Ingestion:** Code snippet (e.g. middleware, reverse proxy, or dual-client setup) showing simultaneous emission to both endpoints.
  - **Stage 2: Historical Backfill & Translation:** Script or CLI instructions for exporting data from the incumbent's API and transforming schema into our native format.
  - **Stage 3: Delta Reconciliation & Verification:** Query or verification procedure to validate record parity and property alignment.
  - **Stage 4: Atomic Cutover & Graceful Deprecation:** Switching production reads and maintaining a 7-day observation buffer before terminating the incumbent account.

### Section 5: Switching Payback & TCO Economic Model
- Present a concrete financial model based on the calculations in `RUBRIC.md`:
  - Migration Engineering Investment (hours × standard blended engineering rate of $120/hr).
  - Monthly SaaS Spend Comparison (Incumbent vs Target at 1x, 5x, and 10x volume scale).
  - Breakeven Payback Period (in months).
  - 3-Year Cumulative Net Savings.

### Section 6: Technical Objection Counter-Playbook
- Provide direct, engineering-grounded answers to the top three buyer objections:
  1. *"What if our engineering team doesn't have bandwidth to migrate right now?"*
  2. *"How do we guarantee we won't lose historical events or customer state?"*
  3. *"What happens if we need to roll back during the transition?"*

---

## Output Contract

Write the completed document exclusively to `reports/MIGRATION_BATTLECARD.md`. Do not write to any other file path. Do not include unsubstantiated marketing hyperbole.

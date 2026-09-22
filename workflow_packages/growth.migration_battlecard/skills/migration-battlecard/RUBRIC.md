# Migration Battlecard Quality & Economic Rubric

This document defines the strict engineering rubrics, verification rules, and financial models for constructing an unassailable competitor battlecard.

## 1. Editorial & Technical Tone Standards

- **The Anti-Hyperbole Gate:** Under no circumstances may the battlecard use subjective marketing superlatives ("revolutionary", "game-changing", "world-class", "effortless", "blazing fast"). Every performance or speed claim must be stated in concrete units (e.g. "p99 latency < 15ms under 10k rps", "queries execute over raw ClickHouse columnar storage").
- **The Radical Honesty Mandate:** Technical decision-makers (staff engineers, VP Eng, CTOs) immediately distrust one-sided marketing collateral. The battlecard **MUST** explicitly state at least two areas where the incumbent vendor holds structural superiority (e.g. "Incumbent maintains 600+ turnkey SaaS connectors", "Incumbent holds FedRAMP High certification").
- **Verifiable Migration Steps:** Never state "migration is simple". Provide explicit code snippets, curl commands, or configuration stanzas detailing how dual-writing is configured.

---

## 2. Quantitative Verification Engine

The following Python model computes exact switching payoff timelines and multi-year Total Cost of Ownership (TCO). It must be used to calculate figures presented in the report.

```python
"""Quantitative economic calculations for competitor displacement and migration."""

from typing import Any


def calculate_migration_payback(
    *,
    migration_hours: float,
    blended_hourly_rate: float,
    incumbent_monthly_cost: float,
    target_monthly_cost: float,
) -> dict[str, Any]:
    """Calculate migration investment, monthly savings, and payback period in months.

    Raises ValueError on negative or invalid non-numeric inputs.
    """
    for name, val in [
        ("migration_hours", migration_hours),
        ("blended_hourly_rate", blended_hourly_rate),
        ("incumbent_monthly_cost", incumbent_monthly_cost),
        ("target_monthly_cost", target_monthly_cost),
    ]:
        if not isinstance(val, (int, float)) or isinstance(val, bool) or val < 0:
            raise ValueError(f"{name} must be a non-negative real number")

    investment = float(migration_hours * blended_hourly_rate)
    monthly_savings = float(incumbent_monthly_cost - target_monthly_cost)

    if monthly_savings <= 0:
        return {
            "migration_investment_usd": round(investment, 2),
            "monthly_savings_usd": round(monthly_savings, 2),
            "payback_months": None,
            "annual_net_savings_usd": round(monthly_savings * 12 - investment, 2),
            "viable": False,
            "status": "cost_negative_or_neutral",
        }

    payback_months = investment / monthly_savings
    annual_net_savings = (monthly_savings * 12) - investment
    annual_roi_pct = (annual_net_savings / investment) * 100 if investment > 0 else 0.0

    return {
        "migration_investment_usd": round(investment, 2),
        "monthly_savings_usd": round(monthly_savings, 2),
        "payback_months": round(payback_months, 1),
        "annual_net_savings_usd": round(annual_net_savings, 2),
        "annual_roi_percent": round(annual_roi_pct, 1),
        "viable": payback_months <= 12.0,
        "status": "viable" if payback_months <= 6.0 else "extended_payback",
    }


def calculate_tco_trajectory(
    *,
    incumbent_base_monthly: float,
    target_base_monthly: float,
    annual_volume_multiplier: float = 1.5,
    years: int = 3,
) -> list[dict[str, Any]]:
    """Model multi-year spend under volume growth across incumbent and target."""
    if years < 1 or years > 10:
        raise ValueError("years must be between 1 and 10")
    if annual_volume_multiplier < 1.0:
        raise ValueError("annual_volume_multiplier must be >= 1.0")

    trajectory = []
    current_incumbent = incumbent_base_monthly * 12
    current_target = target_base_monthly * 12

    for year in range(1, years + 1):
        delta = current_incumbent - current_target
        trajectory.append(
            {
                "year": year,
                "incumbent_annual_spend": round(current_incumbent, 2),
                "target_annual_spend": round(current_target, 2),
                "annual_savings": round(delta, 2),
            }
        )
        current_incumbent *= annual_volume_multiplier
        current_target *= 1.0 + (annual_volume_multiplier - 1.0) * 0.4

    return trajectory


def score_migration_feasibility(
    *,
    lock_in_classes: list[str],
    complexity_tier: str,
) -> dict[str, Any]:
    """Score feasibility and friction index on a 0-100 scale."""
    valid_classes = {"Class A", "Class B", "Class C", "Class D"}
    valid_tiers = {"low", "medium", "high"}

    if not set(lock_in_classes).issubset(valid_classes):
        raise ValueError("invalid lock-in classes supplied")
    if complexity_tier not in valid_tiers:
        raise ValueError("invalid complexity tier")

    tier_weights = {"low": 10, "medium": 30, "high": 55}
    base_score = 100 - tier_weights[complexity_tier] - (len(lock_in_classes) * 10)
    feasibility_score = max(10, min(100, base_score))

    return {
        "feasibility_score": feasibility_score,
        "risk_level": "low" if feasibility_score >= 70 else ("moderate" if feasibility_score >= 40 else "elevated"),
        "recommended_buffer_days": 3 if complexity_tier == "low" else (7 if complexity_tier == "medium" else 21),
    }
```

---

## 3. Required Report Sections

Every generated `reports/MIGRATION_BATTLECARD.md` must contain these exact Markdown headers:

1. `# [Target Product] vs [Competitor Name]: Technical Migration & Switcher Guide`
2. `## Executive Summary & Switching Thesis`
3. `## Incumbent Lock-in & Friction Analysis`
4. `## Honest Architectural Parity Matrix`
5. `## 4-Stage Zero-Downtime Migration Runbook`
6. `## Switching Payback & TCO Economic Model`
7. `## Technical Objection Counter-Playbook`

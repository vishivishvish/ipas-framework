"""Configurable business rules and tolerances (per-entity tax rules, payment-term
validation, duplicate-detection thresholds, milestone tolerances) expressed
declaratively rather than hardcoded, so a rollout across entities in the UAE,
India and Saudi Arabia doesn't require a code change per entity.

Sprint 2/3 fills in the actual rule schema and evaluator; this stub defines
the shape a rule takes.
"""

from __future__ import annotations

from pydantic import BaseModel


class Rule(BaseModel):
    rule_id: str
    entity_code: str
    description: str
    expression: str  # e.g. "abs(invoice.total_amount - po.total_amount) <= tolerance"
    tolerance_percent: float | None = None


class RuleSet(BaseModel):
    entity_code: str
    rules: list[Rule]


def evaluate_rules(rule_set: RuleSet, context: dict) -> list[str]:
    """Evaluate every rule in `rule_set` against `context`; return the ids of
    rules that failed. Placeholder — real implementation needs a safe
    expression evaluator, not raw eval().
    """
    raise NotImplementedError

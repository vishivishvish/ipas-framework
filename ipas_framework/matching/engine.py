"""Matching engine: 2-way (invoice vs PO) and 3-way (invoice vs PO vs receipt)
matching, plus milestone and bank-guarantee validation for progressive/EPC
billing. Every mismatch must produce a reason, never a bare rejection — that's
a hard requirement from the client, not a nice-to-have (see ExceptionRecord).
"""

from __future__ import annotations

from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

from ipas_framework.models import Invoice, PurchaseOrder, Receipt


class MatchOutcome(str, Enum):
    MATCHED = "matched"
    EXCEPTION = "exception"


class ExceptionRecord(BaseModel):
    """A flagged mismatch. `reason` must always be populated — invoices can
    be exceptioned, but never silently rejected without an explanation.
    """

    code: str
    reason: str
    field: str | None = None
    expected: str | None = None
    actual: str | None = None


class MatchResult(BaseModel):
    invoice_number: str
    outcome: MatchOutcome
    exceptions: list[ExceptionRecord] = []


def match_invoice(
    invoice: Invoice,
    po: PurchaseOrder | None,
    receipts: list[Receipt],
    tolerance_percent: Decimal = Decimal("0.02"),
) -> MatchResult:
    """Run 2-way (no receipts) or 3-way (with receipts) matching, including
    milestone amount/percent checks and BG expiry checks where applicable.

    Placeholder for sprint 2. Signature reflects the configurable-tolerance
    requirement from the client's capability list.
    """
    raise NotImplementedError

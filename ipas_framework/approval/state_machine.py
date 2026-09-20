"""Approval workflow modelled as an explicit state machine, with notification
delivered through a pluggable channel (in-app / email now; Teams Adaptive
Cards and EBS AME are phase 2) so adding a channel never touches the state
transition logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ipas_framework.models import InvoiceStatus

# Legal transitions. Anything not listed here is rejected by advance().
ALLOWED_TRANSITIONS: dict[InvoiceStatus, set[InvoiceStatus]] = {
    InvoiceStatus.RECEIVED: {InvoiceStatus.EXTRACTED},
    InvoiceStatus.EXTRACTED: {InvoiceStatus.MATCHED, InvoiceStatus.EXCEPTION},
    InvoiceStatus.EXCEPTION: {InvoiceStatus.EXTRACTED, InvoiceStatus.REJECTED},
    InvoiceStatus.MATCHED: {InvoiceStatus.PENDING_APPROVAL},
    InvoiceStatus.PENDING_APPROVAL: {InvoiceStatus.APPROVED, InvoiceStatus.REJECTED},
    InvoiceStatus.APPROVED: {InvoiceStatus.POSTED},
    InvoiceStatus.POSTED: {InvoiceStatus.PAID},
}


class ApprovalChannel(ABC):
    """A way to notify an approver that something needs their attention."""

    @abstractmethod
    def notify(self, invoice_number: str, approver_id: str, message: str) -> None: ...


def advance(current: InvoiceStatus, target: InvoiceStatus) -> InvoiceStatus:
    """Validate and perform a state transition. Raises ValueError on an
    illegal transition rather than allowing silent, ungoverned status jumps.
    """
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"Illegal transition: {current} -> {target}")
    return target

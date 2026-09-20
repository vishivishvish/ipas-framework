"""The ERPAdapter interface: the swappable boundary between IPAS and whatever
ERP it's pointed at (mock EBS today, real Oracle EBS during pilot, Oracle
Fusion later). Every concrete adapter — mock, EBS, Fusion — implements this
same contract, so nothing above this layer (matching, rules, approval) needs
to know which ERP it's talking to.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ipas_framework.models import (
    Invoice,
    InvoiceStatus,
    PostingResult,
    PurchaseOrder,
    Receipt,
    Supplier,
)


class ERPAdapter(ABC):
    """Read/write boundary to a single ERP system.

    Reads (get_po, get_receipts, get_supplier) feed the matching and rules
    engines. post_invoice is the only write path, and it must be idempotent:
    calling it twice with the same invoice_number should not create a
    duplicate posting in the target ERP. get_status lets the approval
    workflow and dashboard poll for posting/payment progress after a write.
    """

    @abstractmethod
    def get_po(self, po_number: str) -> PurchaseOrder | None:
        """Fetch a purchase order and its lines, or None if not found."""

    @abstractmethod
    def get_receipts(self, po_number: str) -> list[Receipt]:
        """Fetch all goods/service receipts recorded against a PO."""

    @abstractmethod
    def get_supplier(self, supplier_id: str) -> Supplier | None:
        """Fetch supplier master data, including any bank guarantees on file."""

    @abstractmethod
    def post_invoice(self, invoice: Invoice) -> PostingResult:
        """Write a matched/approved invoice into the ERP. Must be idempotent
        on invoice_number: a retry after a partial failure must not double-post.
        """

    @abstractmethod
    def get_status(self, invoice_number: str) -> InvoiceStatus:
        """Look up the current lifecycle status of a previously posted invoice."""

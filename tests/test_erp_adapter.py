"""Sanity check that ERPAdapter is a usable interface: a minimal in-memory
implementation can satisfy it end-to-end, and post_invoice is idempotent.
"""

from decimal import Decimal

from ipas_framework.erp.adapter import ERPAdapter
from ipas_framework.models import (
    Invoice,
    InvoiceLine,
    InvoiceStatus,
    InvoiceType,
    PostingResult,
    PurchaseOrder,
    PurchaseOrderLine,
    Receipt,
    Supplier,
)


class InMemoryERPAdapter(ERPAdapter):
    """Trivial adapter over Python dicts, standing in for the mock EBS
    container until Docker Compose is wired up.
    """

    def __init__(self):
        self._pos: dict[str, PurchaseOrder] = {}
        self._receipts: dict[str, list[Receipt]] = {}
        self._suppliers: dict[str, Supplier] = {}
        self._posted: dict[str, PostingResult] = {}

    def get_po(self, po_number: str) -> PurchaseOrder | None:
        return self._pos.get(po_number)

    def get_receipts(self, po_number: str) -> list[Receipt]:
        return self._receipts.get(po_number, [])

    def get_supplier(self, supplier_id: str) -> Supplier | None:
        return self._suppliers.get(supplier_id)

    def post_invoice(self, invoice: Invoice) -> PostingResult:
        if invoice.invoice_number in self._posted:
            return self._posted[invoice.invoice_number]
        result = PostingResult(
            invoice_number=invoice.invoice_number,
            erp_invoice_id=f"ERP-{invoice.invoice_number}",
            status=InvoiceStatus.POSTED,
        )
        self._posted[invoice.invoice_number] = result
        return result

    def get_status(self, invoice_number: str) -> InvoiceStatus:
        result = self._posted.get(invoice_number)
        return result.status if result else InvoiceStatus.RECEIVED


def _sample_invoice() -> Invoice:
    return Invoice(
        invoice_number="INV-001",
        supplier_id="SUP-001",
        entity_code="UAE-01",
        invoice_type=InvoiceType.PO,
        invoice_date="2026-09-01",
        currency="AED",
        total_amount=Decimal("1000.00"),
        po_number="PO-001",
        lines=[
            InvoiceLine(line_number=1, description="Consulting", amount=Decimal("1000.00")),
        ],
    )


def test_erp_adapter_round_trip():
    adapter = InMemoryERPAdapter()
    adapter._pos["PO-001"] = PurchaseOrder(
        po_number="PO-001",
        supplier_id="SUP-001",
        entity_code="UAE-01",
        currency="AED",
        total_amount=Decimal("1000.00"),
        lines=[
            PurchaseOrderLine(line_number=1, description="Consulting", amount=Decimal("1000.00")),
        ],
    )

    po = adapter.get_po("PO-001")
    assert po is not None
    assert po.total_amount == Decimal("1000.00")

    result = adapter.post_invoice(_sample_invoice())
    assert result.status == InvoiceStatus.POSTED
    assert adapter.get_status("INV-001") == InvoiceStatus.POSTED


def test_post_invoice_is_idempotent():
    adapter = InMemoryERPAdapter()
    invoice = _sample_invoice()

    first = adapter.post_invoice(invoice)
    second = adapter.post_invoice(invoice)

    assert first == second
    assert first.erp_invoice_id == second.erp_invoice_id

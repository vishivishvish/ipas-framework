"""Domain models shared across ingestion, matching, rules, approval and ERP modules.

These are intentionally ERP-agnostic: any ERPAdapter implementation (Oracle EBS,
Oracle Fusion, a mock, etc.) maps its own schema onto these before handing data
back to the rest of the framework.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class InvoiceType(str, Enum):
    PO = "po"
    NON_PO = "non_po"
    MILESTONE = "milestone"
    ADVANCE = "advance"
    CREDIT_NOTE = "credit_note"


class Milestone(BaseModel):
    milestone_id: str
    description: str
    percent_of_contract: Decimal
    amount: Decimal
    is_advance: bool = False
    requires_bank_guarantee: bool = False


class BankGuarantee(BaseModel):
    bg_id: str
    supplier_id: str
    po_number: str
    amount: Decimal
    issuing_bank: str
    expiry_date: date
    is_active: bool = True


class PurchaseOrderLine(BaseModel):
    line_number: int
    description: str
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    amount: Decimal
    milestone: Milestone | None = None


class PurchaseOrder(BaseModel):
    po_number: str
    supplier_id: str
    entity_code: str
    currency: str
    total_amount: Decimal
    lines: list[PurchaseOrderLine]
    payment_terms: str | None = None


class Receipt(BaseModel):
    receipt_number: str
    po_number: str
    line_number: int
    quantity_received: Decimal | None = None
    amount_received: Decimal | None = None
    received_date: date


class Supplier(BaseModel):
    supplier_id: str
    name: str
    tax_registration_number: str | None = None
    bank_guarantees: list[BankGuarantee] = []


class InvoiceLine(BaseModel):
    line_number: int
    description: str
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    amount: Decimal
    tax_amount: Decimal | None = None
    po_line_number: int | None = None
    milestone_id: str | None = None


class Invoice(BaseModel):
    invoice_number: str
    supplier_id: str
    entity_code: str
    invoice_type: InvoiceType
    invoice_date: date
    currency: str
    total_amount: Decimal
    tax_amount: Decimal | None = None
    po_number: str | None = None
    lines: list[InvoiceLine]
    source_file: str | None = None
    extraction_confidence: float | None = None


class InvoiceStatus(str, Enum):
    RECEIVED = "received"
    EXTRACTED = "extracted"
    MATCHED = "matched"
    EXCEPTION = "exception"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    POSTED = "posted"
    PAID = "paid"
    REJECTED = "rejected"


class PostingResult(BaseModel):
    invoice_number: str
    erp_invoice_id: str | None = None
    status: InvoiceStatus
    message: str | None = None

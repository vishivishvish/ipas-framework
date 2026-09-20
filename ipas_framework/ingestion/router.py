"""Routes an incoming file to the right extraction path based on what it is,
before any OCR or LLM call happens. Native PDFs with a text layer, scanned
images, and structured e-invoice XML/JSON each need a different extractor;
picking the cheap/fast path first is what keeps OCR and vision-model spend down.

Sprint 1 fills in the actual detection logic; this stub defines the contract.
"""

from __future__ import annotations

from enum import Enum


class InputKind(str, Enum):
    NATIVE_PDF = "native_pdf"
    SCANNED_IMAGE = "scanned_image"
    E_INVOICE_XML = "e_invoice_xml"
    E_INVOICE_JSON = "e_invoice_json"
    UNKNOWN = "unknown"


def classify_input(file_path: str) -> InputKind:
    """Inspect a file and decide which extraction path it should take.

    Placeholder: real implementation checks file extension, then for PDFs
    checks whether PyMuPDF finds an extractable text layer (native) or not
    (scanned, route to Document Intelligence).
    """
    raise NotImplementedError

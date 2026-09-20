"""Extractor interface: every extraction backend (native-PDF text parse,
Document Intelligence OCR, e-invoice XML/JSON parse, vision-model fallback)
implements this so the pipeline can swap backends without touching callers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ipas_framework.models import Invoice


class Extractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> Invoice:
        """Parse a source file into a structured Invoice.

        Implementations should set extraction_confidence on the returned
        Invoice so the pipeline can route low-confidence results to a human
        review queue instead of straight into matching.
        """

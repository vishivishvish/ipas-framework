# ipas-framework

Generic, ERP-agnostic invoice processing framework: ingestion, extraction,
matching, configurable rules, approval workflow, and an ERP adapter interface.

This repo holds only generic logic — no client data, no client-specific
configuration, and no tuned business rules. Client solutions (e.g. an Oracle EBS
integration for a specific EPC company) depend on this package and layer
their own entity configs, tax rules, and ERP adapters on top of it. Code
flows from framework to solution, never back.

## Module layout

- `ipas_framework/models.py` — shared domain models (Invoice, PurchaseOrder,
  Receipt, Supplier, Milestone, BankGuarantee, PostingResult, ...).
- `ipas_framework/ingestion/` — routes an incoming file (native PDF, scanned
  image, e-invoice XML/JSON) to the right extraction path.
- `ipas_framework/extraction/` — turns a source file into a structured
  `Invoice`, with a confidence score for routing low-confidence results to
  human review.
- `ipas_framework/matching/` — 2-way and 3-way matching, milestone and bank
  guarantee validation. Every mismatch produces a reason (`ExceptionRecord`),
  never a bare rejection.
- `ipas_framework/rules/` — declarative, per-entity business rules and
  tolerances, so a multi-entity rollout doesn't require a code change per
  entity.
- `ipas_framework/approval/` — approval workflow as an explicit state
  machine, with notification delivered through a pluggable channel.
- `ipas_framework/erp/` — the `ERPAdapter` interface: `get_po`,
  `get_receipts`, `get_supplier`, `post_invoice`, `get_status`. Every ERP
  integration (mock, Oracle EBS, Oracle Fusion) implements this same
  contract, so nothing above it needs to know which ERP it's talking to.

## Status

Scaffold stage. `ERPAdapter` and the domain models are stable enough to build
against; ingestion, extraction, matching, rules, and approval are stubs with
defined interfaces, filled in sprint by sprint.

## Development

```bash
pip install -e ".[dev]"
pytest
```

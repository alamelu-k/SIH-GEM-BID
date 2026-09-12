"""
tender_intelligence/

Pipeline: clause_extraction -> requirement_parser -> threshold_extraction
-> evidence_mapping.

Takes a tender PDF's full text (from document_ai.ocr.pdf_text_extractor)
and produces a structured, evidence-linked list of TenderRequirement
objects that feed Alamelu's Requirement table and rules engine.

This is a separate module from document_ai because it operates on a
different input (tender PDFs, not bidder documents) and produces a
different output (requirements, not bidder field values) — see the
architecture discussion in project notes.
"""

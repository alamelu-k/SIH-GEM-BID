"""
document_ai/

Pipeline: preprocessing -> ocr -> classification -> extraction ->
validation -> evaluation.

Takes a scanned/PDF bidder document and produces structured,
validated fields (legal name, PAN, GSTIN, Udyam number, turnover,
dates, OEM name), plus an accuracy report measured against ground
truth.
"""

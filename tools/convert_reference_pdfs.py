#!/usr/bin/env python3
"""Convert lecture PDFs to page-indexed Markdown using Poppler's pdftotext."""
from pathlib import Path
import argparse
import json
import re
import subprocess


def normalize(text: str) -> str:
    return re.sub(r"[^\w]", "", text.casefold())


def text_block(text: str) -> str:
    fence = "`" * max(3, 1 + max((len(m) for m in re.findall(r"`+", text)), default=0))
    return f"{fence}text\n{text}\n{fence}\n"


def convert(pdf: Path, ocr_executable: str | None = None) -> tuple[int, list[int]]:
    info = subprocess.run(
        ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
    ).stdout
    expected = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
    extracted = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    pages = extracted.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    if len(pages) != expected:
        raise ValueError(f"{pdf.name}: expected {expected} pages, got {len(pages)}")
    ocr_pages = None
    if ocr_executable:
        ocr_pages = json.loads(subprocess.run(
            [ocr_executable, str(pdf)], check=True, stdout=subprocess.PIPE, text=True
        ).stdout)
        if len(ocr_pages) != expected:
            raise ValueError(f"{pdf.name}: OCR page count mismatch")
    output = [
        f"# {pdf.stem}\n",
        f"Source: [{pdf.name}](<{pdf.name}>)\n",
        f"Pages: {expected}\n",
        "Extracted with `pdftotext -layout`. Page numbers match the PDF. "
        "Text blocks preserve spacing for code, tables, and columns. "
        "Diagrams, plotted data, and equations may need inspection in the original PDF.\n",
    ]
    if ocr_pages is not None:
        output.append("Apple Vision OCR supplements include recognized lines absent from the "
                      "PDF text layer. These are search aids and may contain recognition errors; "
                      "verify code, formulas, and numbers against the PDF.\n")
    empty = []
    for number, page in enumerate(pages, 1):
        page = "\n".join(line.rstrip() for line in page.splitlines()).strip("\n")
        lines = [line.strip() for line in page.splitlines() if line.strip()]
        title = next((line for line in lines if not line.startswith("Image Source:")),
                     "No extractable text")
        output.append(f"## Page {number}: {title}\n")
        if not lines:
            empty.append(number)
            output.append("No extractable text; inspect this page in the PDF.\n")
        else:
            output.append(text_block(page))
        if ocr_pages is not None:
            native = normalize(page)
            supplement = [item["text"] for item in ocr_pages[number - 1]
                          if normalize(item["text"]) and normalize(item["text"]) not in native]
            if supplement:
                output.append("### OCR supplement (verify against PDF)\n")
                output.append(text_block("\n".join(supplement)))
    pdf.with_suffix(".md").write_text("\n".join(output), encoding="utf-8")
    return expected, empty


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ocr-executable", help="Optional compiled ocr_reference_pdf.swift binary")
    args = parser.parse_args()
    references = Path(__file__).resolve().parents[1] / "reference_materials"
    for pdf in sorted(references.glob("*.pdf")):
        pages, empty = convert(pdf, args.ocr_executable)
        print(f"{pdf.name}: {pages} pages; pages without text: {empty}", flush=True)

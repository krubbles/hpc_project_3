# HPC Project 3 — Parallelizing Vector-Matrix Multiply

CSC 746, Fall 2026. This workspace contains the assignment references, the original
OpenMP VMM harness, and the required course LaTeX template.

## Layout

- [reference_materials/](reference_materials/README.md): assignment description,
  four original lecture PDFs, and page-indexed searchable Markdown with OCR supplements.
- [code/](code/README.md): VMM reference implementation, timed harness, and correctness checks.
- [writeup/](writeup/README.md): downloaded LaTeX template; entry point is `00_main.tex`.
- `tools/`: scripts to regenerate the reference Markdown.

Read the [reference index](reference_materials/README.md) and assignment description
before starting implementation or the report. The lecture Markdown contains all
232 pages; inspect the PDFs when you need diagrams or exact code and equations.

On a Perlmutter login node, run `python3 code/run_benchmarks.py`. It submits and
waits for a CPU-node job that builds, verifies, benchmarks, and generates a portable
`deliverables/` folder with source ZIP, charts, tables, data, and environment details.
See [code/README.md](code/README.md) for defaults, options, and copy-back instructions.
The report and interpretation remain manual work.

## Upstream sources

| Component | Repository | Downloaded commit |
| --- | --- | --- |
| VMM harness | [vmmul-omp-harness-instructional](https://github.com/SFSU-Bethel-Instructional/vmmul-omp-harness-instructional) | `e1b94206b1483b861c3119b23a6b0f27e646f412` |
| LaTeX template | [CSC_746_HomeworkTemplate](https://github.com/SFSU-Bethel-Instructional/CSC_746_HomeworkTemplate) | `6cb2038076b25c39d1a1885784c55f7e82794501` |

Both sources are the repositories named in the Project 3 assignment, included
directly without nested Git repositories or submodules. On the
`reference-implementation` branch, the VMM stubs are implemented, the harness is
timed, and correctness checks are included. The original starter remains on
`main`; the writeup template is unmodified. See [code/README.md](code/README.md)
for build instructions, comparison guidance, and validation coverage.

## Regenerating searchable references

Requires Python 3.10+ and Poppler's `pdftotext` and `pdfinfo`. For the OCR supplements
used in the checked-in Markdown, macOS with Swift and Apple Vision is also required:

```sh
swiftc tools/ocr_reference_pdf.swift -o /tmp/hpc-project-3-ocr
python3 tools/convert_reference_pdfs.py --ocr-executable /tmp/hpc-project-3-ocr
```

For text-layer extraction alone, run `python3 tools/convert_reference_pdfs.py`.
That command overwrites the Markdown without OCR supplements. Native PDF text is
preserved in layout-oriented blocks, and OCR adds lines absent from that text.
OCR supplements are explicitly labeled and require checking against the PDF for
precise code, formulas, and numeric values.

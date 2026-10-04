# Project 3 reference materials

Start with the [assignment description](<CSC 746 F26 CP3 -- Parallelizing Vector-Matrix Multiply.md>).
It specifies the vector-matrix multiply implementations, benchmark configurations,
report requirements, and deliverables.

## Lecture slides

| Lecture | Searchable Markdown | Original PDF | Pages |
| --- | --- | --- | ---: |
| Lecture 08 — Vectorization and ILP | [Markdown](<CSC 746 F26 Lecture 08 -- Vectorization and ILP.md>) | [PDF](<CSC 746 F26 Lecture 08 -- Vectorization and ILP.pdf>) | 66 |
| Lecture 09 — CP2 Discussion, Parallelism, Parallel Perf Measures | [Markdown](<CSC 746 F26 Lecture 09 -- CP2 Discussion, Parallelism, Parallel Perf Measures.md>) | [PDF](<CSC 746 F26 Lecture 09 -- CP2 Discussion, Parallelism, Parallel Perf Measures.pdf>) | 35 |
| Lecture 10 — Parallel Perf Measures, SMP Programming | [Markdown](<CSC 746 F26 Lecture 10 -- Parallel Perf Measures, SMP Programming.md>) | [PDF](<CSC 746 F26 Lecture 10 -- Parallel Perf Measures, SMP Programming.pdf>) | 68 |
| Lecture 12 — OMP Worksharing, Sync, Data Environment | [Markdown](<CSC 746 F26 Lecture 12 -- OMP Worksharing, Sync, Data Environment.md>) | [PDF](<CSC 746 F26 Lecture 12 -- OMP Worksharing, Sync, Data Environment.pdf>) | 63 |

## Using these references in future threads

Search the assignment and lecture Markdown first. Each lecture has one section per
PDF page, with original text layout preserved in fenced text blocks. Additional
OCR text makes screenshots, chart labels, and code images searchable. OCR can
misread syntax, numbers, and equations; use the original PDF to verify those and
to inspect visual relationships. These files are transcripts, not summaries.

To search all reference text from the project root:

```sh
rg -n -i 'speedup|schedule|reduction|bandwidth' reference_materials --glob '*.md'
```

All 232 PDF pages have text sections, with no pages missing from extraction.
See the root README for instructions to regenerate the Markdown.

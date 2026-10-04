# CSC 746 F26 Lecture 09 -- CP2 Discussion, Parallelism, Parallel Perf Measures

Source: [CSC 746 F26 Lecture 09 -- CP2 Discussion, Parallelism, Parallel Perf Measures.pdf](<CSC 746 F26 Lecture 09 -- CP2 Discussion, Parallelism, Parallel Perf Measures.pdf>)

Pages: 35

Extracted with `pdftotext -layout`. Page numbers match the PDF. Text blocks preserve spacing for code, tables, and columns. Diagrams, plotted data, and equations may need inspection in the original PDF.

Apple Vision OCR supplements include recognized lines absent from the PDF text layer. These are search aids and may contain recognition errors; verify code, formulas, and numbers against the PDF.

## Page 1: CSC 746: High Performance Computing

```text
  CSC 746: High Performance Computing
CP2 Discussion, Parallelism and Perf Metrics
                   22 Sep 2026




                                 Copyright © 2026, E. Wes Bethel   1
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 2: Today

```text
Today
CP#2

●   Presentations: Cordano, Bellenberg
●   Discussion                           Compute time at NERSC is
                                                  limited
Parallelism and Concurrency

Parallel Performance Measures




                                          Copyright © 2026, E. Wes Bethel   2
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 3: CP#2 Discussion

```text
CP#2 Discussion



                  Copyright © 2026, E. Wes Bethel   3
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 4: Main observations:

```text
Main observations:

CBLAS
 ● MFLOP/s increases with
    problem size up to 512,
    then flattens out
 ● At N=>512, exceeding
    theoretical peak 39.2
    GFLOPS!
 ● Requires a “Warm-up”
    run

Basic:
 ● 2.7 GFLOP/s at N=64,
     ~6% of peak
 ● 128.0 MFLOP/s min at
     N=2048, 0.3% of peak



   Copyright © 2026, E. Wes Bethel   4
```

### OCR supplement (verify against PDF)

```text
MMUL CBLAS vs Basic MFLOP/s, AMD Milan 7763
50000
40000
, 30000
- - AMX EPYC 7763 Max GFLOP/s=39.2
20000
10000
256
Problem Sizes
1024
```

## Page 5: Main observations:

```text
Main observations:

Blocked: (except for B=2) relatively
steady performance regardless of N
  ● B=16 → 4.0 GF, 10% of peak
  ● B=32 → 3.9 GF, 10% of peak
  ● B=64 → 3.3 GF, 8% of peak

CBLAS: at N=2048, 51.6 GF, 130%
of peak !!

Blocking helps to avoid the severe
penalties of memory access patterns
with large N

Blocking best (4 GFLOP/s, ~10% of
peak) nowhere near CBLAS best
(51.6 GFLOP/s 130% of peak)

         Copyright © 2026, E. Wes Bethel   5
```

### OCR supplement (verify against PDF)

```text
MMUL CBLAS vs Blocked MFLOP/s, AMD Milan 7763
Blocked-2
Blocked-16
Blocked-32
Blocked-64
- AMD Milan 7763 Max GFLOP/s=39.2
MFLOP/s
103
128
256
512
Problem Sizes
1024
```

## Page 6: Main observations:

```text
Main observations:

At small problem sizes, basic is
competitive (everything fits into
cache)

At larger problem sizes, basic
quickly becomes non-competitive

For B=2, lots of overhead copying
data around




          Copyright © 2026, E. Wes Bethel   6
```

### OCR supplement (verify against PDF)

```text
MFLOP/s
104
Basic vs Blocked MFLOP/s, AMD Milan 7763
Blocked-2
Blocked-16
Blocked-32
Blocked-64
AMD Milan 7763 Max GFLOP/s=39.2
103
102
64
128
9SZ
512
1024
2048
```

## Page 7: CP2 Problem Sizes, memory footprint, Perlmutter CPU Node Cache Sizes

```text
CP2 Problem Sizes, memory footprint, Perlmutter CPU Node Cache Sizes




                                                         Copyright © 2026, E. Wes Bethel   7
```

### OCR supplement (verify against PDF)

```text
64
128
256
512
1024
2048
Block Size
16
23
A, B, C mem
Mem footprint (KiB) footprint
32
128
512
2048
8192
32768
96
384
1536
6144
24576
98304
L1 cache (KiB)
32
32
32
32
32
32
L2 cache (KiB)
512
512
512
512
512
512
L3 cache (KiB)
32MB * 1024
32768
32768
32768
32768
32768
32768
A, B, C mem
Mem footprint (KiB) footprint
0.03125
0.09375
4.1328125
32
12.3984375
96
L1 cache (KiB)
32
32
32
32
L2 cache (KiB)
512
512
512
512
L3 cache (KiB)
256 MB * 1024
262144
262144
262144
262144
```

## Page 8: Three Questions about CBLAS dgemm()

```text
Three Questions about CBLAS dgemm()
1. Why is it so much faster than our basic and
   OpenMP implementations?
2. What MMUL algorithm does BLAS use for its
   implementation?
3. Is it really exceeding the 39.2 GFLOP/s
   theoretical peak per-core performance?




                                                 Copyright © 2026, E. Wes Bethel   8
```

### OCR supplement (verify against PDF)

```text
50000
40000
g 30000
20000
10000
MFLOP/s
103
SAN FRANCISCO
STATE UNIVERSITY
MMUL CBLAS vs Basic MFLOP/s, AMD Milan 7763
AMX EPYC 7763 Max GFLOP/s=39.2
64
128
256
512
Problem Sizes
1024
2048
MMUL CBLAS vs Blocked MFLOP/s, AMD Milan 7763
- Blocked-2
Blocked-16
Blocked-32
Blocked-64
AMD Milan 7763 Max GFLOP/s=39.2
128
256
512
1024
2048
Problem Sizes
copyпignt o zuzo, c. wes bemer
```

## Page 9: Image credit: David Bindel

```text
                                           Image credit: David Bindel
                                           (Cornell)

CBLAS dgemm() – highly optimized implementation




                                        Copyright © 2026, E. Wes Bethel   9
```

### OCR supplement (verify against PDF)

```text
Timing for matrix multiply
7000
6000
Naive
Blocked
DSB
Vendor
5000
4000
Mflop/s
3000
2000
1000
SAN FRAN
STATE UNIV
100
200
300 400 500 600 700 800 900 1000 1100
Dimension
```

## Page 10: CBLAS dgemm() – highly optimized implementation

```text
CBLAS dgemm() – highly optimized implementation
Hand-tuned, processor-specific assembly language code

●   AVX2 instructions on AMD EPYC 7763
     ○   Intel Knights Landing chip had dual AVX-512 units
     ○   Impossible to access both through g++ and user written C++ code
●   Special Fused multiply-add instruction (FMA), 2 FLOPS/clock

Autotuning the block size to match specific processor/cache architecture

●   We studied square block sizes
●   Would rectangular block shapes perform better?
●   What sizes of rectangular blocks might perform best?

                                                                           Copyright © 2026, E. Wes Bethel   10
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 11: Q2. What MMUL algorithm does BLAS use?

```text
Q2. What MMUL algorithm does BLAS use?
Basic MM:

●   FLOPS: 2n^3
●   Mem accesses: n^3 + 3n^2 (no cache)
     ○     → Some papers say 4n^2, but that’s not how your implementation works

Blocked:

●   FLOPS: 2n^3
●   Mem accesses: (2N_b + 2) * n^2, (at N=1024, B=64, N_b=16), = 18n^2




                                                                           Copyright © 2026, E. Wes Bethel   11
```

### OCR supplement (verify against PDF)

```text
• Мem accesses: n^3 + 3n^2 (no cache)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 12: Q2. What MMUL algorithm does BLAS use, ctd.?

```text
Q2. What MMUL algorithm does BLAS use, ctd.?
Strassen’s: (1969)
 ●   FLOPS: O(N^2.8074)
 ●   Mem accesses: similar,
      ○   Access pattern not cache friendly (recursion)
 ●   Replaces some multiplications with additions


 ●   Not as numerically stable as basic/blocked (not
     used in CBLAS)
 ●   Performs better for Large N, basic does better
     at small N
                                                          Thanks GPT




                                                            Copyright © 2026, E. Wes Bethel   12
```

### OCR supplement (verify against PDF)

```text
1. Basic Idea of Strassen's Algorithm:
• Strassen's algorithm divides two matrices A and B of size n x n into four
submatrices of size n/2 x n/2.
• It computes 7 matrix multiplications (instead of 8 in the classical approach)
using a recursive divide-and-conquer method.
• The idea is to trade some scalar multiplications for additional additions and
subtractions, which are computationally cheaper than multiplications.
The key steps of Strassen's algorithm reduce the number of multiplications from
8 to 7 for 2 x 2 blocks and rely on recursion to perform larger multiplications.
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 13: Q2. What MMUL algorithm does BLAS use, ctd.?

```text
Q2. What MMUL algorithm does BLAS use, ctd.?
Williams, Xu, Xu, and Zhuo (WXYZ), 2024

●   FLOPS O(N^2.3728596)
●   Mem accesses: similar to FLOPS
     ○   Memory access pattern is not cache friendly: recursion
●   Similar to Strassen’s: uses recursion to divide-conquer
●   Additional optimizations to reduce number of FLOPS



●   Not as numerically stable as basic/blocked (not used in CBLAS)
●   Performs better for Large N, basic does better at small N

                                                                  Copyright © 2026, E. Wes Bethel   13
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 14: Q2. What MMUL algorithm does BLAS use, ctd.?

```text
Q2. What MMUL algorithm does BLAS use, ctd.?
Williams, Xu, Xu, and Zhuo (WXYZ), 2024
                                         CBLAS most likely uses a variation of
●   FLOPS O(N^2.3728596)                      your block+copy MMUL

●   Mem accesses: similar to FLOPSHand-optimized assembler
                               ●
     ○                                ● Leverages
        Memory access pattern is not cache             vector instructions (eg,
                                           friendly: recursion
                                          AVX2, AVS512)
●   Similar to Strassen’s: uses recursion        to divide-conquer
                                      ● Fine-tuning     the block size
●   Additional optimizations to reduce number of FLOPS
                                Name of the game:
                                 ● Perform minimum memory
                                    accesses while doing the 2N^3
                                    FLOPS
●   Not as numerically stable as basic/blocked    (not used in CBLAS)
                                 ● Some papers mention 4N^2
●   Performs better for Large N, basic doesaccesses
                                    memory    better at small N

                                                                             Copyright © 2026, E. Wes Bethel   14
```

### OCR supplement (verify against PDF)

```text
• Leverages vector instructions (eg,
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 15: Further reading on MMUL and CBLAS/DGEMM

```text
Further reading on MMUL and CBLAS/DGEMM
Further reading:

J. Dongarra et al, A Set of Level 3 Basic Linear Algebra Subprograms, ACM TOMS 16(1), 1990.
https://dl.acm.org/doi/10.1145/77626.79170

S. Hadjis, BLAS-level CPU Performance in 100 lines of C-code. https://cs.stanford.edu/people/shadjis/blas.html

T. Smith et al., Anatomy of High-performance Many-threaded Matrix Multiplication, IPDPS, 2014.
https://www.cs.utexas.edu/users/flame/pubs/blis3_ipdps14.pdf

R. van de Geijn, E. Quintana-Ortí, The Science of Programming Matrix Computations, 2007

F. van Zee and R. van de Geijn, BLIS: A Framework for Rapid Instantiation of BLAS Functionality, ACM TOMS 2015

Computational Complexity of matrix multiplication (wikipedia)




                                                                                        Copyright © 2026, E. Wes Bethel   15
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 16: Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?

```text
Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?
The AMD 7764

39.2 GFLOP/s / 2.45 GHz → 16 dp FLOPS / clock

16 dp FLOPS/clock? How?

AVX2 instructions, 256-bit vector instructions, or 16 dp FLOPS/clock

●   Each 256-bit AVX2 vector register can hold 4, 8-byte doubles
●   Use a “fused multiply add” instruction for 2 FLOPs/clock
●   There are two such AVX2 vector units per core
●   4 doubles * 2 FLOPS * 2 FMA units = 16 FLOPS/clock

                                                              Copyright © 2026, E. Wes Bethel   16
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 17: Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?

```text
Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?
The AMD 7764
AVX2 instructions, 256-bit vector instructions, or 16 dp FLOPS/clock
How to use both FMA units?
●   Loop unrolling
●   Ensure load/compute instructions don’t have contention
●   Careful hand-crafted x86 assembly language …
Does G++ -O3 produce this kind of code?
●   Not sure, would have to examine assembly language produced by G++

                                                              Copyright © 2026, E. Wes Bethel   17
```

### OCR supplement (verify against PDF)

```text
Does G++ -03 produce this kind of code?
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 18: Q3. CBLAS and the AMD 7763 → 39.2 GFLOP/s peak?

```text
Q3. CBLAS and the AMD 7763 → 39.2 GFLOP/s peak?
CBLAS: assume 2*N^3 FLOPS
Assumption of 39.2 GFLOP/s peak is computed as:
    2.45 GHz * 16 FLOPS/clock
On the spec sheet:
●   Base clock = 2.45 GHz
●   Max boost clock = 3.5 GHz
At 3.5 GHz, then the peak is 56 GFLOPS



                                                  Copyright © 2026, E. Wes Bethel   18
```

### OCR supplement (verify against PDF)

```text
General Specifications
Platform:
Product Family:
Product Line:
# of CPU Cores:
# of Threads:
Max. Boost ClockO:
Server
AMD EPYC™
AMD EPYC™ 7003 Series
64
128
Up to 3.5GHz
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 19: Q3. CBLAS and the AMD 7763

```text
Q3. CBLAS and the AMD 7763
CBLAS: assume 2*N^3 FLOPS                         Conditions when clock rate will boost:
Assumption of 39.2 GFLOP/s peak is computed as:
                                                   ●   Workload demand
     2.45 GHz * 16 FLOPS/clock                     ●   Thermal and power conditions
                                                   ●   Number of active cores
On the spec sheet:                                 ●   Duration and load
                                                   ●   BIOS settings
 ●   Base clock = 2.45 GHz                         ●   Serial computation (not multi-core)
 ●   Max boost clock = 3.5 GHz

At 3.5 GHz, then the peak is 56 GF                Could clock boost be happening for us?
                                                   ● If BIOS settings permit
 ●   If using 2 FMAs, then                         ● Then it is likely
 ●   3.5 GHz * 32 FLOPS/clock = 112 GF peak
                                                  Question: we measure 51 GFLOPS



                                                                          Copyright © 2026, E. Wes Bethel   19
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 20: Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?

```text
Q3. Is CBLAS dgemm() exceeding the 39.2 GF peak?
Yes, it clearly is exceeding 39.2 GF: our charts show this clearly

Why?

●   3.5 GHz clock in effect during have serial workload: 56 GF peak
●   Likely: using both FMA units with carefully crafted x86 AVX2 assembly code
●   It is using a variant of your block+copy optimization
     ○   Block sizes tuned for the architecture
     ○   Thoughts about block sizes in CP#2?




                                                                Copyright © 2026, E. Wes Bethel   20
```

### OCR supplement (verify against PDF)

```text
• Likely: using both FMA units with carefully crafted ×86 AVX2 assembly code
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 21: Parallelism and Concurrency

```text
Parallelism and Concurrency



                       Copyright © 2026, E. Wes Bethel   21
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 22: What is Parallelism? Concurrency?

```text
 What is Parallelism? Concurrency?
 Concurrency: a condition of a system in which multiple tasks are logically active at
 one time

 Parallelism: a condition of a system in which multiple tasks are actually active at
 one time




Image Credit: Tim Mattson, Intel
Modified locally for correctness



                                                                 Copyright © 2026, E. Wes Bethel   22
```

### OCR supplement (verify against PDF)

```text
Concurrent, non-parallel Execution
SAN FRANCISCO
STATE UNIVERSITY
Concurrent, parallel Execution
```

## Page 23: What is Parallelism? Concurrency?

```text
 What is Parallelism? Concurrency?
 Concurrency: a condition of a system in which multiple tasks are logically active at
 one time

 Parallelism: a condition of a system in which multiple tasks are actually active at
 one time




Image Credit: Tim Mattson, Intel




                                                                 Copyright © 2026, E. Wes Bethel   23
```

### OCR supplement (verify against PDF)

```text
Programs
Concurrent
Programs
Programs
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 24: Concurrency in Action: The Web Server

```text
    Concurrency in Action: The Web Server




Image Credit: (top) hackr.io, (bottom) digitalocean



                                                      Copyright © 2026, E. Wes Bethel   24
```

### OCR supplement (verify against PDF)

```text
Web Application Architecture
CLIENT
WIDGETS
AJAX
JSON
HTML
SERVICES
BUSINESS
LOGIC
App01
requests app.com
User
SAN FRANCISCO
STATE UNIVERSITY
Internet
Load Balancer
app.com
App02
Аpp03
```

## Page 25: Pipelining vs. Concurrency vs. Parallelism

```text
Pipelining vs. Concurrency vs. Parallelism

              Wash      Dry
Laundry:
2-stage
pipeline                  Wash      Dry

                                      Wash            Dry




                                             Copyright © 2026, E. Wes Bethel   25
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 26: Pipelining vs. Concurrency vs. Parallelism

```text
Pipelining vs. Concurrency vs. Parallelism

                Wash       Dry
                             Wash     Dry
                                        Wash                 Dry

Laundromat:
N-way           Wash       Dry
(potential)                  Wash     Dry
parallelism
                                        Wash                 Dry


                Wash       Dry
                             Wash     Dry
                                        Wash                 Dry
                                               Copyright © 2026, E. Wes Bethel   26
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 27: Image Credit: Kathy Yelick, UCB

```text
                                                                       Image Credit: Kathy Yelick, UCB


Parallel Machine Models


                                                                                                     Abstract
                                                                                                     machine
                                                                                                     models




   Shared memory                    Distributed memory       SIMD (Vector)

   Processors execute own           Processors execute own   One instruction stream applied to
   instruction stream               instruction stream       multiple data

   Communicate by reading/writing   Communicate by sending   Communicate through memory
   memory                           messages

                                                                          Copyright © 2026, E. Wes Bethel   27
```

### OCR supplement (verify against PDF)

```text
Network
Network
SAN
T RANOIDCO
STATE UNIVERSITY
Network
Network
Network
```

## Page 28: Image Credit: Kathy Yelick, UCB

```text
                                                    Image Credit: Kathy Yelick, UCB


From Vector to MPP to Accelerator Systems




                                            Copyright © 2026, E. Wes Bethel   28
```

### OCR supplement (verify against PDF)

```text
100%
90%
Reprogrammed
again ®
80%
70%
Programmed by rethinking
algorithms and software for
parallelism
60%
50%
40%
30%
• Accelerated
• Cluster x86
• Constellation
I SMP
• SIMD
Programmed by
"annotating" serial
programs
10%
TOP 500®
SUPERCOMPUTER SITES
```

## Page 29: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)

 ●   Parallel “languages” were loop annotations
     to specify vectorization
 ●   Performance was fragile, good user
     support




                                                  Copyright © 2026, E. Wes Bethel   29
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 30: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)

 ●   Parallel “languages” were loop annotations
     to specify vectorization
 ●   Performance was fragile, good user
     support

SIMD machine era (Connection Machine)

 ●   Data parallel languages popular and
     successful (CMF, C*, *Lisp, …)
 ●   Irregular data (sparse mat-vec multiply
     OK), but irregular computation (adaptive
     meshes, divide-conquer) less clear


                                                  Copyright © 2026, E. Wes Bethel   30
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 31: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)

 ●    Parallel “languages” were loop annotations
 ●    Performance was fragile, good user support

SIMD machine era (Connection Machine)

 ●    Data parallel languages popular and
      successful (CMF, C*, *Lisp, …)
 ●    Irregular data (sparse mat-vec multiply OK),
      but irregular computation (adaptive meshes,
      divide-conquer) less clear

SMP era (SGI Onyx, etc.)

 ●    Shared memory programming models: fork,
      POSIX threads, OpenMP (task parallelism,
      data parallelism)


                                                     Copyright © 2026, E. Wes Bethel   31
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 32: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)          Clusters era (Cray T3E, CM5, …)
 ●    Parallel “languages” were loop annotations      ●   The Message Passing Interface (MPI)
 ●    Performance was fragile, good user support
                                                          became dominant
SIMD machine era (Connection Machine)                       ○   You divide up the problem, coordinate data
                                                                movement and synchronization
 ●    Data parallel languages popular and
                                                            ○   Data parallelism (mostly)
      successful (CMF, C*, *Lisp, …)
 ●    Irregular data (sparse mat-vec multiply OK),
      but irregular computation (adaptive meshes,
      divide-conquer) less clear

SMP era (SGI Onyx, Cray S-MP, etc.)

 ●    Shared memory programming models: fork,
      POSIX threads, OpenMP



                                                                            Copyright © 2026, E. Wes Bethel   32
```

### OCR supplement (verify against PDF)

```text
successtul (CMF, C*
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 33: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)          Clusters era (Cray T3E, CM5, …)
 ●    Parallel “languages” were loop annotations      ●   The Message Passing Interface (MPI)
 ●    Performance was fragile, good user support
                                                          became dominant
SIMD machine era (Connection Machine)                       ○   You divide up the problem, coordinate data
                                                                movement and synchronization
 ●    Data parallel languages popular and
                                                            ○   Data parallelism (mostly)
      successful (CMF, C*, *Lisp, …)
 ●    Irregular data (sparse mat-vec multiply OK),
      but irregular computation (adaptive meshes,    Addition of accelerators (GPU, FPGA)
      divide-conquer) less clear
                                                      ●   CUDA, OpenACC, ..
SMP era (SGI Onyx, Cray S-MP, etc.)                   ●   Data parallelism, disjoint memory spaces
 ●    Shared memory programming models: fork,
      POSIX threads, OpenMP



                                                                            Copyright © 2026, E. Wes Bethel   33
```

### OCR supplement (verify against PDF)

```text
successtul (CMF, C*
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 34: Brief History of Parallel “Languages”

```text
Brief History of Parallel “Languages”
Vector machine era (Cray 1, XMP, YMP, etc.)          Clusters era (Cray C90, CM5, …)
 ●    Parallel “languages” were loop annotations
 ●    Performance was fragile, good user support      ●   The Message Passing Interface
SIMD machine era (Connection Machine)                     (MPI) became dominant

 ●    Data parallel languages popular and            Addition of accelerators (GPU, FPGA)
      successful (CMF, C*, *Lisp, …)
 ●    Irregular data (sparse mat-vec multiply OK),    ●   CUDA, OpenACC, ..
      but irregular computation (adaptive meshes,
      divide-conquer) less clear                      ●   Data parallelism, disjoint memory spaces

SMP era (SGI Onyx, Cray S-MP, etc.)                  Cloud computing
 ●    Shared memory programming models: fork,
      POSIX threads, OpenMP                           ●   Hadoop, SPARK (task parallelism)


                                                                          Copyright © 2026, E. Wes Bethel   34
```

### OCR supplement (verify against PDF)

```text
successtul (CMF, C*
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 35: Copyright © 2026, E. Wes Bethel   35

```text
Copyright © 2026, E. Wes Bethel   35
```

### OCR supplement (verify against PDF)

```text
The Ena
A Warner Bros.
PICTURE
SAN FRANC
STATE UNIVERSITY
copyngnt o zozô, E. Wes Bethel
```

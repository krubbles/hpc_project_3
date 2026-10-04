# VMM reference implementation

This branch contains a reference implementation for comparing your own work.
The original downloaded stubs remain on `main`. To compare a file against its
starter version, use `git diff main -- code/dgemv-basic.cpp`.

## One-command Perlmutter workflow

From this project's root on a **Perlmutter login node**, outside an existing
allocation, run:

```sh
python3 code/run_benchmarks.py
```

This adapts Project 2's Python benchmark/plotting workflow. It submits one exclusive
CPU-node Slurm job and waits. The job loads `cpu`, `PrgEnv-gnu`, and `python`, builds
a snapshot of the sources, checks correctness, runs the assignment problem sizes
for basic, vectorized, serial CBLAS, and static OpenMP at 1/4/16/64 threads, and
generates `deliverables/`. The default account is the class account `m3930`, QoS
is `regular`, time limit is 30 minutes, and each configuration is repeated three
times. Change those when needed, for example:

```sh
python3 code/run_benchmarks.py --account m3930 --time 00:45:00 --repetitions 5
```

There is no optimization sweep: the current `-O1` basic/OpenMP and `-O3` vectorized
flags are preserved. The script checks the effective compilation flags and saves
them. CBLAS timing runs use one library thread. The requested full node has 256
logical CPUs (128 physical cores); benchmarks run sequentially to avoid interference.

Watch the printed job ID with `squeue -j JOB_ID` or follow
`deliverables/raw/slurm.log`. The Python command returns successfully only when
`deliverables/status.json` says `complete`. A failed build, bad numerical result,
missing measurement, or failed job leaves a failed status and diagnostic logs.
Stopping the waiting command can leave the job running; cancel with `scancel JOB_ID`.

The folder contains the source ZIP and a source tree, raw/summary CSVs, all three
required charts as PNG/PDF, bandwidth and performance tables as CSV/Markdown/LaTeX,
compiler/vectorization evidence, system metadata, and reproducibility hashes.
Copy it back from this Mac, substituting your username and remote project path:

```sh
scp -r USER@perlmutter.nersc.gov:/path/to/hpc_project_3/deliverables ./
```

The report and interpretation remain manual. The bandwidth table is explicitly a
useful-traffic estimate, not hardware-counter data: `8*(N*N+3*N) / seconds`, divided
by the whole-node theoretical peak of 409.6 GB/s. The default preserves the
starter's serial first-touch memory placement; `--interleave-memory` selects and
records an alternative using `numactl`. Chart 2 uses the basic serial baseline
shown in Lecture 10's CP3 example; an OpenMP-one-thread speedup table is also
generated. Chart 3 selects one fixed concurrency using geometric mean runtime.
Full formulas and sources are recorded in the generated folder's README.

The script never overwrites an existing output folder. For another run, use
`--output deliverables_run2`. The generated source archive excludes binaries,
build caches, references, and the report. Matplotlib is the only Python dependency
(`requirements.txt`); the job loads NERSC's Python module and checks it before work.

To validate locally without submitting jobs (output is marked as local validation):

```sh
python3 code/run_benchmarks.py --local --sizes 256,1024 --repetitions 2 \
  --output build/local-deliverables \
  --cmake-arg=-DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-16 \
  --cmake-arg=-DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-16 \
  --cmake-arg=-DBLA_VENDOR=OpenBLAS \
  --cmake-arg=-DCMAKE_PREFIX_PATH=/opt/homebrew/opt/openblas
```

## Kernel behavior

All kernels compute `y += A*x` for a double-precision, row-major, square matrix.
`A` and `x` remain unchanged. Buffers must not overlap; `n` must be nonnegative.

- `dgemv-basic.cpp`: one scalar dot product per row, accumulated into the existing `y`.
- `dgemv-vectorized.cpp`: the exact same function body. Compiler flags enable automatic
  vectorization; there are no vector intrinsics or pragmas in this version.
- `dgemv-openmp.cpp`: distributes rows using `parallel for schedule(static)`. Each row
  has a private sum and writes a distinct output element, so no atomic or reduction
  directive is needed. Threads are selected with `OMP_NUM_THREADS`.
- `dgemv-blas.cpp`: the upstream CBLAS wrapper, with `alpha=1` and `beta=1`.

The basic and OpenMP kernels use `-O1` with automatic vectorization disabled on
GNU/Clang, preserving the scalar baseline. The vectorized kernel uses `-O3` and
`-ffast-math`, allowing reordered floating-point reductions. Small rounding
differences relative to CBLAS are expected. Do not expect bitwise equality.

## Build

Requires CMake 3.14+, a C++11 compiler supporting OpenMP, and BLAS with CBLAS headers.
On Perlmutter, load the CPU/compiler and math-library environment used in class,
then run from the project root:

```sh
module load cpu
cmake -S code -B build
cmake --build build -j 4
ctest --test-dir build --output-on-failure
```

If CBLAS headers are not found automatically, add
`-DCBLAS_INCLUDE_DIR=/path/to/headers` when configuring. The build uses CMake's
OpenMP dependency rather than hard-coded OpenMP link flags.

On this Mac, the following configuration was built and tested using the already
installed Homebrew GCC 16 and OpenBLAS:

```sh
cmake -S code -B build \
  -DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-16 \
  -DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-16 \
  -DBLA_VENDOR=OpenBLAS \
  -DCMAKE_PREFIX_PATH=/opt/homebrew/opt/openblas
cmake --build build -j 4
ctest --test-dir build --output-on-failure
```

Use a fresh build directory when changing compilers. With GCC, inspect
`build/report.txt` for the vectorization report. Clang emits vectorization remarks
during compilation instead. Do not globally enable `-ffast-math`: the benchmark
and tests must retain their finite-value checks. The vectorized kernel alone uses it.

## Run and compare

For a quick correctness run with small inputs:

```sh
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_DYNAMIC=FALSE
./build/benchmark-basic --sizes 3,17,65,1024
./build/benchmark-vectorized --sizes 3,17,65,1024
OMP_NUM_THREADS=4 ./build/benchmark-openmp --sizes 3,17,65,1024
./build/benchmark-blas --sizes 3,17,65,1024
```

No size argument runs the assignment's `1024,2048,4096,8192,16384` sequence. The
largest run allocates about 4 GiB for two matrices and four vectors. Run that
sequence on the intended compute node. The generated `build/job-openmp` runs all
sizes with 1, 4, 16, and 64 threads, requests 64 CPUs, and stops on a failed run.
Review its account/time settings for your allocation; run it from `build`.

The harness uses seeded input data and times only `my_dgemv`, including OpenMP team
launch/join. Initialization, copying, and CBLAS verification occur outside the timer.
The first size is run twice; discard the row with `warmup=1` when analyzing timing.
CSV columns are:

```text
n,seconds,flops,mflops,verified,warmup
```

The first output line is a description comment beginning with `#`. FLOPs are
`2*n*n`: `n` multiplications and `n` additions per row, including accumulation into
`y`. `mflops = flops / seconds / 1e6`. Tiny inputs can finish below clock resolution;
those rows have zero seconds and `nan` MFLOP/s, and are useful for correctness only.

Exit status is 0 when all results match CBLAS, 1 on a numerical mismatch, and 2
on invalid arguments or setup errors. The checker rejects nonfinite outputs and
allows an absolute tolerance of `1e-10` plus a relative tolerance of `1e-10`.

## Correctness coverage

The CTest suite compares each student kernel to CBLAS, plus a hand-computed
asymmetric 2-by-2 example. It covers zero/one/odd sizes, mixed signs and scales,
zero and identity matrices, nonzero initial outputs, repeated accumulation, and
preservation of `A` and `x`. OpenMP is checked with 1, 4, 16, and 64 threads,
including cases with more threads than rows. The CBLAS comparisons allow rounding
error; the small integer hand-computed case is checked exactly.

Local validation used GCC/OpenBLAS on macOS. Perlmutter execution and the full
assignment-size performance study still need to be done on the target machine.

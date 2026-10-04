#!/usr/bin/env python3
"""Project 3: submit one Perlmutter CPU job and produce portable deliverables.

Adapted from Project 2's run_benchmarks.py and plot_project_2_results.py.
Run from a login node: python3 code/run_benchmarks.py
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import shlex
import shutil
import statistics
import subprocess
import sys
import textwrap
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SIZES = [1024, 2048, 4096, 8192, 16384]
THREADS = [1, 4, 16, 64]
CONFIGURATIONS = [("blas", 1), ("basic", 1), ("vectorized", 1)] + [
    ("openmp", threads) for threads in THREADS
]
ARCHITECTURE_URL = "https://docs.nersc.gov/systems/perlmutter/architecture/"
JOBS_URL = "https://docs.nersc.gov/systems/perlmutter/running-jobs/"
PYTHON_URL = "https://docs.nersc.gov/development/languages/python/using-python-perlmutter/"
SAMPLE_FIELDS = ["implementation", "threads", "repetition", "n", "seconds", "flops", "mflops"]


def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def write_csv(path, rows, fields=None):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def label(implementation, threads):
    return f"omp-{threads}" if implementation == "openmp" else implementation


def benchmark_environment(threads):
    return dict(os.environ, OMP_NUM_THREADS=str(threads), OMP_DYNAMIC="FALSE",
                OMP_SCHEDULE="static", OMP_PLACES="cores", OMP_PROC_BIND="spread",
                OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", BLIS_NUM_THREADS="1",
                GOTO_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", MPLBACKEND="Agg")


def run_logged(command, log_path, env=None):
    print("Running: " + shlex.join(map(str, command)), flush=True)
    with log_path.open("w") as log:
        log.write("$ " + shlex.join(map(str, command)) + "\n")
        log.flush()
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env, check=True)


def optional_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"unavailable": str(error)}


def parse_benchmark(text, sizes):
    """Accept exactly one warmup and one verified, measurable row per requested size."""
    lines = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(lines)))
    required = {"n", "seconds", "flops", "mflops", "verified", "warmup"}
    if set(reader.fieldnames or []) != required:
        raise ValueError("Unexpected benchmark CSV header")
    rows = list(reader)
    if len(rows) != len(sizes) + 1:
        raise ValueError("Incomplete benchmark output (expected warmup plus all sizes)")
    result = []
    for index, (row, n) in enumerate(zip(rows, [sizes[0]] + sizes)):
        if int(row["n"]) != n or int(row["warmup"]) != (1 if index == 0 else 0):
            raise ValueError("Unexpected problem order or warmup flag")
        if row["verified"] != "PASS":
            raise ValueError(f"CBLAS verification failed at N={n}")
        if int(row["flops"]) != 2 * n * n:
            raise ValueError(f"Incorrect FLOP count at N={n}")
        if index == 0:
            continue
        seconds = float(row["seconds"])
        mflops = float(row["mflops"])
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError(f"Unmeasurable runtime at N={n}; choose a larger problem size")
        derived = 2 * n * n / seconds / 1e6
        if not math.isfinite(mflops) or not math.isclose(mflops, derived, rel_tol=1e-7):
            raise ValueError(f"Inconsistent throughput at N={n}")
        result.append({"n": n, "seconds": seconds, "flops": 2 * n * n, "mflops": derived})
    return result


def summarize(samples, sizes, repetitions, peak_gbs):
    grouped = {}
    for row in samples:
        key = (row["implementation"], row["threads"], row["n"])
        grouped.setdefault(key, []).append(row)
    expected = {(kind, threads, n) for kind, threads in CONFIGURATIONS for n in sizes}
    if set(grouped) != expected:
        raise ValueError("Missing or unexpected benchmark configurations")
    summary = []
    for kind, threads in CONFIGURATIONS:
        for n in sizes:
            measurements = grouped[kind, threads, n]
            if sorted(row["repetition"] for row in measurements) != list(range(1, repetitions + 1)):
                raise ValueError("Incomplete or duplicated repetitions")
            values = [row["seconds"] for row in measurements]
            if any(not math.isfinite(value) or value <= 0 for value in values):
                raise ValueError("Invalid timing sample")
            median = statistics.median(values)
            # Minimum useful traffic: A once, x once, and one read/write of y.
            useful_bytes = 8 * (n * n + 3 * n)
            bandwidth = useful_bytes / median / 1e9
            summary.append(dict(implementation=kind, threads=threads, n=n,
                                samples=len(values), median_seconds=median,
                                min_seconds=min(values), max_seconds=max(values),
                                stdev_seconds=statistics.stdev(values) if len(values) > 1 else 0.0,
                                flops=2*n*n, mflops=2*n*n/median/1e6,
                                useful_bytes=useful_bytes, estimated_bandwidth_gbs=bandwidth,
                                estimated_peak_bandwidth_percent=100*bandwidth/peak_gbs))
    lookup = {(row["implementation"], row["threads"], row["n"]): row for row in summary}
    for row in summary:
        n = row["n"]
        row["speedup_vs_basic"] = lookup["basic", 1, n]["median_seconds"] / row["median_seconds"]
        row["speedup_vs_omp1"] = lookup["openmp", 1, n]["median_seconds"] / row["median_seconds"]
        fastest_serial = min(lookup[kind, 1, n]["median_seconds"] for kind in ["blas", "basic", "vectorized"])
        row["speedup_vs_best_serial"] = fastest_serial / row["median_seconds"]
    # Select one fixed team size across all sizes; geometric means weight sizes equally.
    best_threads = min(THREADS, key=lambda threads: statistics.mean(
        math.log(lookup["openmp", threads, n]["median_seconds"]) for n in sizes))
    return summary, best_threads


def make_charts(summary, sizes, best_threads, directory, local):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lookup = {(row["implementation"], row["threads"], row["n"]): row for row in summary}
    prefix = "LOCAL VALIDATION — " if local else ""

    def chart(filename, title, ylabel, series):
        figure, axes = plt.subplots(figsize=(8.2, 5.0))
        for kind, threads, field, name in series:
            axes.plot(sizes, [lookup[kind, threads, n][field] for n in sizes], marker="o", label=name)
        axes.set_xscale("log", base=2)
        axes.set_xticks(sizes)
        axes.set_xticklabels([str(n) for n in sizes])
        axes.set_xlabel("Matrix dimension N")
        axes.set_ylabel(ylabel)
        axes.set_title("\n".join(textwrap.wrap(prefix + title, 70)), fontsize=11)
        axes.grid(True, linestyle="--", alpha=0.35)
        axes.legend()
        if "speedup" in filename:
            axes.axhline(1, color="gray", linewidth=0.8, linestyle=":")
        figure.tight_layout()
        figure.savefig(directory / (filename + ".png"), dpi=200)
        figure.savefig(directory / (filename + ".pdf"))
        plt.close(figure)

    chart("01_serial_mflops", "Serial VMM: basic, vectorized, and CBLAS", "MFLOP/s",
          [(kind, 1, "mflops", name) for kind, name in
           [("basic", "Basic"), ("vectorized", "Vectorized"), ("blas", "CBLAS (1 thread)")]])
    chart("02_openmp_speedup", "Static-scheduled OpenMP speedup relative to basic serial", "Speedup (basic time / OpenMP time)",
          [("openmp", threads, "speedup_vs_basic", f"OpenMP, {threads} thread(s)") for threads in THREADS])
    chart("03_best_openmp_vs_cblas", f"Best fixed OpenMP team ({best_threads} threads) vs. serial CBLAS", "MFLOP/s",
          [("openmp", best_threads, "mflops", f"OpenMP, {best_threads} threads"),
           ("blas", 1, "mflops", "CBLAS (1 thread)")])


def make_tables(summary, sizes, directory):
    lookup = {(row["implementation"], row["threads"], row["n"]): row for row in summary}
    columns = [label(kind, threads) for kind, threads in CONFIGURATIONS]
    for filename, field, caption in [
        ("bandwidth_utilization", "estimated_peak_bandwidth_percent", "Estimated percentage of whole-node peak memory bandwidth; useful-traffic model."),
        ("mflops", "mflops", "MFLOP/s derived from median runtime."),
        ("speedup_vs_basic", "speedup_vs_basic", "Speedup relative to basic serial runtime."),
        ("speedup_vs_omp1", "speedup_vs_omp1", "Strong-scaling speedup relative to the one-thread OpenMP runtime."),
    ]:
        rows = [{"n": n, **{label(kind, threads): lookup[kind, threads, n][field]
                            for kind, threads in CONFIGURATIONS}} for n in sizes]
        write_csv(directory / (filename + ".csv"), rows)
        headers = ["N"] + columns
        formatted = [[str(row["n"])] + [f"{row[column]:.2f}" for column in columns] for row in rows]
        markdown = caption + "\n\n| " + " | ".join(headers) + " |\n| " + " | ".join(["---:"]*len(headers)) + " |\n"
        markdown += "".join("| " + " | ".join(row) + " |\n" for row in formatted)
        (directory / (filename + ".md")).write_text(markdown)
        latex = "\\begin{table*}[t]\n\\centering\n\\small\n\\begin{tabular}{r|" + "r"*len(columns) + "}\n\\hline\n"
        latex += " & ".join(headers) + " \\\\\n\\hline\n"
        latex += "".join(" & ".join(row) + " \\\\\n" for row in formatted)
        latex += "\\hline\n\\end{tabular}\n\\caption{" + caption + "}\n\\label{tab:" + filename.replace("_", "-") + "}\n\\end{table*}\n"
        (directory / (filename + ".tex")).write_text(latex)


def source_snapshot(root, destination):
    destination.mkdir()
    for path in sorted((root / "code").rglob("*")):
        relative = path.relative_to(root / "code")
        if any(part in {"build", "CMakeFiles", "__pycache__", ".git", ".venv"} for part in relative.parts):
            continue
        if path.is_file() and (path.name in {"CMakeLists.txt", "README.md", "job.in", "requirements.txt"}
                               or path.suffix in {".cpp", ".h", ".hpp", ".py"}):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def package_sources(out):
    with zipfile.ZipFile(out / "project_3_source.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("project_3/README.md", "# Project 3 source\n\nRun `python3 code/run_benchmarks.py` on a Perlmutter login node.\nSee code/README.md for build and comparison instructions.\n")
        for path in sorted((out / "code").rglob("*")):
            if path.is_file():
                archive.write(path, "project_3/" + str(path.relative_to(out)))


def record_environment(config, out, build):
    cache = (build / "CMakeCache.txt").read_text()
    compiler = next(line.split("=", 1)[1] for line in cache.splitlines()
                    if line.startswith("CMAKE_CXX_COMPILER:"))
    commands = {"lscpu": ["lscpu"], "numa": ["numactl", "--hardware"],
                "compiler": [compiler, "--version"],
                "cmake": ["cmake", "--version"],
                "blas_linkage": ["otool", "-L", str(build / "benchmark-blas")] if sys.platform == "darwin"
                else ["ldd", str(build / "benchmark-blas")],
                "git_head": ["git", "-C", config["root"], "rev-parse", "HEAD"]}
    info = {"captured_utc": timestamp(), "hostname": platform.node(), "platform": platform.platform(),
            "python": sys.version, "loaded_modules": os.environ.get("LOADEDMODULES", ""),
            "slurm": {key: value for key, value in os.environ.items() if key.startswith("SLURM_")},
            "omp_and_blas_environment": {key: value for key, value in benchmark_environment(1).items()
                                         if key.startswith(("OMP_", "OPENBLAS_", "MKL_", "BLIS_", "GOTO_", "VECLIB_"))},
            "commands": {key: optional_command(command) for key, command in commands.items()}}
    if hasattr(os, "sched_getaffinity"):
        info["cpu_affinity"] = sorted(os.sched_getaffinity(0))
    if Path("/proc/meminfo").exists():
        info["meminfo"] = Path("/proc/meminfo").read_text()
    write_json(out / "metadata/environment.json", info)
    for name in ["CMakeCache.txt", "compile_commands.json", "report.txt"]:
        source = build / name
        if source.exists():
            shutil.copy2(source, out / "metadata" / name)
    return info


def validate_build_flags(build):
    flags = {}
    commands = json.loads((build / "compile_commands.json").read_text())
    for kind in ["basic", "vectorized", "openmp", "blas"]:
        entry = next(item for item in commands if Path(item["file"]).name == f"dgemv-{kind}.cpp")
        arguments = entry.get("arguments") or shlex.split(entry["command"])
        optimization = [arg for arg in arguments if arg in {"-O0", "-O1", "-O2", "-O3", "-Os", "-Ofast", "-Og", "-Oz"}]
        expected = "-O1" if kind in {"basic", "openmp"} else "-O3"
        if not optimization or optimization[-1] != expected:
            raise ValueError(f"{kind} must use {expected}; use the current harness with GNU/Clang Release flags")
        if kind == "vectorized" and "-ffast-math" not in arguments:
            raise ValueError("Vectorized kernel is missing its -ffast-math flag")
        if kind in {"basic", "openmp"} and not any(arg in arguments for arg in ["-fno-tree-vectorize", "-fno-vectorize"]):
            raise ValueError(f"{kind} must retain the scalar baseline flags")
        flags[kind] = {"effective_optimization": expected, "command": shlex.join(arguments)}
    return flags


def write_deliverables_readme(out, config, best_threads):
    repetitions = config["repetitions"]
    (out / "README.md").write_text(f"""# Project 3 generated deliverables

Run mode: {'LOCAL VALIDATION — not Perlmutter results' if config['local'] else 'Perlmutter CPU compute-node run'}.
Check `status.json`: only `complete` means the pipeline finished successfully.

- `project_3_source.zip` and `code/`: portable source, CMake build file, run instructions,
  scripts, and correctness checks; no binaries or local build cache.
- `samples.csv`: all measured repetitions, with the warmup rows excluded.
- `summary.csv`: median/min/max/stdev runtime, throughput, speedup, and estimated bandwidth.
- `figures/`: the three assignment charts, each as PNG and PDF.
- `tables/`: bandwidth utilization, MFLOP/s, and both speedup baselines, in CSV/Markdown/LaTeX.
- `raw/`: every benchmark stdout/stderr including warmups, configure/build/test logs, and Slurm logs.
- `metadata/`: actual compiler flags, vectorization report, system/software details, and run configuration.
- `analysis.json`: fixed-team selection and metric definitions.
- `SHA256SUMS`: hashes of the generated assets and sources (live logs/status files excluded).

## Methodology

All seven configurations are run sequentially on the same exclusive CPU node,
with {repetitions} repetitions each. Per-size statistics use the median of those
repetitions. Each executable repeats the first size for warmup; that extra row is
excluded. CBLAS is kept serial using `OMP_NUM_THREADS=1` for its timing runs plus
library-specific thread limits. OpenMP uses static scheduling, core places, and
spread binding. Initialization and verification are outside the kernel timer.

Only the current harness flags are used: basic/OpenMP `-O1` with vectorization
disabled; vectorized `-O3 -ffast-math`; the CBLAS wrapper uses Release `-O3`.
The linked BLAS library's optimization is determined by its own build. See
`metadata/compile_commands.json` for the exact command lines used.

Chart 2 uses `basic_serial_time / openmp_time`, matching the CP3 example in
Lecture 10, page 11. `speedup_vs_omp1` is also supplied for the strong-scaling
discussion. `summary.csv` includes speedup relative to the fastest serial
implementation as well. Ratios are never clipped to 1 or to the thread count.

Chart 3 uses one fixed team size, **{best_threads} threads**, selected by the
lowest geometric mean median runtime over all problem sizes. The same team size
is used throughout that chart; individual sizes can favor other team sizes.

FLOPs = `2*N*N`; MFLOP/s = FLOPs / seconds / 1e6.
Useful bytes = `8*(N*N + 3*N)` (read A and x once, read/write y once).
Estimated bandwidth = useful bytes / seconds / 1e9 GB/s.
Estimated utilization = 100 * estimated bandwidth / {config['peak_gbs']} GB/s.
The default whole-node denominator is 409.6 GB/s: two CPUs at 204.8 GB/s each,
derived from [NERSC's architecture specifications]({ARCHITECTURE_URL}#cpu-nodes).
The estimate is useful traffic, not measured DRAM traffic; caches, repeated reads,
NUMA placement, and prefetching can change physical traffic. Values above 100%
are retained, since cache-resident runs can exceed a DRAM bandwidth denominator.

Memory placement policy: {config['numa_policy']}. The original serial first-touch
initialization is preserved by default and recorded; `--interleave-memory` makes
an explicit alternative experiment rather than silently changing placement.

The report, platform/methodology discussion, interpretation of results, and any
presentation are still manual work. No report or invented conclusions are generated.
Figures and table snippets are ready to include in your own LaTeX report.

## Reproduce

From a fresh checkout/source archive on a Perlmutter login node:
`python3 code/run_benchmarks.py --account {config['account']}`.
Scheduling follows [NERSC's job documentation]({JOBS_URL}); modules follow the
[NERSC Python guide]({PYTHON_URL}). Review `metadata/run_config.json` for custom
sizes, repetition count, peak bandwidth, or memory-placement options used here.
""")


def checksum_assets(out):
    lines = []
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.name in {"SHA256SUMS", "status.json"} or path.suffix in {".log", ".tmp"}:
            continue
        lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + str(path.relative_to(out)))
    (out / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def run_pipeline(config):
    out, build = Path(config["output"]), Path(config["build"])
    write_json(out / "status.json", {"status": "running", "started_utc": timestamp()})
    try:
        os.environ["MPLCONFIGDIR"] = str(build / "matplotlib-cache")
        build.mkdir(parents=True, exist_ok=True)
        try:
            import matplotlib  # Fail before expensive benchmark work if plotting cannot run.
        except ImportError as error:
            raise RuntimeError("Matplotlib is unavailable. Load the NERSC python module or install code/requirements.txt.") from error
        env = benchmark_environment(1)
        command = ["cmake", "-S", str(out / "code"), "-B", str(build),
                   "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTING=ON",
                   "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"]
        if not config["local"]:
            command += ["-DCMAKE_C_COMPILER=cc", "-DCMAKE_CXX_COMPILER=CC"]
        command += config["cmake_args"]
        run_logged(command, out / "raw/configure.log", env)
        write_json(out / "metadata/kernel_flags.json", validate_build_flags(build))
        run_logged(["cmake", "--build", str(build), "-j", "4"], out / "raw/build.log", env)
        run_logged(["ctest", "--test-dir", str(build), "--output-on-failure"], out / "raw/correctness.log", env)
        record_environment(config, out, build)
        prefix = []
        if config["interleave_memory"]:
            if not shutil.which("numactl"):
                raise RuntimeError("--interleave-memory requires numactl")
            prefix = ["numactl", "--interleave=all"]
        samples = []
        for repetition in range(1, config["repetitions"] + 1):
            for kind, threads in CONFIGURATIONS:
                name = f"{label(kind, threads)}-repeat-{repetition}"
                print(f"Benchmarking {name}", flush=True)
                command = prefix + [str(build / f"benchmark-{kind}"), "--sizes", ",".join(map(str, config["sizes"]))]
                with (out / "raw" / (name + ".stdout.csv")).open("w") as stdout, \
                     (out / "raw" / (name + ".stderr.log")).open("w") as stderr:
                    subprocess.run(command, stdout=stdout, stderr=stderr,
                                   env=benchmark_environment(threads), check=True)
                text = (out / "raw" / (name + ".stdout.csv")).read_text()
                for row in parse_benchmark(text, config["sizes"]):
                    samples.append(dict(implementation=kind, threads=threads, repetition=repetition, **row))
                write_csv(out / "samples.csv", samples, SAMPLE_FIELDS)
        summary, best_threads = summarize(samples, config["sizes"], config["repetitions"], config["peak_gbs"])
        write_csv(out / "summary.csv", summary)
        write_json(out / "analysis.json", {
            "best_fixed_openmp_threads": best_threads,
            "selection": "lowest geometric mean of per-size median runtime",
            "chart_2_baseline": "basic serial (Lecture 10, page 11)",
            "bandwidth_kind": "minimum useful traffic estimate, not hardware counters",
            "useful_bytes": "8*(N*N+3*N)", "peak_bandwidth_gbs": config["peak_gbs"],
            "peak_source": ARCHITECTURE_URL + "#cpu-nodes", "matplotlib_version": matplotlib.__version__,
        })
        make_charts(summary, config["sizes"], best_threads, out / "figures", config["local"])
        make_tables(summary, config["sizes"], out / "tables")
        package_sources(out)
        write_deliverables_readme(out, config, best_threads)
        checksum_assets(out)
        write_json(out / "status.json", {"status": "complete", "finished_utc": timestamp(),
                                        "samples": len(samples), "best_fixed_openmp_threads": best_threads})
        print(f"Complete: {out}", flush=True)
    except Exception as error:
        write_json(out / "status.json", {"status": "failed", "failed_utc": timestamp(), "error": str(error)})
        raise


def batch_script(config, config_path):
    # Shell-quote all user-controlled paths/arguments. No directives interpolate paths.
    worker = shlex.join(["python3", str(Path(config["output"]) / "code/run_benchmarks.py"),
                         "--worker", str(config_path)])
    return ("#!/bin/bash -l\nset -euo pipefail\n"
            "module load cpu\nmodule load PrgEnv-gnu\nmodule load python\n"
            "export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1\n"
            "export OMP_DYNAMIC=FALSE\n"
            f"cd {shlex.quote(config['root'])}\n"
            "srun --nodes=1 --ntasks=1 --cpus-per-task=256 --cpu-bind=cores " + worker + "\n")


def submit(config, config_path):
    out = Path(config["output"])
    script = out / "metadata/job.sh"
    script.write_text(batch_script(config, config_path))
    command = ["sbatch", "--wait", "--parsable", "--nodes=1", "--ntasks=1",
               "--cpus-per-task=256", "--constraint=cpu", "--exclusive",
               "--account=" + config["account"], "--qos=" + config["qos"],
               "--time=" + config["walltime"], "--job-name=project3-deliverables",
               "--output=" + str(out / "raw/slurm.log"), str(script)]
    write_json(out / "status.json", {"status": "submitted", "submitted_utc": timestamp()})
    print("Submitting an exclusive CPU node; waiting for the job to finish.", flush=True)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    job_line = process.stdout.readline().strip()
    job_id = job_line.split(";")[0]
    if job_id.isdigit():
        write_json(out / "metadata/slurm_submission.json", {"job_id": job_id, "command": command})
        print(f"Slurm job {job_id}; monitor with squeue -j {job_id}. Log: {out / 'raw/slurm.log'}", flush=True)
    try:
        _, stderr = process.communicate()
    except KeyboardInterrupt:
        print(f"\nStopped waiting. Submitted job {job_id} can continue; use scancel {job_id} to cancel it.", file=sys.stderr)
        raise
    if process.returncode:
        status = json.loads((out / "status.json").read_text())
        if status["status"] != "failed":
            write_json(out / "status.json", {"status": "failed", "error": stderr.strip() or "Slurm job failed"})
        raise RuntimeError(f"Slurm job failed: {stderr.strip()}; inspect {out / 'raw/slurm.log'}")
    if json.loads((out / "status.json").read_text())["status"] != "complete":
        write_json(out / "status.json", {"status": "failed", "error": "Slurm ended without completing the pipeline"})
        raise RuntimeError("Slurm ended without a complete deliverables folder")
    print(f"Complete: {out}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account", default="m3930")
    parser.add_argument("--qos", default="regular")
    parser.add_argument("--time", dest="walltime", default="00:30:00")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--output", type=Path, default=ROOT / "deliverables")
    parser.add_argument("--peak-bandwidth-gbs", dest="peak_gbs", type=float, default=409.6)
    parser.add_argument("--interleave-memory", action="store_true")
    parser.add_argument("--local", action="store_true", help="Run locally for validation; skip Slurm/modules")
    parser.add_argument("--sizes", default=",".join(map(str, SIZES)), help="Comma-separated dimensions (defaults are assignment sizes)")
    parser.add_argument("--cmake-arg", dest="cmake_args", action="append", default=[])
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        run_pipeline(json.loads(args.worker.read_text()))
        return
    try:
        sizes = [int(item) for item in args.sizes.split(",")]
    except ValueError:
        parser.error("--sizes must contain comma-separated positive integers")
    if not sizes or any(n <= 0 or n > 2147483647 for n in sizes) or len(set(sizes)) != len(sizes):
        parser.error("--sizes must contain distinct positive 32-bit integers")
    if args.repetitions < 1 or not math.isfinite(args.peak_gbs) or args.peak_gbs <= 0:
        parser.error("Repetitions and peak bandwidth must be positive")
    if not args.local and os.environ.get("SLURM_JOB_ID"):
        parser.error("Start the default command on a login node, outside an existing allocation")
    if not args.local and not shutil.which("sbatch"):
        parser.error("sbatch is unavailable; run on Perlmutter or use --local for validation")
    out = args.output.resolve()
    if out.exists():
        parser.error(f"Output already exists: {out}. Use --output deliverables_run2 to preserve earlier results.")
    out.mkdir(parents=True)
    for directory in ["raw", "metadata", "figures", "tables"]:
        (out / directory).mkdir()
    source_snapshot(ROOT, out / "code")
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + f"-{os.getpid()}"
    config = {**vars(args), "output": str(out), "root": str(ROOT), "sizes": sizes,
              "build": str(ROOT / "build/pipeline" / run_id), "worker": None,
              "numa_policy": "interleave all NUMA nodes" if args.interleave_memory else "original serial first-touch initialization"}
    config_path = out / "metadata/run_config.json"
    write_json(config_path, config)
    if args.local:
        run_pipeline(config)
    else:
        submit(config, config_path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

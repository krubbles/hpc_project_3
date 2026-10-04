import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location("runner", Path(__file__).resolve().parents[1] / "run_benchmarks.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def benchmark_csv(sizes=(1024, 2048)):
    result = "# kernel description\nn,seconds,flops,mflops,verified,warmup\n"
    for index, n in enumerate([sizes[0]] + list(sizes)):
        result += f"{n},0.25,{2*n*n},{2*n*n/0.25/1e6},PASS,{int(index == 0)}\n"
    return result


def samples():
    result = []
    durations = {("blas", 1): 3, ("basic", 1): 8, ("vectorized", 1): 2,
                 ("openmp", 1): 4, ("openmp", 4): 1, ("openmp", 16): 2, ("openmp", 64): 3}
    for (kind, threads), seconds in durations.items():
        for n in [1024, 2048]:
            for repetition, factor in enumerate([0.5, 1, 4], 1):
                result.append(dict(implementation=kind, threads=threads, n=n,
                                   repetition=repetition, seconds=seconds*factor))
    return result


class PipelineTests(unittest.TestCase):
    def test_csv_warmup_and_integrity(self):
        self.assertEqual([row["n"] for row in runner.parse_benchmark(benchmark_csv(), [1024, 2048])], [1024, 2048])
        invalid = [benchmark_csv().replace("PASS", "FAIL", 1),
                   "\n".join(benchmark_csv().splitlines()[:-1]),
                   benchmark_csv().replace("0.25", "nan"),
                   benchmark_csv().replace("2097152", "2097153"),
                   benchmark_csv().replace("PASS,0", "PASS,1"),
                   benchmark_csv().replace("8.388608", "99")]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                runner.parse_benchmark(text, [1024, 2048])

    def test_median_metrics_and_fixed_team_selection(self):
        summary, best = runner.summarize(samples(), [1024, 2048], 3, 409.6)
        row = next(row for row in summary if row["implementation"] == "openmp" and row["threads"] == 4 and row["n"] == 1024)
        self.assertEqual(best, 4)
        self.assertEqual(row["median_seconds"], 1)
        self.assertEqual(row["speedup_vs_basic"], 8)
        self.assertEqual(row["speedup_vs_omp1"], 4)
        self.assertEqual(row["speedup_vs_best_serial"], 2)
        self.assertEqual(row["flops"], 2*1024**2)
        self.assertEqual(row["useful_bytes"], 8*(1024**2+3*1024))
        self.assertAlmostEqual(row["estimated_peak_bandwidth_percent"], 100*row["useful_bytes"]/1e9/409.6)

    def test_incomplete_or_duplicate_samples_fail(self):
        for data in [samples()[:-1], samples()+[samples()[0]]]:
            with self.subTest(data=len(data)), self.assertRaises(ValueError):
                runner.summarize(data, [1024, 2048], 3, 409.6)

    def test_serial_blas_thread_limits(self):
        environment = runner.benchmark_environment(64)
        self.assertEqual(environment["OMP_NUM_THREADS"], "64")
        self.assertEqual(environment["OPENBLAS_NUM_THREADS"], "1")
        self.assertEqual(environment["MKL_NUM_THREADS"], "1")
        self.assertEqual(runner.benchmark_environment(1)["OMP_NUM_THREADS"], "1")

    def test_tables_and_zip_are_portable(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            runner.source_snapshot(runner.ROOT, out / "code")
            runner.package_sources(out)
            with runner.zipfile.ZipFile(out / "project_3_source.zip") as archive:
                names = archive.namelist()
                self.assertIn("project_3/code/CMakeLists.txt", names)
                self.assertIn("project_3/code/run_benchmarks.py", names)
                self.assertFalse(any("CMakeCache" in name or "/build/" in name for name in names))
            summary, _ = runner.summarize(samples(), [1024, 2048], 3, 409.6)
            runner.make_tables(summary, [1024, 2048], out)
            latex = (out / "bandwidth_utilization.tex").read_text()
            self.assertIn("N & blas & basic & vectorized & omp-1 & omp-4 & omp-16 & omp-64 \\\\", latex)
            self.assertIn("\\caption{", latex)

    def test_shell_quoting_and_full_cpu_node(self):
        config = {"root": "/tmp/source's directory; false", "output": "/tmp/output's directory"}
        script = runner.batch_script(config, Path("/tmp/config's file.json"))
        result = subprocess.run(["bash", "-n"], input=script, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--cpus-per-task=256", script)
        self.assertIn("--cpu-bind=cores", script)
        self.assertIn("module load PrgEnv-gnu", script)

    def test_actual_compilation_flags_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            commands = []
            for kind in ["basic", "vectorized", "openmp", "blas"]:
                flags = "-O3 -O1 -fno-tree-vectorize" if kind in {"basic", "openmp"} else "-O3"
                if kind == "vectorized":
                    flags += " -ffast-math"
                commands.append({"file": f"dgemv-{kind}.cpp", "command": f"g++ {flags} -c dgemv-{kind}.cpp"})
            path = build / "compile_commands.json"
            path.write_text(json.dumps(commands))
            self.assertEqual(runner.validate_build_flags(build)["basic"]["effective_optimization"], "-O1")
            commands[0]["command"] += " -O3"
            path.write_text(json.dumps(commands))
            with self.assertRaises(ValueError):
                runner.validate_build_flags(build)

    def test_worker_failure_leaves_failed_status(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / "raw").mkdir()
            config = {"output": str(out), "build": str(out / "build"), "local": True, "cmake_args": []}
            with mock.patch.object(runner, "run_logged", side_effect=RuntimeError("Build failed")):
                with self.assertRaisesRegex(RuntimeError, "Build failed"):
                    runner.run_pipeline(config)
            self.assertEqual(json.loads((out / "status.json").read_text())["status"], "failed")
            self.assertFalse((out / "project_3_source.zip").exists())

    def test_slurm_submission_waits_and_checks_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / "metadata").mkdir()
            (out / "raw").mkdir()
            config = dict(root=str(out), output=str(out), account="m3930", qos="regular", walltime="00:30:00")
            process = mock.Mock(stdout=io.StringIO("12345\n"), returncode=0)
            def finish():
                runner.write_json(out / "status.json", {"status": "complete"})
                return "", ""
            process.communicate.side_effect = finish
            with mock.patch.object(runner.subprocess, "Popen", return_value=process) as launch:
                runner.submit(config, out / "metadata/run_config.json")
            command = launch.call_args.args[0]
            self.assertIn("--wait", command)
            self.assertIn("--exclusive", command)
            self.assertIn("--cpus-per-task=256", command)
            self.assertEqual(json.loads((out / "metadata/slurm_submission.json").read_text())["job_id"], "12345")
            process.stdout = io.StringIO("12346\n")
            process.communicate.side_effect = None
            process.communicate.return_value = ("", "")
            with mock.patch.object(runner.subprocess, "Popen", return_value=process):
                with self.assertRaisesRegex(RuntimeError, "without a complete"):
                    runner.submit(config, out / "metadata/run_config.json")
            self.assertEqual(json.loads((out / "status.json").read_text())["status"], "failed")


if __name__ == "__main__":
    unittest.main()

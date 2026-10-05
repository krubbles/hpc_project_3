#!/usr/bin/env python3
"""Build and collect benchmark output in one Perlmutter CPU job."""
import argparse
from pathlib import Path
import shutil
import subprocess

# parent is code, parent of parent is root
ROOT = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "deliverables")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True)

    job = out / "job.sh"
    shutil.copy2(ROOT / "code/run_benchmarks.sh", job)

    print(f"Submitting job. out = {out}", flush=True)
    subprocess.run([
        "sbatch", "--wait", "--nodes=1", "--ntasks=1", "--cpus-per-task=256",
        "--constraint=cpu", "--exclusive", "--account=m3930",
        "--qos=regular", "--time=00:30:00", "--job-name=project3-benchmarks",
        f"--output={out / 'slurm.log'}", str(job),
        str(ROOT / "code"), str(out),
    ], check=True)
    print(f"Done: {out}")


if __name__ == "__main__":
    main()

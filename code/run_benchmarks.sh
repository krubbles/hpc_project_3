#!/bin/bash -l
set -e
module load cpu PrgEnv-gnu
cd "$2"
cmake -S "$1" -B build -DCMAKE_C_COMPILER=cc -DCMAKE_CXX_COMPILER=CC
cmake --build build
cd build
OMP_NUM_THREADS=1 ./benchmark-basic > ../basic.txt
OMP_NUM_THREADS=1 ./benchmark-vectorized > ../vectorized.txt
OMP_NUM_THREADS=1 ./benchmark-blas > ../blas.txt
bash job-openmp > ../openmp.txt

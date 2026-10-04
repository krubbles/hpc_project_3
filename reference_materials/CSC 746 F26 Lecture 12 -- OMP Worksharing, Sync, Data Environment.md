# CSC 746 F26 Lecture 12 -- OMP Worksharing, Sync, Data Environment

Source: [CSC 746 F26 Lecture 12 -- OMP Worksharing, Sync, Data Environment.pdf](<CSC 746 F26 Lecture 12 -- OMP Worksharing, Sync, Data Environment.pdf>)

Pages: 63

Extracted with `pdftotext -layout`. Page numbers match the PDF. Text blocks preserve spacing for code, tables, and columns. Diagrams, plotted data, and equations may need inspection in the original PDF.

Apple Vision OCR supplements include recognized lines absent from the PDF text layer. These are search aids and may contain recognition errors; verify code, formulas, and numbers against the PDF.

## Page 1: CSC 746: High Performance Computing

```text
 CSC 746: High Performance Computing
OMP Worksharing, Sync, Data Environment
                 1 Oct 2026




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
Serial Reductions and Vectorization

Parallel Reductions

Example: Parallel Computation of Pi in OpenMP

OpenMP Parallel Loops, Worksharing

OpenMP Data Environment




                                                Copyright © 2026, E. Wes Bethel   2
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 3: Serial: Reductions and Vectorization

```text
Serial: Reductions and Vectorization



                            Copyright © 2026, E. Wes Bethel   3
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 4: Code 1: Simple reduction                      On Perlmutter:

```text
Code 1: Simple reduction                      On Perlmutter:
                                              module load cpu

Function signature: int sum(int N, int A[])   To compile the code manually:
                                              g++ -O2 -ftree-vectorize
Arguments:                                    -fopt-info-vec-all=report.txt -c
                                              foo.cpp
 ●   N is the number of items to process
 ●   A[] is an array of ints
Code objective: compute the sum of all A[i]
and return that sum
Compile the code with flags to enable
automatic vectorization
Submit: cut-paste of your code, the report

                                                    Copyright © 2026, E. Wes Bethel   4
```

### OCR supplement (verify against PDF)

```text
Function signature: int sum(int N, int AI)
• Al] is an array of ints
SAN FRANCISCO
STATE UNIVERSITY
g++ -02 -ftree-vectorize
```

## Page 5: Code to sum up A[] (left)

```text
Code to sum up A[] (left)

Vectorization report (below)

Did the loop vectorize?




         Copyright © 2026, E. Wes Bethel   5
```

### OCR supplement (verify against PDF)

```text
2 int sum_a(int N, int A[])
int sum-0;
for (int i=0;i<N;i++)
sum += A[i];
return sum;
Code to sum up AI (left)
9
10
39 [SFSU/openmp_examples] % g++-13 -03 -fopt-info-vec-all -c ./vectorization.cpp
./vectorization.cpp:6:18: optimized: loop vectorized using 16 byte vectors
/vectorization.cpp:2:5: note: vectorized 1 loops in function.
./vectorization.cpp:9:11: note: ***** Analysis failed with vector mode V4SI
./vectorization.cpp:9:11: note: ***** Skipping vector mode V16QI, which would repeat t
he analysis for V4SI
-SAN 7RANGSC
STATE UNIVERSITY
```

## Page 6: On Perlmutter:

```text
                                                                   On Perlmutter:
Code 2: Row reduction – vectorized                                 module load cpu

Function signature: void sum(int N, int A[], int Y[])              To compile the code manually:
                                                                   g++ -O2 -ftree-vectorize
Arguments:                                                         -fopt-info-vec-all=report.txt -c
                                                                   foo.cpp
 ●    N is the number of items to process
 ●    A[] is an array of ints of length NxN (like CP3)
 ●    Y[] is an array of ints of length N

Code objective: each Y[i] is the sum of all items in each row of
A[i:*]

This code has two nested loops

Compile the code with automatic vectorization enabled, examine
the vectorization report

Submit: cut-paste of the code, cut-paste of the report.txt


                                                                               Copyright © 2026, E. Wes Bethel   6
```

### OCR supplement (verify against PDF)

```text
Function signature: void sum(int N, int AI, int YD)
• AI] is an array of ints of length NxN (like CP3)
• YI is an array of ints of length N
А[i:*]
SAN FRANCISCO
STATE UNIVERSITY
g++ -02 -ftree-vectorize
too.cpp
```

## Page 7: Code to sum up rows of A[i,*],

```text
Code to sum up rows of A[i,*],
place result into Y[i]

Vectorization report (below)

Did the loop vectorize?

How do we fix the code so it will
vectorize?




                     Copyright © 2026, E. Wes Bethel   7
```

### OCR supplement (verify against PDF)

```text
12 void sum_row(int N, int AL], int Y[])
13
14
15
16
17
18
19
21
22
// Assume A is NxN 1D array, Y[] is Nx1 1D array
// Objective here is to sum each row of A[i,*] and place result in Y[i]
for (int row=0; row<N; row++) f
Y[row] = ø;
for (int col=0; col<N; col++)
Y[row] += A[row*N + col];
./vectorization.cpp:17:23: missed: couldn't vectorize loop
./vectorization.cpp:20:33: missed: not vectorized: complicated access pattern.
./vectorization.cpp:19:26: missed: couldn't vectorize loop
./vectorization.cpp:20:17: missed: not vectorized: complicated access pattern.
./vectorization.cpp:12:6: note: vectorized 0 loops in function.
./vectorization.cpp:22:1: note: ***** Analysis failed with vector mode V4SI
/vectorization.cpp:22:1: note: ***** Skipping vector mode V16QI, which would repeat t
he analysis for V4SI
```

## Page 8: Code to sum up rows of A[i,*],

```text
Code to sum up rows of A[i,*],
place result into Y[i]

Vectorization report (below)

Did the loop vectorize?

What happened?




                    Copyright © 2026, E. Wes Bethel   8
```

### OCR supplement (verify against PDF)

```text
24 void sum_row_v2(int N, int AL], int Y[])
25
27
// Assume A is NxN 1D array, Y[] is Nx1 1D array
// Objective here is to sum each row of A[i,*] and place result in Y[i]
28
29
30
31
32
33
for (int row=0; row<N; row++) {
int accum = 0;
for (int col-0; col<N; col++)
accum += A[row*N + col1;
Y[row] = accum;
34
35
./vectorization.cpp:29:23: missed: couldn't vectorize loop
./vectorization.cpp:32:32: missed: not vectorized: complicated access pattern.
./vectorization.cpp:31:26: optimized: loop vectorized using 16 byte vectors
./vectorization.cpp:24:6: note: vectorized 1 loops in function.
./vectorization.cpp:35:1: note: ***** Analysis failed with vector mode V4SI
./vectorization.cpp:35:1: note: ***** Skipping vector mode V16QI, which would repeat t
he analysis for V4SI
```

## Page 9: g++ -O2 -ftree-vectorize -fopt-info-vec-all -c svs.cpp

```text
                            g++ -O2 -ftree-vectorize -fopt-info-vec-all -c svs.cpp
Vectorization Report Output Shows Use of SSE
Instructions




                                                      Copyright © 2026, E. Wes Bethel   9
```

### OCR supplement (verify against PDF)

```text
g++ -02 -ftree-vectorize -fopt-info-vec-all -c svs.cpp
10
11 int64_t
12 sum(int64_t N, uint64_t AL1)
13 {
14 //
15
16
17
18
for (i=0;i<N;i++)
accum += A[il;
19
return accum;
21
printf(" inside sum_vector perform_sum, N=%lld \n", N);
int64_t i, accum=0;
Iwes@perlmutter: Login08:
g++ -02 -ftree-vectorize -fopt-info-vec-all -c svs.cpp
svs.cpp:17:14: optimized: loop vectorized using 16 byte vectors
svs.cpp:12:1: note: vectorized 1 loops in function.
svs.cpp:20:11: note:
***** Analysis failed with vector mode V2DI
svs.cpp:20:11: note:
***** Skipping vector mode V16QI, which would repeat the analysis for VZDI
/opt/cray/pe/gcc/11.2.ø/snos/include/g++/iostream:74:25: missed: statement clobbers memory: std::ios_base::Init::Ini
t (&__ioinit);
/opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: statement clobbers memory: __cxxabiv1::__cxa_atexit
(__dt_comp , &__ioinit, &__dso_handle);
svs.cpp:21:1: note: ***** Analysis failed with vector
mode VOID
```

## Page 10: g++ -O2 -march=native -ftree-vectorize -fopt-info-vec-all -c svs.cpp

```text
                    g++ -O2 -march=native -ftree-vectorize -fopt-info-vec-all -c svs.cpp

Vectorization Report Output Shows Use of AVX/AVX2
Instructions




                                                            Copyright © 2026, E. Wes Bethel   10
```

### OCR supplement (verify against PDF)

```text
g++ -02 -march=native -ftree-vectorize -fopt-info-vec-all -c svs.cpp
11 int64_t
12
sum(int64_t N,
uint64_t A[])
14 //
15
16
17
18
19
21 }
printf(" inside sum_vector perform_sum, N=%lld \n", N);
int64_t i, accum=0;
for (i=0;i<N;i++)
ассum += A[il;
return accum;
wes@perlmutter:login08:
g++ -02 -march=native -ftree-vectorize -fopt-info-vec-all -c svl
/s.cpp:17:14: optimized: loop vectorized using 32 byte vectors
/s.cpp:12:1: note: vectorized 1 loops in function.
svs.cpp:20:11: note: ***** Analysis failed with vector mode V4DI
svs.cpp:20:11: note: ***** Skipping vector mode V32QI, which would repeat the analysis for V4DI
/opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: statement clobbers memory: std::ios_base::Init::Ini
t (&__ioinit);
/opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: statement clobbers memory: __cxxabiv1::__cxa_atexit
(__dt_comp , &__ioinit, &_dso_handle);
svs.cpp:21:1: note: ***** Analysis failed with vector mode VOID
```

## Page 11: Parallel Reductions

```text
Parallel Reductions



                      Copyright © 2026, E. Wes Bethel   11
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 12: Direct Sum Reduction – Concurrency and Independence

```text
Direct Sum Reduction – Concurrency and Independence
The sum operator is associative:

A + B + C + D = (A+B) + (C+D)

So we may safely compute subsets of
the sum in any order then add them
together.

E.g.:




                                        Copyright © 2026, E. Wes Bethel   12
```

### OCR supplement (verify against PDF)

```text
E.9•
Ёan-ŽAn+Ề
i=n/271
A[ż]
20 int64_t
21
22
23
24
25
27
28
29 }
sum(int64_t N, uint64_t A[])
int64_t 1, accum=0;
for (i=0;i<N; i++)
accum += i;
return accum;
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 13: Direct Sum Reduction – Implementing parallelism

```text
Direct Sum Reduction – Implementing parallelism
In OpenMP:
#pragma omp parallel
Defines a region of code that will run in
parallel
#pragma omp for
Defines a worksharing construct, ie, a
way to divide up the problem
Can combine them in one line as shown
here on L25

                                            Copyright © 2026, E. Wes Bethel   13
```

### OCR supplement (verify against PDF)

```text
21
22
23
24
27
28
29
30
int64_t
sum(int64_t N, uint64_t A[])
int64_t i, accum=0;
#pragma omp parallel for
for (i=0; i‹N; i++)
accum += i;
return accum;
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 14: Direct Sum Reduction – Hazards?

```text
Direct Sum Reduction – Hazards?
In this code, there is a data race
condition on L27

A data race occurs when more than 1
thread of execution is attempting to
write to a given location (register,
memory location)

The last one doing the write is the one
that wins



                                          Copyright © 2026, E. Wes Bethel   14
```

### OCR supplement (verify against PDF)

```text
21
int64_t
sum(int64_t N, uint64_t A[])
22
23
int64_t i, accum=0;
24
25
#pragma omp parallel for
for (i=0;i‹N; i++)
accum += i;
28
29
return accum;
30
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 15: Option #1 for working around race conditions

```text
Option #1 for working around race conditions
Solution:
Use a “critical section” so that
only one thread at a time may
perform the write to the variable
“accum”
Correctness: produces the correct
answers
Pitfalls: defeats parallelism, this
code is effectively serial

                                           Copyright © 2026, E. Wes Bethel   15
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
19
20 int64_t
21 sum(int64_t N, uint64_t A[])
22
23
int64_t i, accum=0;
24
25 #pragma omp parallel for
for (i=0;i<N;i++)
27
#pragma omp critical
28
accum += i;
29
30
return accum;
31
32
```

## Page 16: Option #2 for working around race conditions

```text
Option #2 for working around race conditions
Solution: each thread uses a different
location in a shared array to store partial
results

Correctness: produces the correct answer

Pitfalls: while there is no critical section,
there is the potential for false sharing that
will result in poor performance (poor
scalability)



                                                Copyright © 2026, E. Wes Bethel   16
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
20 int64_t
21
um(int64_t N, uint64_t A[])
22 1
23
int64_t i, accum=0;
24
#define MAX_THREADS 8
25
int64_t accum_buffer[MAX_THREADS] = {};
27 #pragma omp parallel
28
29
int my_thread = omp_get_thread_num();
30
31
32
33
#pragma omp for
for (i=0;i<N;i++)
accum_buffer[my_thread] += i;
34
35
36
37
or (i=0;i<MAX_THREADS;i++)
ccum += accum_buffer[i];
38
39
return accum;
40
41
```

## Page 17: Option #3 for working around race conditions

```text
Option #3 for working around race conditions
Solution: use thread-local storage for local
computations, then combine the partial
results in parallel using a critical section
Correctness: produces the correct answer
Pitfalls: while there is a critical section, it is
entered only once by each thread after all
other computations are finished
This approach is the best solution for this
particular problem: minimizes serialization,
no false sharing

                                                     Copyright © 2026, E. Wes Bethel   17
```

### OCR supplement (verify against PDF)

```text
19
20 int64_t
21
sum(int64_t N, uint64_t A[])
22 1
23
int64_t i, accum=0;
24
25
#pragma omp parallel
27
int64_t tls=0;
28
29
#pragma omp for
30
for (i=0;i<N;i++)
31
tls += i;
32
33 #pragma omp critical
34
accum += tls;
35
36
37
return
SAN FRANCISCO
accum;
STATE UNIVERSITY
38
39
```

## Page 18: Option #3 for working around race conditions

```text
Option #3 for working around race conditions
Solution: use thread-local storage for local
computations, then combine the partial
results in parallel using a critical section
Correctness: produces the correct answer
                         These 3 options are all manual solutions.
Pitfalls: while there is a critical section, it is
entered only once byOpenMP      has built-in
                         each thread         support
                                         after  all for reduction
                         operations so there are more options
other computations are     finishedavailable to you.
This approach is the best solution for this
                    #pragma omp parallel for reduction(+:foo)
particular problem: minimizes serialization,
no false sharing

                                                                     Copyright © 2026, E. Wes Bethel   18
```

### OCR supplement (verify against PDF)

```text
19
20 int64_t
21
sum(int64_t N, uint64_t A[])
22
23
int64_t i, accum=0;
24
OpenMP has built-in support for reduction
SAN FRANCISCO
STATE UNIVERSITY
35
36
37
38
39
int64_t tls=0;
agma omp for
for (i=0;i<N;i++)
tls += i;
agma omp critical
accum += tls;
return
accum;
```

## Page 19: Example: Parallel Computation of 𝛑

```text
Example: Parallel Computation of 𝛑




                            Copyright © 2026, E. Wes Bethel   19
```

### OCR supplement (verify against PDF)

```text
Example: Parallel Computation of f
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 20: Image credit: Tim Mattson, Intel

```text
                                                        Image credit: Tim Mattson, Intel




Computing 𝛑




              Image credit: Tim Mattson, Intel   Copyright © 2026, E. Wes Bethel     20
```

### OCR supplement (verify against PDF)

```text
Computing n
SAN FRANCISCO
STATE UNIVERSITY
4.0
0.0
Mathematically, we know that:
4.0
(1+х2)
dx = П
We can approximate the
integral as a sum of
rectangles:
, F(x)ДX ~ П
İ=0
Where each rectangle has
width Ax and height F(xi) at
the middle of interval i.
```

## Page 21: Image credit: Kathy Yelick,

```text
                     Image credit: Kathy Yelick,
                     UCB, and Tim Mattson, Intel



Computing 𝛑




              Copyright © 2026, E. Wes Bethel      21
```

### OCR supplement (verify against PDF)

```text
Computing n
static long num_steps = 100000;
double step;
void main ()
int i;
double x, pi, sum = 0.0;
step = 1.0/(double) num_steps;
x = 0.5 * step;
for (i=0;i<= num_steps; i++){
×+=step;
sum += 4.0/(1.0+x*x);
pi = step * sum;
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 22: Image credit: Kathy Yelick,

```text
                                  Image credit: Kathy Yelick,
                                  UCB, and Tim Mattson, Intel


Identify Concurrency




                       Copyright © 2026, E. Wes Bethel    22
```

### OCR supplement (verify against PDF)

```text
Loop iterations
can in principle
be executed
concurrently
static long num_steps = 100000;
double step;
void main ()
int i;
double x, pi, sum = 0.0;
step = 1.0/(double) num_steps;
x = 0.5 * step;
for (i=0;i<= num_steps; i++){
×+=step;
sum += 4.0/(1.0+x*x);
pi = step * sum;
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 23: Image credit: Kathy Yelick,

```text
                                  Image credit: Kathy Yelick,
                                  UCB, and Tim Mattson, Intel


Identify Concurrency




                              Would this loop
                               vectorize??




                       Copyright © 2026, E. Wes Bethel    23
```

### OCR supplement (verify against PDF)

```text
static long num_steps = 100000;
double step;
void main ()
int i;
double x, pi, sum = 0.0;
Loop iterations
can in principle
be executed
concurrently
step = 1.0/(double) num_steps;
x = 0.5 * step;
for (i=0;i<= num_steps; i++){
x+=step;
sum += 4.0/(1.0+x*x);
pi = step * sum;
But is the loop as
written safe for
parallel execution?
```

## Page 24: Image credit: Kathy Yelick,

```text
                                    Image credit: Kathy Yelick,
                                    UCB, and Tim Mattson, Intel


Expose Concurrency (1)

    Partition




                         Copyright © 2026, E. Wes Bethel    24
```

### OCR supplement (verify against PDF)

```text
data
that must be
shared from
data local to
a task
static long num_steps = 100000;
double step;
void main ()
double pi, sum = 0.0;
step = 1.0/(double) num_steps;
This is called a reduction
... results from each
iteration accumulated
into a single global.
int i; double x;
for (i=0;k<= num_steps; i++)
x = (i+0.5)*step;
sum += 4.0/(1.0+x*x);
pi = step * sum;
Redefine x to
remove loop
carried
dependence
```

## Page 25: Image credit: Kathy Yelick,

```text
                                    Image credit: Kathy Yelick,
                                    UCB, and Tim Mattson, Intel


Expose Concurrency (2)




                         Copyright © 2026, E. Wes Bethel    25
```

### OCR supplement (verify against PDF)

```text
Deal with the
reduction
static long num_steps = 100000;
#define NUM 4 //expected max thread count
double step;
void main ()
double pi, sum[NUM] = {0.0};
step = 1.0/(double) num_steps;
Note: this is a serial program
... but l've now exposed the
concurrency so it can be
safely exploited in a parallel
execution.
int i, ID=0; double x;
for (i=0;i<= num_steps; i++){
x = (i+0.5)*step;
sum[ID] += 4.0/(1.0+x*x);
for(int i=0, pi=0.0;i<NUM;i++)
pi += step * sum[i];
Common Trick: privatize
variable (sum) by
promoting a scalar to an
array indexed by the
number of threads
Need to add up
partial sums
```

## Page 26: Image credit: Kathy Yelick,

```text
                                                Image credit: Kathy Yelick,
                                                UCB, and Tim Mattson, Intel


Express Concurrency




                      Note: creating NUM threads inside
                      your program is not good practice.
                      Specify concurrency outside your
                      program in an environment
                      variable.    Copyright © 2026, E. Wes Bethel      26
```

### OCR supplement (verify against PDF)

```text
SPMD
This style of
parallelism is called
ẠỊạồsingle program
multiple data"
(fixed number of
threads execute
same code,
independently)
#include <omp.h>
static long num_steps = 100000;
#define NUM 4
double step;
void main ()
double pi, sum[NUM] = {0.0};
step = 1.0/(double) num_steps;
#pragma omp parallel num_threads(NUM)*
int i, ID; double x;
ID = omp_get_thread_num();
for (i=ID;i<= num_steps; i+=NUM){
x = (i+0.5)*step;
sum[ID] += 4.0/(1.0+x*x);
Create NUM threads
Each thread executes code in the
parallel block
Simple mod to loop to deal out
iterations to threads
for(int i=0, pi=0.0;i<NUM;i++)
pi += step * sum[i];
```

## Page 27: Image credit: Kathy Yelick,

```text
                                                Image credit: Kathy Yelick,
                                                UCB, and Tim Mattson, Intel


Express Concurrency




                      Note: creating NUM threads inside
                      your program is not good practice.
                      Specify concurrency outside your
                      program in an environment
                      variable.    Copyright © 2026, E. Wes Bethel      27
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
static long num_steps = 100000;
#define NUM 4
double step;
void main ()
double pi, sum[NUM] = {0.0};
step = 1.0/(double) num_steps;
#pragma omp parallel num_threads(NUM)
variables declared
inside a thread are
private to that
int i, ID; double x;
ID = omp_get_thread_num();
for (i=ID;i<= num_steps; i+=NUM){
x = (i+0.5)*step;
sum[ID] += 4.0/(1.0+x*x);
automatic variables
declared outside a
parallel region are
shared between threads
Create NUM threads
Each thread executes code in the
parallel block
Simple mod to loop to deal out
iterations to threads
for(int i=0, pi=0.0;i<NUM;i++)
pi += step * sum[i];
```

## Page 28: Image credit: Kathy Yelick,

```text
                                                Image credit: Kathy Yelick,
                                                UCB, and Tim Mattson, Intel


Express Concurrency




                      Note: creating NUM threads inside
                      your program is not good practice.
                      Specify concurrency outside your
                      program in an environment
                      variable.    Copyright © 2026, E. Wes Bethel      28
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
static long num_steps = 100000;
#define NUM 4
double step;
void main ()
double pi, sum[NUM] = {0.0};
step = 1.0/(double) num_steps;
#pragma omp parallel num_threads(NUM)*
variables declared
inside a thread are
private to that
int i, ID; double x;
ID = omp_get_thread_num();
for (i=ID;i<= num_steps; i+=NUM){
x = (i+0.5)*step;
sum[ID] += 4.0/(1.0+x*x);
Where's
the bug?
for(int i=0, pi=0.0;i<NUM;i++)
pi += step * sum[i];
automatic variables
declared outside a
parallel region are
shared between threads
Create NUM threads
Each thread executes code in the
parallel block
Simple mod to loop to deal out
iterations to threads
```

## Page 29: Image credit: Kathy Yelick,

```text
                                 Image credit: Kathy Yelick,
                                 UCB, and Tim Mattson, Intel


Express Concurrency




                      Copyright © 2026, E. Wes Bethel    29
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
static long num_steps = 100000;
#define NUM 4
double step;
void main ()
double pi, sum[NUM] = {0.0};
step = 1.0/(double) num_steps;
#pragma omp parallel num_threads(NUM)
int nthreads = omp_get_num_threads();
int i, ID;
double x;
ID = omp_get_thread_num();
for (i=ID;i<= num_steps; i+=nthreads){
x = (i+0.5)*step;
sum[ID] += 4.0/(1.0+x*x);
for(int i=0, pi=0.0;i<NUM;i++)
pi += step * sum[i];
SAN FRAN
STATE UNIVI
NUM is a requested
number of threads,
but an OS can choose
to give you fewer.
Hence, you need to
add a bit of code to
get the actual
number of threads
Nes Bethel
```

## Page 30: Image credit: Kathy Yelick,

```text
                                            Image credit: Kathy Yelick,
                                            UCB, and Tim Mattson, Intel



𝛑 Program: performance results




                                 Copyright © 2026, E. Wes Bethel    30
```

### OCR supplement (verify against PDF)

```text
л Program: performance results
5
4
Speedup
• Original Serial pi program with 100000000 steps ran in 1.83 seconds.
OpenMP Pi Array + Serial sum
threads
1
- Serial sum
-- - Ideal
4
Serial Sum
1.86
1.03
1.08
0.97
Speedup
1.8x
1.7x
1.9x
1
4
Why is the performance so poor?
*Intel compiler (icpc) with no optimization on Apple OS X 10.7.3 with a dual core (four HW
thread) Intel® Core™ i5 processor at 1.7 Ghz and 4 Gbyte DDR3 memory at 1.333 Ghz.
17
```

## Page 31: Image credit: Kathy Yelick,

```text
                                              Image credit: Kathy Yelick,
                                              UCB, and Tim Mattson, Intel



𝛑 Program Performance Bottleneck




                                   Copyright © 2026, E. Wes Bethel    31
```

### OCR supplement (verify against PDF)

```text
л Program Performance Bottleneck
False sharing: Independent variables sit on the same cache line, each update will
cause the cache lines to "slosh back and forth" between threads
HW thrd. 0
HW thrd. 1
HW thrd. 2
HW thrd. 3
L1 $ lines
Sum[0] sum[1] Sum[2]| Sum[3]
L1 $ lines
Sum[0]| Sum[1] Sum[2]
Sum[З]
Core 0
Core 1
Shared last level cache and connection to I/O and DRAM
• Privatized scalars into an array to support parallelism... Writes to
contiguous elements result in poor scalability.
• Solution: Pad arravs so elements vou use are on distinct cache lines.
```

## Page 32: Image credit: Kathy Yelick,

```text
                                                            Image credit: Kathy Yelick,
                                                            UCB, and Tim Mattson, Intel



𝛑 Program Performance Bottleneck
                  Q: How large is the an L1 cache line on the AMD
                  Milan?
                  A: 64 bytes

                  #define CACHE_LINE_SIZE 64
                  double sum[Nthreads * CACHE_LINE_SIZE]

                  # pragma omp parallel for
                  for i:0,N
                         sum[i*CACHE_LINE_SIZE] = compute(i);




                                                 Copyright © 2026, E. Wes Bethel    32
```

### OCR supplement (verify against PDF)

```text
л Program Performance Bottleneck
False sharing: Independent varia
cause the cache lines to "slosh b
HW thrd. 0
HW thrd. 1
L1 $ lines
Sum[0] Sum[1] Sum[2] Sum
for i:O,N
Core 0
Shared last level cache ar
• Privatized scalars into an array to support parallelism... Writes to
contiguous elements result in poor scalability.
• Solution: Pad arravs so elements vou use are on distinct cache lines.
```

## Page 33: Image credit: Kathy Yelick,

```text
                                                                   Image credit: Kathy Yelick,
                                                                   UCB, and Tim Mattson, Intel


Synchronization: “critical” regions
Only one thread at a time may enter a critical region




                                                        Copyright © 2026, E. Wes Bethel    33
```

### OCR supplement (verify against PDF)

```text
Threads wait
their turn -
only one at a
time calls
consume()
float res;
#pragma omp parallel
float B; int i, id, nthrds;
id = omp_get_thread_num();
nthrds = omp_get_num_threads();
for(i=id;i<niters;i+=nthrds){
B = big_job(i);
#pragma omp critical
res += consume (B);
```

## Page 34: Image credit: Kathy Yelick,

```text
                                              Image credit: Kathy Yelick,
                                              UCB, and Tim Mattson, Intel



𝛑 program: Safely Update Shared Data




                                   Copyright © 2026, E. Wes Bethel    34
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
static long num_steps = 100000;
#define NUM 4
double step;
int main ()
double pi, sum=0.0;
step = 1.0/(double) num_steps;
#pragma omp parallel num_threads(NUM)
int i, ID; double x, psum= 0.0;
int nthreads = omp_get_num_threads();
ID = omp_get_thread_num();
for (i=ID;i= num_steps; i+=nthreads){
x = (i+0.5)*step;
psum += 4.0/(1.0+x*x);
#pragma omp critical
sum += psum;
pi = step * sum;
Use a critical section so only
one thread at a time can
update sum, i.e. you can
safely combine psum values
Replace array for sum
with a local/private
version of sum (psum) ...
no more false sharing
```

## Page 35: Image credit: Kathy Yelick,

```text
                                             Image credit: Kathy Yelick,
                                             UCB, and Tim Mattson, Intel



𝛑 Program Updated Performance Results




                                  Copyright © 2026, E. Wes Bethel    35
```

### OCR supplement (verify against PDF)

```text
л Program Updated Performance Results
Original Serial pi program with 100000000 steps ran in 1.83 seconds.
OpenMP Pi Critial Region
4
Serial sum
Ideal
Critical Region
Speedup
threads
Serial
Sum
1.86
1.03
1.08
0.97
Critical
Region
1.87
1.00
0.68
0.53
1
1
4
*Intel compiler (icpc) with no optimization on Apple OS X 10.7.3 with a dual core (four HW
thread) Intel® Core™ i5 processor at 1.7 Ghz and 4 Gbyte DDR3 memory at 1.333 Ghz.
```

## Page 36: Image credit: Kathy Yelick,

```text
                                              Image credit: Kathy Yelick,
                                              UCB, and Tim Mattson, Intel



𝛑 Program: Use omp to safely compute reduction




                                   Copyright © 2026, E. Wes Bethel    36
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
static long num_steps = 100000; double step;
void main ()
int i;
double x, pi, sum = 0.0;
step = 1.0/(double) num_steps;
#pragma omp parallel
double x;
#pragma omp for reduction(+:sum)
for (i=0;i< num_steps; i++){
x = (i+0.5)*step;
sum = sum + 4.0/(1.0+x*x);
pi = step * sum;
```

## Page 37: Image credit: Kathy Yelick,

```text
                                             Image credit: Kathy Yelick,
                                             UCB, and Tim Mattson, Intel



𝛑 Program Updated Performance Results




                                  Copyright © 2026, E. Wes Bethel    37
```

### OCR supplement (verify against PDF)

```text
л Program Updated Performance Results
Original Serial pi program with 100000000 steps ran in 1.83 seconds.
OpenMP Pi Critial Region
Serial sum
- - Ideal
• Critical Region
• Loop + Reduce
threads
1
4
Serial
Sum
1.86
1.03
1.08
0.97
Critical
Region
1.87
1.00
0.68
0.53
4.5
4
3.5
З
peedup
2.5
1.5
1
0.5
Loop +
Reduction
1.91
1.02
0.80
0.68
1
4
ore (four HW
*Intel compiler (icpc) with no optimization on Apple OS X 10.7.3 with a dual core (four HW
thread) Intelo CoreTM i5 nrocescor at 1 7 Gh7 and 4 Chvte DDR3 memorv at 1 223 Ch7
```

## Page 38: Image credit: Kathy Yelick,

```text
                                                       Image credit: Kathy Yelick,
                                                       UCB, and Tim Mattson, Intel


Discussion
Serial sum:
 ●   False sharing: inner loop
     synchronization
Critical region:
 ●   Independent computations,
     accumulate in local variables
 ●   Serialize sum outside inner loop
Loop+reduce:
 ●   Similar to critical region
 ●   Relying on compiler optimizations:
     didn’t seem to work out so well here

                                            Copyright © 2026, E. Wes Bethel    38
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
4.5
4
3.5
З
2.5
1.5
1
0.5
- - Ideal
1
```

## Page 39: OpenMP Parallel Loops, Worksharing

```text
OpenMP Parallel Loops, Worksharing



                          Copyright © 2026, E. Wes Bethel   39
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 40: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




Copyright © 2026, E. Wes Bethel   40
```

### OCR supplement (verify against PDF)

```text
The loop worksharing Constructs
• The loop worksharing construct splits up loop
iterations among the threads in a team
#pragma omp parallel
#pragma omp for
for (I=0;kN;I++){
NEAT_STUFF(I);
Loop construct
name:
•C/C++: for
•Fortran: do
SAN
STAI
The variable I is made "private" to each
thread by default. You could do this
explicitly with a "private(l)" clause
```

## Page 41: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




Copyright © 2026, E. Wes Bethel   41
```

### OCR supplement (verify against PDF)

```text
Loop worksharing Constructs
A motivating example
Sequential code
OpenMP parallel
region
for(i=0;i<N;i++) { a[i] = a[i] + b[i];}
#pragma omp parallel
int id, i, Nthrds, istart, iend;
id = omp_get_thread_num();
Nthrds = omp_get_num_threads();
istart = id * N / Nthrds;
iend = (id+1) * N / Nthrds;
if (id == Nthrds-1)iend = N;
for(i=istart;i<iend;i++) { ali] = ali] + b[i]:}
SAN FI
STATE U
OpenMP parallel
region and a
worksharing for
construct
#pragma omp parallel
#pragma omp for
for(i=0;i<N;i++) { a[i] = a[i] + b[i];}
76
```

## Page 42: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




Copyright © 2026, E. Wes Bethel   42
```

### OCR supplement (verify against PDF)

```text
Combined parallel/worksharing construct
• OpenMP shortcut: Put the "parallel" and the
worksharing directive on the same line
double res[MAX]; int i;
#pragma omp parallel
double res[MAX]; int i;
#pragma omp parallel for
for (i=0;i< MAX; i++) {
#pragma omp for
res[i] = huge0;
for (i=0;i< MAX; i++) {
res[i] = huge0;
These are equivalent
```

## Page 43: Copyright © 2026, E. Wes Bethel   43

```text
    Copyright © 2026, E. Wes Bethel   43
Source: Tim Mattson, Intel
```

### OCR supplement (verify against PDF)

```text
Working with loops
• Basic approach
•Find compute intensive loops
•Make the loop iterations independent .. So they can
safely execute in any order without loop-carried
dependencies
•Place the appropriate OpenMP directive and test
Note: loop index
"¡" is private by
default
int i, j,A[MAX];
j=5;
for (i=0;i< MAX; i++) {
j +=2;
A[i] = big(j);
int i, A[MAX];
#pragma omp parallel for
for (i=0;i< MAX; i++) {
int j = 5 + 2*(i+1);
A[i] = big(i);
Remove loop
carried
dependence
```

## Page 44: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




 Copyright © 2026, E. Wes Bethel   44
```

### OCR supplement (verify against PDF)

```text
Nested loops
• For perfectly nested rectangular loops we can parallelize
multiple loops in the nest with the collapse clause:
#pragma omp parallel for collapse(2)
for (int i=0; i<N; i++) {
for (int j=0; j<M; j++) {
Number of
loops to be
parallelized,
counting from
the outside
• Will form a single loop of length NxM and then
parallelize that.
• Useful if N is O(no. of threads) so parallelizing the
outer loop makes balancing the load difficult.
```

## Page 45: Source:  Tim© 2026,

```text
Source:  Tim© 2026,
   Copyright  Mattson,
                    E. WesIntel
                           Bethel   45
```

### OCR supplement (verify against PDF)

```text
Reduction
• How do we handle this case?
double ave-0.0, A[MAX]; int i;
for (i=0;i< MAX; i++) {
ave + = A[i];
ave = ave/MAX;
• We are combining values into a single accumulation
variable (ave) ... there is a true dependence between
loop iterations that can't be trivially removed
• This is a very common situation ... it is called a
"reduction".
• Support for reduction operations is included in most
parallel programming environments.
Source: Tim Mattson, Intel
```

## Page 46: Source: Tim© 2026,

```text
Source: Tim© 2026,
   Copyright Mattson,   Intel
                   E. Wes Bethel   46
```

### OCR supplement (verify against PDF)

```text
Reduction
• OpenMP reduction clause:
reduction (op : list)
• Inside a parallel or a work-sharing construct:
- A local copy of each list variable is made and initialized
depending on the "op" (e.g. 0 for "+").
- Updates occur on the local copy.
- Local copies are reduced into a single value and
combined with the original global value.
• The variables in "list" must be shared in the enclosing
parallel region.
double ave=0.0,A[MAX]; int i;
#pragma omp parallel for reduction (+:ave)
for (i=0;i< MAX; i++) {
ave + = A[i];
Source: Tim Mattson, Intel
ave = ave/MAX;
```

## Page 47: Copyright

```text
   Copyright
Source: Tim©Mattson,
             2026, E. Wes Bethel
                        Intel      47
```

### OCR supplement (verify against PDF)

```text
OpenMP: Reduction operands/initial-values
• Many different associative operands can be used with reduction:
• Initial values are the ones that make sense mathematically.
Operator
Initial value
1
min
max
Largest pos. number
Most neg. number
C/C++ only
Operator Initial value
Operator
.AND.
.OR.
.NEQV.
.IEOR.
JOR.
.IAND.
.EQV.
Fortran Only
Initial value
.true.
.false.
.false.
All bits on
.true.
1
Source: Tim Mattson, Intel
```

## Page 48: Vector-matrix multiplication: y = y+A*x

```text
Vector-matrix multiplication: y = y+A*x
 Assume:
 x, y are vectors of length n
 A is an nxn matrix

 for i=1:n      // 1-based indexing
     for j=1:n
         y[i] = y[i] + A[i,j] * x[j]          =          +                     *




                                       y(i)       y(i)       A(i,:)                x(:)




                                                                      Copyright © 2026, E. Wes Bethel   48
```

### OCR supplement (verify against PDF)

```text
x, y are vectors ot length n
У[i] = y[i] + А[i.j] * x[j]
У(i)
SAN FRANCISCO
STATE UNIVERSITY
A(і,:)
х(:)
```

## Page 49: OpenMP Data Environment

```text
OpenMP Data Environment



                    Copyright © 2026, E. Wes Bethel   49
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 50: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




 Copyright © 2026, E. Wes Bethel   50
```

### OCR supplement (verify against PDF)

```text
Data environment:
Default storage attributes
• Shared Memory programming model:
- Most variables are shared by default
• Global variables are SHARED among threads
- Fortran: COMMON blocks, SAVE variables, MODULE
variables
- C: File scope variables, static
- Both: dynamically allocated memory (ALLOCATE, malloc, new)
• But not everything is shared...
- Stack variables in subprograms(Fortran) or functions(C) called
from parallel regions are PRIVATE
- Automatic variables within a statement block are PRIVATE.
```

## Page 51: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




   Copyright © 2026, E. Wes Bethel   51
```

### OCR supplement (verify against PDF)

```text
Data sharing: Examples
double A[10];
int main() {
int index[10];
#pragma omp parallel
work(index);
printf(*%d\n", index[0]);
extern double A[10];
void work(int *index) {
double temp[10];
static int count;
A, index and count are
shared by all threads.
temp is local to each
thread
A, index,
count
temp
temp
temp
A, index, count
```

## Page 52: Copyright

```text
   Copyright
Source: Tim©Mattson,
             2026, E. Wes Bethel
                        Intel      52
```

### OCR supplement (verify against PDF)

```text
Data Sharing: Private Clause
• private(var) creates a new local copy of var for each thread.
- The value of the private copies is uninitialized
- The value of the original variable is unchanged after the region
void wrong() {
int tmp = 0;
#pragma omp parallel for private(tmp)
for (int j = 0; j < 1000; ++j)
tmp += j; •
printf(*%d\n", tmp);
tmp was not
initialized
tmp is 0 here
Source: Tim Mattson, Intel
```

## Page 53: Copyright

```text
Copyright
Source:© Tim
          2026, Mattson,
                E. Wes Bethel
                           Intel53
```

### OCR supplement (verify against PDF)

```text
Firstprivate Clause
• Variables initialized from shared variable
• C++ objects are copy-constructed
incr = 0;
#pragma omp parallel for firstprivate(incr)
for (i = 0; i <= MAX; i++) {
if ((i%2)==0) incr++;
A[i] = incr;
Each thread gets its own copy
of incr with an initial value of 0
Source: Tim Mattson, Intel
```

## Page 54: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




    Copyright © 2026, E. Wes Bethel   54
```

### OCR supplement (verify against PDF)

```text
Lastprivate Clause
• Variables update shared variable using value
from last iteration
• C++ objects are updated as if by assignment
void sq2(int n, double *lastterm)
double x; int i;
#pragma omp parallel for lastprivate(x)
for (I = 0; 1 < n; i++){
x = a[i]*a[i] + b[i]*b[i];
b[i] = sqrt(x);
*lastterm = x;
"x" has the value it held
for the last sequential®
iteration (i.e., for i=(n-1))
```

## Page 55: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




  Copyright © 2026, E. Wes Bethel   55
```

### OCR supplement (verify against PDF)

```text
SAI
STA
Data Sharing:
A data environment test
• Consider this example of PRIVATE and FIRSTPRIVATE
variables: A = 1,B = 1, C = 1
#pragma omp parallel private(B) firstprivate(C)
• Are A,B,C local to each thread or shared inside the parallel region?
• What are their initial values inside and values after the parallel region?
Inside this parallel region ...
• "A" is shared by all threads; equals 1
• "B" and "C" are local to each thread.
- B's initial value is undefined
- C's initial value equals 1
Following the parallel region ...
• B and C revert to their original values of 1
• A is either 1 or the value it was set to inside the parallel region
```

## Page 56: Source: Tim Mattson, Intel

```text
 Source: Tim Mattson, Intel




Copyright © 2026, E. Wes Bethel   56
```

### OCR supplement (verify against PDF)

```text
Data Sharing: Default Clause
• Note that the default storage attribute is DEFAULT(SHARED) (so
no need to use it)
• Exception: #pragma omp task
• To change default: DEFAULT(PRIVATE)
• each variable in the construct is made private as if specified in a
private clause
• mostly saves typing
• DEFAULT(NONE): no default for variables in static extent. Must
list storage attribute for each variable in static extent. Good
programming practice!
Only the Fortran API supports default(private).
C/C++ only has default(shared) or default(none).
```

## Page 57: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




  Copyright © 2026, E. Wes Bethel   57
```

### OCR supplement (verify against PDF)

```text
The Mandelbrot Area program
#include <omp.h>
# define NPOINTS 1000
# define MXITR 1000
void testpoint(void);
struct a_complex{
double r; double i;
struct d_complex c;
int numoutside = 0;
int main(
int i, j;
double area, error, eps = 1.0e-5;
#pragma omp parallel for default(shared) private(c,eps)
for (i=0; i<NPOINTS; i++) {
for (i=0; j<NPOINTS; j++) {
c.r = -2.0+2.5*(double)(i)/(double)(NPOINTS)+eps;
c.i = 1.125*(double)(i)(double)(NPOINTS)+eps;
testpoint();
void testpoint(void){
struct a_complex z;
int iter;
double temp;
Z=C;
for (iter=0; iter<MXITR; iter++){
temp = (z.r*z.r)-(z.i*z.i)+c.r;
z.i = z.r*z.i*2+c.i;
z.r = temp;
if ((z.r*z.r+z.i*z.i)>4.0) {
numoutside++;
break;
SAN
STATE
area=2.0*2.5*1.125*(double)(NPOINTS*NPOINTS-
numoutside)/(double)(NPOINTS*NPOINTS);
error=area/(double)NPOINTS;
When I run this program, 1 get a
different incorrect answer each
time I run it ... there is a race
condition!!!!
117
```

## Page 58: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




   Copyright © 2026, E. Wes Bethel   58
```

### OCR supplement (verify against PDF)

```text
Debugging parallel programs
• Find tools that work with your environment and learn to use
them. A good parallel debugger can make a huge
difference.
• But parallel debuggers are not portable and you will
assuredly need to debug "by hand" at some point.
• There are tricks to help you. The most important is to use
the default(none) pragma
#pragma omp parallel for default(none) private(c, eps)
for (i=0; i<NPOINTS; i++) {
for (i=0; j<NPOINTS; j++) {
c.r = -2.0+2.5*(double)(i)/(double)(NPOINTS)+eps;
c.i = 1.125*(double)(j)/(double)(NPOINTS)+eps;
testpoint();
Using
default(none)
generates a
compiler
error that j is
unspecified.
SAI
STA
```

## Page 59: Copyright

```text
   Copyright
Source: Tim©Mattson,
             2026, E. Wes Bethel
                        Intel      59
```

### OCR supplement (verify against PDF)

```text
Serial PI Program
Now that you understand
how to modify the data
environment, let's take one
last look at our pi program.
SA
ST.
static long num_steps = 100000;
double step;
int main ()
int i; double x, pi, sum = 0.0;
step = 1.0/(double) num_steps;
for (i=0;i< num_steps; i++){
x = (i+0.5)*step;
sum = sum + 4.0/(1.0+x*x);
pi = step * sum;
What is the
minimum change 1
can make to this
code to parallelize
it?
Source: Tim Mattson, Intel
```

## Page 60: Source: Tim Mattson, Intel

```text
Source: Tim Mattson, Intel




Copyright © 2026, E. Wes Bethel   60
```

### OCR supplement (verify against PDF)

```text
Example: Pi program ... minimal changes
i private by
default
SAN
STAT
#include <omp.h>
static long num_steps = 100000;
double step;
For good OpenMP
void main ()
implementations,
reduction is more
int i;
double x, pi, sum = 0.0;
scalable than critical.
step = 1.0/(double) num_steps;
#pragma omp parallel for private(x) reduction(+:sum)
for (i=0;i< num_steps; i++)
x = (i+0.5)*step;
sum = sum + 4.0/(1.0+x*x);
pi = step * sum;
Note: we created a
parallel program without
changing any executable
code and by adding 2
simple lines of text!
```

## Page 61: Copyright © 2026, E. Wes Bethel   61

```text
Copyright © 2026, E. Wes Bethel   61
Source: Tim Mattson, Intel
```

### OCR supplement (verify against PDF)

```text
SAN
STA
Data sharing:
Changing storage attributes
• One can selectively change storage attributes for
constructs using the following clauses*
- SHARED
All the clauses on this page
- PRIVATE
apply to the OpenMP construct
- FIRSTPRIVATE
NOT to the entire region.
• The final value of a private inside a parallel loop can be
transmitted to the shared variable outside the loop with:
- LASTPRIVATE
• The default attributes can be overridden with:
- DEFAULT (PRIVATE | SHARED | NONE)
DEFAULT(PRIVATE) is Fortran only
*All data clauses apply to parallel constructs and worksharing constructs
except "shared" which only applies to parallel constructs.
```

## Page 62: Copyright © 2026, E. Wes Bethel   62

```text
Copyright © 2026, E. Wes Bethel   62
```

### OCR supplement (verify against PDF)

```text
Major OpenMP constructs we've covered so far
• To create a team of threads
• #pragma omp parallel
• To share work between threads:
• #pragma omp for
• #pragma omp single
• To prevent conflicts (prevent races)
• #pragma omp critical
• #pragma omp atomic
• #pragma omp barrier
• #pragma omp master
• Data environment clauses
• private (variable_list)
• firstprivate (variable_list)
• lastprivate (variable_list)
• reduction(+:variable_list)
Where variable list is a
comma separated list of
variables
Print the value of the macro
OPENMP
And its value will be
УУУутт
For the year and month of the
spec the implementation used
neli
```

## Page 63: Copyright © 2026, E. Wes Bethel   63

```text
Copyright © 2026, E. Wes Bethel   63
```

### OCR supplement (verify against PDF)

```text
The End
A Warner Bros.
PICTURE
SAN FRANC
STATE UNIVERSITY
copyngnt o zoz6, E. Wes Bethel
```

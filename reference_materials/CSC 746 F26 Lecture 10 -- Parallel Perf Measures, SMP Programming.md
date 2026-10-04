# CSC 746 F26 Lecture 10 -- Parallel Perf Measures, SMP Programming

Source: [CSC 746 F26 Lecture 10 -- Parallel Perf Measures, SMP Programming.pdf](<CSC 746 F26 Lecture 10 -- Parallel Perf Measures, SMP Programming.pdf>)

Pages: 68

Extracted with `pdftotext -layout`. Page numbers match the PDF. Text blocks preserve spacing for code, tables, and columns. Diagrams, plotted data, and equations may need inspection in the original PDF.

Apple Vision OCR supplements include recognized lines absent from the PDF text layer. These are search aids and may contain recognition errors; verify code, formulas, and numbers against the PDF.

## Page 1: CSC 746: High Performance Computing

```text
 CSC 746: High Performance Computing
Parallel Perf Measures, SMP Programming
                24 Sep 2026




                              Copyright © 2026, E. Wes Bethel   1
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 2: What’s up today

```text
What’s up today
Last time:
●   CP2 discussion
●   Shared-memory parallelism
Today:
●   Parallel performance measures
●   Shared-memory parallel programming
     ○   POSIX threads
     ○   OpenMP
●   Hello CP#3
●   (Everyone) in-class presentation/idea pitch on Tue 9/29/2026

                                                            Copyright © 2026, E. Wes Bethel   2
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 3: Image Credit: Tim Mattson, Intel

```text
                                                  Image Credit: Tim Mattson, Intel



The Process of Going from Serial To Parallel

●   Identifying
    parallelism
●   Overhead
    balance
●   Load balance
●   Communication
●   Locality
●   Synchronization
    and coordination


                                           Copyright © 2026, E. Wes Bethel       3
```

### OCR supplement (verify against PDF)

```text
Find
Concurrency
Original Problem
Algorithm
strategy
Implementation
strategy
SAN FRANCISCO
STATE UNIVERSITY
Units of execution + new shared data
for extracted dependencies
Tasks, shared and local
data
Program SPMD Emb Par 0
Program SPMD Emb Par 0
Program SPMD Emb Par 0
Program SPMD_Emb_Par 0
TYPE *tmp, *funcO;
global_array Data(TYPE);
global_array Res(TYPE);
int Num = get_num_procsO;
int id = get_proc_idO;
if (id0) setup_problem(N, Data);
for (int I= ID; I<N;I=I+Num){
tmp = func(L, Data);
Res.accumulate(tmp);
Corresponding source
code
```

## Page 4: Part 2 of CSC 746 - Shared memory parallelism

```text
Part 2 of CSC 746 - Shared memory parallelism
Considerations:                        As we:

●   Identify parallelism               ●   Write parallel code
●   Consider also overhead balance     ●   Measure performance, scalability
●   Load balance                       ●   Optimizations to work around
●   Communication                          performance limits
●   Locality
●   Synchronization and coordination




                                                        Copyright © 2026, E. Wes Bethel   4
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 5: Parallel Performance Measures

```text
Parallel Performance Measures



                        Copyright © 2026, E. Wes Bethel   5
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 6: Terminology in Parallel Computing

```text
Terminology in Parallel Computing
N - the problem size

 ●     A measure of the amount of work to be done
 ●     Independent of algorithm complexity: O(N), O(log(N)), O(N^2), etc.

P - parallelism

 ●     The number of parallel “processes”
 ●     Independent of, but related to, how the problem N is divided up among the P workers

Rank

 ●     From MPI, refers to one of the P workers. “A rank”, “Rank 0”, or “P ranks”
 ●     Logically independent of how implemented: can have multiple ranks actually map to a
       single hardware thread, this is an O/S implementation issue

                                                                            Copyright © 2026, E. Wes Bethel   6
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 7: Parallel Performance Measures

```text
Parallel Performance Measures
                                                             Image source: wikpedia.com


Speedup* - how much faster a parallel
code performs compared to a serial
version

Scalability* - is speedup linear,
sublinear, superlinear with increasing P?

Load balance - degree of variance in
execution time across P ranks
                 *
                  Caveat: for the present, we are oversimplifying some
                 key concepts and terms. These terms will unfold into
                 other terms and concepts as we go on.
                                                                            Copyright © 2026, E. Wes Bethel   7
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 8: Speedup: How much faster is parallel vs. serial?

```text
Speedup: How much faster is parallel vs. serial?
Speedup is a ratio of a parallel program’s speed to a
sequential program’s speed

For a problem size n and p parallel ranks:

T*(n) is the time for the best serial algorithm on a
problem of size n

T(n,p) is the time it takes to run the program on a
problem of size n using p parallel ranks
                                                  Useful reference:
                                                  https://hpc-wiki.info/hpc/Scaling

                                                                 Copyright © 2026, E. Wes Bethel   8
```

### OCR supplement (verify against PDF)

```text
S(n,p) =
Т*(п)
Т(п‚p)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 9: Speedup “Warm-up”: Plot of Runtime

```text
 Speedup “Warm-up”: Plot of Runtime

Two codes: serial, and OpenMP p=4
Varying problem size N




                                      Copyright © 2026, E. Wes Bethel   9
```

### OCR supplement (verify against PDF)

```text
Runtime Serial vs. P=4
1
5
100
200
400
800
10
40
80
p=4 time
2.8571429
6.0606061
13.793103
38.095238
Runtime (sec)
80
70
60
50
40
30
10
serial time
P=4 time
SAN FRANCISCO
STATE UNIVERSITY
100
200
400
800 g
Problem Sizes
```

## Page 10: Speedup Plot Example 1

```text
Speedup Plot Example 1




                         Copyright © 2026, E. Wes Bethel   10
```

### OCR supplement (verify against PDF)

```text
5
Speedup: T*(n)/T(n,p), p=4
ideal speedup
actual speedup
4
4
5
3 -
100
200
400
800
Problem Sizes
Problem size
100
200
400
800
serial
40
80
p=4 time
2.8571429
6.0606061
13.793103
38.095238
T*(n)/T(n,p)
3.5
3.3
2.9
2.1
Т*(n)
S(n,P) = I(n,P)
```

## Page 11: Intel Icelake 2.00 GHz

```text
                             Intel Icelake 2.00 GHz
                             4 cores
Speedup Plot Example 2       L2 Cache: 512 KB per core
                             L3 Cache: 6 MB
                             Hyperthreading: Enabled




                                Discussion of results: part of
                                your CP3 assignment.

                         This result at N=1024 is correct: the runtimes for
                         serial, omp-2, omp-4, omp-4 are all about the
                         same so the speedup times (time for serial
                         divided by time for parallel) are all about 1.0 at
                         N=1024.




                                        Copyright © 2026, E. Wes Bethel   11
```

### OCR supplement (verify against PDF)

```text
Speedup VMM OpenMP vs Basic, Intel Icelake (Core i5)
omp-8
Т*(n)
S(n,p) :
Т (п,р)
2048
4096
Problem Sizes
8192
16384
```

## Page 12: What Do Speedup Plots Tell Us?

```text
What Do Speedup Plots Tell Us?
For a given problem size N, the Speedup metric shows how much faster are we
able to solve the problem using P ranks rather than using a serial implementation

Why is the maximum possible Speedup=P ??

What does it mean if Speedup > P ??

What does it mean if Speedup < P ??




                                                              Copyright © 2026, E. Wes Bethel   12
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 13: Strong Scaling

```text
Strong Scaling
Refers to running a problem of size N on P ranks rather than on 1 rank:

 ●    Problem size is constant = N                                                Image credit: Kaminsky, 2015
 ●    Increase parallelism P

Ideally, each of the P ranks works on N/P of the problem (equal work)

Ideally, the serial runtime, T*(N), is reduced by a factor of 1/P when there is ideal
strong scaling

 ●    When P=2, the problem completes in ½ the time of T*(N)
 ●    When P=8, the problem completes in ⅛ the time of T*(N), etc.

Realistically, things don’t often work out that way, and T*(N) is reduced by 1/(P+F)

What is F?


                                                                                    Copyright © 2026, E. Wes Bethel   13
```

### OCR supplement (verify against PDF)

```text
T sec
K=1
I> Size N
T/K sec
Refers to running a problem of size N on P ranks rather than on 1 ranks 4
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 14: Amdahl’s Law

```text
Amdahl’s Law
For any given program, only a portion of it can
be run in parallel, while the remainder must be
run in serial.

As a result, there is a limit to the achievable
speedup in strong scaling


 G. Amdahl. Validity of the single processor approach to achieving large scale
 computing capabilities. Proceedings of the AFIPS Spring Joint Computer
 Conference, 1967, pages 483–485.




                                                                                 Copyright © 2026, E. Wes Bethel   14
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
100
Speedup: T*(n)/T(n,p), p=4
+ ideal speedup
* actual speedup
200
400
Problem Sizes
800
```

## Page 15: Amdahl’s Law, ctd

```text
Amdahl’s Law, ctd
Let:

f be the portion of the program that must be serial (f in [0..1])

(1-f) is the portion of the program that can run in parallel

The limit to scaling for a given n and p is then:


  Smaller f: closer to ideal scaling
  Larger f: further from ideal scaling




                                                                    Copyright © 2026, E. Wes Bethel   15
```

### OCR supplement (verify against PDF)

```text
S(n‚p)
f+ (1-f)/P
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 16: Amdahl’s Law, ctd.

```text
Amdahl’s Law, ctd.
The effect becomes amplified with increasing p

More time time spent doing serial work: f*P

Less time spent doing parallel work: (1-f)*P




                                                 Copyright © 2026, E. Wes Bethel   16
```

### OCR supplement (verify against PDF)

```text
S(n,p) = I+ (1-f)/P
SAN FRANCISCO
STATE UNIVERSITY
speedup w
0 100
Speedup: T*(n)/T(n,p), p=4
+ ideal speedup
* actual speedup
200
400
800
Problem Sizes
```

## Page 17: Image credit: Kaminsky, 2015

```text
                                         Image credit: Kaminsky, 2015

Amdahl’s Law, ctd.
Increasing values of f increasingly
limit scalability

In the limit as f -> 1.0, S(n,p) = 1/f




                                                    Copyright © 2026, E. Wes Bethel   17
```

### OCR supplement (verify against PDF)

```text
S(n,p) = F+ (1-f)/p
SAN FRANCISCO
STATE UNIVERSITY
Speedup
9
8
4
Speedup vs. Cores
F = 0.01
F = 0.02
F = 0.05
F = 0.1
F = 0.2
F = 0.5
56
Cores
9 10
```

## Page 18: Image credit: Kaminsky, 2015

```text
                                                                    Image credit: Kaminsky, 2015



Weak Scaling
Recall: strong scaling holds N constant
and increases P to reduce the time to
solution
Weak scaling: as P increases, so does N;
perfect scaling occurs when T(1) == T(P)
A key idea for using larger machines to
tackle larger problems:
 -   Higher resolution climate grids
                                           J. Gustafson. Reevaluating Amdahl’s law.
 -   More complex systems in molecular     Communications of the ACM, 31(5):532–533, May
     dynamics models                       1988.




                                                              Copyright © 2026, E. Wes Bethel      18
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
K=1
T sec
y Size N
T sec
K = 4
- Size KxN
```

## Page 19: Gustafson’s Law                             J. Gustafson. Reevaluating Amdahl’s law.

```text
Gustafson’s Law                             J. Gustafson. Reevaluating Amdahl’s law.
                                            Communications of the ACM, 31(5):532–533, May
                                            1988.

Recall:

●   Problem size = N
●   Number of processors = P

A performance model focusing on scalability of parallel computing as N increases

Key observation:

●   When increasing P, can also increase N to achieve greater parallel efficiency




                                                                         Copyright © 2026, E. Wes Bethel   19
```

### OCR supplement (verify against PDF)

```text
Communications of the АCM, 31(5):532-533, May
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 20: Gustafson’s, ctd.

```text
Gustafson’s, ctd.
Scalability with increased P
●   Rather than hold N constant and increase P, we also increase N
Constant execution time
●   If time required on size N for P=1 is t, then
●   Time required for size N*P on P processors is also t
Parallel workload
●   Proportion of the workload that can be parallelized is what defines
    performance as P increases

                                                              Copyright © 2026, E. Wes Bethel   20
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 21: Gustafson’s, ctd.

```text
Gustafson’s, ctd.




Amdahl: limits speedups by focusing on the serial portion of the code

●   As P (here, N) increases, the serial portion dominates

Gustafson: as problems scale in size, the parallel portion grows significantly

●   As P (here, N) increases, the parallel portion dominates

                                                                Copyright © 2026, E. Wes Bethel   21
```

### OCR supplement (verify against PDF)

```text
S(N) = N - a(N -1)
Where:
• S(IV) is the speedup of the system with N processors.
• N is the number of processors.
• a is the fraction of the workload that is serial (non-parallelizable).
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 22: Gustafson’s Law, ctd.

```text
Gustafson’s Law, ctd.
If a is the serial portion of
the code (0.0…1.0)

When a → 0, then the
potential speedup → P

As a → 1, then the
potential speedup → 0

Not a surprise…



                                Copyright © 2026, E. Wes Bethel   22
```

### OCR supplement (verify against PDF)

```text
Gustafson's Law: S(P) = P-a*(P-1)
120
100 -
80
x - 0.1 * (x-1)
x - 0.2 * (x-1)
x - 0.3 * (x-1)
x -0.4* (x-1)
x-0.5* (x-1)
x - 0.6*(x-1)
x - 0.7 * (x-1)
x -0.8*(x-1)
x -0.9 * (x-1)
Speedup - S(P)
60
40
40
80
SAN FRANCISCO
STATE UNIVERSITY
60
Number of Processors - P
100
120
```

## Page 23: Amdahl’s vs. Gustafson’s

```text
Amdahl’s vs. Gustafson’s




 Amdahl: The mere presence of serial        Gustafson: the presence of serial code reduces
 code limits scalability (strong scaling)   but doesn’t limit scalability (weak
                                                                     Copyright    scaling)
                                                                               © 2026, E. Wes Bethel   23
```

### OCR supplement (verify against PDF)

```text
Speedup vs. Cores
10
F = 0.01
F = 0.02
7
F = 0.05
Speedup
F = 0.1
F = 0.2
F = 0.5
10
Cores
Speedup - S(P)
Gustafson's Law: S(P) = P-a*(P-1)
120
100
80
x - 0.1 * (x-1)
x - 0.2 * (x-1)
x -0.3 * (x-1)
x -0.4 (x-1)
x-0.5 * (x-1)
x -0.6* (x-1)
x - 0.7 * (x-1)
x -0.8* (x-1)
x -0.9 * (x-1)
60
40
60
Number of Processors - P
80
100
120
but doesn't limit scalability (weak scaling)
```

## Page 24: Amdahl’s vs. Gustafson’s

```text
Amdahl’s vs. Gustafson’s


                          Amdahl: as P grows, the impact of the serial code
                          will grow and dominate thus limiting scalability

                          Gustafson: as P grows, the impact of the serial
                          code does not grow




 Amdahl: The mere presence of serial              Gustafson: the presence of serial code reduces
 code limits scalability (strong scaling)         but doesn’t limit scalability (weak
                                                                           Copyright    scaling)
                                                                                     © 2026, E. Wes Bethel   24
```

### OCR supplement (verify against PDF)

```text
Gustafson's Law: S(P) = P-a*(P-1)
Speedup vs. Cores
120
10
/ F = 0.01
100 -
x -0.1 * (x-1)
x - 0.2 * (x-1)
x - 0.3 * (x-1)
x -0.4* (x-1)
x-0.5 * (x-1)
x -0.6* (x-1)
x - 0.7 * (x-1)
x -0.8* (x-1)
x -0.9 * (x-1)
Speedup
F = 0.5
9
10
60
Number of Processors - P
80
100
120
Cores
but doesn't limit scalability (weak scaling)
```

## Page 25: Computational Rate: Weak Scaling Performance Measure

```text
Computational Rate: Weak Scaling Performance Measure
Rather than think about speedup, instead think about
computational rate
Ratio of problem size to running time
R(n,p) is the rate at which computations are performed
for a given problem size n and parallelism level p
T(n,p) is the time required to do the computation for a
given problem size n and parallelism level p




                                                          Copyright © 2026, E. Wes Bethel   25
```

### OCR supplement (verify against PDF)

```text
R(n,P) = T(n,P)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 26: Parallel Performance Metric: Load Balance

```text
Parallel Performance Metric: Load Balance
Key problem in parallel computing: dividing up the N evenly across the P

Desired outcome: each P does the same amount of work

Examples:




  Good load balance: each thread executes                 Load imbalance: over 2.5x difference
  in about the same amount of time.                       between fastest and slowest thread

                                            Image credit: Kaminsky, 2015        Copyright © 2026, E. Wes Bethel   26
```

### OCR supplement (verify against PDF)

```text
Thread rank
WNH
19154 msec
19155 msec
19155 msec
19156 msec
SAN FRANCISCO
STATE UNIVERSITY
Thread rank
10780 msec
17893 msec
22249 msec
25602 msec
```

## Page 27: Sources of Load Imbalance

```text
Sources of Load Imbalance
Uneven work distribution across the set of p

Data dependency: for some problems, the amount of work required varies as a
function of the input data

Systemic fluctuations: some of the p’s may be delayed due to system issues

(These are all active research areas)




                                                            Copyright © 2026, E. Wes Bethel   27
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 28: Quantifying Load Imbalance

```text
Quantifying Load Imbalance
Straightforward approach:

●   Measure elapsed time for all P’s
●   Compute a statistical measure, like standard deviation:

Many other ways (this is a big research area)




                                                              Copyright © 2026, E. Wes Bethel   28
```

### OCR supplement (verify against PDF)

```text
• Compute a statistical measure, like standard deviation: g = V2(Tp - ()2
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 29: Visualizing Load Imbalance

```text
Visualizing Load Imbalance




                             Performance profiling: green denotes work done by the
                             solver, gray shows chemistry computations, red shows time
                             spent waiting.

                             Image credit: Zirwes et. al, 2018, Optimizing Load Balancing
                             of Reacting Flow Solvers in OpenFOAM for High
                             Performance Computing.




                                                         Copyright © 2026, E. Wes Bethel    29
```

### OCR supplement (verify against PDF)

```text
Eile Edit Chart Eilter Window Help
10.0 s
Timeline
11,5 s
13.0 S
14.5 s
MPI
USER
Monitor
THREADS
Application
Master thread: 18
Master thread:21
Master thread:24
Master thread:27
Master thread:30
Master thread:33
Master thread:36
Master thread:39
Master thread:42
Master thread:45
Master thread:48
Master thread:51
Master thread:54
Master thread:57
Master thread:60
Master
Master
thread:63
thread:66
Master thread:69
Master thread:72
Master
thread: 75
Master thread: 78
Master thread:81
Master
thread:84
Master thread:87
Master thread:90
Master thread:93
Master thread: 96
Master thread:99
Master thread: 102
Master thread:105
Master thread:108
Master thread: 111
Master thread: 114
Master thread: 117
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 30: Shared-memory parallel programming

```text
Shared-memory parallel programming



                          Copyright © 2026, E. Wes Bethel   30
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 31: Shared-memory Programming

```text
Shared-memory Programming
fork() system call - Berkeley Unix, late 1980s-early 1990s
 ●   Creates a child process of the calling (master process)
 ●   Same address space as the caller
 ●   Communicates by reading/writing shared memory
This is how all early OSs, web browsers, persistent network services, etc. were built “back in the
day”
Pro: straightforward coding model
Cons:
 ●   Creating a process is “heavyweight” and expensive (not good for HPC), various limits to
     scalability to high process count, large numbers of open files, etc.
 ●   Explicit, manual methods for creating “shared memory segments”

                                                                          Copyright © 2026, E. Wes Bethel   31
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 32: Image Credit: Kathy Yelick, UCB

```text
                                                                                Image Credit: Kathy Yelick, UCB


Shared Memory Programming
Program is a collection of threads of control

●   Can be created dynamically, mid-execution in some languages
     ○   Each thread has a set of private variables (thread-local storage)
     ○   Also a set of shared variables, e.g., static, global heap (visible to all threads)
●   Threads communicate implicitly by writing and reading shared variables
●   Threads coordinate by synchronizing on shared variables




                                                                                  Copyright © 2026, E. Wes Bethel   32
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 33: Threads - Popularized in Solaris OS (Sun Microsystems)

```text
Threads - Popularized in Solaris OS (Sun Microsystems)
Key ideas/objectives:
Avoid expensive startup cost
associated with launching a new
process
Keep a pool of threads in the
kernel, then map them to a
“lightweight process” at runtime as
needed by user code
Specialized thread library in
Solaris (early 1990s)

                                      Image Credit: linuxjournal.com
                                                                       Copyright © 2026, E. Wes Bethel   33
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
Process 1
Process 2 Process 3
user-level
Kemel
CPU
CPU
CPU
CPU
```

## Page 34: Image Credit: nersc.gov

```text
                                                                       Image Credit: nersc.gov


POSIX Threads (pthreads) (1995ish-present)
A library providing methods for applications
to:                                            pthreads is the POSIX threading interface

 ●    Create, join threads
 ●    Synchronize access to critical regions
 ●    Condition variables

Broad industry support, many vendor
implementations

POSIX standard: Portable Operating
System Interface

Write code once, it runs on all
POSIX-compliant OS’s (on CPUs, not
GPUs)

                                                                         Copyright © 2026, E. Wes Bethel   34
```

### OCR supplement (verify against PDF)

```text
Master
in green
System Intertace
SAN FRANCISCO
STATE UNIVERSITY
Parallel Regions
A Nested
Parallel
Sequential Parts
```

## Page 35: “Forking” POSIX threads

```text
“Forking” POSIX threads




     ●   thread_id is a handle, used to join, halt, etc.
     ●   thread_attribute : various attributes like stack size, priority. NULL gives default attribs
     ●   thread_func: the function to be run by the new thread
     ●   func_arg: a pointer to arg/args passed to thread_func
     ●   errorcode: will be set to nonzero if the create operation fails

                                                                              Copyright © 2026, E. Wes Bethel   35
```

### OCR supplement (verify against PDF)

```text
Signature:
int pthread_create (pthread_t *,
const pthread_attr_t *,
void * (*) (void *),
void *) ;
Example call:
errcode = pthread_create (&thread_id; &thread_attribute
&thread_fun; &fun_arg);
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 36: Pthreads Example

```text
Pthreads Example
L17: pthread_create()
creates a thread and
starts it executing

L5: Each thread runs
the function hello()

L21: pthread_join()
waits for a thread to
finish



                        Copyright © 2026, E. Wes Bethel   36
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
1 #include <stdio.h>
2 #include <pthread.h>
4 /* each thread executes this function */
5 void *hello(void *foo)
printf(" Hello world!
return NULL;
8 }
9
10
#define NTHREADS 4
11 int main() {
12
pthread_t threads[NTHREADS];
13
int tn;
14
15
/* first, create the threads and start them running */
16
for (tn=0;tn<NTHREADS;tn++)
pthread_create(&threads[tn], NULL, hello, NULL);
18
19
/* then wait for the threads to finish */
for (tn=0;tn<NTHREADS;tn++)
pthread_join(threads[tn], NULL);
22
23
return 0;
24 }
25
```

## Page 37: Image Credit: wikipedia.org

```text
                                              Image Credit: wikipedia.org



Pthreads w/args
pthread_create(..., function, …)

 ●   Maps user function() to a thread
     and launches it
 ●   Can pass arguments

function(args) {do work}

 ●   The function runs in a separate
     thread

pthread_join( … )

 ●   Waits for forked threads to finish
 ●   “Fork-join” model

                                          Copyright © 2026, E. Wes Bethel   37
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
#define NUM_THREADS 5
void *perform_work(void *arguments) {
int index = *((int *)arguments);
int sleep_time = 1 + rand() & NUM_THREADS;
printf("THREAD &d: Started.\n", index);
printf("THREAD &d: Will be sleeping for Ed seconds.\n", index, sleep_time);
sleep(sleep_time);
printf("THREAD &d: Ended.\n", index);
int main(void) {
_t threads [NUM_THREADS];
int thread_args [NUM_THREADS];
int i;
int result_code;
//create all threads one by one
for (i = 0; i ‹ NUM_THREADS; i++) {
printf("IN MAIN: Creating thread &d.\n", i);
thread_args[i] = i;
result_code = pthread_create(&threads[i], NULL, perform_work, &thread_args[i]);
assert(!result_code);
printf("IN MAIN: Al1 threads are created. \n");
//wait for each thread to complete
for (i = 0; i < NUM_THREADS; i++) {
result
_code = pthread_join(threads[i], NULL);
assert(!result_code);
printf("IN MAIN: Thread &d has ended.\n", i);
printf("MAIN program has ended.\n");
return 0;
```

## Page 38: Work Decomposition Problem

```text
Work Decomposition Problem
Assume we have an array A[N]

We want to divide the work of N items across P threads

What might that code look like?

●   Step 1: Inside a for loop, set limits based on loop iteration, make function call
●   Step 2: modify that model to use pthreads




                                                                Copyright © 2026, E. Wes Bethel   38
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 39: Work Decomp

```text
Work Decomp




              Copyright © 2026, E. Wes Bethel   39
```

### OCR supplement (verify against PDF)

```text
28
29 #define N (1<<20)
30 #define NTHREADS 4
31
int main() {
32
33
34
35
1
#include
<stdio.h›
2 #include <pthread.h>
#include <math.h>
36
37
4
5
typedef struct
7
38
int thread_num;
/* which thread am I? */
40
int start, end;
/* what is my subset of the 1D d,41
int return_val;
/* nice to have return values */42
10
double *A;
/* the data to work with */
43
11 }
ThreadArgs;
44
12
45
13 /* each thread executes this function */
14 void *cos_subset(void *args) {
46
15
ThreadArgs *ta = (ThreadArgs *)args;
47
16
17
double *my_A = ta->A;
48
18
49
printf(" thread %d: inside cos_subset, start, end 50
->start, ta->end);
51
19
21
22
23
24
25
27 }
/* do some work */
52
for (int i=ta->start; i<ta->end; i++)
53
my_A[i] = cos(my_A[i]);
54
55
ta->return_val = ta->end -
ta->start + 1;
rep'56
return NULL;
57
58
59
SAN FRANCISCO
STATE UNIVERSITY
60
61
62
return 0;
63 1
pthread_t threads[NTHREADS];
ThreadArgs ta[NTHREADS];
int tn;
ouble *A = (double *)malloc(sizeof(double)*N);
/* initialize A -- this is serial */
double x=0.0, dx = 2.0*M_PI / (double)N;
for (int i=0; i<N; i++, x+=dx)
A[i] = ×;
/* launch threads to compute A[i] = cos(A[i]); */
for (tn=0;tn<NTHREADS;tn++)
/* find start/end limits for each thread */
ta[tn].start = tn*(N / NTHREADS);
ta[tn].end = ta[tn].start + (N / NTHREADS - 1); /* potential bugs */
ta[tn].thread_num = tn;
ta[tn].A = A;
ta[tn].return_val = -1; /* init to something */
pthread_create(&threads[tn], NULL, cos_subset, (void *)(ta+tn));
/* then wait for the threads to finish */
for (tn=0;tn<NTHREADS; tn++)
pthread_join(threads[tn], NULL);
printf(" Thread %d processed %d items \n", ta[tn].thread_num, ta[tn].return_val);
```

## Page 40: Concept:

```text
                                                                                    Concept:
Loop Level Parallelism in Pthreads                                          Fine-grained vs.
                                                                       coarse-grained parallelism
Many scientific applications have parallelism in loops

With threads:                    for i = 0, N
                                   for j = 0, N
                                      pthread_create(update_cell[i][j], …
                                                     my_array[i][j]);


But the overhead of thread creation is non-trivial

●   update_cell() should have a significant amount of work
●   1/p’th of total work if possible


                                                                            Copyright © 2026, E. Wes Bethel   40
```

### OCR supplement (verify against PDF)

```text
tor i = 0, N
pthread_create(update_cell[i]i], ....
my_array[D);
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 41: Data Race Example

```text
Data Race Example


The problem: a race condition on the variable s
What is a race condition?
 ●   When two or more threads try to write the same memory location
 ●   Whoever writes last wins
A race condition occurs when:
 ●   Two or more processes or threads attempt to access the same variable and at least
     one of them is doing a write
 ●   The accesses are concurrent, but not synchronized, so they may happen in any
     order, producing unpredictable results

                                                                 Copyright © 2026, E. Wes Bethel   41
```

### OCR supplement (verify against PDF)

```text
static int s = 0;
Thread 1
for i = 0, n/2-1
s = s + f(A[i])
Thread 2
for i = n/2, n-1
s = s + f(A[i])
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 42: Basic Types of Synchronization: Mutexes

```text
Basic Types of Synchronization: Mutexes
Mutexes – mutual exclusion, aka “locks”
                                                                lock *l = alloc_and_init(); /* shared */
●   Threads are working mostly independently                    acquire(l);
●   Need access to a common data structure                        Safely access data here
                                                                release(l);



●   Locks only affect processors using them
     ○   A “rogue” thread can still accesses data w/o acquiring/releasing the mutex
     ○   All threads need to “play nicely” and use mutexes on critical data
●   Java, C++ and others have lexically scoped synchronization
●   Semaphores generalize locks to allow P threads simultaneous access: good
    for limited resources

                                                                             Copyright © 2026, E. Wes Bethel   42
```

### OCR supplement (verify against PDF)

```text
lock *I = alloc_and_init(); /* shared */
acquire(I);
release(I);
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 43: Mutexes in POSIX Threads

```text
Mutexes in POSIX Threads




                           Copyright © 2026, E. Wes Bethel   43
```

### OCR supplement (verify against PDF)

```text
• To create a mutex:
#include <pthread.h>
pthread_mutex_t amutex = PIHREAD_MUTEX_INITIALIZER;
// or pthread_mutex_init (&amutex, NULL) ;
• To use it:
int pthread_mutex_lock (amutex) ;
int pthread_mutex_unlock (amutex) ;
• To deallocate a mutex
int pthread_mutex_destroy (pthread_mutex t *mutex) ;
• Multiple mutexes may be held, but can lead to problems:
threadl
thread2
lock (a)
lock (b)
lock (b)
lock (a)
deadlock
SAN FRANO
STATE UNIVE
• Deadlock results if both threads acquire one of their locks,
so that neither can acquire the second
```

## Page 44: Summary of Programming with POSIX Threads

```text
Summary of Programming with POSIX Threads
POSIX Threads are based on OS features
 ●   Can be used from multiple languages
 ●   Familiar language for most of program
 ●   Ability to share data is convenient
Pitfalls
 ●   Overhead of thread creation is high: once per inner loop iter is too much
 ●   Data race bugs are hard to find: intermittent
 ●   Deadlocks are easier to find, but can also be intermittent
 ●   Coding overhead of implementing data parallelism
Researchers look at transactional memory models as an alternative (sync)

                                                               Copyright © 2026, E. Wes Bethel   44
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 45: Pthreads: an important part of the computing landscape

```text
Pthreads: an important part of the computing landscape
Pthreads are the “backbone” for
many different aspects of modern
multiprocessing
Not used so much in HPC
applications
“task parallelism” as opposed to “data
parallelism”
Likely a “dead end” if want platform     Threading packages in MacOSX
                                         Image source: Apple Developer Connection
portability across both CPUs and
GPUs

                                                              Copyright © 2026, E. Wes Bethel   45
```

### OCR supplement (verify against PDF)

```text
Multprocesaing
Thread Manager
Services (Carbon)
(Carbon)
NSThread
(Cocoa)
java lang. Thread
parallelismiịồii
POSIX threads
Mach threads
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 46: Implementing shared-memory parallel code

```text
Implementing shared-memory parallel code
              with OpenMP



                              Copyright © 2026, E. Wes Bethel   46
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 47: The OpenMP Standard

```text
The OpenMP Standard
A set of compiler directives and library routines for writing multi-threaded,
shared-memory parallel code
Includes environment variables that influence run-time behavior
Greatly simplifies writing multi-threaded programs in Fortran, C, and C++ for
execution on shared-memory platforms
An easy way to get started with parallel coding
OpenMP is managed by a technology consortium (Intel, IBM, Cray, HP, Fujitsu,
Red Hat, AMD, Cray, …)
Supported by virtually all modern C, C++, Fortran compilers and OS’s

                                                                 Copyright © 2026, E. Wes Bethel   47
```

### OCR supplement (verify against PDF)

```text
OpenMP is managed by a technology consortium (Intel, IBM, Cray, HP, U itsu,
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 48: Programmer’s View of OpenMP

```text
Programmer’s View of OpenMP
OpenMP is a portable, threaded, shared-memory programming specification with “light” syntax
 ●   Combination of #pragma’s and function calls
 ●   Requires compiler support
OpenMP will:
 ●   Enable a programmer to specify parallel regions of code that execute in parallel
 ●   Hides stack management
 ●   Provides synchronization constructs
OpenMP will not:
 ●   Parallelize automatically
 ●   Guarantee speedup
 ●   Provide freedom from data race conditions

                                                                         Copyright © 2026, E. Wes Bethel   48
```

### OCR supplement (verify against PDF)

```text
• Enable a programmer to specity parallel regions of code that execute in parallel
Provide treedom trom data race conditions
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 49: Growth of Complexity in OpenMP Over Time

```text
Growth of Complexity in OpenMP Over Time




                                       Copyright © 2026, E. Wes Bethel   49
```

### OCR supplement (verify against PDF)

```text
Page counts (not counting front matter, appendices or index) for versions of OpenMP
Page counts (spec only)
350
300
250
Fortran spec
C/C++ spec
Merged C/C++ and Fortran spec
200
150
2.5
100
50
1.0 1.0
1.1
3.0
3.1
4.5
4.0
1996
1998
2000
2002
2004
2006
year
2008
2010
2012
2014
2016
SAN
STAT
OpenMP 5.0 (November 2018) is actually 666 pages.
```

## Page 50: OpenMP Example: Loop Parallelism

```text
OpenMP Example: Loop Parallelism
Specify where parallelism happens: the
#pragma

#pragma omp parallel for will produce
parallel code where each thread will
execute a portion of that loop

E.g., if there are two threads, then
thread 0 executes i=0..50000 and
thread 1 executes i=50001..100000

All other portions of the code are serial

                                            Image Credit: wikipedia.org
                                                                          Copyright © 2026, E. Wes Bethel   50
```

### OCR supplement (verify against PDF)

```text
return 0;
SAN FRANCISCO
STATE UNIVERSITY
int main(int argc, char **argv)
int a[100000];
for (int i = 0; i < 100000; i++) {
a[i] = 2 * i;
```

## Page 51: OpenMP Hello World

```text
OpenMP Hello World


                     Defines a parallel region of code
                     All code inside the {} executes in parallel




                                           Copyright © 2026, E. Wes Bethel   51
```

### OCR supplement (verify against PDF)

```text
10
11
12
13
14
15
16 }
#include <omp.h>
#include <stdio.h>
int main
#pragma omp parallel
// ID of the thread in the current team
int thread_id = omp_get_thread_num();
// Number of threads in the current team
int nthreads = omp_get_num_threads();
printf('I'm thread %d out of %d threads.\n", thread_id, nthreads)
return 0;
```

## Page 52: gcc -fopenmp hello.c -o hello

```text
                     gcc -fopenmp hello.c -o hello
OpenMP Hello World   (Note: the default gcc on macosx is busted,
                     do a “brew install gcc-15”, then use gcc-15)



                     Defines a parallel region of code
                     All code inside the {} executes in parallel




                                           Copyright © 2026, E. Wes Bethel   52
```

### OCR supplement (verify against PDF)

```text
10
11
12
13
14
16 }
#include <omp.h>
#include <stdio.h>
int main
#pragma omp parallel
// ID of the thread in the current team
int thread_id = omp_get_thread_num();
// Number of threads in the current team
int nthreads = omp_get_num_threads();
printf('I'm thread %d out of %d threads.\n", thread_id, nthreads)
return 0;
```

## Page 53: gcc -fopenmp hello.c -o hello

```text
                     gcc -fopenmp hello.c -o hello
OpenMP Hello World   (Note: the default gcc on macosx is busted,
                     do a “brew install gcc-15”, then use gcc-15)



                     Defines a parallel region of code
                     All code inside the {} executes in parallel




                                           Copyright © 2026, E. Wes Bethel   53
```

### OCR supplement (verify against PDF)

```text
#include <omp.h>
#include <stdio.h>
int main
10
11
12
13
14
16 }
#pragma omp parallel
// ID of the thread in the current team
int thread_id = omp_get_th|46 [wes/omptest] % gcc-10 -fopenmp hello.c-o hello
[wes/omptest] % ./hello
// Number of threads in th I'm thread 1 out of 8 threads.
int nthreads = omp_get_num
I'm
thread 2
out
of 8
threads.
I'm
thread 5
out
of 8
threads.
I'm
printf("I'm thread %d out
thread
out
of 8
threads.
I'm
thread
out
of 8
threads.
I'm thread
out
of 8
threads.
return 0;
I'm thread 4
out of 8
threads.
I'm thread 7
out of 8 threads.
```

## Page 54: Image Credit: wikipedia.org

```text
                         Image Credit: wikipedia.org

OpenMP - lots of depth




                                    Copyright © 2026, E. Wes Bethel   54
```

### OCR supplement (verify against PDF)

```text
OpenMP language
extensions
parallel control
structures
work sharing
data
environment
synchronization
runtime
functions, env.
variables
governs flow of
control in the
program
parallel directive
distributes work
among threads
do/parallel do
and
section directives
scopes
variables
coordinates thread
execution
runtime environment
shared and
private
clauses
critical and
atomic directives
barrier directive
omp_set_num
L_threads ()
omp_get_thread_
num ()
OMP
NUM THREADS
OMP
SCHEDULE
```

## Page 55: Copyright © 2026, E. Wes Bethel   55

```text
Copyright © 2026, E. Wes Bethel   55
```

### OCR supplement (verify against PDF)

```text
SAN FE
STATE U
The OpenMP Common Core: Most OpenMP programs only use these 19 items
OpenMP pragma, function, or clause
#pragma omp parallel
Concepts
Parallel region, teams of threads, structured block, interleaved
execution across threads
int omp_get_thread_num()
int omp_get_num_threads()
double omp_get_wtime()
Create threads with a parallel region and split up the work using
the number of threads and thread ID
Speedup and Amdahl's law.
False Sharing and other performance issues
setenv OMP_NUM_THREADS N
Internal control variables. Setting the default number of threads
with an environment variable
#pragma omp barrier
Synchronization and race conditions. Revisit interleaved
#pragma omp critical
execution.
#pragma omp for
Worksharing, parallel loops, loop carried dependencies
#pragma omp parallel for
reduction(op:list)
schedule(dynamic [,chunk])
Reductions of values across a team of threads
Loop schedules, loop overheads and load balance
schedule (static [,chunk])
private(list), firstprivate(list), shared(list)
Data environment
nowait
#pragma omp single
#pragma omp task
#pragma omp taskwait
Disabling implied barriers on workshare constructs, the high cost of
barriers, and the flush concept (but not the flush directive)
Workshare with a single thread
Tasks including the data environment for tasks.
Ves Bethel
```

## Page 56: Copyright © 2026, E. Wes Bethel   56

```text
Copyright © 2026, E. Wes Bethel   56
```

### OCR supplement (verify against PDF)

```text
OpenMP basic definitions: Basic Solution stack
User layer
End User
Application
System layer
Prog.
Directives,
Compiler
OpenMP library
Environment
variables
OpenMP Runtime library
OS/system support for shared memory and threading
HW
Proc1
Procz
Shared Address Space
ProCz
ProcN
```

## Page 57: CP#3

```text
             CP#3
Shared-memory Parallel (OpenMP)
   Vector-Matrix Multiplication



                         Copyright © 2026, E. Wes Bethel   57
```

### OCR supplement (verify against PDF)

```text
CР#3
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 58: Vector-matrix multiplication: y = y+A*x

```text
  Vector-matrix multiplication: y = y+A*x
         Assume:
         x, y are vectors of length n
         A is an nxn matrix

         for i=1:n      // 1-based indexing
             for j=1:n
                 y[i] = y[i] + A[i,j] * x[j]          =          +                 *

How many memory references?

2n : we will access each Y[i] twice (r+w)
                                               y(i)       y(i)       A(i,:)              x(:)
n2: we will access all of A once (r only)
n2: we will access all of X n times (r only)

m = number of (slow) memory refs = 2n + 2n2
f = number of arithmetic operations = 2n2
CI = f/m ≅ n2/(n+n2) < 1.0 (not so good)                             Copyright © 2026, E. Wes Bethel   58
```

### OCR supplement (verify against PDF)

```text
У[i] = y[i] + А[i.j] * x[i]
CI = f/m = n-/(n+n-) < 1.0 (not so good)
У(i)
А(і:)
х(:)
```

## Page 59: Vector-matrix mult improvement: copy optimization

```text
Vector-matrix mult improvement: copy optimization
 Assume:
                                                  Note: you are not doing the block+copy
 x, y are vectors of length n                          optimization in VMM in CP#3
 A is an nxn matrix

 {read/copy x[1:n] into fast memory}
 {read/copy y[1:n] into fast memory}
                                                  =           +                       *
 for i=1:n
     {copy row i of A into fast memory}
     for j=1:n
         y[i] = y[i] + A[i,j] * x[j]       y(i)        y(i)         A(i,:)                x(:)

 {write/copy y[1:n] back to slow memory}

                                                                             Copyright © 2026, E. Wes Bethel   59
```

### OCR supplement (verify against PDF)

```text
У[i] = v[i] + А[i.j] * x[i]
У(i)
y(ї)
А(і,:)
х(:)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 60: CP#3 – Parallel VMM – due Mon 5 Oct 2026

```text
CP#3 – Parallel VMM – due Mon 5 Oct 2026
Parallelization of vector-matrix multiply using OpenMP
Evaluate performance at varying problem sizes and levels of concurrency
Compare to a reference implementation (CBLAS)
Versions:
 ●   Serial VMM
 ●   Vectorized Serial VMM                      Important dates:
 ●   OpenMP Parallel VMM                         ● 24 Sep 2026: submissions open
                                                 ● 05 Oct 2026 23:59 PDT: submissions due
Deliverables:                                    ● 07 Oct 2026 23:59 PDT: submissions close
                                                 ● 06 Oct 2026: 2 in-class presentations
 ●   Code tarball
 ●   Report

                                                                       Copyright © 2026, E. Wes Bethel   60
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 61: Term Project: In-class elevator pitch

```text
Term Project: In-class elevator pitch
        Tues 29 Sep 2026



                              Copyright © 2026, E. Wes Bethel   61
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 62: Semester Project Schedule

```text
Semester Project Schedule

  Due              What                                      Grade %

  29 Sep 2026      In-class pre-pre-proposal pitch session   1.0% of semester grade

  02 Oct 2026      Project preproposal: problem statement,   1.5% of semester grade
                   approach, anticipated results

  12 Oct 2026      Project proposal: problem statement,      2.5% of semester grade
                   approach, anticipated results

  01-10 Dec 2026   Project presentations                     5% of semester grade

  11 Dec 2026      Project deadline: code+report             25% of semester grade



                                                                    Copyright © 2026, E. Wes Bethel   62
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 63: CSC 746 Speaking Assignment Policy

```text
CSC 746 Speaking Assignment Policy
TLDR:

●   There are multiple speaking assignments in this course
●   They are required, not optional
●   If you skip a speaking assignment, e.g., coding project presentation or term
    project presentation, you receive an F in the course
●   Only excused absences (doctor’s note, etc.) will be considered for
    rescheduling




                                                              Copyright © 2026, E. Wes Bethel   63
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 64: Project Preproposal Idea Pitch Session Tue 29 Sep 2026

```text
Project Preproposal Idea Pitch Session Tue 29 Sep 2026
We will do this in class on Tue 29 Sep 2026
Each person gives a pitch for a project idea or two, you will
receive feedback
 ●   No slides
 ●   Just you speaking, ok to use the whiteboard
                                                                ●   Hi, I’m Joe! (smile!)
Desired outcome:
                                                                ●   Problem being solved/studied
 ●   Everyone gets a better sense of what makes for a           ●   Approach (what are you going to
     good project idea                                              implement?)
                                                                ●   Evaluation strategy (how will you
Turn in: PDF with a problem statement, approach, how you            evaluate your implementation?)
might evaluate your method, potential results                   ●   Potential outcomes (what do you
                                                                    hope to learn?)
                                                                        Copyright © 2026, E. Wes Bethel   64
```

### OCR supplement (verify against PDF)

```text
30 SECONDS
SAN FRANCISCO
STATE UNIVERSITY
оорупунь e
```

## Page 65: Project Preproposals – Due Friday 02 Oct 2026

```text
Project Preproposals – Due Friday 02 Oct 2026
1 page of info:

●   What problem or question are you studying?
●   How will you go about studying the problem?
     ○   What’s the approach?
     ○   What are you going to implement?
●   How will you evaluate the work?
●   What are anticipated outcomes?

Can’t decide on one? I’ll review up to 2 ideas and give you feedback.



                                                              Copyright © 2026, E. Wes Bethel   65
```

### OCR supplement (verify against PDF)

```text
Can't decide on one? I'Il review up to 2 ideas and give you feedback.
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 66: Project Ideas

```text
Project Ideas
Performance analysis and optimization of a code

●   Blocking/tiling, loop reordering
●   Metrics: runtime, MFLOP/s, % mem b/w, latency
●   Metrics: hardware performance counters: cache miss rate, etc.

Parallelization of a code (shared memory, distributed memory)

●   Make it run faster
●   Make it accommodate a problem too large for a node (memory)



                                                                Copyright © 2026, E. Wes Bethel   66
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 67: Project Planning: Technology Pathways within Reach

```text
Project Planning: Technology Pathways within Reach
Take a serial code, and make it run in parallel:
●   On both CPU+GPU: OpenMP
●   On just GPU: CUDA
●   Across multiple compute nodes: MPI (Message Passing Interface)
Instrumenting code to hardware performance counters (cache misses, etc.)
Types of applications:
●   Scientific computing, esp those based on dense linear algebra solvers
●   Other apps where you have a clear serial→parallel story and “code in hand”
●   AI/ML: working with Python-based libraries (Torch, etc.) can be tricky but may
    be doable

                                                              Copyright © 2026, E. Wes Bethel   67
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 68: Copyright © 2026, E. Wes Bethel   69

```text
Copyright © 2026, E. Wes Bethel   69
```

### OCR supplement (verify against PDF)

```text
The End
A Warner Bros.
PICTURE
SAN FRANC
STATE UNIVERSITY
copyngnt o zoz6, E. Wes Bethel 69
```



**Overview** 

Parallelization of vector-matrix multiply (VMM) using OpenMP on modern multi-core CPU architectures, evaluate performance at varying concurrency and problem sizes, and include a comparison to a standard reference VMM implementation (CBLAS).

**Deliverables**

* A tarball/zipfile (no RAR files\!) containing source code for the VMM implementations, a CMakeLists.txt file suitable for use with cmake to build your codes, a README.md that has complete and concise instructions for building and running your code on the various problem sizes, and any additional scripts/etc. as needed to run your codes.  
* A PDF report describing your implementation, results, and answers to homework questions (more details below).  
* On Tue 06 Oct 2026 two students will give brief presentations to the class describing their implementation and results. Please volunteer by Thu 01 Oct 2026, else The Cat will make random speaker selections.

**Coding Project Part 0 \- Problem Setup, Configuration, and Correctness**

Test code harness: for this assignment, please grab and use the following code harness:

git clone https\://github.com/SFSU-Bethel-Instructional/vmmul-omp-harness-instructional

Problem sizes: for all configurations, run your implementation on these problem sizes N=\[1024, 2048, 4096, 8192, 16384\], which are "baked in" to the test code harness in benchmark.cpp. 

Variable/datum size: for all implementations, use double-precision floating point values. This convention is set in the template code that you will be provided. Note: the variable type is "baked in" to the test code harness.

Performance data: instrument your code to measure runtime. Use the example code from chrono\_timer.cpp, and make sure that the clock readings occur only around the VMM part of the code, not the problem setup or verification of the computation. Have your code report the problem size and the elapsed time.

Correctness: a correctness check will be included with the harness code, and it must produce verification that your VMM implementation produces the same answer as the CBLAS reference implementation. 

**Coding Project Part 1 \- VMM Basic (Serial) Version**

Implement a basic VMM as y \= y \+ A\*x, where A is a square, N-by-N matrix, and y and x are N-by-1 vectors. This implementation is a doubly nested loop as we have discussed in class. You will add your implementation into the stub routine inside dgemv-basic.cpp in the code harness. 

**Coding Project Part 2 – VMM Basic (Serial) with Automatic Vectorization Enabled**

Copy your basic VMM code into the routine my\_dgemv in the dgemv-vectorized.cpp file. The compile flags for this file are set up to invoke automatic compiler vectorization. Look in the report.txt file generated during the build process to see if the compiler was able to vectorize your code.

Important: this code should be exactly the same code as your basic implementation. You are relying on the compiler to automatically vectorize the code. Do not add anything at all, no pragmas etc. to this code to make it vectorize. Instead, follow the guidelines we discussed in class for writing clean compact code that will automatically vectorize. 

**Coding Project Part 3 – VMM OpenMP-parallel Version**

In the dgemv-openmp.cpp file, implement an OpenMP-parallel version of your Basic VMM code. Use OpenMP pragmas/directives to set up loop parallelism such that for each y \= y \+ A\[i\] \* x happens in parallel for all rows *i* of matrix A.

**The Report** 

Using the [CSC 746 Homework Latex Template](https://github.com/SFSU-Bethel-Instructional/CSC_746_HomeworkTemplate), produce a report for this assignment that contains the following information (note: you *must* use this template and do your report in LaTeX):

Abstract: describes the focus of the study, the approach, and the primary findings/results (3 or 4 sentences total).

Introduction section: consists of 3 short paragraphs consisting of the problem statement, your approach, and a brief summary of the findings/results. Here, short paragraph means 3-4 sentences.

Implementation section: include a separate subsection for each of the different implementations. Briefly describe your implementation, and include the use of code or compact pseudocode as necessary in code listings. The focus here should be on conciseness and clarity.

Results section: consists of several subsections that follow:

Subsection: Include a subsection describing your computational platform and software environment. Please add a citation to the location where you found this information (hint: use the LaTeX \\cite{} command, and add a new entry to the template.bib file provided with the Overleaf template).

Subsection: Include a subsection describing your test methodology (what are you measuring, how do you measure it, what are the problem sizes, etc). Here you may need to define the formulas you are using to derive performance metrics. 

Note: there are two types of charts in this report\!

* The familiar MFLOP/s chart where the horizontal axis is problem size, and the vertical axis is MFLOP/s, which you will need to compute/derive from your runtime data, your knowledge of the algorithm and its required computations, and the problem size. In other words, you will have to compute the number of floating point operations (FLOPS) your algorithm performs and then compute MFLOP/s using FLOPS and elapsed time, and then use MFLOP/s as the performance measure you report in your charts, tables, etc.  
* A speedup chart showing how your code's performance changes as a function of problem size (in the case of this assignment). Refer to the lecture notes for the method for computing a speedup chart.

Subsection: Comparison of CBLAS with your Basic VMM and your Vectorized VMM

* Chart \#1: MFLOPS. Produce a MFLOP/s chart comparing the performance of these three implementations across all problem sizes. The horizontal axis is problem size, the vertical axis is MFLOP/s (which you'll have to derive from runtime and your knowledge of the algorithm).  
* Discuss the performance of your Basic VMM and Vectorized VMM across the set of problem sizes. Do you see any changes of MFLOP/s across problem sizes? Describe the nature of those changes, if any, and provide an explanation of why the performance numbers change.  
* How does the performance of your Basic VMM and Vectorized VMM implementations compare to CBLAS, the reference implementation? Why do you think that is the case? Couch your answers in terms of how the codes make use of the memory subsystem, instruction-level parallelism, and so forth. 

Subsection:  Evaluation of OpenMP-parallel VMM

* Chart \#2: Speedup chart. Run your OpenMP-parallel code using *static thread scheduling* at varying concurrency \[1, 4, 16, 64\] across all problem sizes. Create a single chart showing ***speedup*** at varying levels of concurrency. Note: this one chart has 4 datasets. In this chart, the horizontal axis is problem size, and the vertical axis is speedup, which will be a number between 1 and P, where P is the maximum concurrency level (in this case, it is 64).  
* Discuss the features you see in that 4-variable speedup chart using static thread scheduling. What trends and features do you see? Why do you think those are happening?

Subsection: Comparison of OpenMP-parallel VMM with CBLAS

* Chart \#3: MFLOPS. From the previous subsection, identify the the OpenMP Parallel VMM configuration (e.g, which concurrency) that performs the best, and create a 2-variable chart (problem size vs. runtime in MFLOP/s) comparing the MFLOP/s of your best OpenMP configuration with that of a serial CBLAS. In this chart, the horizontal axis is problem size and the vertical axis is MFLOP/s.  
* What trends and features do you see in the chart? Why do you think those are happening?

Subsection: Overall Findings and Discussion

* Memory bandwidth % utilization across various implementations. Prepare a Table where the rows are different problem sizes, the columns are different implementations (CBLAS, basic, vectorized, omp-1, omp-4, omp-16, omp-64), and entries are % of peak bandwidth utilization. Discuss the following points/ideas:  
  * Which configuration has the best % bandwidth utilization, and why?  
  * Which configuration has the worst % bandwidth utilization, and why?  
  * For the OpenMP runs, how does % bandwidth utilization change as a function of level of concurrency?  
* Parallel performance and scalability. Considering the data in your charts, is your implementation exhibiting *linear speedup*? That is, if the time required to do a problem size of N using 1 thread is T, then a true linear speedup using P threads would be T/P for the same problem size N. Discuss why or why not. 

**Grading** 

50% Coding: Code correctness and completeness: does the tarball you submit include everything needed to build the code, does the code build and run on Perlmutter@NERSC, do you show how you run over different problem sizes?

50% Report: 

* Completeness (does it contain everything the assignment asks for)   
* Correctness (is what is in the report actually correct).   
* Charts: meaningful title, axis labels, comparative charts have multiple datasets in one chart.  
* Tables: avoid use of large numbers and exponential notation.   
* Both charts and tables have meaningful captions that state what is in the chart/table along with a statement about "what's your point" of showing the chart/table.   
* All charts/tables need to be referenced from within the text.

**Important Dates** 

* 24 Sep 2026 \- submissions open  
* 05 Oct 2026 23:59 PDT \- submissions due   
* 07 Oct 2026 23:59 PDT \- submissions not accepted after this time   
* 06 Oct 2026 \- 3 in-class presentations

**Late submission policy** 

Per the CSC 746 syllabus, late submissions incur a 10%-per-day penalty up to a maximum of 2 days late, after which point submissions are no longer accepted.
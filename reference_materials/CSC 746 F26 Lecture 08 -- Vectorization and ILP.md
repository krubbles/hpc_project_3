# CSC 746 F26 Lecture 08 -- Vectorization and ILP

Source: [CSC 746 F26 Lecture 08 -- Vectorization and ILP.pdf](<CSC 746 F26 Lecture 08 -- Vectorization and ILP.pdf>)

Pages: 66

Extracted with `pdftotext -layout`. Page numbers match the PDF. Text blocks preserve spacing for code, tables, and columns. Diagrams, plotted data, and equations may need inspection in the original PDF.

Apple Vision OCR supplements include recognized lines absent from the PDF text layer. These are search aids and may contain recognition errors; verify code, formulas, and numbers against the PDF.

## Page 1: CSC 746: High Performance Computing

```text
  CSC 746: High Performance Computing
Vectorization and Instruction-level Parallelism
                    17 Sep 2026




                                   Copyright © 2026, E. Wes Bethel   1
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 2: Today                                                     CP2 due:

```text
Today                                                     CP2 due:
                                                  Mon 21 Sep 2026 23:59 PDT
Course schedule update
                                                       CP2 presentations:
                                                        Tue 22 Sep 2026:
Term project schedule, etc.                            Cordano, Bellenberg

Pipelining                                        Project idea “first light” pitch to
                                                               class:
Vectorization and Instruction-level Parallelism         Tue 30 Sep 2025




                                                          Copyright © 2026, E. Wes Bethel   2
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 3: Course Roadmap/Schedule

```text
Course Roadmap/Schedule

   Performance Analysis +        25 Aug – 15 Sep 2026   2 projects/assignments
   Optimization                  (3.5 weeks)

   SMP on CPUs                   17 Sep – 08 Oct 2026   2 projects/assignments
                                 (3.5 weeks)

   SMP on GPUs                   13 Oct – 29 Oct 2026   1 project/assignment
                                 (3 weeks)

   Distributed Memory            03 Nov – 19 Nov 2026   1 project/assignment
   Parallelism, Advanced         (3 weeks)
   Processor Architectures

   Final Project Presentations   01 Dec – 10 Dec 2026


                                                                  Copyright © 2026, E. Wes Bethel   3
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 4: Semester Project Schedule

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



                                                                    Copyright © 2026, E. Wes Bethel   4
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 5: Project Preproposal Idea Pitch Session Tue 29 Sep 2026

```text
Project Preproposal Idea Pitch Session Tue 29 Sep 2026
We will do this in class on Tue 29 Sep 2026
Each person gives a pitch for a project idea or two, you will
receive feedback
 ●   No slides
 ●   Just you speaking, ok to use the whiteboard
Desired outcome:
 ●   Everyone gets a better sense of what makes for a
     good project idea
Turn in: PDF with a problem statement, approach, how you
might evaluate your method, potential results

                                                                Copyright © 2026, E. Wes Bethel   5
```

### OCR supplement (verify against PDF)

```text
30 SECONDS
SLIDEMODEL.COM
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 6: Project Preproposals – Due Friday 02 Oct 2026

```text
Project Preproposals – Due Friday 02 Oct 2026
1 page of info:

●   What problem or question are you studying?
●   How will you go about studying the problem?
     ○   What’s the approach?
     ○   What are you going to implement?
●   How will you evaluate the work?
●   What are anticipated outcomes?

Can’t decide on one? I’ll review up to 3 ideas and give you feedback.



                                                              Copyright © 2026, E. Wes Bethel   6
```

### OCR supplement (verify against PDF)

```text
Can't decide on one? I'Il review up to 3 ideas and give you feedback.
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 7: Project Ideas

```text
Project Ideas
Performance analysis and optimization of a code

●   Blocking/tiling, loop reordering
●   Metrics: runtime, MFLOP/s, % mem b/w, latency
●   Metrics: hardware performance counters: cache miss rate, etc.

Parallelization of a code (shared memory, distributed memory)

●   Make it run faster
●   Make it accommodate a problem too large for a node (memory)



                                                                Copyright © 2026, E. Wes Bethel   7
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 8: Pipelining

```text
Pipelining



             Copyright © 2026, E. Wes Bethel   8
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 9: Latency – Measure of Time Required for an Action

```text
Latency – Measure of Time Required for an Action
What is the latency in communication when:

●   Sending a letter via US Postal Service?
●   Hand carrying a note on a plane from SFO to NYC?
●   Speaking a sentence to someone across the room?
●   Sending a message via a blinking light using Morse code?




                                                           Copyright © 2026, E. Wes Bethel   9
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 10: Single Cycle Execution

```text
                                                              Image Source: P&H, 4.5



Single Cycle Execution




     ●   The “instruction”: do the wash
     ●   Has multiple stages
           ○ Wash, dry, fold, store
     ●   Each “instruction” must complete
         before the next “instruction” can begin
     ●   What is the latency of doing a load of
         laundry in this model?                    Copyright © 2026, E. Wes Bethel     10
```

### OCR supplement (verify against PDF)

```text
6 PM
Time
Task
order
SAN
STATE
o Wash, dry, told, store
12
2 AM
```

## Page 11: Pipelined Model   In a pipelined model:

```text
                                                     Image Source: P&H, 4.5



Pipelined Model   In a pipelined model:

                   ●   We still have 4 “instructions”, each of
                       which consists of multiple stages
                   ●   As soon as the first resource from
                       Instruction N is released, we can begin
                       Instruction N+1
                   ●   Same idea applies to all resources:
                         ○ Wash, dry, fold, store
                   ●   What is the latency of doing a load of
                       laundry in this model?




                                          Copyright © 2026, E. Wes Bethel     11
```

### OCR supplement (verify against PDF)

```text
Task
order
SAN FRANCISCO
STATE UNIVERSITY
o Wash, dry, told, store
```

## Page 12: Time required for sequential

```text
                 Image Source: P&H, 4.5




Time required for sequential
model:
 ● Each instruction uses 4
     resources, ½ hour each
 ● Time for 4 instructions:
       ○ 2 * 4 instructions
       ○ = 8 hours

0.5 loads/hour




     Copyright © 2026, E. Wes Bethel      12
```

### OCR supplement (verify against PDF)

```text
6 PM
7
Task
order
J
SAN FRANCISCO
STATE UNIVERSITY
9
10
11
2 AM
```

## Page 13: Time required for sequential model:

```text
                   Image Source: P&H, 4.5

Time required for sequential model:
 ● T = Ntp
       ○ N=4 instructions
       ○ t time per stage (0.5hr)
       ○ p=4 pipeline stages
 ● T=8 hrs
 ● 0.5 loads per hour

Time for pipelined model (4 instr):
 ● Time for one instruction, plus
 ● Time for one resource at N-1
     instructions
 ● = 2 hrs + 1½ hrs
 ● = 3 ½ hrs

2 loads/hour sustained rate

T = tp + (N-1)t

Potential speedup =
  Ntp / (tp + (N-1)t) ~= p as N→inf
        Copyright © 2026, E. Wes Bethel     13
```

### OCR supplement (verify against PDF)

```text
Task
order
_ D
Task
order
6 PM
6 PM
9
10
10
11
12
12
2 AM
2 AM
```

## Page 14: MIPS Pipeline Model

```text
                                       Image Source: P&H, 4.6



MIPS Pipeline Model
Key idea:

Each of these 5 stages
executes in parallel in 1
clock cycle




                            Copyright © 2026, E. Wes Bethel     14
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
IF: Instruction fetch
Add
Address
Instruction
Instruction
memory
ID: Instruction decode/
register file read
Read
register 1
Read
register 2
Registers
Write
register
Write
data
Read
data 1
Read
data 2
Sign-
extend
EX: Execute/
address calculation
Add
ADD resuit
Shift
left 2
Zero
MEM: Memory access
WB: Write back
Address
Read
data
Data
memory
Write
data
```

## Page 15: Simple MIPS Pipeline

```text
Simple MIPS Pipeline
IF: instruction fetch from instruction memory

ID: instruction decode/register fetch, generate control signals, get rs, rt

EX: engage the ALU to compute something

MEM: memory access, read data back from memory, write data to memory

WB: write result back to rt

                                 Each stage uses a different part of the datapath

                                 Can overlap steps: pipelined MIPS implementation

                                                                  Copyright © 2026, E. Wes Bethel   15
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 16: Resources May Require Different Amounts of Time

```text
                                                                       Image Source: P&H, 4.5



Resources May Require Different Amounts of Time




               All of these instruction types use many of
               the same resources

                                                            Copyright © 2026, E. Wes Bethel     16
```

### OCR supplement (verify against PDF)

```text
Instruction class
Load word (Iw)
Store word (SW)
R-format (add, sub, AND,
OR, slt)
Branch (beq)
fetch
200 ps
200 ps
200 ps
200 ps
Register
read
100 ps
100 ps
100 ps
100 ps
ALU
operation
200 ps
200 ps
200 ps
200 ps
Data
access
200 ps
200 ps
Register
write
100 ps
100 ps
Total
800 ps
700 ps
600 ps
500 ps
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 17: Resources May Require Different Amounts of Time

```text
                                                          Image Source: P&H, 4.5



Resources May Require Different Amounts of Time




                                Some instructions use slower, or more
                                resources

                                               Copyright © 2026, E. Wes Bethel     17
```

### OCR supplement (verify against PDF)

```text
Instruction class
Load word (Iw)
Store word (SW)
R-format (add, sub, AND,
OR, slt)
Branch (bed)
Instruction Register
fetch
read
200 ps
200 ps
200 ps
200 ps
100 ps
100 ps
100 ps
100 ps
ALU
operation
200 ps
200 ps
200 ps
200 ps
Data
access
200 ps
200 ps
Register
write
100 ps
100 ps
Total
800 ps
700 ps
600 ps
500 ps
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 18: Resources May Require Different Amounts of Time

```text
                                                                   Image Source: P&H, 4.5



Resources May Require Different Amounts of Time




                  Because of differences in resource
                  requirements and their performance,
                  these instructions require varying
                  amounts of time to complete.
                                                        Copyright © 2026, E. Wes Bethel     18
```

### OCR supplement (verify against PDF)

```text
Instruction class
Load word (Iw)
Store word (Sw)
R-format (add, sub, AND,
OR, slt)
Branch (beq)
fetch
200 ps
200 ps
200 ps
200 ps
Register
read
100 ps
100 ps
100 ps
100 ps
ALU
operation
200 ps
200 ps
200 ps
200 ps
Data
access
200 ps
200 ps
Register
write
100 ps
100 ps
Total
800 ps
700 ps
600 ps
500 ps
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 19: Single-cycle, non-pipelined execution

```text
                                                                 Image Source: P&H, 4.5



Single-cycle, non-pipelined execution
                             What is the clock cycle time needed for this
                             single-cycle, non-pipelined implementation?




                                                      Copyright © 2026, E. Wes Bethel     19
```

### OCR supplement (verify against PDF)

```text
200
400
600
800
1000
1200
1400
1600
Program
execution Time
order
(in instructions)
Iw $1, 100($0)
Iw $2, 200($0)
Iw $3, 300($0)
1800
Instruction
fetch
Reg
ALU
800 ps
Data
access
Reg
Instruction
fetch
Reg
ALU
800 ps
Data
access
Reg
STATE UNIVERSITY
Instruction
fetch
800 ps
```

## Page 20: Resources May Require Different Amounts of Time

```text
                                                                    Image Source: P&H, 4.5



Resources May Require Different Amounts of Time




                  What is the minimum clock cycle time
                  required to accommodate all these
                  instructions?
                                                         Copyright © 2026, E. Wes Bethel     20
```

### OCR supplement (verify against PDF)

```text
Instruction class
Load word (Iw)
Store word (SW)
R-format (add, sub, AND,
OR, slt)
Branch (beq)
fetch
200 ps
200 ps
200 ps
200 ps
Register
read
100 ps
100 ps
100 ps
100 ps
ALU
operation
200 ps
200 ps
200 ps
200 ps
Data
access
200 ps
200 ps
Register
write
100 ps
100 ps
Total
800 ps
700 ps
600 ps
500 ps
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 21: Top: non-pipelined implementation

```text
                     Image Source: P&H, 4.5




Top: non-pipelined implementation

Bottom: pipelined implementation


          Copyright © 2026, E. Wes Bethel     21
```

### OCR supplement (verify against PDF)

```text
Program
execution Time
order
(in instructions)
200
Iw $1, 100($0)
Instruction
fetch
Reg
Iw $2, 200($0)
Iw $3, 300($0)
400
600
800
1000
1200
1400
1600
1800
ALU
800 ps
Data
access
Reg
Instruction
fetch
Reg
ALU
800 ps
Data
access
Reg
Instruction
fetch
800 ps
Program
execution Time
order
(in instructions)
Iw $1, 100($0)
Instruction
fetch
Iw $2, 200($0) 200 ps
Iw $3, 300($0)
200 400 600 800 1000 1200 1400
Reg
Instruction
fetch
200 ps
ALU
Reg
Instruction
fetch
Data
access
Reg
ALU
Reg
Data
access
ALU
Reg
Data
access
Reg
200 ps 200 ps 200 ps 200 ps 200 ps
```

## Page 22: Instruction-level Parallelism

```text
Instruction-level Parallelism



                         Copyright © 2026, E. Wes Bethel   22
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 23: Instruction-level parallelism (ILP)

```text
Instruction-level parallelism (ILP)
Pipelining exploits potential parallelism among instructions known as ILP
Two methods for increasing potential amount of ILP:
●   Increase pipeline depth to overlap more instructions
     ○   If wash stage takes most time, then
     ○   Decompose washing machine into 3 that each perform: wash, rinse, spin
     ○   Potential speedup: depth of pipeline
●   Replicate internal components to launch, process multiple instructions in
    every pipeline stage
     ○   “Multiple issue” – scheme where multiple instructions are launched in each clock
     ○   Washer analogy: replace single washer/dryer with 3 washers/dryers
          ■ Extra overhead in preparing instructions, data, keeping the components busy


                                                                           Copyright © 2026, E. Wes Bethel   23
```

### OCR supplement (verify against PDF)

```text
Decompose washing machine into 3 that each pertorm: wash, rinse, spin
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 24: Approaches for Multiple Issue

```text
Approaches for Multiple Issue
Issuing multiple instructions per clock

Static multiple issue:

●   Decisions made by compiler before execution
●   Strategy remains fixed over execution

Dynamic multiple issue:

●   Processor makes decisions at runtime




                                                  Copyright © 2026, E. Wes Bethel   24
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 25: Speculation

```text
Speculation
Basic idea:
●   Want to issue multiple instructions per clock
●   Need to identify dependencies between instructions
     ○   beq results of register comparison impacts subsequent PC
     ○   Arithmetic operations require first loading something from memory

Using prediction, “guess” about the properties of an instruction
●   For instruction reordering
●   For provisional resource marshaling
Performed by compiler or by hardware

                                                                             Copyright © 2026, E. Wes Bethel   25
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 26: Static Multiple Issue with MIPS ISA

```text
                                                                            Image Source: P&H, 4.10



Static Multiple Issue with MIPS ISA
Instruction pairs: (1) memory load/store, (2) ALU/branch

Use “no op” (nop) instructions when there isn’t a matched pair




                                                                 Copyright © 2026, E. Wes Bethel   26
```

### OCR supplement (verify against PDF)

```text
Instruction type
ALU or branch instruction
Load or store instruction
ALU or branch instruction
Load or store instruction
ALU or branch instruction
Load or store instruction
ALU or branch instruction
Load or store instruction
IF
IF
ID
ID
IF
EX
- X
ID
ID
IF
IF
Pipe stages
EX
EX
ID
WB
NE
EX
ID
IF
IF
EX
ID
ID
WB
WB
EX
EX
WB
WB
WB
WB
```

## Page 27: Loop “Unrolling”

```text
Loop “Unrolling”
A software technique for obtaining more performance from loops that access
arrays

Basic idea:

●   create multiple copies of the loop body inside the loop itself
●   Need to adjust # of iterations, stride of index variable

Helps to set up instructions in a way that make them easier for the compiler and
processor to multiple-issue



                                                                Copyright © 2026, E. Wes Bethel   27
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 28: C++ Example of loop unrolling

```text
C++ Example of loop unrolling
Start with vector_sum code:
                              for (i=0;i<N;i+=4)
                              {
     for (i=0;i<N;i++)           s1 = A[i];
        sum += A[i];             s2 = A[i+1];
                                 s3 = A[i+2];
                                 s4 = A[i+3];
                                 sum += s1+s2+s3+s4;
                              }




                                               Copyright © 2026, E. Wes Bethel   28
```

### OCR supplement (verify against PDF)

```text
for (i=0;i<N;it=4)
sum += s1ts2+s3+s4;
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 29: Sample Code (MIPS Assembly Language)

```text
                                                  Image Source: P&H, 4.10



Sample Code (MIPS Assembly Language)




                                       Copyright © 2026, E. Wes Bethel   29
```

### OCR supplement (verify against PDF)

```text
Loop: Iw
addu
SW
addi
bne
$to, O($s1)
# $tO=array element
$to,$to,$s2# add scalar in $s2
$t0, 0($s1)# store result
$s1,$s1,-4# decrement pointer
$s1,$zero, Loop# branch $s1!=0
ALU or branch instruction
Loop:
Data transfer instruction
IW
$tO, O($s1)
Clock cycle
addi
addu
bne
STATE UNIVERSITY
$s1,$s1,-4
$to, $to,$s2
$s1, $zero, Loop
SW
$to, 4($s1)
```

## Page 30: Unroll 4x

```text
                       Image Source: P&H, 4.10



Unroll 4x




            Copyright © 2026, E. Wes Bethel   30
```

### OCR supplement (verify against PDF)

```text
Loop:
ALU or branch instruction
addi
addu
bne
$s1,$s1,-ąłą
$to,$to,$s2
$s1,$zero, Loop
Data transfer instruction
TW
$to, O($s1)
SW
$tO, 4($s1)
Clock cycle
З
Loop:
ALU or branch instruction
addi
$s1,$s1,-16
addu
addu
addu
addu
$to, $to, $s2
$t1,$t1,$s2
$t2,$t2,$s2
$t3,$t3,$s2
bne
$s1,$zero, Loop
Data transfer instruction
Tw
TW
Tw
Tw
SW
SW
SW
SW
$to, O($s1)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
$t0, 16($s1)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
Clock cycle
5
```

## Page 31: Unroll 4x

```text
                                                                Image Source: P&H, 4.10



Unroll 4x




            Clock Cycle 1 executes 2 instructions:
             ● Increment loop index by 4
             ● Load word from array[0]


                                                     Copyright © 2026, E. Wes Bethel   31
```

### OCR supplement (verify against PDF)

```text
ALU or branch instruction
addi
addu
bne
$s1,$s1,-ął
$to,$to,$s2
$s1,$zero, Loop
Data transfer instruction
TW
$to, O($s1)
SW
$tO, 4($s1)
З
nch instruction
Data tranefer
addi
$s1,$s1,-16
Tw
addu
addu
addu
addu
bne
$to,$to,$s2
IW
Tw
$s1,$zero, Loop
SW
$to, O($s1)
$t1,12($51)
$t2, 8($s1)
$s1)
Б($s1)
($s1)
$s1)
$t3, 4($s1)
Clock evele
5
8
```

## Page 32: Unroll 4x

```text
                                                               Image Source: P&H, 4.10



Unroll 4x




            Clock Cycle 2 executes 1 instruction:
             ● Load word for array[3]

                                                    Copyright © 2026, E. Wes Bethel   32
```

### OCR supplement (verify against PDF)

```text
Loop:
ALU or branch instruction
addi
addu
bne
$s1,$s1,-4
$to,$to,$s2
$s1,$zero, Loop
Data transfer instruction
TW
$to, O($s1)
SW
$tO, 4($s1)
З
oop:
ALU or branch instruction
addi $s1,$s1, 16
addu
addu
addu
addu
$to,sto,$sz
$t1,$t1,$s2
bne
Data transfer instruction
7w
TW
TW
Tw
$1O, O($51)
$t1,12($s1)
$t2, 8($51)
$t3, 4($s1)
5($s1)
5
8
```

## Page 33: Unroll 4x

```text
                                                                Image Source: P&H, 4.10



Unroll 4x




            Clock Cycle 3 executes 2 instructions:
             ● Add constant $s2 to array[0]
             ● Load word array[2]
                                                     Copyright © 2026, E. Wes Bethel   33
```

### OCR supplement (verify against PDF)

```text
Loop:
ALU or branch instruction
addi
addu
bne
$s1,$s1,-4
$to,$to,$s2
$s1,$zero, Loop
Data transfer instruction
TW
$to, O($s1)
SW
$tO, 4($s1)
З
Loop:
ALU or branch instruction
addi
$s1,$s1,-16
addu
addu
addu
addu
$to,$to,$s2
$ti,$ti,$sz
$+0 ++0 $.0
bne
Data transfer instruction
TW
$to, O($s1)
7w
- $t1,12($s1)
Tw
$t2, 8($s1)
TW
$t3, 4($51)
16($s1)
($s1)
($s1)
($s1)
5
```

## Page 34: Unroll 4x

```text
                                                                Image Source: P&H, 4.10



Unroll 4x
            Clock Cycle 4 executes 2 instructions:
             ● Add constant $s2 to array[3]
             ● Load word array[1]




                                                     Copyright © 2026, E. Wes Bethel   34
```

### OCR supplement (verify against PDF)

```text
ALU or branch instruction
Loop•
Data transfer instruction
$+0 0(8<1)
З
Loop:
ALU or branch instruction
addi
$s1,$s1,-16
addu
addu
addu
addu
$to,$to,$s2
$t1,$t1,$s2
$t2,s12,$52
$t3,$t3,$s2
bne
$s1,$zero, Loop
Data transfer instruction
Tw
TW
łw
Tw
SW
SW
SW
SW
$to, O($s1)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
$t0, 16($51)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
5
```

## Page 35: Unroll 4x

```text
                                                          Image Source: P&H, 4.10



Unroll 4x

            Clock Cycle 5 executes 2 instructions:
             ● Add constant $s2 to array[2]
             ● Store word array[0]
                   ○ Note: bug in this line for sw
                   ○ Should be 0($s1) not 16($s1)




                                               Copyright © 2026, E. Wes Bethel   35
```

### OCR supplement (verify against PDF)

```text
Data transfer instruction
TW
$to, O($s1)
Loop:
ALU or branch instruction
Loop:
ALU or branch instı
addi
$s1,$s1,-16
addu
addu
addu
addu
$to,$to,$s2
$t1,$t1,$52
$t2,$t2,$s2
$13,$13,$52
bne
$s1,$zero, Loop
addi
$s1,$s1,-4
addu
$+0 8+n 8c2
Tw
$to, O($s1)
TW
$t1,12($s1)
Tw
$t2, 8($s1)
$t3, 4($s1)
$to, 16($s1)
$t1,12($ST)
$t2, 8($s1)
$t3, 4($s1)
З
```

## Page 36: Unroll 4x

```text
                                                                Image Source: P&H, 4.10



Unroll 4x


            Clock Cycle 6 executes 2 instructions:
             ● Add constant $s2 to array[1]
             ● Store word array[3]




                                                     Copyright © 2026, E. Wes Bethel   36
```

### OCR supplement (verify against PDF)

```text
Loop:
Loop:
ALU or branch instı
addi
$s1,$s1,
ALU or branch instruction
addi
addu
bne
$s1,$s1,-4
$to,$to,$s2
$s1,$zero, Loop
SW
Data transfer instruction
TW
$to, O($s1)
$to, 4($s1)
З
addu
addu
addu
addu
$to,$to,$s2
$t1,$t1,$s2
$t2,$t2,$s2
$t3,$t3,$s2
bne
$s1,$zero, Loop
TW
Tw
Tw
SW
SW
SW
SW
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
$t0, 10($s1)
$t1,12($s1)
$12, 8($51)
$t3, 4($s1)
5
7
8
```

## Page 37: Unroll 4x

```text
                                                          Image Source: P&H, 4.10



Unroll 4x


            Clock Cycle 7 executes 1 instructions:
             ● Store word array[2]
             ● (No ALU operation to perform here)




                                               Copyright © 2026, E. Wes Bethel   37
```

### OCR supplement (verify against PDF)

```text
Loop:
Loop:
ALU or branch instı
addi
$S1,$s1,
ALU or branch instruction
addi
addu
bne
$s1,$s1,-ą
$to,$to,$s2
$s1,$zero, Loop
SW
Data transfer instruction
TW
$to, O($s1)
$to, 4($s1)
З
addu
$to,$to,$s2
addu
$t1,$t1,$s2
addu
$t2,$t2,$s2
addu $t3,$t3,$32
pre
$si,$zero,Loop
TW
Tw
Tw
SW
SW
SW
SW
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
$to, 16($s1)
$t1,12($s1)
$t2, 8($s1)
$13, 4($51)
5
```

## Page 38: Unroll 4x

```text
                                                                Image Source: P&H, 4.10



Unroll 4x


            Clock Cycle 8 executes 2 instructions:
             ● Store word array[1]
             ● BNE instruction




                                                     Copyright © 2026, E. Wes Bethel   38
```

### OCR supplement (verify against PDF)

```text
Loop:
Loop:
ALU or branch instı
addi
$s1,$s1,
ALU or branch instruction
addi
addu
$s1,$s1,-ą
$to,$to,$s2
$s1,$zero, Loop
SW
Data transfer instruction
TW
$to, O($s1)
$to, 4($s1)
З
addu
addu
addu
addu
$to, $to,$s2
$t1,$t1,$s2
$t2,$t2,$s2
$t3,$t3,$s2
$s1, $zero, Loop
TW
Tw
Tw
SW
SW
SW
SW
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
$t0, 16($s1)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
5
```

## Page 39: Comparison of Clocks: Rolled vs. Unrolled

```text
                                                                                       Image Source: P&H, 4.10



Comparison of Clocks: Rolled vs. Unrolled



4 clocks * N iterations

= 4N clocks

                                                     8 clocks * N/4 iterations

                                                     = 2N clocks



                          This example shows a 2x speedup of code simply
                          by doing loop unrolling

                                                                            Copyright © 2026, E. Wes Bethel   39
```

### OCR supplement (verify against PDF)

```text
ALU or branch instruction
addi
addu
bne
$s1,$s1,-Ąął
$to,$t0.$s2
$s1,$zero, Loop
Data transfer instruction
Tw
$tO, O($s1)
SW
$t0, 4($s1)
Clock cycle
ALU or branch instruction
addi
$s1,$s1,-16
addu
addu
addu
addu
$to,$to,$s2
$t1,$t1,$s2
$t2,$t2,$s2
$t3,$t3,$s2
bne
$s1, $zero, Loop
Data transfer instruction
Tw
Tw
Tw
$tO, O($s1)
$t1,12($s1)
$t2, 8($s1)
$t3, 4($s1)
SW
SW
SW
SW
$to, 16($s1)
$t1,12($S1)
$t2, 8($s1)
$t3, 4($51)
Clock cycle
7
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 40: Vectorization

```text
Vectorization



                Copyright © 2026, E. Wes Bethel   40
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 41: Image Credit: Kathy Yelick, UCB

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

                                                                          Copyright © 2026, E. Wes Bethel   41
```

### OCR supplement (verify against PDF)

```text
Network
Network
SAN FRANCISCO
STATE UNIVERSITY
Network
Network
Network
```

## Page 42: Vectorization and SIMD Processing

```text
Vectorization and SIMD Processing
Scalar operations act on
individual data elements, one at a
time
Vector operations are single
instructions applied to multiple
data items
Single Instruction Multiple Data
(SIMD parallelism)
  -   Caveat: SIMD and
      vectorization are similar
      concepts, but are not strictly
      the same thing
                                       Image credit: Raskulinec & Fiksman, Elsevier 2015
                                       https://doi.org/10.1016/B978-0-12-803819-2.00006-9

                                                                             Copyright © 2026, E. Wes Bethel   42
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
• Scalar mode
- One instruction produces
one result (SISD)
ali]
a+b
- One instruction can produce multiple results (SIMD)
- using AVX VADDPS instruction
for (i=0; i<=MAX; i++)
c[i] = a[i] + b[i];
a[i+7]
ali+6] ali+5] a[i+4] a[i+3] a[i+2] a[i+1]
b[i÷7|
b[i-+5]
b[і+4]
bli+s
b[i+2]
[b[ї+1]
a[i]+b[i]
c[j+7|
cli+6]
c[+5]
c[i+4]
c[+3]
c[i+2]
c[i+1]
cП
```

## Page 43: Vectorization Analogy: Loop Unrolling

```text
Vectorization Analogy: Loop Unrolling

 Original loop: processes one   Unrolled loop: processes 4
 item at a time                 items at a time
 for (off_t i=0; i<N; i++)      for (off_t i=0; i<N; i+=4)
     c[i] += a[i]*b[i]          {
                                    c[i] += a[i]*b[i]              Vectorization:
                                    c[i+1] += a[i+1]*b[i+1]        performs all these
                                    c[i+2] += a[i+2]*b[i+2]        operations with 1
                                    c[i+3] += a[i+3]*b[i+3]        instruction in “1 tick”
                                }




                                                              Copyright © 2026, E. Wes Bethel   43
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 44: How to Do Vectorization

```text
How to Do Vectorization
●   (x86) Write assembler that uses AVX-512 instructions
     ○   vfmadd231pd zmm1, zmm0, zmm0 // fused multiply add on AVX-512 registers, 16 dp FLOPs
     ○   Highly platform dependent, not portable
     ○   Squeeze out last drop of performance
●   Use “vector intrinsics”
     ○   Like assembler, more easily mixed with your C++ code
     ○   Also not portable
●   Automatic compiler vectorization
     ○   Highly portable, this is what we’ll focus on
     ○   Can be tricky to get right: you have to write good code
●   Use a library that’s already vectorized
     ○   A good option for portability, rapid code development

                                                                      Copyright © 2026, E. Wes Bethel   44
```

### OCR supplement (verify against PDF)

```text
• Scalar mode
- One instruction produces
one result (SISD)
• SIMD processing
- One instruction can produce multiple results (SIMD)
- using AVX VADDPS instruction
for (i=0; i<=MAX;
c[i] = a[i] + b[i];
ali+oj
afi+5]ai+4]a[i+3] a[i+2] a[i+1]
bi5] bi+4] bi+] b[i+2] b[i+1] b]
e(+5) c(+5] c(i+4] c(+3] c(i+2] c(i+1] c]
ü+bü
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 45: Vectorization Coding Strategies

```text
Vectorization Coding Strategies
●   Focus your attention on sections of code that can actually benefit from
    vectorization
●   Look for loops where you are doing lots of computation, e.g.:
        for (off_t i=0;i<N;i++)
             c[i] += a[i]*b[i]
●   Write code in a form the compiler will actually vectorize
●   Use the correct compiler flags to request automatic vectorization
●   Verify the compiler vectorized your code
●   Implement fixes, hints where the compiler didn’t vectorize your code

                                                              Copyright © 2026, E. Wes Bethel   45
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 46: Basic Requirements for Loops to be Vectorized

```text
Basic Requirements for Loops to be Vectorized
●   The loop must be countable at runtime
     ○   N must be known before the loop executes
     ○   No conditional terminations inside the loop (e.g., break)
●   Single control flow within the loop
     ○   Branching, conditionals, switch statements impede vectorization
     ○   Workaround: masked operations
●   Avoid function calls
     ○   Exceptions: to functions that can be replaced with inline vector instructions, such as math
         functions, etc.




                                                                              Copyright © 2026, E. Wes Bethel   46
```

### OCR supplement (verify against PDF)

```text
tunctions, etc.
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 47: Vectorization Data Dependencies: Read-after-write

```text
Vectorization Data Dependencies: Read-after-write
     int a[5] = {0,1,2,3,4};
                                                    For this code example, each loop iteration
     int b[5] = {5,6,7,8,9};
                                                    depends on a value completed in the previous
                                                    loop iteration.
     for (i=1; i<5; i++) {
        a[i] = a[i-1] + b[i];
                                                    We are “reading after writing”.
     }
                                                    If we look at a serial evaluation of this loop (left),
                                                    we see that it produces the correct results.

                                                    Red numbers indicate values written by one
                                                    iteration, then read by the next.


                                                             When executed in a vectorized fashion, it fails
                                                             due to the read-after-write dependency
                                                             because it cannot be computed correctly on
                                                             vector hardware.

                                                             Read-after-write is NOT vectorizable
                                Image Credit:                                          Copyright © 2026, E. Wes Bethel   47
                                https://cvw.cac.cornell.edu/vector/coding_dependencies
```

### OCR supplement (verify against PDF)

```text
for (i=1; i<5; it+) {
a[1] = a[0] + b[1] - a[1] =
0+6→
a[1] =
a[2] = a[1] + b[2] → a[2] =
6 + 7 → a[2] = 13
a[3] = a[2] + b[3] → a[3] = 13 + 8 → a[3] = 21
a[4] = a[3] + b[4] → a[4] = 21 + 9
→ a[4] = 30
a = (0, 6, 13, 21, 30)
a[i-1] = (0,1,2,3}
(load)
(load)
{0,1,2,3) + (6,7,8,9) = (6,8,10,12)
a[i] = {6,8,10,12)
(store)
(operate)
a = (0, 6, 8, 10, 12) * (0, 6, 13, 21, 30)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 48: Vectorization Data Dependencies: Write-after-read

```text
Vectorization Data Dependencies: Write-after-read
     int a[5] = {0,1,2,3,4};
     int b[5] = {5,6,7,8,9};                          The opposite of read-after-write: a value
                                                      used as input in an earlier iteration, then
     for (i=0; i<4; i++) {                            written in a later iteration.
        a[i] = a[i+1] + b[i];
     }                                                If we look at a serial evaluation of this loop
                                                      (left), we see that it produces the correct
                                                      results.

                                                      There are no red numbers as before: none
                                                      are written in the current iteration then used
                                                      in a later one.
                                                      When executed in a vectorized fashion, we
                                                      get the same result as if done in serial.

                                                      Write-after-read IS vectorizable.

                                Image Credit:                                          Copyright © 2026, E. Wes Bethel   48
                                https://cvw.cac.cornell.edu/vector/coding_dependencies
```

### OCR supplement (verify against PDF)

```text
for (i=0; i<4; itt) {
a[1] = a[0] + b[1]
a [2] = a[1] + b[2]
a [3] = a[2] + b[3]
a[4] = a[3] + b[4]
a[1] = 1 + 5
a[2] = 2 + 6
→ a[3] = 3 + 7
a [4] = 4 + 8
a = (6, 8, 10, 12, 4)
a[i+1] = (1,2,3,4)
(load)
(load)
{1,2,3,4) + {5,6,7,8) = (6,8,10,12)
a[i] = {6,8,10,12)
(store)
a = (6, 8, 10, 12, 4)
SAN FRANCISCO
STATE UNIVERSITY
a[1] = 6
a [2] = 8
a[3] = 10
a [4] = 12
(operate)
```

## Page 49: Vectorization Data Dependencies: Write-after-write

```text
Vectorization Data Dependencies: Write-after-write

                              Write-after-write occurs when multiple loop
   int a[5] = {0,1,2,3,4};    iterations alter the value at a single location.
   int b[5] = {5,6,7,8,9};
   int c[5];
                              A value is written by one loop iteration, and
   for (i=0; i<4; i++) {      then written again by a later iteration.
      c[i%2] = a[i] + b[i];
   }                          If an identical address exists for any two or
                              more store operations, the result to be
                              stored is indeterminate.

                              Write-after-write is NOT vectorizable.



                                                       Copyright © 2026, E. Wes Bethel   49
```

### OCR supplement (verify against PDF)

```text
int b[5] = {5,6,],8,9};
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 50: Vectorization Data Dependencies: Read-after-read

```text
Vectorization Data Dependencies: Read-after-read

                              Read-after-read happens when a single
                              vector location is read and used during
   int a[5] = {0,1,2,3,4};    multiple iterations.
   int b[5] = {5,6,7,8,9};
   int c[5];                  In this case, b[i%2] may be used during
                              multiple iterations, depending on the value of
   for (i=0; i<4; i++) {      the loop index variable i.
      c[i] = a[i] + b[i%2];
   }                          In principle, there’s no problem here because
                              we are not writing into b, we are only reading
                              from it; b’s contents don’t change over the
                              course of the execution.

                              Read-after-read IS vectorizable.
                                                       Copyright © 2026, E. Wes Bethel   50
```

### OCR supplement (verify against PDF)

```text
c[i] = a[i] + b[ig2];
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 51: Pointer Aliasing: A “Hidden” Data Dependency

```text
Pointer Aliasing: A “Hidden” Data Dependency
                                     Here we have a function that takes 3 input
Void compute(double *a, double *b,   arrays, a, b, and c.
double *c, int n) {
   for (i=1;i<n;i++)                 Is it safe to vectorize the for loop?
      a[i] = b[i] + c[i];
}                                    Are there any obvious bad data dependencies?

                                     This is valid syntax, a perfectly valid thing to do.
/* assume arrays s and t */
                                     Inside compute(), a and b refer to overlapping
compute(s, s-1, t);
                                     regions of s.

                                     Rewriting compute() with the variable names s
                                     and t to illustrate the overlap, we quickly see a
for (i=1;i<n; i++)
                                     Read-after-write data dependency.
   s[i] = s[i-1] + t[i];
                                     Concept: avoid use of pointers
                                                              Copyright © 2026, E. Wes Bethel   51
```

### OCR supplement (verify against PDF)

```text
for (i=1;i<n;it+)
for (i=1;i<n; it+)
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 52: Compiler Vectorization Flags on Perlmutter

```text
Compiler Vectorization Flags on Perlmutter
We are using the g++ compiler (11.2.0) or the Cray g++ wrappers (CC)

Enabling vectorization:

-O2 -ftree-vectorize # enables vectorization, by default produces SSE (128-bit) vector instructions

Reporting:

-fopt-info-vec-all=rpt.txt # generates vectorization report, goes into file rpt.txt

Specifying x86 vector instruction level:

-mavx # use AVX instructions, 128-bit
                                                        Useful info: (1) https://colfaxresearch.com/knl-avx512/
-mavx2 # use AVX2 instructions, 256-bit                 (2) https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html
-mavx512f # use AVX512 instructions, 512-bit

                                                                                      Copyright © 2026, E. Wes Bethel   52
```

### OCR supplement (verify against PDF)

```text
-02 -ftree-vectorize # enables vectorization, by default produces SSE (128-bit) vector instructions
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 53: Compiler Vectorization Flags on Perlmutter

```text
Compiler Vectorization Flags on Perlmutter
We are using the g++ compiler (11.2.0) or the Cray g++ wrappers (CC)

Enabling vectorization:

-O2 -ftree-vectorize # enables vectorization, by default produces SSE (128-bit) vector instructions

Reporting:                                         Caution:
-fopt-info-vec-all=rpt.txt # generates vectorization report, goes into file rpt.txt
                                                     Don’t use these mavx* flags on perlmutter!!
Specifying x86 vector instruction level:
                                                     Instead, use -O3 -march=native
-mavx # use AVX instructions, 128-bit
                                                     Compiler will generate correct AVX2 instructions
-mavx2 # use AVX2 instructions, 256-bit
                                                   This is the default config when using the RELEASE
-mavx512f # use AVX512 instructions, 512-bit
                                                   cmake build type in the code harnesses

                                                                                  Copyright © 2026, E. Wes Bethel   53
```

### OCR supplement (verify against PDF)

```text
-02 -ftree-vectorize # enables vectorization, by default produces SSE (128-bit) vector instructions
-fopt-info-vec-all=rpt.txt # generates vectorizatior
Instead, use -03 -march=native
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 54: Image credit:

```text
                                                  Image credit:
                                                  https://cvw.cac.cornell.edu/vector/hw_registers

Verify the Compiler Vectorized Your Code
Compiler reports

Look at the assembler generated
by the compiler

●   Compiler-generated
    assembler
●   Godbolt.org compiler
    explorer (live demo)
                                  What are we looking for in the assembly code?
                                  Evidence of scalar, SSE, AVX, or AVX-512
                                  instructions: different sets of registers for each

                                                          Copyright © 2026, E. Wes Bethel       54
```

### OCR supplement (verify against PDF)

```text
64-bit double
32-bit float
SSE, 128-bit (1999)
xmmO
AVX, 256-bit (2011)
8
ymmo
AVX-512 (KNL, 2016; prototyped by KNC, 2013)
16
SAN FRANCISCO
STATE UNIVERSITY
zmmO
```

## Page 55: g++ 11.2.0 -O0 -S → x86 assembly output

```text
g++ 11.2.0 -O0 -S → x86 assembly output




                                          Copyright © 2026, E. Wes Bethel   55
```

### OCR supplement (verify against PDF)

```text
g++ 11.2.0 -00 -S → x86 assembly output
4
7
sum(long, long*):
push
mov
mov
mov
mov
mov
jmp
rbp
rop, rsp
QWORD PTR [rbp-24], rdi
QWORD PTR [rbp-32], rsi
QWORD PTR [rbp-16], 0
QWORD PTR [rbp-8], 0
.L2
C++ source #1 ø X
A- D +-V&•
1 #include <iostream›
4
// Type your code here, or load an example.
int sum(int64_t N, int64_t A[])
int64_t i, accum=0;
for
(i=0;i<N;i++)
accum += A[i];
10
return accum;
e C++
SAN FRANCISCO
STATE UNIVERSITY
9
10
13
14
15
16
17
18
19
21
22
23
.L3:
mov
lea
mov
add
mov
add
add
rax, QWORD PTR [rbp-8]
rdx, [0+rax*8]
rax, QWORD PTR [rbp-32]
rax, rdx
rax, QWORD PTR [rax]
QWORD PTR [rbp-16], rax
QWORD PTR [rbp-8], 1
.L2:
mov
стр
j1
mov
pop
ret
rax, QWORD PTR [rbp-8]
rax, QWORD PTR [rbp-24]
_L3
rax, QWORD PTR [rbp-16]
rbp
```

## Page 56: How many memory accesses?

```text
   How many memory accesses?
   → 7 memory accesses per loop !!
g++ 11.2.0 -O0 -S → x86 assembly output
   How many bytes/access?
   → accesses are 8 bytes (mov qword ptr)

   Memory access and compute pattern:
   → one item at a time




                                            Copyright © 2026, E. Wes Bethel   56
```

### OCR supplement (verify against PDF)

```text
g+- → 7 memory accesses per loop !!
C++ sourd
// Type your code here, or load an example.
int sum(int64_t N, int64_t A[])
int64_t i, accum=0;
for
(i=0;i<N;i++)
accum += A[i];
return accum;
SAN FRANCISCO
STATE UNIVERSITY
sum(long, long*):
push
jmp
rbp
rop, rsp
QWORD PTR [rbp-24], rdi
QWORD PTR [rbp-32], rsi
QWORD PTR [rbp-16], 0
QWORD PTR [rbp-8], 0
. L2
.L3:
13
14
15
16
17
18
19
21
22
23
lea
add
add
add
.L2:
стр
j1
pop
ret
rax, QWORD PTR [rbp-8]
rdx, [0+rax*8]
rax, QWORD PTR [rbp-32]
rax, rdx
rax, QWORD PTR [rax]
QWORD PTR [rbp-16], rax
QWORD PTR [rbp-8], 1
rax, QWORD PTR [rbp-8]
rax, QWORD PTR [rbp-24]
_L3
rax, QWORD PTR [rbp-16]
rbp
```

## Page 57: g++ 11.2.0 -O2 -free-vectorize -S → x86

```text
g++ 11.2.0 -O2 -free-vectorize -S → x86
assembly output


    How many memory accesses?
    → 1 memory accesses per loop

    How many bytes/access?
    → accesses are 16 bytes (movdqu)

    Memory access and compute pattern:
    → two items at a time (paddq)




                                          Copyright © 2026, E. Wes Bethel   57
```

### OCR supplement (verify against PDF)

```text
g++ 11.2.0 -02 -free-vectorize -S → x86
C++ source
#j
ir
4
return accum;
SAN FRANCISCO
STATE UNIVERSITY
4
9
10
13
14
15
17
18
19
21
22
23
24
25
27
28
29
sum(long, long*):
test
Jie
стр
je
pxor
shr
sal
•L4:
.L3:
стр
jne
movdqa
psridą
movq
je
ret
rdi, rdi
-L6
rdi, 1
_LZ
rax, rai
rax, rsi
xтто, xтте
rdx
rax,
rdx. rsi
xmm2, XMMWORD PTR [rax]
rax, 16
xmm0, xmm2
rdx, rax
.L4
xmm1, xmmо
rdx, rdi
xmm1, 8
rdx,
edi, 1
xmm0, xmm1
rax, xmmo
.L10
rax, QWORD PTR [rsi+rdx*8]
.L10:
```

## Page 58: g++ 11.2.0 -O2 -free-vectorize -mavx2 -S →

```text
g++ 11.2.0 -O2 -free-vectorize -mavx2 -S →
x86 assembly output


    How many memory accesses?
    → 1 memory accesses per loop

    How many bytes/access?
    → accesses are 32 bytes (YMMWORD PTR)

    Memory access and compute pattern:
    → 4 items at a time (vpaddq ymm1)




                                             Copyright © 2026, E. Wes Bethel   58
```

### OCR supplement (verify against PDF)

```text
g++ 11.2.0 -02 -free-vectorize -mavx2 -S
C++ source
#j
ir
7
return accum;
SAN FRANCISCO
STATE UNIVERSITY
9
10
13
14
15
16
17
18
19
21
22
sum(long, long*):
test
jle
lea
стр
Jbe
mov
mov
vpxor
shr
sal
rdi, rai
.L7
rax, [rdi-1]
rax, 2
_L8
rdx, rdi
rax, rsi
xmm1, xmm1, xmm1
rdx, 2
rdx, 5
ndy
nci
.L4:
vpaddq ymm1, ymm1, YMMWORD PTR [rax]
rax, 32
стр
rax, rax
jne
.L4
vmovdqa xmme, xmm1
vextracti128
xmт1, ymт1, 0x1
mov
rax, rdi
xmmo, xmmо, xmm1
rax, -4
1mma
```

## Page 59: g++ 11.2.0 -O2 -free-vectorize -mavx512f -S

```text
g++ 11.2.0 -O2 -free-vectorize -mavx512f -S
→ x86 assembly output


    How many memory accesses?
    → 1 memory accesses per loop

    How many bytes/access?
    → accesses are 64 bytes (ZMMWORD PTR)

    Memory access and compute pattern:
    → 8 items at a time (vpaddq zmm0)




                                              Copyright © 2026, E. Wes Bethel   59
```

### OCR supplement (verify against PDF)

```text
g++ 11.2.0 -02 -free-vectorize -mavx512f -S
C++ source
7
ir
return accum;
13
14
15
16
SAN FRANCISCO
STATE UNIVERSITY
sum(long, long*) :
test
jle
lea
стр
jbe
mov
mov
vpxor
shr
sal
rdi, rdi
.LZ
rax, [rdi-1]
гax, 6
.L8
rdx, rdi
rax, rsi
xmmе, xmmе, xmme
rax, 3
rax, 6
rax, rsi
.L4:
zmmo, zmme, ZMMWORD PTR [rax]
rax, 64
стр
rax, rax
```

## Page 60: g++ -O2 -ftree-vectorize -fopt-info-vec-all -c svs.cpp

```text
                            g++ -O2 -ftree-vectorize -fopt-info-vec-all -c svs.cpp
Vectorization Report Output Shows Use of SSE
Instructions




                                                      Copyright © 2026, E. Wes Bethel   60
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
printf(" inside sum_vector perform_sum, N=%lld \n", N);
int64_t i, accum=0;
16
17
18
for (i=0;i<N;i++)
accum += A[il;
19
return accum;
21
lwes@perlmutter:login08:~/SFSU/sum_harness_answerkey> g++ -02 -ftree-vectorize -fopt-info-vec-all -c svs.cpp
svs.cpp:17:14: optimized: loop vectorized using 16 byte vectors
svs.cpp:12:1: note: vectorized 1 loops in function.
svs.cpp:20:11: note:
***** Analysis failed with vector mode VZD1
svs.cpp:20:11: note:
***** Skipping vector mode V16QI, which would repeat the analysis for VZDI
/opt/cray/pe/gcc/11.2.ø/snos/include/g++/iostream:74:25: missed: statement clobbers memory: std::ios_base::Init::Ini
t (&__ioinit);
opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: sta
missed: statement clobbers memory: __cxxabiv1::__cxa_atexit
(__dt_comp , &__ioinit, &__dso_handle);
svs.cpp:21:1: note: ***** Analysis failed with vector
mode VOID
```

## Page 61: g++ -O2 -march=native -ftree-vectorize -fopt-info-vec-all -c svs.cpp

```text
                    g++ -O2 -march=native -ftree-vectorize -fopt-info-vec-all -c svs.cpp

Vectorization Report Output Shows Use of AVX/AVX2
Instructions




                                                            Copyright © 2026, E. Wes Bethel   61
```

### OCR supplement (verify against PDF)

```text
10
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
wes@perlmutter:login08:~/SFSU/sum_harness_answerkey> g++ -02 -march=native -ftree-vectorize -fopt-info-vec-all -c svl
vs.cpp:17:14: optimized: loop vectorized using 32 byte vectors
vs.cpp:12:1: note: vectorized 1 loops in function.
svs.cpp:20:11: note: ***** Analysis failed with vector mode V4DI
svs.cpp:20:11: note: ***** Skipping vector mode V32QI, which would repeat the analysis for V4DI
/opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: statement clobbers memory: std::ios_base::Init::Ini
t (&__ioinit);
/opt/cray/pe/gcc/11.2.0/snos/include/g++/iostream:74:25: missed: statement clobbers memory: __cxxabiv1::__cxa_atexit
(__dt_comp , &__ioinit, &_dso_handle);
svs.cpp:21:1: note: ***** Analysis failed with vector mode VOID
```

## Page 62: Guidelines for Writing Vectorizable Code

```text
Guidelines for Writing Vectorizable Code
Do:                                              Avoid:
 ●    Use simple for loops
 ●    Straight-line code in loops (avoid
                                                 ●   Function calls (other than math
      conditionals, breaks, returns)                 library calls)
 ●    Use vector-based data structures           ●   read-after-write dependencies
      (arrays)                                   ●   Pointers
 ●    Use array notation rather than pointers
 ●    Use loop index variable directly as a      ●   Non-vectorizable operations
      subscript                                  ●   Mixing vectorizable types in the
 ●    Access memory efficiently: unit stride,        same loop
      avoid indirect addressing, align data to
      16-byte boundaries:                        ●   Data-dependent operations,
       ○   __declspec(align(16)) double a[N];        including loop termination
 ●    Choose data layout with care

                                                                    Copyright © 2026, E. Wes Bethel   62
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 63: Vectorization Thoughts

```text
Vectorization Thoughts
Vectorization can produce significant performance gains

Auto-vectorizing compilers are the way to go: portability

Requires that you pay close attention to how you write your code

You will be studying the performance impact of vectorization in CP#3




                                                             Copyright © 2026, E. Wes Bethel   63
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 64: More Information on Vectorization

```text
More Information on Vectorization
Computer Architecture, Hennessey and Patterson, 5th ed., 2012

Section 4.2: Vector Architecture

https://csu-sfsu.primo.exlibrisgroup.com/permalink/01CALS_SFR/7tr8po/cdi_safari
_books_v2_9780123838735




                                                           Copyright © 2026, E. Wes Bethel   64
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
```

## Page 65: AVX Lineage

```text
AVX Lineage




 Source: https://en.wikipedia.org/wiki/AVX-512




                                                 Copyright © 2026, E. Wes Bethel   65
```

### OCR supplement (verify against PDF)

```text
SAN FRANCISCO
STATE UNIVERSITY
Name
Extension
sets
Registers
Legacy SSE
SSE-
SSE4.2
xmm0-xmm15
AVX-128 (VEX)
AVX, AVX2
xmm0-xmm15
AVX-256 (VEX)
AVX, AVX2
ymm0-ymm15
AVX-128 (EVEX)
AVX-512VL
xmm0-xmm31
(kO-K7)
AVX-256 (EVEX) AVX-512VL
уmm0-уmm31
(kO-k7)
AVX-512 (EVEX)
AVX-512F
zmm0-zmm31
(kO-k7)
Types
single floats
from SSE2: bytes, words,
doublewords, quadwords and
double floats
bytes, words, doublewords,
quadwords, single floats and
double floats
single float and double float
from AVX2: bytes, words,
doublewords, quadwords
doublewords, quadwords, single
float and double float
with AVX512BW: bytes and words.
with AVX512-FP16: half float
doublewords, quadwords, single
float and double float
with AVX512BW: bytes and words.
with AVX512-FP16: half float
doublewords, quadwords, single
float and double float
with AVX512BW: bytes and words
with AVX512-FP16: half float
```

## Page 66: Copyright © 2026, E. Wes Bethel   67

```text
Copyright © 2026, E. Wes Bethel   67
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

# Flyer-1
Customized RISC, 24-bit simulated CPU, heavily inspired by use of computers in aerospace and defense application.

The Flyer-1 computer sports a 24-bit wide data bus, capable of computation in both integer and fixed-point format. With an address bus identical in size, a total memory of 50.3MB (16.7MB × 3B) can be allocated for both data and instructions. Basic arithmetic and bitwise logic operations are implemented inside the ALU with Logisim's stock circuit components. Available peripheral components include 8 digital ports that can be connected to I/O devices such as TTY (Teletypewriter), along with 4 analog ports (simulated as digital, because Logisim can't bother to add analog functionality... sigh).

Hardware and software design of Flyer-1 takes inspiration from RISC (_Reduced Instruction Set Computer_) and CISC (_Complex Instruction Set Computer_) processors from 1960s up to 1990s, being the MOS 6502 (Commodore 64), Intel 8086 (Tandy 1000), Motorola 68000 and Intel i386 (Airbus Flight Computers). As far as the author concerns, this computer's classification between RISC and CISC is somewhat blurry, and the author would be glad to consult with experts on this matter.

This README is barely enough to serve as an entire technical documentation; it's merely a quick introduction to the system and practices of programming it.

## Instruction Set Architecture

![Flyer 1 - 01](https://github.com/user-attachments/assets/2d20c872-8f3d-4c9e-b0fa-8e2ab72c9dd0)

_Figure 1. Flyer-1 computer general circuitry._

### Processor Registers

![Flyer 1 - 02](https://github.com/user-attachments/assets/f3fea21f-3d84-4767-9246-711c09332730)

_Table 1. Flyer-1 computer registers._

### Data Formats

1. Integer Number (2's complement system)

![Flyer 1 - 03](https://github.com/user-attachments/assets/7e4bdc95-fe17-423e-9f5d-e2e9cda7418c)

_Table 2a. Integer number formatting._

2. Fixed-Point Number (2's complement system)

![Flyer 1 - 04](https://github.com/user-attachments/assets/767e9b89-7c16-46ff-9f75-1c4a065328ce)

_Table 2b. 24-bit Fixed-Point number formatting._

3. ASCII 3-Character String

![Flyer 1 - 05](https://github.com/user-attachments/assets/7931b4cf-fec9-4b45-aa46-561f5077ab8f)

_Table 2c. ASCII 3-Char string formatting._

### Major Components

#### 1. Arithmetic Logic Unit (ALU)

The ALU is where every mathematical and bitwise logic operations are commenced within the processor. Instructions include basic math (add, subtract, multiply, divide) and bitwise logic (AND, OR, XOR, NOT, comparison, barrel shift, cyclic shift/rotate). The 'A' input is connected to general data bus via TX (temporary) register, that retrieves the contents of AX (accumulator) for instructions involving data inside AX. On the other hand, 'B' input is directly connected to general data bus, enabling shorter execution time and simpler circuitry. The two outputs of ALU being the 'S' (operation results) and 'F' (flags), each connected to AX and FLAG registers.

Inside the ALU are multiple circuits dedicated for specific operations. Addition and subtraction utilize a full adder-subtractor (FAS) unit, capable of subtraction by complimenting 'B' input and turning the carry input HIGH, while the reverse applies for addition. Multiplication and division operation each utilize stock circuit components already simulated in Logisim. Bitwise logic operations saw the use of commonly-found logic gates, barrel and cyclic shifters, and comparator circuits. The outputs for all ALU instructions, except comparison (CMP), is channeled through three-state bus buffers, controlled by instruction decoders.

Per v1.0 (24/4/2025), the conversion circuit between integer and fixed-point numbers are still being developed.

![Flyer 1 - 06](https://github.com/user-attachments/assets/da35a84a-98eb-4b8b-a3c2-98d0901ff65b)

_Figure 2. Arithmetic Logic Unit (ALU) internal circuitry._

#### 2. Control Unit (CU)

Control unit determines which and when do counters increment/decrement, registers/memory would be read from or written into, which peripheral ports would be selected and where data flows inside the processor. This operation is accomplished by the use of combinational logic gates, similar to what is used in RISC processors. This approach is selected on the basis of convenience in configuring the logic wiring, as opposed to using ROM and determining its contents (control words) that is known as micro-coding, and are commonly found in CISC processors.

Inputs required to determine the control words are first most-significant 9 bits of opcode word (B<sub>23-15</sub>) and 3-bit clock cycle counter, along with ALU flags stored in FLAG register. The latter is used to determine whether or not conditional branching instructions concurs with status/flags after previous instructions. The FLAG input would pass through a flag matching unit (top left corner, array of AND gates connected to one OR gate). If the opcode bits of B<sub>18-15</sub> matches those with flags coming in, then corresponding AND gate would turn HIGH, and a conditional branching instruction can be executed.

The 3-bit clock cycles and opcode bits B<sub>23-19</sub> each passes through decoders. If a control wire needs to turn HIGH at clock cycle X (0..7) and when instruction Y (00..1F) is inputted, then a corresponding AND gate connects to both the decoded X and Y, where the gate's output is then channeled through OR gates for that control wire. Said OR gate also takes input from numerous similar AND gate corresponding to other instruction and clock cycles. The AND gate that correlates to conditional branching instructions have 3 inputs instead of normal 2, connected to the outputs of flag matching unit.

Another possible way to implement said combinational logic is through the use of PLA (Programmable Logic Array) or FPGA (Field-Programmable Gate Array), where these options are also considered for future developments of the Flyer-1 computer.

![Flyer 1 - 07](https://github.com/user-attachments/assets/fdeb1c01-cd4e-44a9-a7b3-fcf45df6658b)

_Figure 3. Control Unit (CU) internal circuitry._

Clock cycle counter, also commonly known as digital frequency divider, is comprised of a counter connected to clock (square wave input) and D-latch circuits. Whether the reference for clock cycle change is a rising-edge or falling-edge wave segment, it counts and outputs an n-bit value of how many clock cycles have passed (0..(2^n)-1). The latching circuit is connected to 'HALT' and 'RESET' inputs, where 'HALT' would have the effect of stopping further clock cycle counting when a HALT instruction is evaluated, and 'RESET' resets said stopping condition by manual inputs (e.g., a push button). 

![Flyer 1 - 08](https://github.com/user-attachments/assets/21f98a7e-4fde-4f02-9fb9-ae0a10782942)

_Figure 4. Digital frequency divider / clock cycle counter unit._

#### 3. Peripheral Unit (PU)

Peripheral unit consists of 8 digital ports (PD) and 4 analog ports (PA), each with its respective gate selector and data buffers.

![Flyer 1 - 09](https://github.com/user-attachments/assets/df66f556-6937-4c7a-9bd0-11e597a8d331)

_Figure 5. Peripheral unit with 8 digital ports and 4 analog ports._

#### 4. Random Access Memory (RAM)

Flyer-1 main memory runs on 24-bit wide data and address bus, giving a total of 16.777.216 memory locations; considering that 24-bit equals to 3 bytes, this gives the total memory capability of 50.3 MByte. The memory is further divided into five segments based on their use, as shown in Figure 6 below. The stack can be allocated to store variables in case of mathematical operations that require PEMDAS rule when executed, or other conditions that may necessitate priority-based memory. Reserve memory can be allocated to store peripheral data or programs etc.

![Flyer 1 - 10](https://github.com/user-attachments/assets/b77fe7a9-ff55-495d-8085-14e28f61f2af)

_Table 3. Memory segmentation chart for Flyer-1 computer._

### Instruction Set

Below are listed the total 43 instructions valid for programming the Flyer-1 computer. The list below only contains the basic addressing modes without any variable or loop name whatsoever; for that segment, please refer to Assembly Language section of this README.
_CAUTION: Illegal opcodes may have the risk of stalling the device, corrupting stored data or any other unintended consequences. USE UNDER YOUR OWN RISK._

![Flyer 1 - 12](https://github.com/user-attachments/assets/34166b05-9ff0-48ff-bb69-ef957f9481c1)

_Table 4. Instruction set table for Flyer-1 computer._

### Control Code Table

Execution of instructions are divided into clock cycle counts, which differs between one instruction and the other. This clock cycle count is provided by 3-bit (0..7) digital frequency divider unit, always counting upwards and resets at max value.

Each components within the computer has its own control codes, that dictates whether it must store (hold) or output (open) data flow from and into buses, when counters must count up or down and output their values, when to read from or write into RAM etc. In total, there are 26 control wires.

![Flyer 1 - 11](https://github.com/user-attachments/assets/e724d595-ec96-4f88-a948-5b0f4ac11561)

_Table 5. Flyer-1 control word truth table._

## Assembly Language

Assembly program of Flyer-1 consists of three sections separated by curly brackets; **stat** (contains static variable declarations), **var** (contains dynamic variable declarations) and **text** (where your instructions are written). Below is an example of Fibonacci program, that counts Fibonacci numbers from 1 to 105329 as an upper limit.

```
// This is how you write a comment in one line.
// This is how you
// write a comment that
// spans multiple lines.

stat {
  // Variables declared inside this bracket won't change along program runtime.
  int lit_0,#05ae4c             // For int variables, if there's a slash (#), the numbers you typed after that are read as hexadecimals.
  int lit_1,105329              // If you just typed a number without #, it's read as decimals.
  fix lit_2,1305.06275          // Fixed-point variables are directly typed with dots for decimal points.
  asc lit_3,hW!                 // For ASCII 3-char string variables, you just type the corresponding ASCII character (can't be more than 3!)
}

var {
  // Variables declared within var are flexible to change by the program during runtime.
  int x,0
  int y,1
  int z,0
}

text {
  // This is where you'll write your instructions.
start:
  // THIS SEGMENT MUST EXIST. IF YOU DELETE 'start:' THEN ANY INSTRUCTION YOU'VE TYPED IN
  // WON'T BE ABLE TO RUN, AS YOU DIDN'T PROVIDE A STARTING POINT OF EXECUTION.
  dop x,01        // x is outputted to Digital Port 01
  add x,y         // AX = x + y
  sta z           // z = AX. Hence, z = x + y
  trx y,x         // x = y
  trx z,y         // y = z
  cmp x,lit_1     // Compares x against lit_1 (105329)
  jna start       // If x isn't larger than lit_1, back to start (count again)
  jmp end         // If the 'jna' above isn't met, jump to end (termination)
end:
  // AT LEAST THERE MUST BE ONE TERMINATION POINT, MARKED WITH 'hlt' INSTRUCTION.
  // Termination segment doesn't necessarily need to be written as 'end:' though.
  dop lit_3,02    // lit_3 (hW!) is outputted to Digital Port 02.
  hlt             // Halt until reset.
}
```

### Typing Discipline
#### Declaring Variables
To declare an integer variable, one can follow either methods below:
```
int __name__,__value__

int x,314159    // Declare 'x' as an integer with value of 314159 (decimal)
int y,#271828   // Declare 'y' as an integer with value of 271828 (hexadecimal)
```
To declare a fixed-point variable, one must follow this method below:
```
fix __name__,__whole__.__fraction__

fix z,1.73205   // Declare 'z' as a fixed-point with value of 1.73209 (this would later be converted into fractional binary)
```
To declare an ASCII 3-char variable, one must adhere to the method below:
```
asc __name__,__char__

asc goodword,Hi!  // Declare 'goodword' as ASCII 3-char string with characters 'Hi!'
```
Based on which sections does the variable live (**stat** or **var**), the assembler would automatically allocate memory locations to store it. The storage order follows which variable is written first within the brackets.

#### Instruction Operands
In the previous **Instruction Set** segment, the operands are written in what they signify within its execution, either an $ADDRESS, #DATA or PORT. While one can program the entire Flyer-1 computer without even once replacing variable addresses with their names (or labels, as it's called in an assembler program), it would be worthwhile to understand what other methods can one use to program the computer.
**Memory Instructions** (lda, sta, trx, pst, pop)
```
lda $00347a          // Directly load data from address ($) 00347a to accumulator
lda x                // Load the contents of variable 'x' into accumulator (x --> signifies its location)
sta $33165f          // Same thing goes for 'sta' instruction,
sta y                // both the $ or variable-name addressing methods.

trx $17ff3e,a        // Transfer whatever is at $17ff3e to wherever 'a' is located
trx b,$7940ab        // Same thing for 'trx' in reverse, wherever 'b' is got transferred to $7940ab
trx $649007,$172943  // A direct transfer involving specified addresses can also be done

pst x                // One can accomplish stack operations (both 'pst' and 'pop') by either using variables,
pst $3306ac          // Or by directly writing which address would have its contents got pushed into stack.
```
**Branching Instructions** (jmp, jcb, ..., jpo)
```
jeq foo              // Jump if equal to 'foo:' loop
jmp bar              // Jump to 'bar:' loop without conditions
jmp $000374          // NOT RECOMMENDED: You can directly type in where to jump, but that location might not contain an opcode...
jng $30511e          // NOT RECOMMENDED: Same thing goes for conditional branching instructions...
```

### How To Program It?

## Future Plans
Per this release (v1.0), the foreseeable developments of Flyer-1 would involve some of the topics listed below.
1. Development of a general-purpose OS (operating system) similar to computers between 1980-1990, e.g. MS-DOS, Unix, Commodore64. May also try to develop graphical OS, similar to Windows 1.0 or Windows 95.
2. Physical (microprocessor package) circuit based on the Flyer-1's architecture; Said microprocessor chip are planned for integration into a single-board computer (currently also under feasibility study), akin to PE6502 or Gigatron TTL.

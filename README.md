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

|**Instruction**|**Action**|**Description**|
|-|-|-|
|`lda $addr`|`AX = [$addr]`|Load from location `$addr` into accumulator|
|`ldi #data`|`AX = #data`|Load immediate value `#data` into accumulator|
|`sta $addr`|`[$addr] = AX`|Store accumulator into location `$addr`|
|`sti $addr,#data`|`[$addr] = #data`|Store immediate value `#data` into `$addr`|
|`trx $adr1,$adr2`|`[$adr1] = [$adr2]`|Transfer addressed from `$adr1` to `$adr2`|
|`jmp $addr`|`PC = $addr`|Jump unconditional to next instruction at `$addr`|
|`jcb $addr`|`PC = $addr`|Jump if carry or borrow to `$addr`|
|`jnc $addr`|`PC = $addr`|Jump if not carry or borrow to `$addr`|
|`jal $addr`|`PC = $addr`|Jump if A>B to `$addr`|
|`jna $addr`|`PC = $addr`|Jump if not A>B to `$addr`|
|`jeq $addr`|`PC = $addr`|Jump if A=B to `$addr`|
|`jnq $addr`|`PC = $addr`|Jump if not A=B to `$addr`|
|`jzr $addr`|`PC = $addr`|Jump if A=0 to `$addr`|
|`jnz $addr`|`PC = $addr`|Jump if not A=0 to `$addr`|
|`jng $addr`|`PC = $addr`|Jump if A negative to `$addr`|
|`jps $addr`|`PC = $addr`|Jump if A positive to `$addr`|
|`jpe $addr`|`PC = $addr`|Jump if A parity even to `$addr`|
|`jpo $addr`|`PC = $addr`|Jump if A parity odd to `$addr`|
|`clf`|`FLAG = 0`|Clear the flag register|
|`dip $addr,port_D`|`[$addr] <- port_D`|Digital input from port `port_D` to `$addr`|
|`dop $addr,port_D`|`port_D <- [$addr]`|Digital output to port `port_D` from `$addr`|
|`aip $addr,port_A`|`[$addr] <- port_A`|Analog input from port `port_A` to `$addr`|
|`aop $addr,port_A`|`port_A <- [$addr]`|Analog output to port `port_A` from `$addr`|
|`pst $addr`|`[$addr] -> stack, sp++`|Push from `$addr` to stack|
|`pop $addr`|`stack -> [$addr], sp--`|Pop from stack to `addr`|
|`nop`| |No operation|
|`hlt`| |Halt until reset|
|`add $adr1,$adr2`|`ax = [$adr1]+[$adr2]`|Add contents of address `$adr1` and `$adr2`|
|`sub $adr1,$adr2`|`ax = [$adr1]-[$adr2]`|Subtract contents of address `$adr1` and `$adr2`|
|`mul $adr1,$adr2`|`ax = [$adr1]*[$adr2]`|Multiply contents of address `$adr1` and `$adr2`|
|`div $adr1,$adr2`|`ax = [$adr1]/[$adr2]`|Divide contents of address `$adr1` and `$adr2`|
|`ana $addr`|`ax = ax & [$addr]`|Logical AND accumulator with contents of `$addr`|
|`ora $addr`|`ax = ax ∨ [$addr]`|Logical OR accumulator with contents of `$addr`|
|`xra $addr`|`ax = ax ⊕ [$addr]`|Logical XOR accumulator with contents of `$addr`|
|`not $addr`|`ax = ¬[$addr]`|Logical NOT contents of `$addr`|
|`cmp $adr1,$adr2`|`flag = [$adr1]?=[$adr2]`|Compare the contents on locations `$adr1` and `$adr2`|
|`shl $adr1,$adr2`|`ax = [$adr1] << [$adr2]`|Shift left `[$adr1]` by `[$adr2]`|
|`shr $adr1,$adr2`|`ax = [$adr1] >> [$adr2]`|Shift right `[$adr1]` by `[$adr2]`|
|`rol $adr1,$adr2`|`ax = [$adr1] <: [$adr2]`|Rotate left `[$adr1]` by `[$adr2]`|
|`rol $adr1,$adr2`|`ax = [$adr1] :> [$adr2]`|Rotate right `[$adr1]` by `[$adr2]`|
|`cla`|`ax = 0`|Clear accumulator|
|`itf $addr`|`ax = fix([$addr])`|Convert `[$addr]` from integer to fixed-point|
|`fti $addr`|`ax = int([$addr])`|Convert `[$addr]` from fixed-point to integer|

### Control Code Table

Execution of instructions are divided into clock cycle counts, which differs between one instruction and the other. This clock cycle count is provided by 3-bit (0..7) digital frequency divider unit, always counting upwards and resets at max value.

Each components within the computer has its own control codes, that dictates whether it must store (hold) or output (open) data flow from and into buses, when counters must count up or down and output their values, when to read from or write into RAM etc. In total, there are 26 control wires.

![Flyer 1 - 11](https://github.com/user-attachments/assets/e724d595-ec96-4f88-a948-5b0f4ac11561)

_Table 4. Flyer-1 control word truth table._

## Assembly Language

### General Overview

The computer's assembly language follows that of computers mentioned earlier. The source file is divided into three sections: **stat**, containing declaration of static variables; **var**, declaration of dynamic variables; and **text** that contains all instructions necessary to work with said variables before. These sections are separated by brackets as shown below. Current version can only support single-line comments, that begin with ```//``` slashes.
```
.stat
  // Declaration of static variables: __type__ __name__,__value__
  // Variables declared as static (in this section) cannot, and will not, have its values manipulated by corresponding instructions during its runtime.

.var
  // Declaration of dynamic variables: __type__ __name__,__value__
  // As opposed to static, dynamic variables can be freely manipulated by corresponding instructions.

.text
  // Where one would write every instructions necessary.
start:        // Loop 'start'
  __inst_0__  // 'start' segment must always exist within text{...}. Otherwise, any programs and loop segments you've written won't run.
  __inst_1__  // This is because 'start' segment provides a starting point of program execution for the processor.
  __inst_2__
  __inst_3__
foo:          // Loop 'foo'
  __inst_4__
  __inst_5__
  __inst_6__
bar:          // Loop 'bar'
  __inst_7__
  __inst_8__
  __inst_9__
```

### Instruction Loops

In more elaborate programs, it is necessary to separate segments of instructions based on their functions (complex math functions, pixel rendering, etc.). This separation of instruction segments are known as loops, which are written in Flyer-1 assembly format as ```__loopName__:``` (it always ends with colons).

These separated programs begin in different addresses, and with the compiled code having no comments for the programmer to know which instruction starts which loop, this task of memory allocation is automatically handled by assembler program. As long as there's a loop name, whenever it is required to jump to some loop, you can just write the loop name after branching instructions, as shown below,
```
foo:
  __inst_0__
  __inst_1__
  ...
  jeq bar      // Jump if A=B to bar
  jal foo      // Jump if A>B to foo
  jmp baz      // Jump to baz
bar:
  __inst_2__
  __inst_3__
  ...
  jzr foo      .. Jump if A=0 to foo
  jmp qux      // Jump to qux
baz:
  __inst_4__
  __inst_5__
  ...
  jcb bar      // Jump if Carry or Borrow to bar
  jmp qux      // Jump to qux
qux:
  __inst_6__
  __inst_7__
  ...
  jpe foo       // Jump if A Even to foo
  hlt
```

### Variable Declarations

As previously mentioned in the **Instruction Set Architecture** chapter, there are three supported types of variable used within the Flyer-1 computer, that are **int** (integer number), **fix** (fixed-point number) and **asc** (ASCII 3-char string).

To declare **int** variables, one can follow either format below,
```
int a,#33ae4c       // #NUMBER --> NUMBER is declared as Hex, and are now the value of 'a'
int b,314285        // NUMBER --> NUMBER is declared as Dec, and are now the value of 'a'
```
To declare **fix** variables, one must adhere to the format below,
```
fix c,2.71828       // Just directly type the number with points as decimal fractions.
```
To declare **asc** variables, this format must be used,
```
asc d,wt?           // Just directly type any keyboard character, as long as it's just 3 chars long.
```

The variables would be automatically placed into memory locations based on their type (static or dynamic), where the first declared variable gets first place, and so on. Since the address of each variables are only shown in the assembled (hex memory maps) file, one has no method to obtain specific locations of each and every variable unless directly modifying the assembled hex file. For this, one only have to write the involved variable's name as operands, where it represents (or acts as a pointer towards) the variable's location.

### Example Program: Fibonacci

```
// This program counts Fibonacci numbers, a(N) = a(N-1) + a(N-2), from 0. (0, 1, 1, 2, 3, 5, 8, 13, ...)
// The upper limit for this Fibonacci calculation is 100000, stated as lit_0.

.stat
  int lit_0,100000    // lit_0: literal 0, int, 100000 decimal
  asc lit_1,Hw!       // lit_1: literal 1, asc, 'Hw!'

.var
  int x,0    // x = 0 decimal
  int y,0    // y = 1 decimal
  int z,0    // z = 0 decimal

.text
start:
  dop x,01       // Output x to port digital 01
  add x,y        // AX = x + y
  sta z          // z = AX; hence z = x + y
  trx y,x        // x = y
  trx z,y        // y = z
  cmp x,lit_0    // Compare x against lit_0 (100000 decimal)
  jna start      // Jump if not A>B to start
  jmp end        // Jump to end if previous instruction isn't fulfilled
end:
  dop lit_1,01   // Output lit_1 ('Hw!') to port digital 01
  dop x,02       // Output x to port digital 02
  hlt            // Halt
```

### How Do I Run The Program?

If one were to operate the simulated hardware (`Flyer1.circ`) and write programs in it, the pre-requisites are **Logisim Evolution v3.8.0** along with **Python 3.0 and above**.
1. After validating that the two pre-requisites are already installed as they are (yes, it does not require further add-on modules or libraries), download the file.
2. Write the program according to the guidelines above, and save it with `__name__.asm` extension.
3. Using the CMD or Powershell (Windows) or Terminal (Linux), change directory to the path of this downloaded file.
4. Type the following command: `python Flyer1_Assembler.py __name__.asm`
5. The output would have the words `v3.0 hex words addressed`. Copy all the output lines, paste them into a text editor. Save it as `Flyer1RAMContent.txt` for easier identification.
6. Open the circuit `Flyer1.circ`, right-click on the RAM and select 'Load Image' then search for `Flyer1RAMContent.txt`
7. Click Ctrl+K, and off it goes until you halt them.

## Future Plans
Per this release (v1.0), the foreseeable developments of Flyer-1 would involve some of the topics listed below.
1. Making a better assembler that visually appears similar to code editors.
2. Addition of more data formats (long strings, floating-point numbers, list/tuple etc.) and macros in the assembler.
3. An emulator built on Python (and then transferred to C/C++ for better speed), running as if it's real time.
4. Development of an OS, both general-purpose and embedded.
5. Creating a physical version of the computer, with the help of... I don't know, but if time, resources and plans permit, I wanna do this. 

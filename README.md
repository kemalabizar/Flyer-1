# Flyer-1
Customized RISC, 24-bit simulated CPU, heavily inspired by use of computers in aerospace and defense application.

The Flyer-1 computer sports a 24-bit wide data bus, capable of computation in both integer and fixed-point format. With an address bus identical in size, a total memory of 50.3MB (16.7MB × 3B) can be allocated for both data and instructions. Basic arithmetic (add, subtract, multiply, divide) and bitwise logic operations (AND, OR, XOR, NOT, compare, shift, roll) are implemented inside the ALU as stock circuit components inside Logisim. Available peripheral components include 8 digital ports that can be connected to I/O devices such as TTY (Teletypewriter), along with 4 analog ports (simulated as digital, because Logisim can't bother to add analog functionality... sigh).

Hardware and software design of Flyer-1 takes inspiration from RISC and CISC processors from 1960s up to 1990s, being the MOS 6502 (Commodore 64), Intel 8086 (Tandy 1000), Motorola 68000 (Airbus Flight Computers) and D-37C (Minuteman II ICBM Guidance Computer). If that last bit sounds concerning, _don't worry; it's up there on Wikipedia and Internet Archive, and the docs says **DECLASSIFIED**_.

## Instruction Set Architecture
![Flyer 1 - 01](https://github.com/user-attachments/assets/2d20c872-8f3d-4c9e-b0fa-8e2ab72c9dd0)

### Processor Registers
![Flyer 1 - 02](https://github.com/user-attachments/assets/f3fea21f-3d84-4767-9246-711c09332730)

### Data Formats

1. Integer Number (2's complement system)

![Flyer 1 - 03](https://github.com/user-attachments/assets/7e4bdc95-fe17-423e-9f5d-e2e9cda7418c)

2. Fixed-Point Number (2's complement system)

![Flyer 1 - 04](https://github.com/user-attachments/assets/767e9b89-7c16-46ff-9f75-1c4a065328ce)

3. ASCII 3-Character String

![Flyer 1 - 05](https://github.com/user-attachments/assets/7931b4cf-fec9-4b45-aa46-561f5077ab8f)

### Major Components
#### 1. Arithmetic Logic Unit (ALU)
#### 2. Control Unit (CU)
#### 3. Peripheral Unit (PU)
#### 4. Random Access Memory (RAM)
### Instruction List and Encoding

## Assembly Language
### General Overview
### Writing The Program

## How Do I Make It Run?
### Assembler Program: Making It Run

## Future Plans

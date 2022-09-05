# BIL - Basic Intemediate Language

It's a bit like assembly but with yaml-like syntax and with several shorthands.

BIL programs have a structure very similar to their asm counterparts:

- variables section (section .bss)
- constants section (section .data)
- entry section (section .text)
- run (syscall)

Oh, and it supports complex numbers because you can't tell me what to do :)

## Output

A regular asm program to stdout may look like this:

```x86asm
section .data
  string db "Hello World!", 10
  stringLength equ $-hello

section .text
  global _start

  _start:
    mov rax, 1
    mov rdi, 1
    mov rsi, hello
    mov rdx, helloLength
    syscall

    mov rax, 60
    mov rdi, 0
    syscall
```

The equivalent program in BIL will look like this:

```x86asm
symbols:
  constants:
    string: "Hello World"

entry:
  mode print
  load :string
  run

  mode exit
  run
```
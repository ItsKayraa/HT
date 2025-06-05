section .data
text0 db "6.0", 10
len0 equ $ - text0
section .text
global _start

_start:
mov rax, 1
mov rdi, 1
mov rsi, text0
mov rdx, len0
syscall

mov rax, 60
xor rdi, rdi
syscall

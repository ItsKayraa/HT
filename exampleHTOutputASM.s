section .data
text_d4c0dbc28fc8488bb71c8a6095cf7aa30 db "Hello, World!", 10
len_d4c0dbc28fc8488bb71c8a6095cf7aa30 equ $ - text_d4c0dbc28fc8488bb71c8a6095cf7aa30
section .text
global _start

_start:
mov eax, 4
mov ebx, 1
mov ecx, text_d4c0dbc28fc8488bb71c8a6095cf7aa30
mov edx, len_d4c0dbc28fc8488bb71c8a6095cf7aa30
int 0x80

mov eax, 1
xor edi, edi
int 0x80

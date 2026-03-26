.syntax unified
.arch armv7-a
.fpu vfp
.text
.global main
main:

    @ Habilitar VFP
    MRC p15, 0, r0, c1, c0, 2
    ORR r0, r0, #0xF00000
    MCR p15, 0, r0, c1, c0, 2
    ISB
    MOV r0, #0x40000000
    VMSR FPEXC, r0

    @ ---- linha 0 ----

    @ Carrega 3 -> s0
    LDR r0, =num_0
    VLDR s0, [r0]

    @ Carrega 4 -> s1
    LDR r0, =num_1
    VLDR s1, [r0]

    @ Operacao +: s0 + s1 -> s0
    VADD.F32 s0, s0, s1

    @ Salva resultado da linha 0 em res_array
    LDR r1, =res_array
    LDR r2, =0
    ADD r1, r1, r2, LSL #2
    VSTR s0, [r1]

    @ Exibe resultado de s0 nos LEDs
    PUSH {r4, r5}         @ salva r4/r5 (callee-saved AAPCS)
    VCVT.F64.F32 d0, s0
    VMOV r4, r5, d0
    LDR r1, =0xFF200000
    STR r5, [r1]          @ MSB (parte alta)
    MOV r0, #0
    STR r0, [r1]          @ apaga
    STR r4, [r1]          @ LSB (parte baixa)
    MOV r0, #0
    STR r0, [r1]          @ apaga
    POP {r4, r5}          @ restaura r4/r5

    @ Fim da execucao
    BX LR

.data

res_array:
    .space 4   @ 1 floats de 4 bytes

num_0:
    .float 3

num_1:
    .float 4


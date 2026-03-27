.syntax unified
.arch armv7-a
.fpu vfpv3-d16
.text
.global main
main:

    @ Habilitar VFP (dupla precisao IEEE 754 64 bits)
    MRC p15, 0, r0, c1, c0, 2
    ORR r0, r0, #0xF00000
    MCR p15, 0, r0, c1, c0, 2
    ISB
    MOV r0, #0x40000000
    VMSR FPEXC, r0

    @ ---- linha 0 ----

    @ Carrega 3 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_0
    VLDR d0, [r0]

    @ Carrega 4 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_1
    VLDR d1, [r0]

    @ Operacao +: d0 + d1 -> d0  (F64)
    VADD.F64 d0, d0, d1

    @ Salva resultado da linha 0 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #0
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 1 ----

    @ Carrega 10 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_2
    VLDR d0, [r0]

    @ Carrega 3 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_3
    VLDR d1, [r0]

    @ Operacao -: d0 - d1 -> d0  (F64)
    VSUB.F64 d0, d0, d1

    @ Salva resultado da linha 1 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #1
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 2 ----

    @ Carrega 5 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_4
    VLDR d0, [r0]

    @ Carrega 6 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_5
    VLDR d1, [r0]

    @ Operacao *: d0 * d1 -> d0  (F64)
    VMUL.F64 d0, d0, d1

    @ Salva resultado da linha 2 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #2
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 3 ----

    @ Carrega 20 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_6
    VLDR d0, [r0]

    @ Carrega 4 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_7
    VLDR d1, [r0]

    @ Operacao /: d0 / d1 -> d0  (F64)
    VDIV.F64 d0, d0, d1

    @ Salva resultado da linha 3 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #3
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 4 ----

    @ Carrega 17 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_8
    VLDR d0, [r0]

    @ Carrega 5 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_9
    VLDR d1, [r0]

    @ Operacao //: d0 // d1 -> d0  (F64)
    VDIV.F64 d0, d0, d1
    VCVT.S32.F64 s31, d0
    VCVT.F64.S32 d0, s31

    @ Salva resultado da linha 4 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #4
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 5 ----

    @ Carrega 17 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_10
    VLDR d0, [r0]

    @ Carrega 5 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_11
    VLDR d1, [r0]

    @ Operacao %: d0 % d1 -> d0  (F64)
    VDIV.F64 d2, d0, d1
    VCVT.S32.F64 s31, d2
    VCVT.F64.S32 d2, s31
    VMUL.F64 d2, d2, d1
    VSUB.F64 d0, d0, d2

    @ Salva resultado da linha 5 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #5
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 6 ----

    @ Carrega 2 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_12
    VLDR d0, [r0]

    @ Carrega 8 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_13
    VLDR d1, [r0]

    @ Operacao ^: d0 ^ d1 -> d0  (F64)
    VCVT.S32.F64 s31, d1
    VMOV r1, s31
    LDR r2, =num_14
    VLDR d2, [r2]
pow_14_loop:
    CMP r1, #0
    BLE pow_14_end
    VMUL.F64 d2, d2, d0
    SUB r1, r1, #1
    B pow_14_loop
pow_14_end:
    VMOV.F64 d0, d2

    @ Salva resultado da linha 6 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #6
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 7 ----

    @ Carrega 3 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_15
    VLDR d0, [r0]

    @ Carrega 2 -> d1  (IEEE 754 64 bits)
    LDR r0, =num_16
    VLDR d1, [r0]

    @ Carrega 4 -> d2  (IEEE 754 64 bits)
    LDR r0, =num_17
    VLDR d2, [r0]

    @ Operacao *: d1 * d2 -> d1  (F64)
    VMUL.F64 d1, d1, d2

    @ Operacao +: d0 + d1 -> d0  (F64)
    VADD.F64 d0, d0, d1

    @ Salva resultado da linha 7 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #7
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 8 ----

    @ Carrega 1 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_18
    VLDR d0, [r0]

    @ (N RES) - busca resultado N posicoes atras (64 bits)
    VCVT.S32.F64 s31, d0
    VMOV r1, s31
    MOV r2, #8
    SUB r1, r2, r1
    CMP r1, #0
    BGE res_ok_8_1
    @ indice invalido -> carrega 0.0
    LDR r2, =num_19
    VLDR d0, [r2]
    B res_end_8_1
res_ok_8_1:
    LDR r2, =res_array
    ADD r2, r2, r1, LSL #3
    VLDR d0, [r2]
res_end_8_1:

    @ Salva resultado da linha 8 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #8
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ ---- linha 9 ----

    @ Carrega 42.5 -> d0  (IEEE 754 64 bits)
    LDR r0, =num_20
    VLDR d0, [r0]

    @ (V MEM): salva d0 em MEM_var (64 bits)
    LDR r1, =MEM_var
    VSTR d0, [r1]

    @ Salva resultado da linha 9 em res_array (8 bytes)
    LDR r1, =res_array
    MOV r2, #9
    ADD r1, r1, r2, LSL #3
    VSTR d0, [r1]

    @ Exibe resultado de d0 nos LEDs (IEEE 754 64 bits)
    PUSH {r4, r5}
    VMOV r4, r5, d0        @ r4=LSB, r5=MSB do double
    LDR r1, =0xFF200000
    STR r5, [r1]               @ MSB (parte alta do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    STR r4, [r1]               @ LSB (parte baixa do double)
    MOV r0, #0
    STR r0, [r1]               @ apaga
    POP {r4, r5}

    @ Fim da execucao
    BX LR

.data
.align 3

MEM_var:
    .double 0.0

.align 3
res_array:
    .space 80   @ 10 doubles de 8 bytes (IEEE 754 64 bits)

.align 3
num_0:
    .double 3

.align 3
num_1:
    .double 4

.align 3
num_2:
    .double 10

.align 3
num_3:
    .double 3

.align 3
num_4:
    .double 5

.align 3
num_5:
    .double 6

.align 3
num_6:
    .double 20

.align 3
num_7:
    .double 4

.align 3
num_8:
    .double 17

.align 3
num_9:
    .double 5

.align 3
num_10:
    .double 17

.align 3
num_11:
    .double 5

.align 3
num_12:
    .double 2

.align 3
num_13:
    .double 8

.align 3
num_14:
    .double 1.0

.align 3
num_15:
    .double 3

.align 3
num_16:
    .double 2

.align 3
num_17:
    .double 4

.align 3
num_18:
    .double 1

.align 3
num_19:
    .double 0.0

.align 3
num_20:
    .double 42.5


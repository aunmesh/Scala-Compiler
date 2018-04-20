	.data
t6:	.word	0
m:	.word	0
t4:	.word	0
t5:	.word	0
t2:	.word	0
l:	.word	0
t0:	.word	0
t1:	.word	0
t3:	.word	0
n:	.word	0


	.text
main:

BLOCK1:
	li $t9, 0
	move $t8, $t9
	sw $t8, n
	sw $t9, t0
	li $t9, 0
	move $t8, $t9
	sw $t8, m
	sw $t9, t1
	li $t9, 0
	move $t8, $t9
	sw $t8, l
	sw $t9, t2
	li $t9, 2
	move $t8, $t9
	sw $t9, t3
	li $t9, 3
	move $t3, $t9
	sw $t9, t4
	move $t9, $t8
	add $t9, $t9, $t3
	sw $t8, m
	sw $t3, n
	move $t8, $t9
	sw $t9, t5
	move $t9, $t8
	sw $t9, t6
	sw $t8, l
	li $v0, 1
	lw $t9, t6
	move $a0, $t9
	syscall
	addi $a0, $0, 0xA
	addi $v0, $0, 0xB
	syscall
	li $v0, 10
	syscall



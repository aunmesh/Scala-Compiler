	.data
t8:	.word	0
t9:	.word	0
t6:	.word	0
t7:	.word	0
t5:	.word	0
t10:	.word	0
t11:	.word	0
t12:	.word	0


	.text

BLOCK1:
	fun1: 
	addi $sp, $sp, -12
	li $a0,8
	sw $a0, 8($sp)
	sw $fp, 4($sp)
	sw $ra, 0($sp)
	addi $fp, $sp, 0 
	addi $sp, $sp, -8
	li $t9, 0
	sw $t9, -4($fp)

BLOCK2:
	lw $t9, -4($fp)
	bgt $t9, 0, BLOCK4

BLOCK3:
	b BLOCK6

BLOCK4:
	lw $t9, 12($fp)
	lw $t8, -4($fp)
	move $t3, $t9
	div $t3, $t8
	mfhi $t3
	sw $t9, 16($fp)
	sw $t8, 12($fp)
	move $t9, $t3
	sw $t9, -4($fp)
	sw $t3, -8($fp)

BLOCK5:
	b BLOCK2

BLOCK6:
	lw $v0, -4($fp)
	lw $ra, 0($fp)
	lw $a0, 8($fp)
	addi $a0, 12
	add $sp, $fp, $a0
	lw $fp, 4($fp)
	jr $ra

BLOCK7:
	li $t9, 105
	sw $t9, t5
	li $t9, 10
	sw $t9, t6

BLOCK8:
	addi $sp, $sp, -4
	lw $a0,t5
	sw $a0, 0($sp)

BLOCK9:
	addi $sp, $sp, -4
	lw $a0,t6
	sw $a0, 0($sp)

BLOCK10:
	jal fun1

BLOCK11:
	move $t9, $v0
	move $t8, $t9
	sw $t9, t7
	lw $t9, t5
	div $t9, $t8
	mflo $t9
	move $t3, $t9
	sw $t3, t10
	sw $t9, t9
	lw $t9, t6
	div $t9, $t8
	mflo $t9
	sw $t8, t8
	move $t8, $t9
	sw $t8, t12
	sw $t9, t11
	li $v0, 10
	syscall



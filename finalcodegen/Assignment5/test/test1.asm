	.data
t8:	.word	0
t9:	.word	0
t11:	.word	0
t12:	.word	0
t10:	.space	200


	.text

BLOCK1:
	fun1: 
	addi $sp, $sp, -12
	li $a0,8
	sw $a0, 8($sp)
	sw $fp, 4($sp)
	sw $ra, 0($sp)
	addi $fp, $sp, 0 
	addi $sp, $sp, -20
	li $t9, 2
	li $t8, 5
	sw $t8, -4($fp)
	li $t8, 1
	sw $t8, -8($fp)

BLOCK2:
	li $t9, 2
	lw $t8, -8($fp)
	mult $t9, $t8
	mflo $t9
	li $t8, 1
	move $t3, $t9
	sub $t3, $t3, $t8
	sw $t3, -16($fp)
	sw $t9, -12($fp)

BLOCK3:
	b BLOCK6

BLOCK4:
	li $t9, 2
	lw $t8, -8($fp)
	add $t8, $t8, $t9
	sw $t8, -8($fp)

BLOCK5:
	b BLOCK2

BLOCK6:
	lw $t9, -8($fp)
	lw $t8, -16($fp)
	ble $t9, $t8, BLOCK8

BLOCK7:
	b BLOCK10

BLOCK8:
	li $t9, 1
	lw $t8, -4($fp)
	add $t8, $t8, $t9
	move $t9, $t8
	sw $t9, -4($fp)
	sw $t8, -20($fp)

BLOCK9:
	b BLOCK4

BLOCK10:
	lw $v0, -8($fp)
	lw $ra, 0($fp)
	lw $a0, 8($fp)
	addi $a0, 12
	add $sp, $fp, $a0
	lw $fp, 4($fp)
	jr $ra

BLOCK11:
	addi $sp, $sp, -4
	li $a0,  2
	sw $a0, 0($sp)

BLOCK12:
	addi $sp, $sp, -4
	li $a0,  3
	sw $a0, 0($sp)

BLOCK13:
	jal fun1

BLOCK14:
	move $t9, $v0
	move $t8, $t9
	sw $t8, t9
	sw $t9, t8
	li $t9, 0
	li $t8, 0
	sw $t8, t11

BLOCK15:
	b BLOCK18

BLOCK16:
	li $t9, 1
	lw $t8, t11
	add $t8, $t8, $t9
	sw $t8, t11

BLOCK17:
	b BLOCK15

BLOCK18:
	lw $t9, t11
	ble $t9, 49, BLOCK20

BLOCK19:
	b BLOCK22

BLOCK20:
	la $t9, t10
	lw $a0, t11
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	sw $t9, t12
	lw $t9, t11
	la $t8, t10
	lw $a0, t11
	li $a1, 4
	 mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	move $a0, $t9
	sw $a0, 0($t8)
	sw $t9, t12

BLOCK21:
	b BLOCK16

BLOCK22:
	li $v0, 10
	syscall



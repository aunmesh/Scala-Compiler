	.data


	.text

BLOCK1:
	fun1: 
	addi $sp, $sp, -12
	li $a0,8
	sw $a0, 8($sp)
	sw $fp, 4($sp)
	sw $ra, 0($sp)
	addi $fp, $sp, 0 
	addi $sp, $sp, -24
	li $t9, 0
	sw $t9, -4($fp)

BLOCK2:
	lw $t9, 16($fp)
	lw $t8, 12($fp)
	blt $t9, $t8, BLOCK4

BLOCK3:
	b BLOCK5

BLOCK4:
	lw $t9, 16($fp)
	lw $t8, 12($fp)
	add $t9, $t9, $t8
	move $t3, $t9
	sw $t9, -8($fp)
	move $t9, $t3
	sub $t9, $t9, $t8
	sw $t8, 12($fp)
	move $t8, $t9
	sw $t9, -12($fp)
	move $t9, $t3
	sub $t9, $t9, $t8
	sw $t8, 12($fp)
	move $t8, $t9
	sw $t8, 16($fp)
	sw $t9, -16($fp)

BLOCK5:
	lw $t9, 12($fp)
	beq $t9, 0, BLOCK7

BLOCK6:
	b BLOCK9

BLOCK7:
	lw $t9, 16($fp)
	sw $t9, -4($fp)

BLOCK8:
	b BLOCK18

BLOCK9:
	lw $t9, 16($fp)
	lw $t8, 12($fp)
	div $t9, $t8
	mfhi $t9
	sw $t8, 12($fp)
	move $t8, $t9
	sw $t8, -4($fp)
	sw $t9, -20($fp)

BLOCK10:
	lw $t9, -4($fp)
	bne $t9, 0, BLOCK12

BLOCK11:
	b BLOCK17

BLOCK12:
	addi $sp, $sp, -4
	lw $a0,12($fp)
	sw $a0, 0($sp)

BLOCK13:
	addi $sp, $sp, -4
	lw $a0,-4($fp)
	sw $a0, 0($sp)

BLOCK14:
	jal fun1

BLOCK15:
	move $t9, $v0
	move $t8, $t9
	sw $t8, -4($fp)
	sw $t9, -24($fp)

BLOCK16:
	b BLOCK18

BLOCK17:
	lw $t9, 12($fp)
	sw $t9, -4($fp)

BLOCK18:
	lw $v0, -4($fp)
	lw $ra, 0($fp)
	lw $a0, 8($fp)
	addi $a0, 12
	add $sp, $fp, $a0
	lw $fp, 4($fp)
	jr $ra

BLOCK19:
	main: 
	addi $sp, $sp, -12
	li $a0,0
	sw $a0, 8($sp)
	sw $fp, 4($sp)
	sw $ra, 0($sp)
	addi $fp, $sp, 0 
	addi $sp, $sp, -16
	li $t9, 0
	sw $t9, -12($fp)
	li $t9, 0
	sw $t9, -4($fp)
	li $t9, 0
	sw $t9, -8($fp)
	li $v0, 5
	syscall
	move $t9, $v0
	sw $t9, -12($fp)
	li $v0, 5
	syscall
	move $t9, $v0
	sw $t9, -4($fp)

BLOCK20:
	addi $sp, $sp, -4
	lw $a0,-12($fp)
	sw $a0, 0($sp)

BLOCK21:
	addi $sp, $sp, -4
	lw $a0,-4($fp)
	sw $a0, 0($sp)

BLOCK22:
	jal fun1

BLOCK23:
	move $t9, $v0
	move $t8, $t9
	sw $t8, -8($fp)
	sw $t9, -16($fp)
	li $v0, 1
	lw $t9, -8($fp)
	move $a0, $t9
	syscall
	addi $a0, $0, 0xA
	addi $v0, $0, 0xB
	syscall
	li $v0, 10
	syscall



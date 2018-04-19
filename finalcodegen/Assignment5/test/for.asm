	.data


	.text

BLOCK1:
	main: 
	addi $sp, $sp, -12
	li $a0,0
	sw $a0, 8($sp)
	sw $fp, 4($sp)
	sw $ra, 0($sp)
	addi $fp, $sp, 0 
	addi $sp, $sp, -4064
	li $t9, 0
	li $t8, 0
	sw $t8, -4016($fp)
	li $t8, 0
	sw $t8, -4020($fp)
	li $t8, 0
	sw $t8, -4008($fp)
	li $t8, 0
	sw $t8, -4012($fp)
	li $t8, 1000
	sw $t8, -4012($fp)
	li $t8, 2
	sw $t8, -4024($fp)

BLOCK2:
	b BLOCK5

BLOCK3:
	li $t9, 1
	lw $t8, -4024($fp)
	add $t8, $t8, $t9
	sw $t8, -4024($fp)

BLOCK4:
	b BLOCK2

BLOCK5:
	lw $t9, -4024($fp)
	lw $t8, -4012($fp)
	ble $t9, $t8, BLOCK7

BLOCK6:
	b BLOCK9

BLOCK7:
	add $t9, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	sw $t9, -4028($fp)
	li $t9, 1
	add $t8, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	 mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	move $a0, $t9
	sw $a0, 0($t8)
	sw $t9, -4028($fp)

BLOCK8:
	b BLOCK3

BLOCK9:
	li $t9, 2
	sw $t9, -4024($fp)

BLOCK10:
	b BLOCK13

BLOCK11:
	li $t9, 1
	lw $t8, -4024($fp)
	add $t8, $t8, $t9
	sw $t8, -4024($fp)

BLOCK12:
	b BLOCK10

BLOCK13:
	lw $t9, -4024($fp)
	lw $t8, -4012($fp)
	ble $t9, $t8, BLOCK15

BLOCK14:
	b BLOCK27

BLOCK15:
	add $t9, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	sw $t9, -4032($fp)

BLOCK16:
	lw $t9, -4032($fp)
	beq $t9, 1, BLOCK18

BLOCK17:
	b BLOCK26

BLOCK18:
	lw $t9, -4024($fp)
	lw $t8, -4024($fp)
	mult $t9, $t8
	mflo $t9
	sw $t8, -4024($fp)
	move $t8, $t9
	sw $t8, -4016($fp)
	sw $t9, -4036($fp)

BLOCK19:
	b BLOCK22

BLOCK20:
	lw $t9, -4016($fp)
	lw $t8, -4024($fp)
	add $t9, $t9, $t8
	sw $t9, -4016($fp)
	sw $t8, -4024($fp)

BLOCK21:
	b BLOCK19

BLOCK22:
	lw $t9, -4016($fp)
	lw $t8, -4012($fp)
	ble $t9, $t8, BLOCK24

BLOCK23:
	b BLOCK26

BLOCK24:
	add $t9, $fp -4004
	lw $a0, -4016($fp)
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	sw $t9, -4040($fp)
	li $t9, 0
	add $t8, $fp -4004
	lw $a0, -4016($fp)
	li $a1, 4
	 mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	move $a0, $t9
	sw $a0, 0($t8)
	sw $t9, -4040($fp)

BLOCK25:
	b BLOCK20

BLOCK26:
	b BLOCK11

BLOCK27:
	li $t9, 2
	sw $t9, -4024($fp)

BLOCK28:
	b BLOCK31

BLOCK29:
	li $t9, 1
	lw $t8, -4024($fp)
	add $t8, $t8, $t9
	sw $t8, -4024($fp)

BLOCK30:
	b BLOCK28

BLOCK31:
	lw $t9, -4024($fp)
	lw $t8, -4012($fp)
	ble $t9, $t8, BLOCK33

BLOCK32:
	b BLOCK35

BLOCK33:
	add $t9, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	sw $t9, -4044($fp)
	add $t9, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t9 , $t9, $a0
	lw $t9, 0($t9)
	li $t8, 1
	lw $t3, -4024($fp)
	sub $t3, $t3, $t8
	add $t8, $fp -4004
	move $a0, $t3
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	lw $t8, 0($t8)
	sw $t3, -4052($fp)
	move $t3, $t9
	add $t3, $t3, $t8
	sw $t9, -4048($fp)
	sw $t8, -4056($fp)
	move $t9, $t3
	sw $t3, -4060($fp)
	add $t8, $fp -4004
	lw $a0, -4024($fp)
	li $a1, 4
	 mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	move $a0, $t9
	sw $a0, 0($t8)
	sw $t9, -4044($fp)

BLOCK34:
	b BLOCK29

BLOCK35:
	li $v0, 5
	syscall
	move $t9, $v0
	sw $t9, -4012($fp)
	li $t9, 0
	sw $t9, -4024($fp)

BLOCK36:
	lw $t9, -4024($fp)
	lw $t8, -4012($fp)
	ble $t9, $t8, BLOCK38

BLOCK37:
	b BLOCK40

BLOCK38:
	li $v0, 5
	syscall
	move $t9, $v0
	add $t8, $fp -4004
	move $a0, $t9
	li $a1, 4
	mult $a0, $a1
	mflo $a0
	add $t8 , $t8, $a0
	lw $t8, 0($t8)
	sw $t8, -4064($fp)
	sw $t9, -4008($fp)
	li $v0, 1
	lw $t9, -4064($fp)
	move $a0, $t9
	syscall
	addi $a0, $0, 0xA
	addi $v0, $0, 0xB
	syscall
	li $t9, 1
	lw $t8, -4024($fp)
	add $t8, $t8, $t9
	sw $t8, -4024($fp)

BLOCK39:
	b BLOCK36

BLOCK40:
	li $v0, 10
	syscall



import main
import __main__
def create_block():
	main.block_get.append(0)

	main.lines.append([])
	main.N_BLOCKS = 0
	main.N_LINES = 0

	block = []
	block.append(1)

	f=open(main.testfile,'r')
	
	for line in f:
		main.lines.append(line.split())
		main.N_LINES += 1
		main.block_get.append(0)
		block.append(0)

	main.block_get.append(0)
	block.append(1)

	for i in range(1,main.N_LINES+1):
		line = main.lines[i]
		line.remove(line[0])

		if line[0] == 'label':
			block[i] = 1
		else:
			if line[0] == 'call' or line[0] == 'ret':
				block[i+1] = 1
			else:
				if line[0] == 'ifgoto' or line[0] == 'goto':
					block[i+1] = 1
					#print line[1]
					block[int(line[1])] = 1

		# print i, main.lines[i]

	j = 1
	block[1] = 1

	# print len(block),main.N_LINES

	# for i in range(0,main.N_LINES+2):
		# print i, block[i]

	main.block_start.append(0)

	for i in range(1,main.N_LINES+2):
		if block[i] == 1:
			main.block_end.append(i-1)
			main.block_start.append(i)
			main.N_BLOCKS += 1
		
		main.block_get[i] = main.N_BLOCKS

		# print main.block_get[i]			

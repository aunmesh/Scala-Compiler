import main
import __main__
def generate_block():
	main.get_block.append(0)

	main.lines.append([])
	main.N_BLOCKS = 0
	main.N_LINES = 0

	block = []
	block.append(1)

	f=open(main.testfile,'r')
	
	for line in f:
		main.lines.append(line.split())
		main.N_LINES += 1
		main.get_block.append(0)
		block.append(0)

	main.get_block.append(0)
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

	main.start_block.append(0)

	for i in range(1,main.N_LINES+2):
		if block[i] == 1:
			main.end_block.append(i-1)
			main.start_block.append(i)
			main.N_BLOCKS += 1
		
		main.get_block[i] = main.N_BLOCKS

		# print main.get_block[i]			

import main
import blockgen

def live_gen(n):
	start = main.start_block[n]
	end = main.end_block[n]

	for i in range(start,end+1):
		main.live.append([])

	# print "Block: " , n , " Start: " , start , " End: " , end

	if start != end:
		word = list(main.lines[end])

		if word[0] != 'call' and word[0] != 'goto' and word[0] != 'label':
			if word[0] == 'ret':
				if len(word) > 0: word.remove(word[0])
				for x in word:
					if x.isdigit() == False:
						main.live[end].append(x)
			else:
				if word[0] != "scan":
					word.remove(word[0])
					for x in word:
						if x.isdigit() == False and x != '=' and x != '==' and x != '!=' and x != '==' and x != '>=' and x != '<=':
							main.live[end].append(x)

		for i in range(end-1,start,-1):
			word = list(main.lines[i])
			
			if word[0] == "scan":
				word.remove(word[0])
				main.live[i] = list(main.live[i+1])
				for x in word:
					if x in main.live[i]:
						main.live[i].remove(x)
				continue

			if len(word) > 0 : word.remove(word[0])

			for x in main.live[i+1]:
				if x not in word:
					if x not in main.live[i]:
						main.live[i].append(x)

			if len(word) > 0: word.remove(word[0])
			
			for x in word:
				if x.isdigit() == False and x != '[' and x != ']' and x != '&' and x != '*' and x not in main.live[i]:
					main.live[i].append(x)

	for i in range(start,end):
		main.live[i] = list(main.live[i+1])

	main.live[end] = []

	#for i in range(start,end+1):
		#print main.live[i]


def gen_live():
	main.live.append([])
	blockgen.generate_block()

	# print main.N_BLOCKS

	for i in range(1,main.N_BLOCKS):
		live_gen(i)

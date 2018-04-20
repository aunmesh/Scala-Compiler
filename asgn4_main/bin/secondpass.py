import sys

def secondpass(lines):
	lines = lines.split('\n')
	line_filtered = [t.strip().split(',') for t  in lines]

	label_dict = {}
	label_line = {}
	count = 0
	result = []
	for i,t in enumerate(line_filtered):
		if t[0] == 'label':
			label_dict[t[1]] = count
			label_line[t[1]] = i - count
			count+=1
		else:
			result.append(t)

	ans = []

	for lineno , line in enumerate(result):
		for ind,temp in enumerate(line):
			if(temp in label_line.keys()):
				line[ind] = label_line[temp] + 1

	result.append(["exit 0"])
	for i,t in enumerate(result,1):
		print(t)
		t.insert(0,str(i))
		for i,temp in enumerate(t):
			t[i] = str(temp)
		t = ' '.join(t)
		ans.append(t)

	f = open('/home/mppiyush/project/Scala-Compiler/asgn4_main/test/result.ir','w')

	for t in ans:

		f.write(t+"\n")
	f.close()

import sys

fname = sys.argv[1]

f = open(fname, 'r')
lines = f.readlines()
f.close()

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

'''
	print(line)
	line.insert(0,str(lineno+1))
	print(line)
	ans.append(' , '.join(line))
'''
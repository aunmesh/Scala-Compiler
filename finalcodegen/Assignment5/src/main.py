from collections import defaultdict

N_BLOCKS = 0
N_LINES = 0
block_start = []
block_end = []
block_get = []
lines = []
live = []
ad=defaultdict(list) 				#Stores  register at 0 index, memory at 1 and stack locations after this. Access by ad[var][index]
rd=defaultdict(list)				# Access by rd[var]. This will be a list
mem=[]
free_reg = []
map_ptr = {}
regline={}
testfile=""
memad = {}
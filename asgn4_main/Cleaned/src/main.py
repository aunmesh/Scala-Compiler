from collections import defaultdict

ad=defaultdict(list) 				#register at 0 index is stored, memory at 1 and stack locations after this. Access by ad[var][index]
rd=defaultdict(list)				# Access by rd[var]. This will be a list


block_start = []
block_end = []
block_get = []

mem=[]
free_reg = []
map_ptr = {}
regline={}
testfile=""
memad = {}
N_BLOCKS = 0
N_LINES = 0

lines = []
live = []
import re

minterms = [] #To store the minterms which are input by user.
tables = [] #To store the result of every turn's result.
ua = [] #To store the prime implicant.
ue = [] #To store the essential prime implicant.
va = [] #To store the minterms which has the information about the links to prime implicant.
ve = [] #To store the minterms which are poppoed out in the term of finding essential prime implicant.
data_int = []
data_str = []
bits = 0

def get_data(data_str, data_int):
	global bits
	print "Please input the minterms:"
	print "e.g. 0+2+3+8+10"

	user_input = raw_input()

	data_str = re.findall('\d+',user_input)
	for i in data_str:
		i = int(i) 
		data_int.append(i)

	data_int.sort()
	data_int.sort(reverse = True)

	t = data_int[0]
	while t:
		t /= 2
		bits += 1
def process_data():

	for num in data_int:
		i = num
		string = "" #int to binary string
		for j in range(bits):
			string += str(i % 2)
			i /= 2
			
		string = string[::-1] #reverse the binary string.10110->01101

		time = string.count("1", 0, len(string))

		new_v = {'num': num,'link': []}
		va.append(new_v)

		new_minterm = {'bin': string, 'status': 0, '1': time, 'link': [num]};
		minterms.append(new_minterm)
		
	#sort the list according to number of one
	minterms.sort(key=lambda k: k['1'])

	tables.append(minterms)
def combine(minterms):
	while minterms:
		combined_minterms = []
		length = len(minterms)
		for i in range(length):
			for j in range(i + 1, length):
				#Compared the minterms whose D-value of number of 1 is 1 
				dvalue = minterms[j]['1'] - minterms[i]['1']
				while dvalue <= 1:
					if dvalue == 0:
						break
					elif dvalue == 1:
						cnt = 0
						#Check the numeber of difference
						for m in range(bits):
							if (minterms[i]['bin'][m]
								!= minterms[j]['bin'][m]):
								cnt += 1
						if cnt == 1:
							combined_minterm = {'bin': '', 'status': 0, '1': -1, 'link': []}
							string = dash_replace(minterms[i].copy(), 
												minterms[j].copy())
							combined_minterm['bin'] = string
							time = string.count("1", 0, len(string))
							combined_minterm['1'] = time
							link = (minterms[i]['link'][:] + 
						 		minterms[j]['link'][:])						
							combined_minterm['link'] = link
							combined_minterms.append(combined_minterm)
							minterms[i]['status'] = 1
							minterms[j]['status'] = 1		
						break	
		combined_minterms.sort(key=lambda k: k['1'])
		tables.append(combined_minterms)
		minterms = combined_minterms
		
	#Delete the empty table
	for i in range(len(tables)):
		if len(tables[i]) == 0:
			tables.pop(i)
	#Sort the link in last tables
	lenth = len(tables)
	for i in tables[lenth-1]:
		i['link'].sort()
def dash_replace(i,j):
	for m in range(bits):
		if i['bin'][m] != j['bin'][m]:
			i['bin'] = ''
			i['bin'] += (j['bin'][:m] + '_' + j['bin'][m+1:])
			break			
	return i['bin']		
def get_prime(primes):
	for table in tables:
		for minterm in table:
			if minterm['status'] == 0:
				primes.append(minterm)

	#Delete the same prime according to the link

	i = 0
	while i < len(primes):
		link = primes[i]['link']
		j = i + 1
		while j < len(primes):
			if primes[j]['link'] == link:
				primes.pop(j)
			j += 1
		i += 1
def make_ua(ua):
	for u in ua:
		for num in u['link']:
			for v in va:
				if v['num'] == num:
					v['link'].append(u['bin'])
					break
def get_essential_prime():
	vt = va[:]
	for v in vt:
		if len(v['link']) == 1:
			link = v['link'][0]
			ve.append(v)
			for u in ua:
				if u['bin'] == link:
					index = ua.index(u)
					utemp = ua.pop(index)
					ue.append(utemp)
					for num in utemp['link']:
						for v in va:
							if v['num'] == num:
								index = va.index(v)
								va.pop(index)
								break

	if va:
		for u in ua:
			u['node'] = 0
			for num in u['link']:
				for v in va:
					if v['num'] == num:
						u['node'] += 1
		ua.sort(key=lambda k: k['node'],reverse = True)
		ut = ua[:]
		for u in ut:
			while va:
				index = ua.index(u)
				utemp = ua.pop(index)
				ue.append(utemp)
				for num in u['link']:
					for v in va:
						if v['num'] == num:
							index = va.index(v)
							va.pop(index)
def print_result():
	result = ''
	for u in ue:
		unit = ''
		i = 0
		while i < len(u['bin']):
			if u['bin'][i] == '1':
				unit += chr(i + 65)
			elif u['bin'][i] == '0':
				unit += (chr(i + 65) + '\'')
			i += 1
		result += unit 
		result += '+'
	result = result[:-1]
	print "The result is:"
	print result		



#The start of the program.
get_data(data_str, data_int)
process_data()
combine(minterms)
get_prime(ua)
make_ua(ua)
get_essential_prime()
print_result()

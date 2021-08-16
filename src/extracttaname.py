def extract_name(filename):
	TA_list = dict({})
	with open(filename, 'r') as f:
		s = ''
		for l in f:
			ret = magic(l)
			if(ret[1] == True):
				s = ret[0]
				TA_list[s] = []
			elif(ret[0] != ''):
				TA_list[s].append(ret[0])
	return TA_list

def magic(s):
	begin=False
	end=False
	ret=""
	for i in range(2,len(s)):
		if(s[i-1]=='*' and s[i-2]=='*'):
			if(begin==True):
				end=True
			begin=True
		if(begin==True and end==False):
			ret=ret+s[i]
	if(begin==False):
		return ['',False]
	for x in ret:
		if(x.isupper()==True):
			return [ret[:-2],True]
	return [ret[:-2],False]

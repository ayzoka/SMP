import numpy as np
import random as r

r.seed('lady gaga')
templ = [0]
pop=100
epoch=200
mu_rate=0.9
co_rate=0.9
TA_list=dict({})


def extract_name(s):
	begin = False
	end = False
	ret = ""
	for i in range(2, len(s)):
		if(s[i-1] == '*' and s[i-2] == '*'):
			if(begin == True):
				end = True
			begin = True
		if(begin == True and end == False):
			ret = ret+s[i]
	if(begin == False):
		return ['', False]
	for x in ret:
		if(x.isupper() == True):
			return [ret[:-2], True]
	return [ret[:-2], False]


TA_list = dict({})
with open('TAlist.txt', 'r') as f:
	s = ''
	for l in f:
		ret = extract_name(l)
		if(ret[1] == True):
			s = ret[0]
			TA_list[s] = []
		elif(ret[0] != ''):
			TA_list[s].append(ret[0])


def calc_value(x):
	return r.randint(1,100)


def generate_primary(n):
	ret=[]
	for x in TA_list.keys():
		if(len(TA_list[x])//10+1)>3:
			templ.append(len(TA_list[x])-1)
		templ.append(len(TA_list[x])-1)
	for _ in range(n):
		c=[-1]
		for x in templ:
			c.append(r.randint(0,x))
		c[0]=calc_value(c)
		ret.append(c)
	return ret


def crossover(xi,xj):
	a=pop[xi].copy()
	b=pop[xj].copy()
	for _ in range(r.randint(1,5)):
		if(r.random()<co_rate):
			ptr=r.randint(1,len(a)-1)
			a[ptr:],b[ptr:]=b[ptr:],a[ptr:]
	a[0]=calc_value(a)
	b[0]=calc_value(b)
	ls=[[pop[xi],0],[pop[xj],0],[a,1],[b,1]]
	ls.sort()
	pop[xi]=ls[3]
	pop[xj]=ls[2]


def mutation(xi):
	t=0
	mu=pop[xi].copy()
	for x in range(1,len(templ)):
		if(r.random()<mu_rate and t<3):
			mu[r.randint(1,len(pop[xi])-1)]=r.randint(0,templ[x])
			t+=1
	if(t>0):
		mu[0]=calc_value(mu)
		if(mu[0]>pop[xi][0]):
			pop[xi]=mu

# def main():
	

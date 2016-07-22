

def init_states(n, k):
	cl = eliminate_rotations(generate(n,k))
	return to_view(cl)

def sp4(n):
	cl = take_sp4(eliminate_rotations(generate(n,4)))
	return to_view(cl)


def to_view(cl):
	ret = []
	for el in cl :
		ret.append(config_from_view(el))
	return ret


def config_from_view(v):
	"""à tester, je la trouve marante et débile"""
	ret =[0]
	for i in v:
		ret = ret+[0]*i
		ret[-1]+=1 
	return ret

def eliminate_rotations(cl):
	return cl

def in_sp4(v):
	if (v[0]==v[2]):
		if v[1]%2==1 and v[3]%2 ==0 and v[1]>v[3]:
			return True
		if v[3]%2==1 and v[1]%2 ==0 and v[1]<v[3]:
			return True

	if (v[1]== v[3]):
		if v[0]%2==1 and v[2]%2 ==0 and v[0]>v[2]:
			return True
		if v[2]%2==1 and v[0]%2 ==0 and v[0]<v[2]:
			return True
	return false

def keep_sp4(cl):
	ret =[]
	for i in cl :
		if in_sp4(el):
			ret.append(el)
	return ret





def generate(n, k):
	ret =list()
	if k==1 :
		return [[n]]
	for i in range(n):
		c = generate(n-i, k-1)
		for j in c :
			t = j
			t.append(i)
			ret.append(t)
	return ret


def equivalence(config):
	S=[]
	cur = config
	rcur = reverse(cur)
	for i in range(len(config)) :
		cur = next(cur)
		rcur = reverse(cur)
		p =(min(cur,rcur), min(cur,rcur))
		S.append(p)
	return (min(S),S)



def get_clases(configs):
	dic = dict()
	for c in configs:
		k = equivalence(c)[0]
		dic[str(k)]=k[0]
	return dic.values()

def reverse(config):
	return config[::-1]

def next(config):
	return config[1::]+config[0:1]
""" Similar methods as the ones in Uppaal """
from pprint import*


def getStrat(m, k):
	""" returns the tab of mouvement given by  the strategy m  for each k robots """
	tabStrat = [0]*k
	for i in range(k):
		tabStrat[i]= m % 5
		m=int(m/5)
	return tabStrat

def getView(indice, conf, k):
		"""returns the view of robot indice, in the configuration conf made of k robots"""
		view1 = [0]*k
		for i in range(k):
			view1[i] = conf[(indice+i)%k]
		return view1

def sameView(view1,view2, k):
	""" this function compares two views. It returns 
			0 is the view are not equivalent
			1 if they are the same
			-1 if view1 is the opposite of view2"""
	nb0start1 = 0
	nb0start2 = 0
	#booleens pour savoir si on est toujours dans le bloc de 0 du début
	start1 = True
	start2 = True
	nb0end1 = 0
	nb0end2 = 0	 
	#booleens pour savoir si on est toujours à la fin 
	end1 = True
	end2 = True

	for i in range(k):
		if (view1[i]==0 and start1):
			nb0start1 +=1		
		else:
			start1 = False
		if (view2[i]==0 and start2):
			nb0start2 +=1		
		else:
			start2 = False
		if (view1[((k-1-i)+k)%k]==0 and end1):
			nb0end1 +=1		
		else: 
			end1 = False
		if (view2[((k-1-i)+k)%k]==0 and end2):
			nb0end2 +=1
		else:
			end2 = False	
	
	if (nb0start1+nb0end1) != (nb0start2+nb0end2):
		return False

	nbElt = k - (nb0start1 + nb0end1);
	sens = -1 # vers la droite = 1  /  antihoraire = 0
	for i in range(nbElt):
		if (view1[(i+nb0start1)%k] != view2[(i+nb0start2)%k]) and (view1[(i+nb0start1)%k] !=  view2[(k-1-i-nb0end2)%k] ):
			return False
		else:	#dans le sens horaire
			if(sens == 1):
				if(view1[i+nb0start1] != view2[i+nb0start2]):
					return False
			#// dans le sens anti horaire
			elif(sens == 0):
				if(view1[i+nb0start1] != view2[k-1-i-nb0end2]):
					return False
			#//pas de sens encore obtenu
			elif ((view1[i+nb0start1] == view2[i+nb0start2]) and (view1[i+nb0start1] !=  view2[k-1-i-nb0end2] )):
				sens = 1
			elif ((view1[i+nb0start1] != view2[i+nb0start2]) and (view1[i+nb0start1] == view2[k-1-i-nb0end2])):
				sens = 0
#//autrement a droite on a la même chose qu'a gauche et du coup on continu sur pas de sens jusqu'a trouver de sens 
	
	return True

def isIn (view1, tabView):
	""" boolean function that permits to search for the existence of a view in a tab of views"""
	for i in range(len(tabView)):
		if (sameView(view1, tabView[i],len(view1))):
			return True
	return False


def conf_to_confpos(tabConf,n,k):
		"""return the tab representing a conf as tab of pos from a conf as d_1...d_k  for a ring of size n and k robots """
		j = 0
		#raise ValueError()
		tabpos = [0]*n
		#pprint(tabConf)	
		l = [int(e) for e in tabConf]
		
		for i in range(len(tabConf)):
			#print(type(j))
			var = tabConf[i]
			#print("|",end="")
			#print(var,end="|\n")
			#print(type(tabConf))
			j = (int(tabConf[i])+j)%n
			#print(j)
			tabpos[j] +=1
		return tabpos

def toString(config):
		newString = ""
		for elem in config:
			newString += "{0}".format(elem)
		return newString

def getPos(confPos,n,k):
		tabpos = [0]*k
		rbt=0
		for i in range(n):
			for j in range(confPos[i]):
				tabpos[rbt] = i
				rbt+=1
		return tabpos

def AllClasses(n,k):
	dic = dict()
	configs = AllConfs(n,k)
	for c in configs:
		k = equivalence(c)
		newString = toString(k)
		dic[newString]=1
	StringList = list(dic.keys())
	ret = []
	for config in StringList:
			ret1 = []
			for elem in config:
					ret1.append(elem)
			ret.append(ret1)
	return ret


def AllConfs(n,k):
	ret =list()
	if k==1 :
		return [[n]]
	for i in range(n):
		c = AllConfs(n-i, k-1)
		for j in c :
			t = j
			t.append(i)
			ret.append(t)
	return ret

def notHere(setOfConfig,n,k):
		NotHereConfs=[]
		AllConfigs = AllClasses(n,k)
		#print("et il y a {0} classes d'equ de config".format(len(AllConfigs))) 
		for config in AllConfigs:
			if config not in setOfConfig:
				NotHereConfs.append(config)
		return NotHereConfs

def equivalence(config):
		S = []
		cur = config
		rcur = reverse(cur)
		for i in range(len(config)) :
			cur = next(cur)
			rcur = reverse(cur)
			p = min(cur,rcur)
			S.append(p)
		return (min(S))

def reverse(config):
		return config[::-1]

def next(config):
		return config[1::]+config[0:1]


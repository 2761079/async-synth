from synthNK import *
from pprint import *

def add_rule(nbConfig, view, direction, filename,n, nbView):
		#print("view")
		#pprint(view)
		viewPos =  conf_to_confpos(view,n,len(view))
		myFile = open(filename,"a")
		#myFile  = filename
		strv1 = ""
		strv2 = ""
		for i in range(len(view)):
			strv1 +=" && conf[({0}+pos)%n]=={1}".format(i,viewPos[i])
			strv2 +=" && conf[(pos-{0}+n)%n]=={1}".format(i,viewPos[i])
	
		if (nbView==0):
			myFile.write(",\n//conf{0}\n\t".format(nbConfig))
		elif (direction <4):
			myFile.write(",\n\t")
		if (direction == 0):#gauche
			myFile.write("""RLC -> Back{guard initialized == 0""")
			myFile.write(strv1)
			myFile.write(""";}""")
			myFile.write(""",
		RLC -> Front{guard initialized == k""")
			myFile.write(strv2)
			myFile.write(""";}""")
		elif (direction == 1):#front
			myFile.write("""RLC -> Front{guard initialized == k""")
			myFile.write(strv1)
			myFile.write(""";}""")
			myFile.write(""",
		RLC -> Back{guard initialized == k""")
			myFile.write(strv2)
			myFile.write(""";}""")
		elif (direction == 2):#idle
			myFile.write("""RLC -> Idle{guard initialized == k""") 			
			myFile.write(strv1)
			myFile.write(""";}""")
			myFile.write(""",
		RLC -> Idle{guard initialized == k""") 			
			myFile.write(strv2)
			myFile.write(""";}""")
		elif (direction == 3):#desoriented
			myFile.write("""RLC -> Front{guard initialized==k""")
			myFile.write(strv1)
			myFile.write(""";}""")
			myFile.write(""",
		RLC -> Back{guard initialized == k""")
			myFile.write(strv1)
			myFile.write(""";}""")
		myFile.close()
		#return None /return /      is the same thing for a void like function

def add_rules(nbConfig, strat, conf, n , k, filename):
		tabStrat = getStrat(strat,k)
		#pprint("pour la conf: {0}, on a la strategie : {1} pour k = {2}". format(conf, strat,k))
		#taille = len(tabStrat)
		#pprint("et tabStrat = {0}".format(tabStrat))
		tabView = []
		nbView = 0
		for i in range(k):
			view1 = getView(i, conf, k)
			if (not isIn(view1, tabView)):			
				tabView.append(view1)
				add_rule(nbConfig,view1,tabStrat[len(tabView)-1],filename,n, nbView)
				#print("on ajoute une nouvelle règle")
				nbView +=1
		return 0

def add_rule0(nbConfig, conf, n,k,filename):
		tabStrat = [2]*k
		tabView = []
		nbView = 0
		for i in range(k):
			view1 = getView(i, conf, k)
			#print("v1")
			#pprint(view1)
			if (not isIn(view1, tabView)):			
				tabView.append(view1)
				add_rule(nbConfig,view1,tabStrat[len(tabView)-1],filename,n,nbView)
				#print("on ajoute une nouvelle règle")
				nbView +=1
		return 0


def getFirst(myConfigNb,n,k):
	maLigne = 0
	nbConfig = 0
	with open("tes.txt", 'r') as file:
		for line in file :
			if line.startswith("State: ( Process.Player )") :
				maLigne = 1
				nbConfig += 1
				#remplissage de la conf avec maConfig.group
				conf = getconf(re.search(config,line)) 
			
			elif maLigne == 1 : #On ne veut récupérer que la première règle
				if re.search("Process.Goal",line) is None:
					if(myConfigNb != nbConfig):
						strat = int(re.search("get_confuse_strat\((\d+)\)",line).group(1))
						add_rules(strat, maConf,n,k, "RBTfile.xml")#fais tout le boulot 
				maLigne = 2


import re,sys,os
from synthNK import *
from writing import *

############### Si on veut voir plusieurs formats de sorties il faut rajouter des options à la getopt 
############### IL faut faire un fichier séparé

#TODO
#ce n'est psa du python il va falloir le mettre en vrai python pour que ça marche quelque soit la machine qui appelle ce code
#os.system("rm -rf Conf*")
#os.system("rm RBTfile*")
#os.system("rm newxml*")

def isThereAStrategy(stratFileName):
		myboolean = False
		with open(stratFileName,'r')as stratFile:
			for line in stratFile:
				if "Property is satisfied" in line:
					return True
		return myboolean

def getconf(config):
	conf = []
	for gp in config.groups():
		conf.append(gp)	
	return conf

def getFirst(n,k,stratFileName,filename):
	"""write the strategy stratFileName as a dve model for k robots in a n node ring""" 
	maLigne = 0
	nbConfig = 0
	config = ""
	for i in range(k):
		newString = "conf\[{0}\]=(\d+) ".format(i)
		config += newString
	
	nobodyMove = noMoves(k)
	stratPy = []

	with open(stratFileName, 'r') as file:
		for line in file :
			if line.startswith("State: ( Process.Player )") :
				maLigne = 1
				nbConfig += 1
				#print("config numero = {0} \n à la ligne {1}".format(nbConfig, line))
				#remplissage de la conf avec maConfig.group
				conf = getconf(re.search(config,line))
			elif maLigne == 1 : #On ne veut récupérer que la première règle
				#print("CCCCConfig{0}".format(nbConfig))
				if re.search("Process.goal",line) is None:
					strat = int(re.search("get_confuse_strat\((\d+)\)",line).group(1))
					add_rules(nbConfig, strat, conf,n,k, filename)#fais tout le boulot
					stratPy.append((conf, strat))
				else:#goal reached -> nobody move
					add_rules(nbConfig,noMoves(k),conf,n,k,filename)#idle pour tout le monde
				maLigne = 2
	return stratPy
	#print("blaaaaaaaaaaaa")


def traduction(n,k,filename):
	"""fais la traduction de la strategie contenue dans filename et l'écrit dans le fichier filen_k.dve"""

	if not isThereAStrategy(filename):
		return (False, ())
	

	config = ""
	for i in range(k):
		newString = "conf\[{0}\]=(\d+) ".format(i)
		config += newString

	dveFileString = "strat.dve"
	dveFile = open(dveFileString, "w")

	dveFile.write("byte n = {0};\n".format(n))
	dveFile.write("byte k = {0};\n".format(k))

	tabString  = "byte pos[{0}] = ".format(k) + "{"
	for i in range(k-1):
		tabString += "0,"
	tabString+= "0};\n"
	dveFile.write(tabString)

	tabString  = "byte conf[{0}] = ".format(n) +"{"
	for i in range(n-1):
		tabString += "0,"
	tabString+= "0};\n"
	dveFile.write(tabString)
	dveFile.write("byte initialized = -1;\n\n")

	dveFile.write("""process P_Initializer{
	state start, end;
	init start;
	trans""")
	

	#1 first read of the stretgies file
	# we obtain all possible initial configurations -> we obtain the initializerProcess transitions
	step = 1
	previousConf=False
	nbConfig =0
	confListe=[]
	with open(filename,'r')as stratFile:
		for line in stratFile:
			if line.startswith("State: ( Process.Player ) "):
				step = 1
				nbConfig+=1
				#remplissage de la conf avec maConfig.group
				conf = getconf(re.search(config,line))
				#for elem in conf:
				#		pprint(elem)
				#		elem = int(elem)
				#print("bouh")
				maConf = conf_to_confpos(conf,n,k)
				#print(maConf)
				if previousConf:
					dveFile.write(",\n")
				dveFile.write("""
		start -> end{effect """)
				for pos in range(n):
					#print(type(pos))
					#print(type(str(pos)))
					str = "conf[{0}]={1}, ".format(pos, maConf[pos])
					#print(str)
					dveFile.write(str)

				tabPos= [0]*k
				tabPos = getPos(maConf,n,k)
				str = ""
				for i in range(k):
					str = "pos[{0}]={1}, ".format(i,tabPos[i])
					dveFile.write(str)
				dveFile.write("""initialized = 0;}""")
				previousConf=True
				confListe.append(conf)#) quelle indentation
		#	else:
		#		print(line)

	#2 on recupère les configurations qui n'ont pas été vues interressant que lorsque dans uppall on a enlevé des configuration avec k = 4 ça n'arrive que si le nombre n paircomme on s'interrresse à SP4 pas besoin
	nb = 0
	
	RbtDveFile = "RbtFile.dve"
	os.system("rm RbtFile.dve")

	#print("la synthese renvoit {0} configurations différentes".format(Liste)))
	#noMouvFile = open("noMouvRbtFile.dve","w")
	
	"""print("les conf initiales sont :")
	for c in confListe:
		print(c)
	
	print("\n\net donc il n'ya pas les confs .....")
	for c in notHere(confListe,n,k):
		print(c)"""

	for anyConfig in notHere(confListe,n,k):
		nb += 1
		add_rule0(len(confListe)+nb,anyConfig,n,k,RbtDveFile)

	#print(nb)

	#get the first strategy
	stratPy = getFirst(n,k,filename,RbtDveFile);


	for i in range(k):
		rbtString = """;
	}
process P_Rbt"""
		rbtString += "{0}".format(i)
		rbtString += "{\n" 
		#print(rbtString)
		dveFile.write(rbtString)
		dveFile.write("\tbyte num={0};\n".format(i))
		dveFile.write("""	state wait, RLC, Front, Back, Idle;
	init wait;
	trans
		wait -> RLC{guard initialized == 0;},
		Idle -> RLC{},
		Front -> RLC{effect conf[pos[num]]=conf[pos[num]]-1, 
			conf[(pos[num]+1)%n]=conf[(pos[num]+1)%n]+1,
			pos[num]=(pos[num]+1)%n;},
		Back -> RLC{effect conf[pos[num]]=conf[pos[num]]-1, 
			conf[(pos[num]+n-1)%n]=conf[(pos[num]+n-1)%n]+1,
			pos[num]=(pos[num]+n-1)%n;}""")
		#recupere les configurations pour mettre les positions des robots
		with open(RbtDveFile,'r')as rbtFile:
			for line in rbtFile:
				dveFile.write(line)

	#os.remove(RbtDveFile)
	dveFile.write(""";
	}
system async;""")
	dveFile.close()
	return (True, stratPy)

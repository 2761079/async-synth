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

def getconf(config):
	conf = []
	for gp in config.groups():
		conf.append(gp)	
	return conf

def getFirst(myConfigNb,n,k,path):
	maLigne = 0
	nbConfig = 0
	filepath = path + "/RBT.xml"
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
						add_rules(strat, maConf,n,k, filepath)#fais tout le boulot
				else:
					add_rules(312,maConf,n,k,filepath)#idle pour tout le monde
				maLigne = 2


def traduction(n,k,filename):
	config = ""
	for i in range(k):
		newString = "conf\[{0}\]=(\d+) ".format(i)
		config += newString
	nbConfig = 0


	dveFileString = "file{0}_{1}.dve".format(n,k)
	dveFile = open(dveFileString, "w")

	dveFile.write("byte n = {0};\n".format(n))
	dveFile.write("byte k = {0};\n".format(k))

	tabString  = "byte pos[k] = {"
	for i in range(k-1):
		tabString += "0,"
	tabString+= "0};\n"
	dveFile.write(tabString)

	tabString  = "byte conf[n] = .* stratOK=5{"
	for i in range(n-1):
		tabString += "0,"
	tabString+= "0};\n"
	dveFile.write(tabString)
	dveFile.write("initialized = -1;\n\n")

	dveFile.write("""process P_Initializer{
	state start, end;
	init start;
	trans""")


	#1 first read of the stretgies file
	# we obtain all possible initial configurations -> we obtain the initializerProcess transitions
	# we obtain the first strategy

	step = 1
	previousConf=False
	nbConfig =0
	confListe=[]
	with open(filename,'r')as stratFile:
		for line in stratFile:
			if line.startswith("State: ( Process.Player ) ") and "stratOK=5" in line:
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

	#on recupère les configurations qui n'ont pas été vues interressant que lorsque dans uppall on a enlevé des configuration avec k = 4 ça n'arrive que si le nombre n paircomme on s'interrresse à SP4 pas besoin
	nb = 0

	#print("la synthese renvoir {0} configurations différentes".format(len(confListe)))
	#noMouvFile = open("noMouvRbtFile.dve","w")
	for anyConfig in notHere(confListe,n,k):
		nb += 1
		add_rule0(anyConfig,n,k,"NoMouvRbtFile.dve")

	print(nb)

	#get the first strategy
	getFirst(filename, n,k);


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
		wait -> RLC{guard initialized = 0;},
		Idle -> RLC{},
		Front -> RLC{effect conf[pos[num]]=conf[pos[num]]-1, 
			conf[(pos[num]+1)%n]=conf[(pos[num]+1)%n]+1,
			pos[num]=(pos[num]+1)%n;},
		Back -> RLC{effect conf[pos[num]]=conf[pos[num]]-1, 
			conf[(pos[num]+n-1)%n]=conf[(pos[num]+n-1)%n]+1,
			pos[num]=(pos[num]+n-1)%n;}""")
		#TODO recupere les configurations pour mettre les positions des robots
		if nb > 0:
			with open("NoMouvRbtFile.dve",'r')as NoMouvFile:
				for line in NoMouvFile:
					dveFile.write(line)

	if nb > 0:
		os.remove("NoMouvRbtFile.dve")
	dveFile.write(""";
	}
system async;""")
	dveFile.close()

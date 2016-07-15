import re,sys,os
from synthNK import *
from writing import *
from pprint import *

def strategy(fichier):
	with open(fichier,'r') as stratFile:
		for line in stratFile:
			if "Property is satisfied" in line:
				return True
	return False

def getconf(config):
	conf = []
	for gp in config.groups():
		conf.append(gp)	
	return conf

def getFirst(filename,n,k):
	maLigne = 0
	nbConfig = 0
	fileStrat = "Tmp/stratRbt.txt"
	with open(filename, 'r') as file:
		for line in file :
			if line.startswith("State: ( Process.Player )")  and "stratOK=5" in line:
				maLigne = 1
				nbConfig += 1
				#remplissage de la conf avec maConfig.group
				conf = getconf(re.search(config,line))
				#comment to know which config we are on...
				#with open(fileStrat,"a") as stratFile:
				#		stratFile.write("//conf{0}\n".format(nbConfig))
				#print(line)
				#pprint ("maConf{0} ={1}".format(nbConfig, conf))

			
			elif maLigne == 1 : #first rule only
				if re.search("Process.Goal",line) is None:
					strat = int(re.search("get_confuse_strat\((\d+)\)",line).group(1))
					add_rules(nbConfig, strat, conf,n,k, fileStrat)
				else:
					add_rule0(nbConfig, conf,n,k,fileStrat)#every rbt is idle 
				maLigne = 2

	

def getAllStrats(filename,n,k):
		return 0










############## MAIN BEGINS HERE ##################
os.system("rm -rf Tmp/*")

try:
	filename = sys.argv[3]
	k = int(sys.argv[1])
	n = int(sys.argv[2])
except:
		sys.exit("""Usage: python3 traduction.py nb_robot ring_size filename
		where filename is the name of the file of strategies""")


print("n={0}".format(n))
print("k={0}".format(k))

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


step = 0
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
			confListe.append(conf)
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

#getAll the other strategies
getAllStrats(filename,n,k)





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

import re,sys,os
from synthNK import *
from writing import *

############### Si on veut voir plusieurs formats de sorties il faut rajouter des options à la getopt 
############### IL faut faire un fichier séparé

#TODO
#ce n'est psa du python il va falloir le mettre en vrai python pour que ça marche quelque soit la machine qui appelle ce code
os.system("rm -rf Conf*")
os.system("rm RBTfile*")
os.system("rm newxml*")

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



try:
	k = int(sys.argv[1])
	n = int(sys.argv[2])
except:
	sys.exit("you must give the number of robots in the arguments, and then the size of the ring ")
config=""
for i in range(k): 
	newString = "conf\["+ str(i) +"\]=(\d) "
	config = config + newString
# print(config) ##-> conf\[0\] = (\d] conf....

nbConfig = 0
maLigne = 0 # 	0 = debut 		1 = State 		2= first rules	3= other rules
initializer = open("initializer.xml","w")
initializer.write("""</template>
<template>
		<name x="6" y="6">Initializer</name>
		<declaration>// Place local declarations here.
		</declaration>
		<location id="id6" x="-204" y="8">
			<name x="-214" y="-26">start</name>
		</location>
		<location id="id7" x="161" y="8">
			<name x="151" y="-26">end</name>
		</location>
		<init ref="id6"/>
		""")

with open("tes.txt", 'r') as file:
	for line in file :
		if line.startswith("State: ( Process.Player )") :
			maLigne = 1
			nbConfig += 1
			#remplissage de la conf avec maConfig.group
			conf = getconf(re.search(config,line)) 
			maConf = conf_to_confpos(conf,n,k)
			#print(maConf)
			initializer.write("""
				<transition>
					<source ref="id6"/>
					<target ref="id7"/>
					<label kind="assignment">""")
			for pos in range(n):
				#print(type(pos))
				#print(type(str(pos)))
				str = "conf[{0}]={1}, ".format(pos, maConf[pos])
				#print(str)
				initializer.write(str)
			initializer.write("""initialized =0</label>
			</transition>
""")
			#print(line)
		elif maLigne == 1 : #On ne veut récupérer que la première règle
			if re.search("Process.Goal",line) is None:
				#print(line)
				#print("endline")
				strat = int(re.search("get_confuse_strat\((\d+)\)",line).group(1))
				#print("une new strat")
				add_rules(strat, maConf,n,k, "RBTfile.xml")#fais tout le boulot 
				#rules = rules +" {0}".format(strat)
			maLigne = 2
		elif maLigne >=2: 
			#print(line)
			if re.search("get_confuse_strat\((\d+)\)",line) is not None:
				path = "Conf{0}".format(nbConfig)
				if maLigne == 2:
					os.mkdir(path)
					getFirst(nbConfig,n,k,path)# on cré le fichier de base RBT.xml dans ce dossier
				maLigne +=1
				filePath = path + "/RBT_{0}.xml".format(maLigne-2)
				#myFile = open(filePath, "a")
				add_rules(strat,maConf, n, k, filePath)
					
initializer.write ("""</template>""")
initializer.close()


system = open("sys.xml","w")
system.write("<system> //Place template instantiations here\n")
i=1
str2 = ""
while i <= k:
	str1 = "Process{0} = RBT({0});\n".format(i)
	str2 = str2+"Process{0}".format(i) 
	system.write(str1)
	i+=1
system.write("""PInitializer = Initializer();
// List one or more processes to be composed into a system.
system"""+str2+"""PInitializer;
    </system>
	<queries>
""")
i=1
impl1 = ""
impl2 = ""
while i <=k:
	impl1 += "A[]A<>Process{0}.look and ".format(i)
	impl2 += "A[]A<>Process{0}.front or A[]A<>Process{0}.back or A[]A<>Process{0}.idle".format(i)
	i+=1
impl = impl1+" imply "+impl2
system.write(impl)
system.write("""
</queries>
""")

system.close()


start = open("newxml.xml","w")
start.write("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>
<nta>
	<declaration>// Place global declarations here.
const int k =4;
const int n =6;
int conf[n];
int initialized = -1;

</declaration>
	<template>
		<name x="5" y="5">RBT</name>
		<parameter>int num</parameter>
		<declaration>// Place local declarations here.
int pos = 0;

void update_position(){
    int i=0;
    int cpt=0;
    for(i=0;i&lt;n;i++){
        cpt += conf[i];
        if(cpt &gt;= num){
            pos = i;
            initialized++;
            return;
        }
    }
}

void va_a_droite(){
conf[pos]--;
conf[(pos+1)%n]++;
pos = (pos+1)%n;
}

void va_a_gauche(){
conf[pos]--;
conf[(pos+n-1)%n]++;
pos = (pos+n-1)%n;
}

</declaration>
		<location id="id0" x="-263" y="8">
			<name x="-273" y="-26">wait</name>
		</location>
		<location id="id1" x="-42" y="8">
			<name x="-76" y="-17">look</name>
		</location>
		<location id="id2" x="8" y="-153">
			<name x="-2" y="-187">front</name>
		</location>
		<location id="id3" x="144" y="17">
			<name x="134" y="-17">back</name>
		</location>
		<location id="id4" x="-25" y="170">
			<name x="-34" y="187">idle</name>
		</location>
		<init ref="id0"/>
		<transition>
			<source ref="id0"/>
			<target ref="id1"/>
			<label kind="guard" x="-195" y="-8">initialized &gt;= 0</label>
			<label kind="assignment" x="-204" y="8">update_position()</label>	
		</transition>
		<transition>
			<source ref="id2"/>
			<target ref="id1"/>
			<label kind="assignment" x="-34" y="-85">va_a_droite()</label>
		</transition>
		<transition>
			<source ref="id3"/>
			<target ref="id1"/>
			<label kind="assignment" x="-34" y="-85">va_a_gauche()</label>
		</transition>
		<transition>
			<source ref="id4"/>
			<target ref="id1"/>
		</transition>
""")
start.close()

end = open ("newxml2.xml", "a")
end.write("""<system>// Place template instantiations here. """)
mystring= ""
for i in range(k):
	mystring = "\nProcess{0} = RBT({0});".format(i+1)
	end.write(mystring)
end.write("""
Initializer1 = Initializer();
// List one or more processes to be composed into a system.
system Process1, Process2, Process3, Process4, Initializer1;
    </system>
	<queries>
	</queries>
</nta> """)
end.close()



import sys
import os
from trad import *
from synthNK import *

"""Model Checking divinie call"""

def MC(strat, states,n, k): 
	"""appele Divine """
	#
	os.system("rm asyncStrat.dve")

	#gen_init(states, n, k )#genere fichier asyncStrat.dve
	os.system("cat strat.dve >> asyncStrat.dve")
	
	os.system("rm resultDivine.txt")

	os.system("divine combine asyncStrat.dve -f ltlFile.ltl")
	os.system("divine verify asyncStrat.prop1.dve > resultDivine.txt")

	resultat = open("resultDivine.txt", "r")
	mark = True
	for line in resultat :
		if "The property DOES NOT hold" in line :
			mark = False

	return (mark, get_trace(resultat,n,k))


def get_trace(resultat,n,k):
	"""on cherche la deuxieme conf la premiere etant l'initalisation"""
	mark = False
	maConf = "conf = \["
	for i in range(n-1):
		maConf+="(\d+),"
	maConf+="(\d+)\]"
	for line in resultat :
		if "P_Initializer = 1" in line:
			mark =True
		positionRe = re.search(maConf,line)
		if mark and positionRe :
			return posListe_to_conf(getconf(positionRe))
	return []


def posListe_to_conf(posListe):
	i=0
	ret=[]
	while posListe[0]==0 :
			i+=1
	posListe[i::]+posListe[0:i]#on ne veut pas commencer par des 0
	i=0
	cur=0
	while i < len(posListe):
		if posListe[i]>1:
			ret.append(cur)
			posListe[i]-=1
			cur=0
		else :
			cur+=1
			i+=1
	ret.append(cur)
	return equivalence(ret);


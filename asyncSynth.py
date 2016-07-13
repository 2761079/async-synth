from SS import *
from properties import *


from threading import RLock
from multiprocessing import Process

strategies = Minimum()
POS_INIT = []

def gen_init():
	"""Genere une fois au début l'ensemble des positions initales"""
	POS_INIT =[]#à completer


def set_init():
	"""cree a partir de la lsite des positions initale un ensemble pour etre modifié"""
	return set(POS_INIT)


def retire_etat_init(E, T):#à remplir 
	"""Retire l'état inital donné par la trace dans la Stratégie a verifier"""
	E.remove(T)
 	return E


def proc_MC(S):
	"""Calcule l'ensemble des états à retirer pour que la stratégie soit valide"""
	etats = set_init(init)
	T=MC(S)
	i=0
	while i < Minimum or T[0]== False :
		etats = retire_etat_init(etats,T[1])
		T = MC((S, etats))
		i++
	if T[0]==False :
		return i+1, etats
	return i, etats # (i, S)


def AsyncSynth(C=[], F=[]):
	"""parcourt l'arbre de toutes les stratégies, il stoke au passage les stratégies avec le moins d'états à retirer: n = ring_size, k = nb_robots"""
	"""#first time -> creation 
	if len(C)<1 && len(F)<1:
		ltlgathering(n,k)
		uppaalQuery()"""
	boolSS, strat = SS(C, F)
	if (not boolSS): #la synthese n'a pas marché
		return
	i, E = proc_MC(strat)
	strategies.add(i, (strat,E))
	for a in S:
		pr=Process(AsyncSynth, C+[a], F)
		pr.start()
		pr.join()#ligne a commenter (resp décomenter) pour activer (resp desactiver) la paralellisation
		F+=[a]

def StartAsyncSynth(n,k):
	"""Procédure pour lancer la synthèse"""
	ltlgathering(n,k)
	uppaalQuery()

	gen_init()
	
	AsyncSynth()




class Minimum(Thread):
    """chargé de stoker les stratégies les plus éficaces"""

    def __init__(self):
		Strategies = []
		minimum = 2**50

        mutex = RLock()
    def add(self, min, El):
        """met a jour la liste des stratégies"""
        with mutex :
        	if (minimum == min)
				Strategies.append((strat,E))
			else if i < minimum :
				Strategies = [El]
				minimum = min
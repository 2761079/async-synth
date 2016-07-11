
Strategies = []
Minimum = 2**50
POS_INIT = []

def gen_init():
	"""Genere une fois au début l'ensemble des positions initales"""
	POS_INIT =[]#à completer


def set_init():
	"""cree a partir de la lsite des positions initale un ensemble pour etre modifié"""
	return set(POS_INIT)


def SS(C,F):
	return True


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


def AsyncSynth(C, F):
	"""parcourt l'arbre de toutes les stratégies, il stoke au passage les stratégies avec le moins d'états à retirer"""
	boolSync, strat = SS(C, F)
	if (not boolSync): #la synthese n'a pas marché
		return
	i, E = proc_MC(strat)
	if (Minimum == i)
		Strategies.append((strat,E))
	else if i < Minimum :
		Strategies = [(strat, E)]
		Minimum = i
	for a in S:
		Strategies = AsyncSynth(C+[a], F)
		F+=[a]

from SS import *
from MC import *
from properties import *
#from traduction import *
from initStates import init_states, sp4

from threading import Lock, Semaphore
from multiprocessing import Process
from os import system
import copy
import queue

import copy

USE_MC = False #false : mode comptage de stratégies 

def gen_init(n, k):
	"""Genere une fois au début l'ensemble des positions initales"""
	return init_states(n, k)#à completer 
	#faire un fichier pour generer les position init selon différentes conditions : (de base), sans les symétries, SP4....


def set_init():
	"""cree a partir de la lsite des positions initale un ensemble pour etre modifié"""
	return list(POS_INIT)


def retire_etat_init(E, T):#à remplir 
	"""Retire l'état inital donné par la trace dans la Stratégie a verifier"""
	E.remove(T)
	return E


def proc_MC(S, n, k):
	"""Calcule l'ensemble des états à retirer pour que la stratégie soit valide ne marche pas encore, car on ne recupere pas la trace dans MC
	cette fonction n'est pas encore terminée (MC ne gere pas la trace d'exécution de Divine)
	"""
	etats = set_init()
	T=MC(S, etats, n, k)
	i=0
	while i < Minimum or T[0]== False :
		etats = retire_etat_init(etats,T[1])
		T = MC(S, etats,n, k)
		i+=1
	if T[0]==False :
		return i+1, etats
	return i, etats 


def proc2_MC(S, n, k):
	"""répond uniquement vrai ou faux"""
	etats = set_init()
	T=MC(S, etats, n, k)#retourne une paire (reusite, ensemble des etats gagnants)
	#MC(.)[0] retourne 0 si la verification a echoue, 1 sinon
	return 1-T[0], T[1]


def async_synth(C, F, n, k):
	"""parcourt l'arbre de toutes les stratégies, il stoke au passage les stratégies avec le moins d'états à retirer: n = ring_size, k = nb_robots
	aglorithme de base, nous prefererons utiliser la verson de Ordonancer"""
	boolSS, strat = SS(C, F, n, k)
	if (not boolSS): #la synthese n'a pas marché
		return
	if USE_MC :
		i, E = proc2_MC(strat, n, k)
		strategies.add(i, (strat,E))
	else :
		strategies.add(0, 0)
	print("Nombre de strategies : {0}\nPerformance de la strategie : {1}".format(len(strategies.strats), strategies.minimum))

	for a in strat:
		async_synth(copy.deepcopy(C)+[a],copy.deepcopy(F),n ,k)
		F+=[a]


#TODO main
def StartAsyncSynth(n,k):
	"""Procédure pour lancer la synthèse"""
	ltlgathering(n,k)
	uppaalQuery()

	#async_synth([],[], n, k)
	ordonancer = Ordonancer(n, k, 1)
	ordonancer.run()


class Minimum:
	"""chargé de stoker les stratégies les plus éficaces, c'est un début de structure pour du multithread"""
	def __init__(self, n):
		self.strats = list()
		self.minimum = n
		self.mutex = Lock()

	def add(self, min, El):
		"""met a jour la liste des stratégies"""
		with self.mutex :
			if (self.minimum == min) :
				self.strats.append(El)
			elif min < self.minimum :
				self.strats = [El]
				self.minimum = min




class Ordonancer:
	"""objet pour d'une part gerer manuellement la pille d'appel (implémentation : lifo ou fifo), car on a déja eu une explosion de la pille d'appel
		et permettra à la longue de gérer du multiprocessus, non utilisé pour le moment"""

	def __init__(self, n, k ,pr):
		self.process = list()
		self.sem = Semaphore(pr)
		self.processing = 0
		self.processingMut = Lock()
		self.n = n
		self.k = k

	def async_synth(self, C, F):
		"""parcourt l'arbre de toutes les stratégies, il stoke au passage les stratégies avec le moins d'états à retirer: n = ring_size, k = nb_robots"""
		boolSS, strat = SS(C, F, self.n, self.k)
		if (not boolSS): #la synthese n'a pas marché
			return
		if USE_MC :
			i, E = proc2_MC(strat, self.n, self.k)
			strategies.add(i, (strat,E))
		else :
			strategies.add(0, 0)
		print("Nombre de strategies : {0}\nPerformance de la strategie : {1}".format(len(strategies.strats), strategies.minimum))
		self.add_strats(strat,copy.deepcopy(C), copy.deepcopy(F))

	def add_strats(self, strat,C, F):
		F2=F[:]
		for a in strat:
			add=[copy.deepcopy(C)+[a],copy.deepcopy(F2)]
			self.process.append(add)
			F2=F2[:]+[a]

	def run(self):
		"""met a jour la liste des stratégies"""
		self.process.append([[],[]])
		self.processing = 0
		while len(self.process) != 0: #or self.processing:
			#self.sem.acquire()
			C,F = self.process.pop()
			
			#print(self.process)
			self.async_synth(C[:],F[:])
	


try:
	n = int(sys.argv[1])
	k = int(sys.argv[2])
except:
	sys.exit("you must give the number of robots in the arguments, and then the size of the ring ")


POS_INIT = gen_init(n,k)
strategies = Minimum(len(POS_INIT))
sem = Semaphore(1)
StartAsyncSynth(n,k)

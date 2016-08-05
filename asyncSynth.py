from SS import *
from MC import *
from properties import *
#from traduction import *
from initStates import init_states, sp4

from threading import Lock, Semaphore
from multiprocessing import Process


def gen_init(n, k):
	"""Genere une fois au début l'ensemble des positions initales"""
	POS_INIT = init_states(n, k)#à completer 
	#faire un fichier pour generer les position init selon différentes conditions : (de base), sans les symétries, SP4....


def set_init():
	"""cree a partir de la lsite des positions initale un ensemble pour etre modifié"""
	return set(POS_INIT)


def retire_etat_init(E, T):#à remplir 
	"""Retire l'état inital donné par la trace dans la Stratégie a verifier"""
	E.remove(T)
	return E


def proc_MC(S, n, k):
	"""Calcule l'ensemble des états à retirer pour que la stratégie soit valide"""
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
	"""retourne basiquement vrai ou faux"""
	etats = set_init()
	T=MC(S, etats, n, k)
	
	return 1-T[0], T[1]


def AsyncSynth(C, F, n, k):
	"""parcourt l'arbre de toutes les stratégies, il stoke au passage les stratégies avec le moins d'états à retirer: n = ring_size, k = nb_robots"""
	boolSS, strat = SS(C, F,n, k)
	if (not boolSS): #la synthese n'a pas marché
		return
	i, E = proc2_MC(strat, n,k)
	strategies.add(i, (strat,E))
	#strategies.add(0, 0)
	print("nombre de strategies : {0}".format(len(strategies.strats)))
	for a in strat:
		#pr=Process(AsyncSynth, C+[a], F, n, k)
		AsyncSynth(C+[a], F, n, k)
		"""pr.start()
		with sem :
			if sem.locked() :
				pr.join()#ligne a commenter (resp décomenter) pour activer (resp desactiver) la paralellisation
		"""
		F+=[a]


#TODO main
def StartAsyncSynth(n,k):
	"""Procédure pour lancer la synthèse"""
	ltlgathering(n,k)
	uppaalQuery()


	POS_INIT = init_states(n,k)

	AsyncSynth([],[], n, k)



class Minimum:
	"""chargé de stoker les stratégies les plus éficaces"""

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


try:
	n = int(sys.argv[1])
	k = int(sys.argv[2])
except:
	sys.exit("you must give the number of robots in the arguments, and then the size of the ring ")


POS_INIT = [] 
gen_init(n,k)
strategies = Minimum(len(POS_INIT))

sem = Semaphore(1)

StartAsyncSynth(n,k)
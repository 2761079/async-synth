# async-synth

fichiers 
	asyncSynth : (main)
		algorithme principal de recherche de stratégies : il trouve des stratégies avec upaal et les vérifie avec Divine.
		actuellement ne marche pas, ne semble pas terminer (l'erreur vient peut être d'upaal)
		il faut utiliser la de asyncSynth dans Ordonancer, car il faut gérer la pille d'appel à la main (aplatit la récursion), sinon on a un risque de stack overflow
		l'objet Minimum permet de récupérer la ou les stratégies avec le score minimum, il est prévu pour gérer le multithread et les conflits accès.
		TODO :
			-gestion de proc_MC, (proc_MC2 marche)
			-parallélisation des processus, la structure de Ordonancer est prévue pour ça, cela reste une tache secondaire.
			-
	SS : (Synthèse Synchrone)
		la fonction principale de ce fichier est SS, elle s'occupe de générer le fichier uppaal avec les contraintes, lancer uppaal, récupérer la sortie, générer le fichier .dve (Divine) associé.
		TODO :
		cette méthode est relativement peu élégante, il faudrait générer le début et la fin du fichier au début de l’exécution du programme, et à chaque passe ajouter uniquement la fonction stratOK (avec les gardes correspondant aux contraintes)

	trad : (uppaal to dve)
		génère le fichier .dve à partir de la sortie d'uppaal, et ainsi qu'en 'liste python' pour l'utiliser dans notre arbre de recherche dans asyncSynth.


	initStates : 
		généré les état initiaux du système pour divine, on peut soit générer touts les états (sauf les symétries), soit uniquement les sp4

	properties :
		génère uniquement les requêtes à valider pour uppaal et Divine.

	synthNK :
		contient les implémentation python de fonction du programme uppaal, utile pour traduire les différentes représentations.

	writing :
		écrit certaines lignes pour Divine.

	MC : 
		lance le model checking.



compiler Divine :
[...]this is a bug which surfaced with GCC 6 (DIVINE 3.3.2 is quite old now, we are working on a new version), it can be fixed by changing all occurences of -isystem to -I in CMakeLists.txt (there should be two, line 345 and 390) and  bricks/support.cmake (one, line 110). Then you should be able to remake, however you might still encounter problems with muparser.h; in this case please disable murphi:
    in build dir (defaults to _build, if it is different you will have to change .. to path to DIVINE sources) run
    cmake .. -DOPT_MURPHI=OFF
and then remake DIVINE.

Also please note that if you want LLVM/C/C++ support you will have to have LLVM 3.4 installed. 

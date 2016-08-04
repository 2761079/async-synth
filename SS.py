import sys
import os
from trad import *
""" Synchoronous synthesis call"""

def getStrat(constraint):
	""" return the strat of the constraint"""
	if(len(constraint)!=2):
		sys.exit("Contraint systax error")
	return constraint[1]

def getConf(constraint):
	""" return the configuration of the constraint"""
	


def SS(constraintList, forceList,n,k): #n is the size of the ring, k the number of robots
	""" synchronous synthesis where constraintList is the list of all constraints on strategies
and ForceList is the list of all forced substrategy, an element of these List is of the form tabconf , strat

Cette fonction necessite qu'il y ait deje un fichier ltl qui puisse etre utilise"""
	synthesisFile = open("synthese.xml","w")
	synthesisFile.write("""<?xml version="1.0" encoding="utf-8"?><!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_1.dtd'><nta><declaration>// Place global declarations here.""")
	synthesisFile.write("const int n={0};\nconst int k={1};\n".format(n,k))

	synthesisFile.write("""		
const int BACK = 0; //dans le sens antihoraire
const int FRONT = 1; //dans le sesn horaire
const int IDLE = 2; //do not move
const int DESORIENTED = 3; // don't know where to move
const int NO_MOUV = 4 ;//quand on ne doit pas choisir ... not enough views


const int player_const = 624;//5^k-1  pour k=4 robots
const int adv_const = 15;//2^k-1  pour k = 4 robots


int [-1, player_const] strat = -1;//-1 quand on est dans l'etat joueur )&gt; 5^k
//conf d_1 .... d_k
int [-1, """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1] conf[k]; //n+1 juste pour l'initialisation et -1 autrement
//int conf[k];

//int view1[k];
//int view2[k];
//int tab_views[k][k];//yavait un truc bizare ici a reverifier
//int confuse_strat[k];
int stratTab[k];
int finalStrat[k];
int tabpos[k];
int stratOK;
int nbViews;

//initialise la conf e n+1 partout pour que l'adversaire puisse choisir une conf initiale
void init_conf(){
	int i; 
	for (i = 0; i &lt; k; i++){
		conf[i] = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1;
	}
	stratOK = -1;
}

//renvoie la somme des d_1... d_k qui compose la conf
int somme_conf(){
	int i;
	int somme = 0;
	for(i = 0; i &lt; k ; i++){
		somme += conf[i];
		if(conf[i] == -1 || conf[i]==""")
	synthesisFile.write(str(n))
	synthesisFile.write("""+1)
		return -1;
	}
	return somme;
}

bool conf_periodic(){ 
	int i,j;
	bool periodic = true;
	if (conf[i] ==""")
	synthesisFile.write(str(n))
	synthesisFile.write("""+1)//on est a l'initialisation
		return false;
	for(i=1; i&lt;k; i++){
		for(j=0; j &lt;k ; j++){
			periodic = (periodic &amp;&amp; (conf[j] == conf[(i+j)%k]));
		}
		if (periodic) return periodic;
		periodic = true;
	}
	return false;
}

//on verifie qu'il n'y a pas de strategie si pour la conf (1,1,1,2) on prend la strategie 601
// pour plus d'information sur pourquoi ces lignes sont arrivees le voir le fichier PB_option_uppaal
//pb() permet de savoir si on est dans cette conf 
// PB etait le pour debuggage
//bool pb(){
//	return false;
//	return (conf[0]==1 &amp;&amp; conf[1]==1 &amp;&amp; conf[2]==1 &amp;&amp; conf[3]==2);
//}


// Les deux fonctions suivantes permettent de savoir si la config cree est correcte ou non
bool conf_valid(){
	return ((somme_conf() == """)
	synthesisFile.write(str(n))
	synthesisFile.write(""") &amp;&amp; !conf_periodic()); 
}
bool conf_not_valid(){
	return (somme_conf() != """)
	synthesisFile.write(str(n))
	synthesisFile.write(""");
}

//cette fonction permet e l'adversaire de choisir une configuration initiale
void newConf(int sep){
	int somme = 0;
	int i;
	int j; 
	for (i = 0; i &lt; k-1; i++){
		if(conf[i] == """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1){
			if (somme+sep &gt; """)
	synthesisFile.write(str(n))
	synthesisFile.write("""){
				conf[i]= """)
	synthesisFile.write(str(n))
	synthesisFile.write("""-somme;
				for(j = i+1; j&lt;k; j++)
					conf[j] = 0;
				return;
			}
			conf[i] = sep;
			return;
		}else{
			somme +=conf[i];
		}
	}
	conf[k-1] = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""-somme;
}

//guarde qui permet de savoir si on a atteint la config de rassemblement (i.e., [0,0,...,0,n] )
bool gathering(){
	int i;
	for (i = 0; i &lt;k-1; i++){
		if(conf[i]!=0)
			return false;
	}
	return true;
}

void new_strat (int s) {
	strat = s;
}

void getStrat(int m){
int i;
	for(i=0; i&lt;k; i++){ //for(i : int[0,k-1])
		stratTab[i]= m % 5;
		m/=5;
	}
}

//obtenir la ieme vue de la conf
/*void getView(int indice){
	int i;

	for(i=0; i&lt;k; i++){
		view1[i] = conf[(indice+i+k)%k];
	}
}*/

//retourne 1 si equal
	//-1 si oppose
	//0 si differentes
int sameView(int view1[k],int  view2[k]){
	int nb0start1 = 0;
	int nb0start2 =0;
	//booleens pour savoir si on est toujours dans le bloc de 0 du debut
	int start1 =1;
	int start2 = 1;
	int nb0end1 = 0;
	int nb0end2 = 0;
	//booleens pour savoir si on est toujours e la fin 
	int end1 = 1;
	int end2 = 1;
	int i;

	int nbElt;
	int sens; 
	
	for(i = 0; i &lt; k; i++){
		if (view1[i]==0 &amp;&amp; start1)
			nb0start1++;		
		else 
			start1 = 0;
		if (view2[i]==0 &amp;&amp; start2)
			nb0start2++;		
		else 
			start2 = 0;
		if (view1[((k-1-i)+k)%k]==0 &amp;&amp; end1)
			nb0end1++;		
		else 
			end1 = 0;
		if (view2[((k-1-i)+k)%k]==0 &amp;&amp; end2)
			nb0end2++;
		else
			end2 = 0;
	}		
	if ((nb0start1+nb0end1) != (nb0start2+nb0end2))
		return 0;

	
	nbElt = k - (nb0start1 + nb0end1);
	sens = -1; //vers la droite = 1 //antihoraire = 0
	for(i = 0; i &lt; nbElt; i++){
		if((view1[(i+nb0start1)%k] != view2[(i+nb0start2)%k]) &amp;&amp; 
		   (view1[(i+nb0start1)%k] !=  view2[(k-1-i-nb0end2)%k] ))
			return 0;
		else	//dans le sens horaire
			if(sens == 1){
				if(view1[i+nb0start1] != view2[i+nb0start2])
					return 0;
			}// dans le sens anti horaire
			else if(sens == 0){
				if(view1[i+nb0start1] != view2[k-1-i-nb0end2])
					return 0;
			}//pas de sens encore obtenu
			else if ((view1[i+nb0start1] == view2[i+nb0start2]) &amp;&amp; 
		   	         (view1[i+nb0start1] !=  view2[k-1-i-nb0end2] ))
					sens = 1;
			else if ((view1[i+nb0start1] != view2[i+nb0start2]) &amp;&amp; 
		   	         (view1[i+nb0start1] ==  view2[k-1-i-nb0end2] ))
					sens = 0;
			//autrement a droite on a la meme chose qu'a gauche et
			//du coup on continu sur pas de sens jusqu'a trouver
			//le sens 
	}
	if (sens == 1)
		return 1;
	return -1;
}

//on ajoute la vue si elle nest pas dans le tableau et on renvoie son indice
	//si la vue existe on renvoie son indice
	//si la vue existe dans le sens anti horaire on renvoie son oppose
/*int add_if_not_in(int indice, int view1[k], int tab_views[k][k], int tailleTabViews){
	int i;
	//int sens =-1;//0 = anticlockwise //1 clockwise
	for (i=0; i &lt; tailleTabViews ; i++){
		int equ = sameView(view1,tab_views[i]);
		if (equ != 0){ //avec equ = -1 ou +1 
			//printf("le robot %d a la meme vue que le robot %d opp = %d",indice, i, equ);
			if (equ &gt;0)
				return i*equ;
			else 
				return (i+1)*equ;
		}
	}
	//printf("le robot %d a une vue unique", indice);

	for(i=0; i &lt;k ; i++)
		tab_views[tailleTabViews][i] = view1[i];
	return tailleTabViews;
}*/

// retourne 1 si la vue est un palindrome et 0 sinon
// le robot ayant cette vue est alors desoriente
int is_palindrome(int view1[k]){
	int nb0start = 0;
	//booleens pour savoir si on est toujours dans le bloc de 0 du debut
	int start =1;
	int nb0end = 0;
	//booleen pour savoir si on est toujours e la fin 
	int end = 1;
	int i;
	
	for(i = 0; i &lt; k; i++){
		if (view1[i]==0 &amp;&amp; start)
			nb0start++;		
		else 
			start = 0;
		if (view1[((k-1-i)+k)%k]==0 &amp;&amp; end)
			nb0end++;		
		else 
			end = 0;
	}		
	for(i=0; i &lt; k/2+1 ; i++){
		if (view1[(i+nb0start)%k] !=  view1[((k-1-i-nb0end)+k)%k] )
			return 0;
	}
	return 1;
}

//tab de mouvements tels qu'ils seront envoyes e l'adversaire
// retourne -1 si rien ne va plus
void get_confuse_strat(int s){
	//int nbViews = 0; //nb vues differentes
	int i,j;
	int all_views[k][k];
	int view1[k];

	int index;
	int in;// n+1 ie pas encore trouve
	int move;

	stratOK = 1;
	strat = s;
	
	getStrat(strat);

	nbViews=0;
	for(i=0; i&lt;k; i++){
		in = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1; 
		//getView(i);
		for(j=0; j&lt;k; j++){
			view1[j] = conf[(i+j+k)%k];
		}
		//on contruit le tableau des vues
		//in = add_if_not_in(i,view,all_views, nbViews);
		for (j=0; j &lt; nbViews ; j++){
			int equ = sameView(view1,all_views[j]);//int sens =-1 si elles sont opposees//0 si diff //1 si identiques
			if (equ != 0){ //avec equ = -1 ou +1 
				//printf("le robot %d a la meme vue que le robot %d opp = %d ",indice, i, equ);
				if (equ &gt;0)
					in = j*equ;
				else 
					in = (j+1)*equ;
			}
		}
		//printf("le robot %d a une vue unique", indice);
		if(in == """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1){
			in = nbViews;
			for(j=0; j &lt;k ; j++)
				all_views[nbViews][j] = view1[j];
			nbViews++;
		}
		//desoriented robots
		if(in &lt; 0)
			index = (in*-1)-1;
		else
			index = in;		
		if(is_palindrome(view1)){
			if(stratTab[index]!= IDLE &amp;&amp; stratTab[index]!= DESORIENTED){
				stratOK = 2;
				return;
			}else {	finalStrat[i]= stratTab[index];}
		//non desoriente
		}else{
			if ((stratTab[index] == DESORIENTED) || 
			    (stratTab[index] == NO_MOUV)) {
				stratOK = 3;
				return;
			}
			if(in &gt;=0){ //vue clockwise direction existante
					finalStrat[i]=stratTab[index];
				}else {	//vue anti-clockwise direction existante
					move = stratTab[index];//-1 pour 0
					if (move == IDLE){
						finalStrat[i] = move;
					}else 
						finalStrat[i]=(move+1)%2;
				}
			}

			
	}
	for (i= nbViews; i&lt;k; i++){
		if(stratTab[i] != NO_MOUV) {
			stratOK = 4;
			return;
		}
	}
	stratOK = 5;
}
// si strat_ok(), on va dans un etat de l'adversaire, sinon, on retourne de le d'ou on vient et on recommence.
//Seule utilite : que la contre-strategie quand elle existe, ne tienne pas compte des mauvais choix de strategies du joueur (codes 1,2,3,4)
bool strat_ok () {
if (stratOK != 5)
	return false;
""")
	for forceConstraint in forceList:
		conf = getConf(forceConstraint)
		strat = getStrat(forceConstraint)
		synthesisFile.write("if (")
		i=0
		for elt in conf :
			synthesisFile.write("conf[{0}] == {1} &amp;&amp; ".format(i,elt))
			i+=1
		synthesisFile.write("strat != {0} )\n\treturn false;\n\n".format(strat))

	for constraint in constraintList:
		conf = getConf(constraint)
		strat = getStrat(constraint)
		syntheisFile.write("if(")
		i=0
		for elt in conf :
			synthesisFile.write("conf[{0}] == {1} &amp;&amp; ".format(i,elt))
			i+=1
		synthesisFile.write("strat == {0}\n\treturn false;\n\n".format(strat))

	synthesisFile.write("return true;\n}")	

	synthesisFile.write("""
//met e jour les positions en fonction des mouvements decider par la strategie
//a cette etape les movements sont soit droite soit gauche ou pas bouger
void move(){
	int i; 
	for(i = 0; i &lt; k ; i++){
		if (finalStrat[i] == 1)
			tabpos[i] = (tabpos[i]+1)%""")
	synthesisFile.write(str(n))
	synthesisFile.write(""";
		else if(finalStrat[i]== 0)
			tabpos[i] = (tabpos[i]-1+""")
	synthesisFile.write(str(n))
	synthesisFile.write(""")%""")
	synthesisFile.write(str(n))
	synthesisFile.write(""";
	}
}


void conf_to_tabpos () {
  	int i;
	tabpos[0] = 0;
  	for (i=1;i&lt;k;i++) {
    		tabpos[i] = tabpos[i-1] + conf[i-1];
  	}
}


//cherhche les minimums de la conf
//cherche en profondeur le sens 
//donne rep conf
void conf_to_repconf () {

  //affiche(conf,k);

  //On doit donc trouver la permutation min pour l'ordre lexicographique.
  //On doit donc commencer par chercher le min du tableau, puis parcourir dans les deux dirrections pour chercher le min lexicographique.

  int workingtab[k];//Tableau qui va contenir tous les index d'apparition de la valeur min

  //affiche(workingtab,k);
  //Maintenant on va vouloir parcourir workingtab, et pour chaque indice, verifier e gauche et e droite si on est de nouveau le min.
  //Il faut se souvenir du sens de parcours, parce qu'apres, il est fixe. De plus, on va se souvenir ou on est et d'ou on part, par commodite.
  //Les uples sont de la forme (indice ou on est, sens (0 ou 1), indice d'ou on est parti)

  int size = 2*3*k;
  int firstupletab[2*3*k];//tableau qui contiendra les uples vus plus haut.
  int numofelt = 0;//On va compter le nombre d'elements qu'on va mettre dans firstupletab, comme ca on pourra refaire un tableau de bonne taille.

  //affiche(6*k, firstupletab);
  //On va maintenant continuer e explorer les indices dans le meme ordre jusqu'e n'en avoir plus qu'un seul, ou au pire k fois-2 fois (on a deje parcouru 2 indices)
  //On commence par prendre un tableau plus petit.


  //On va maintenant parcourir pour chercher le min par ordre lexicographique.

  int secondupletab[2*3*k];//On va avoir besoin de stocker les valeurs sans ecraser smallupletab.

  //var
  int start;
  int dirrection;
	//pour findmins
	int temptab[k];
	int minval = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1;//valeur min d'initialisation, donc plus grand que le max.
	int index = 0;//index d'ecriture dans workingtab

	//pour directional tab
	int notover = 1;//On a fini les indices "utiles", ie, on est arrive aux -1.
	int from,pre,post;
	
	//pour lexico_min
	int morethanone =0;
	int numofnewelt;
  	int nextindex;


  int i,j, ji;

  //find_mins (workingtab, temptab);***************************************************************
	//initialisationK(workingtab, -1);//-1 n'etant pas un index valide, on n'aura pas de problemes.
	for (j=0;j&lt;k;j++){
    		workingtab[j]=-1;
		temptab[j] = conf[j];
    	}  	

  	for (i=0;i&lt;k;i++){
    		if (temptab[i] &lt; minval) { //On a trouve une valeur plus petite strictement.
      			//initialisationK(workingtab, -1); //Du coup on efface tout ce qu'on avait.
			for (j=0;j&lt;k;j++){
    				workingtab[j]=-1;
    			}
      			minval = temptab[i];//On garde cette valeur du min.
      			index = 0;//On remet l'index e 0 pour revenir au debut du tableau.
      			workingtab[index++] = i;//On note l'emplacement de le ou on a trouve le min.
    		}
    		else if (temptab[i] == minval) {
      			workingtab[index++] = i;//On a trouve un nouveau indice de valeur min.
    		}
    		//Sinon, temptab[i] &gt; minval, on ne s'interesse pas e la valeur.
  	}
//**************
  //numofelt = directional_tab (firstupletab, temptab, workingtab);$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	numofelt = 0;
	index = 0;
	minval = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1;
	size = 6*k;
	//initialisation (firstupletab, -1);
	for (j=0;j&lt;size;j++){
	    	firstupletab[j]=-1;
    	}
  
	i=0;
  	while(i&lt;k &amp;&amp; notover){
    		if (workingtab[i] == -1) {
      			notover = 0;//On a fini.
    		}
    		else{
      			from = workingtab[i];
      			pre = (from-1+k)%k;
      			post = (from+1+k)%k;
      		if (temptab[pre] &lt; minval) {
			//initialisation (firstupletab, -1);
			for (j=0;j&lt;size;j++){
    				firstupletab[j]=-1;
    			}
			minval = temptab[pre];
			index = 1;
			firstupletab[0] = pre;//Premier element du uple.
			firstupletab[1] = 0;//On va e gauche.
			firstupletab[2] = from;//On est parti de from.
			numofelt = 1;
      		}
      		else if (temptab[pre] ==  minval) {
			firstupletab[3*index] = pre;//Premier element du uple.
			firstupletab[3*index+1] = 0;//On va e gauche.
			firstupletab[3*index+2] = from;//On est parti de from.
			index++;
			numofelt++;
      		}

      		if (temptab[post] &lt; minval) {
			//initialisation (firstupletab, -1);
			for (j=0;j&lt;size;j++){
    				firstupletab[j]=-1;
    			}
			minval = temptab[post];
			index = 1;
			firstupletab[0] = post;//Premier element du uple.
			firstupletab[1] = 1;//On va e droite.
			firstupletab[2] = from;//On est parti de from.
 			numofelt = 1;
      		}
      		else if (temptab[post] == minval) {
				firstupletab[3*index] = post;//Premier element du uple.
				firstupletab[3*index+1] = 1;//On va e droite.
				firstupletab[3*index+2] = from;//On est parti de from.
				index++;
				numofelt++;
			}

			i++;
		}
	}
//$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
size = 3*numofelt;
//lexico_min(secondupletab, firstupletab, temptab, numofelt, size);-------------------------
  minval = """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1;//On initialise avec le max+1.
  morethanone = 0;//On verifie qu'on a bien plus d'un seul element. Sinon on peut s'arreter.
  index = 0;
  if(numofelt &gt; 1) morethanone = 1;
  //initialisation (secondupletab, -1);
  for (j=0;j&lt;size;j++){
  	secondupletab[j]=-1;
  }


  i=0;
  while(i &lt; (k-2) &amp;&amp; morethanone){
    	minval=""")
	synthesisFile.write(str(n))
	synthesisFile.write("""+1;
    	numofnewelt = 0;
	//printf("et smallupletab = ");
	//affiche(size, smallupletab);
    	for (j=0;j&lt;numofelt;j++){
      		if (firstupletab[3*j+1]) {
			nextindex = (firstupletab[3*j]+1+k)%k;//Si c'est 1 on va e droite.
      		}
      		else {
			nextindex = (firstupletab[3*j]-1+k)%k;//Sinon c'est 0, on va e gauche.
      		}
      		if (temptab[nextindex] &lt; minval) {
			//initialisation (secondupletab, -1);
			for (ji=0;ji&lt;size;ji++){
  				secondupletab[ji]=-1;
  			}
			minval = temptab[nextindex];
			index = 1;
			secondupletab[0] = nextindex;//Premier element du uple.
			secondupletab[1] = firstupletab[3*j+1];//On garde le meme sens.
			secondupletab[2] = firstupletab[3*j+2];//On garde le meme from.
			numofnewelt = 1;
      		}
       		else if (temptab[nextindex] ==  minval) {
			secondupletab[3*index] = nextindex;//Premier element du uple.
			secondupletab[3*index+1] = firstupletab[3*j+1];//On garde le meme sens.
			secondupletab[3*index+2] = firstupletab[3*j+2];//On garde le meme from.
			index++;
			numofnewelt++;
      		}
    }
    i++;
	numofelt=numofnewelt;
	//printf("on es ta i+1 = %d et secondupletab = ",i);
	//affiche(size, secondupletab);
    if (numofnewelt == 1) {
      morethanone = 0;
    }
    // il faut remplacer le tableau.
    for (j=0;j&lt;size;j++) {
      firstupletab[j] = secondupletab[j];
    }
    //initialisation (secondupletab, -1);//efface
for (j=0;j&lt;size;j++){
  	secondupletab[j]=-1;
  }
    index = 0;
  }
//------------------------------------

  //affiche(3*numofelt, smallupletab);

  //Maintenant on sait quel est le representant de la classe d'equivalence.
  start = firstupletab[2];
  dirrection = firstupletab[1];
  if (dirrection == 0) {
    dirrection = -1;
  }
  for (i=0;i&lt;k;i++) {
    conf[i] = temptab[(start + i*dirrection+k)%k];
  }
}
    
void tabpos_to_conf () {
  int p = """)
	synthesisFile.write(str(n))
	synthesisFile.write(""";
  int i;
  int tmp;
  int taille = k;
  bool tab_en_ordre = false;

//tri bulle
    while(!tab_en_ordre)
    {
        tab_en_ordre = true;
        for(i=0 ; i &lt; taille-1 ; i++)
        {
            if(tabpos[i] &gt; tabpos[i+1])
            {
             tmp = tabpos[i];
	     tabpos[i] = tabpos[i+1];
	     tabpos[i+1] = tmp; 
             tab_en_ordre = false;
            }
        }
        taille--;
    }


  //temptab est un tableau temporaire qui va etre trie plus tard.
  for (i=0;i&lt;k-1;i++) {
    conf[i] = tabpos[i+1] - tabpos[i];
    p -= conf[i];
  }
  if(p &lt;-1)
	conf[k-1] = -1;
  else if (p &gt; """)
	synthesisFile.write(str(n))
	synthesisFile.write("""+1)
	conf[k-1] = -1;
  else
 	conf[k-1] = p;
  conf_to_repconf();
}


void confuseStrat_to_realStrat (int advdecision[k]) {
	int i;
	for (i=0;i&lt;k;i++) {
		if (finalStrat[i] == DESORIENTED) 
			finalStrat[i]=advdecision[i];
	}
}



//la fonction qui fait bouger les robots selon la strategie choisie et fais bouger les desorientes
//for (i=0;i&lt;k;i++) {
	//	get strat adv
//getStrat player(strat, stratTab);
//transforme strat player -&gt; moves
//transforme moves avec stratadv pour desoriented
//conf_to_tabpos(conf, tabpos);
//move(tabpos, finalStrat);
//tabpos_to_conf(conf, tabpos); en repconf


//fonction qui remet toutes les variables globales e -1;
void reset_all(){
	int i;	
	for (i=0;i&lt;k;i++) {
    		tabpos[i] = 0;
		stratTab[i] = 0;
		finalStrat[i] = 0;
    	}
	new_strat(-1);
	nbViews=0;
}


void move_All(int disoriented) {
	int advDecision[k];
	int problem;
	int i;

	for (i=0;i&lt;k;i++) {
		advDecision[i]=(disoriented%2);
		disoriented/=2;
	}
	confuseStrat_to_realStrat (advDecision);
	conf_to_tabpos();
	move();
	tabpos_to_conf();
	reset_all();
}

""")
	synthesisFile.write("""


void test(){
	conf[0] = 0;
	conf[1] = 3; 
	conf[2] = 4; 
	conf[3] = 3;

	//conf_to_repconf();
}


</declaration><template><name x="5" y="5">Template</name><declaration>// Place local declarations here.
</declaration><location id="id0" x="240" y="-224"><name x="230" y="-254">player2</name></location><location id="id1" x="504" y="96"><urgent/></location><location id="id2" x="-176" y="-56"></location><location id="id3" x="232" y="104"><name x="216" y="120">goal</name></location><location id="id4" x="528" y="-136"><name x="518" y="-166">Adv</name><urgent/></location><location id="id5" x="232" y="-56"><name x="184" y="-80">Player</name></location><location id="id6" x="-16" y="-56"><name x="-32" y="-32">vh</name><urgent/></location><init ref="id2"/><transition controllable="false" action=""><source ref="id4"/><target ref="id5"/><label kind="select" x="360" y="-88">disoriented : int[0,adv_const]</label><label kind="assignment" x="376" y="-72">move_All(disoriented)</label></transition><transition action=""><source ref="id0"/><target ref="id4"/><label kind="guard" x="384" y="-200">strat_ok()</label></transition><transition action=""><source ref="id5"/><target ref="id0"/><label kind="select" x="56" y="-184">s : int[0,player_const]</label><label kind="guard" x="56" y="-168">conf_valid()</label><label kind="assignment" x="56" y="-152">get_confuse_strat(s)</label><label kind="comments">guard &amp;&amp; ! pb()</label><nail x="200" y="-136"/></transition><transition controllable="false" action=""><source ref="id6"/><target ref="id3"/><label kind="guard" x="48" y="48">conf_periodic()</label></transition><transition controllable="false" action=""><source ref="id1"/><target ref="id5"/><label kind="assignment" x="448" y="40">test()</label></transition><transition action=""><source ref="id2"/><target ref="id6"/><label kind="assignment" x="-160" y="-56">init_conf()</label></transition><transition action=""><source ref="id5"/><target ref="id3"/><label kind="guard" x="152" y="-8">gathering()</label></transition><transition controllable="false" action=""><source ref="id6"/><target ref="id5"/><label kind="guard" x="72" y="-72">conf_valid()</label><label kind="assignment" x="48" y="-56">conf_to_repconf()</label></transition><transition controllable="false" action=""><source ref="id6"/><target ref="id6"/><label kind="select" x="-72" y="-168">sep : int[0,""")
	synthesisFile.write(str(n))
	synthesisFile.write("""]</label><label kind="guard" x="-80" y="-184">conf_not_valid()</label><label kind="assignment" x="-72" y="-152">newConf(sep)</label><nail x="-48" y="-128"/><nail x="8" y="-128"/></transition></template><system>// Place template instantiations here.
Process = Template();

// List one or more processes to be composed into a system.
system Process;</system></nta>""")

	
	synthesisFile.close()
	os.system("rm stratyga.txt")
	os.system("./verifytga -w 0 synthese.xml gathering.q > stratyga.txt")
	return traduction(n,k, "stratyga.txt")#bool, strat











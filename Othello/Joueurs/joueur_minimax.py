#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

import math

# Paramètres
horizon=2

global poids
poids = [2,8,-6,4,-5]
#poids=[2, 8, 5.880599999999999, 3.84238404, -5]

#On compte le nombre de l'appel évaluation
global cpt;
cpt=0

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur # attention : ne pas nommer un paramètre de fonction "joueur" !
    joueur = game.getJoueur(jeu)
    meilleurCoup=decision(jeu)
    return meilleurCoup

def decision(jeu):
    """jeu->(int,int)
       Elle renvoie le coup qui a meilleur score à evaluation
    """
    #On prend la décision
    listeCoups = game.getCoupsValides(jeu)
    meilleurScore = -math.inf
    
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        scoreEval = estimation(jeu,coup,horizon)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup

def estimation(jeu,coup,horizon):
    """
    Implémentation de l'algorithme minimax
    """
    copie=game.getCopieJeu(jeu)
    game.joueCoup(copie,coup) 

    if horizon==1:
        return evaluation(copie)
    
    listeCoupsVal = game.getCoupsValides(copie) # peut-être mettre avant appel evaluation ? change pas beaucoup car finJeu calcule coups valides
    if game.getJoueur(jeu) == joueur:
        listeCoupsVal.reverse()
    
    if joueur==game.getJoueur(copie): # si joueur ami
        val=-math.inf
        for nouvCoup in listeCoupsVal:
            val=max(val,estimation(copie,nouvCoup,horizon-1))
        return val           
    
    else: # si joueur ennemi
        val=math.inf
        for nouvCoup in listeCoupsVal:
            val=min(val,estimation(copie,nouvCoup,horizon-1))      
        return val


def evaluation(jeu):
    """jeu,coup->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """    
    global cpt
    cpt=cpt+1

    param=[]
    coup = jeu[3][-1]

    param=[]
    coup = jeu[3][-1]
    # récupère le dernier coup joué
    #La différence de score
    diffScores = game.getScore(jeu,joueur)-game.getScore(jeu,3-joueur)
    param.append(diffScores)
    
    #Les coins
    coins=[(0,0),(0,7),(7,0),(7,7)]
    c=0
    if coup in coins:
        c=1
    param.append(c)
    
    #Zone de danger
    zoneDanger1=[(1,0),(0,1),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6)]
    zoneDanger2=[(6,7),(6,6),(7,6),(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6)]
    d=0
    if coup in zoneDanger1 or zoneDanger2:
        d=d+1
    param.append(d)
    
    #place safe
    placesSures=[(0,2),(0,3),(0,4),(0,5),(7,2),(7,3),(7,4),(7,5),(2,0),(3,0),(4,0),(5,0)]
    ps=0
    if coup in placesSures:
        ps=ps+1
    param.append(ps)
    
    nbCasesVidesAutour=0
    for j in range(-1,1):
        for k in range(-1,1):
            if(coup[0]+j>0 or coup[0]+j<7 or coup[1]+k>0 or coup[1]+k<7 ):
                if(game.getCaseVal(jeu,coup[0]+j,coup[1]+k)==0):
                    nbCasesVidesAutour+=1
    param.append(nbCasesVidesAutour)
    
    return dot(poids,param)

def dot(v1,v2):
    """ Hypothèse : len(v1)==len(v2)
    """
    return sum([v1[i]*v2[i] for i in range(len(v1))])


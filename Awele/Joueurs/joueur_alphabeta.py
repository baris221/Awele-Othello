#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import math

# Paramètres
horizon=5
#On compte le nombre de l'appel évaluation
global cpt
cpt=0

global param1
param1 = []


global poids;
#poids=[1.9999999999671898, -0.9999999999942982, -0.9999999999920975]
#poids=[1.9999997642755254, -0.9999998852316244, -0.9999998833817494]
#poids = [2,-1,-1]
poids=[1391, -16, -10]

def dot(v1,v2):
    """ Hypothèse : len(v1)==len(v2)
    """
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def estimation(jeu,coup,horizon,alpha=-math.inf, beta=math.inf):
    """
    jeu,(int,int),int,int,int->int
    Implémentation de l'algorithme minimax
    """
    copie=game.getCopieJeu(jeu)
    game.joueCoup(copie,coup)
    if horizon==1:
        return evaluation(copie)
    
    listeCoupsVal = game.getCoupsValides(copie)
    if game.getJoueur(jeu) == joueur:
        listeCoupsVal.reverse()
    
    if joueur==game.getJoueur(copie): # si joueur ami
        val=-math.inf
        for nouvCoup in listeCoupsVal:
            val=max(val,estimation(copie,nouvCoup,horizon-1,alpha,beta))
            if val >= beta:
                break
            alpha = max(alpha,val)
        return val           
    
    else: # si joueur ennemi
        val=math.inf
        for nouvCoup in listeCoupsVal:
            val=min(val,estimation(copie,nouvCoup,horizon-1,alpha,beta))      
            if val<=alpha:
                break
            beta = min(beta, val)
        return val

def evaluation(jeu):
    """jeu->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """ 
    global cpt
    cpt=cpt+1
        
    param=[]
    
    # différence de score
    diffScores = game.getScore(jeu,joueur)-game.getScore(jeu,3-joueur)
    param.append(diffScores)

    # nombre de cases vides
    nbCasesVides=0
    for i in range(0,6):
        if(game.getCaseVal(jeu,joueur-1,i)==0):
            nbCasesVides=nbCasesVides+1
    param.append(nbCasesVides)

    # nombre de cases vulnerables
    nbCasesVulnerables=0
    for i in range(0,6):
        if(game.getCaseVal(jeu,joueur-1,i)==1 or game.getCaseVal(jeu,joueur-1,i)==2 ):
            nbCasesVulnerables=nbCasesVulnerables+1
    param.append(nbCasesVulnerables)
    
    global param1
    param1=param
      
    return dot(poids,param)
    

def decision(jeu):
    """jeu->(int,int)
       Elle renvoie le coup qui a meilleur score à evaluation
    """
    #On fait la décision
    listeCoups = game.getCoupsValides(jeu)
    meilleurScore = -math.inf
    
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        scoreEval = estimation(jeu,coup,horizon)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur
    joueur = game.getJoueur(jeu)
    meilleurCoup=decision(jeu)
    return meilleurCoup

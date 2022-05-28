#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import math

global poids;
poids = [2,8,-6,4,-5]

global param1
param1=[]


def dot(v1,v2):
    """ Hypothèse : len(v1)==len(v2)
    """
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def estimation(jeu,coup):
    """jeu,(int,int)->int
    """
    copie=game.getCopieJeu(jeu)
    game.joueCoup(copie, coup)
    return evaluation(copie)

def evaluation(jeu):
    """jeu,coup->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """ 

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
    global param1
    param1=param
    
    return dot(poids,param)

def decision(jeu):
    """jeu->(int,int)
       Elle renvoie le coup qui a meilleur score à evaluation
    """
    #On fait la décision
    listeCoups = game.getCoupsValides(jeu)
    meilleurScore = estimation(jeu,listeCoups[0])
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        scoreEval = estimation(jeu,coup)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup


def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur
    joueur=game.getJoueur(jeu)
    coup = decision(jeu)
    return coup

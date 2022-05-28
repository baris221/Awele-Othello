#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import game

def initialiseJeu():
    """ void -> jeu
    redéfinition initjeu
    """
    jeu = []
    
    # init plateau (tableau à deux dimensions)
    p = []
    for i in range(2):
        p.append([])
        for j in range(6):
            p[i].append(4)
    jeu.append(p)
    
    # init joueur
    jeu.append(1)
       
    # init liste coups valides
    jeu.append(None)
    
    # init liste coups joués
    jeu.append([])
    
    # init scores
    jeu.append([0,0])
    
    return jeu

def estAffame(jeu, joueur):
    """ jeu,int -> bool
    Vérifie si le joueur est affamé
    """ 
    return sum(jeu[0][joueur-1]) == 0

def estValide(jeu, coup, verifGraine = False):
    """ jeu,(int,int),bool -> bool
    Vérifie si le coup est valide
    """
    nbGraines = game.getCaseVal(jeu,coup[0],coup[1])
    if not coup[0] == jeu[1]-1:
        return False
    if jeu[0][coup[0]][coup[1]] == 0:
        return False
    if verifGraine:
        if coup[0] == 0:
            return nbGraines > coup[1]
        if coup[0] == 1:
            return nbGraines > (5-coup[1])
    return True

def listeCoupsValides(jeu):
    """ jeu->List[coup]
    retourne la liste de coups valides
    """
    # jeu[1]%2+1 : adversaire
    affame = estAffame(jeu, jeu[1]%2+1)
    return [(jeu[1]-1,c) for c in range(0,6) if estValide(jeu,(jeu[1]-1,c),affame)]

def nextCase(coup,sensHoraire):
    """coup,bool->coup
    Passe à la prochaine case en prenant en compte le sens
    (horaire ou anti-horaire)
    """
    if sensHoraire:
        if coup == (0,5):
            return (1,5)
        if coup == (1,0):
            return (0,0)
        if coup[0] == 0:
            return (coup[0],coup[1]+1)
        return (coup[0],coup[1]-1)     
    else: # antihoraire
        if coup == (0,0):
            return (1,0)
        if coup == (1,5):
            return (0,5)
        if coup[0] == 0:
            return (coup[0],coup[1]-1)
        return (coup[0],coup[1]+1) 
    
def joueCoup(jeu,coup):
    """jeu,coup->jeu
    hypothèse : le coup en entrée est valide
    Retourne un nouveau jeu avec le coup joué
    NB : le joueur est changé à l'adversaire après que le coup est joué
    """  
    nbGraines=game.getCaseVal(jeu,coup[0],coup[1])
    # remet à 0 la case quand les graines ont été prises en compte
    jeu[0][coup[0]][coup[1]] = 0
    
    # egraine
    # parcours antihoraire
    case=nextCase(coup,False)
    jeu[0][case[0]][case[1]] += 1
    for i in range(0,nbGraines-1):
        # parcours antihoraire
        case=nextCase(case,False)
        jeu[0][case[0]][case[1]] += 1
    
    
    # copie du jeu au cas où l'égrainage est impossible
    copieJeu=game.getCopieJeu(jeu)
    
    #on mange (egraine)
    while case[0] != game.getJoueur(jeu)-1:
        if game.getCaseVal(jeu,case[0],case[1]) == 2 or game.getCaseVal(jeu,case[0],case[1]) == 3:
           jeu[4][game.getJoueur(jeu)-1] += game.getCaseVal(jeu,case[0],case[1])
           jeu[0][case[0]][case[1]] = 0
        else:
            break
        # parcours horaire
        case=nextCase(case,True)
        
    # cas où affamé
    if estAffame(jeu,game.getJoueur(jeu)):
        # on restaure le plateau
        jeu[0] = copieJeu[0]
        # on restaure les scores
        jeu[4] = copieJeu[4]
    
    # ajouter coup aux coups joués
    jeu[3].append(coup)
    
    # changer joueur (cette fonction remet la liste de coups valides à 0 aussi)
    game.changeJoueur(jeu)
    
    return jeu


def finaliseJeu(jeu):
    """jeu->jeu
    Met à jour le score et retourne le jeu final
    """
    #Le score de joueur 1
    score1 = 0
    #Le score de joueur 2 
    score2 = 0

    # prend les sommes de toutes les cases pour rajouter aux scores respectifs
    for i in range(0,6):
        score1+=game.getCaseVal(jeu,0,i) 
    for i in range(0,6):
        score2+=game.getCaseVal(jeu,1,i)  
    
    # incrémentation du score
    jeu[4][0] += score1
    jeu[4][1] += score2
    
    return jeu
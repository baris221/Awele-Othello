#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import game

def initialiseJeu():
    """
    void -> jeu
    redéfinition initialiseJeu
    """
    jeu=[]
    
    # init plateau
    p = []
    for i in range(8):
        p.append([])
        for j in range(8):
            p[i].append(0)
    p[3][3] = 1
    p[4][4] = 1
    p[3][4] = 2
    p[4][3] = 2
    jeu.append(p)
    
    # init joueur
    jeu.append(1)
        
    # init liste coups valide
    jeu.append(None)
    
    # init liste coups joués
    jeu.append([])
    
    # init scores
    jeu.append([2,2])
    
    return jeu

def verifCase(jeu, coup, decalage, joueur, adversaire, valide=False):
    """jeu*coup*List[coup]
    Vérifie si le mouvement dans une case est possible (composante de estValide)
    """ 
    if coup[0]<=0 or coup[0]>=7 or coup[1]<=0 or coup[1]>=7:
        return False
    coupDecale = (coup[0]+decalage[0], coup[1]+decalage[1])
    caseActuelle = game.getCaseVal(jeu,coupDecale[0],coupDecale[1])
    if caseActuelle == 0:
        return False
    if caseActuelle == joueur:
        # True si on a retrouvé un joueur après plusieurs adversaires,
        # False si c'est le premier appel, donc si on a deux cases joueur d'affilée
        return valide
    if caseActuelle == adversaire:
        # vérifie case d'après si possible de faire un encadrement
        return verifCase(jeu,coupDecale,decalage,joueur,adversaire,True)

def estValide(jeu, coup):
    """jeu*(int*int) -> bool
    Vérifie si le coup est valide
    """
    # si la case est déjà remplie
    if game.getCaseVal(jeu,coup[0],coup[1]) != 0:
        return False
    
    if game.getJoueur(jeu) == 1:
        joueur = 1
        adversaire = 2
    else: # == 2
        joueur = 2
        adversaire = 1
        
    coupsDecalage = []
    
    # cas normal
    if coup[0] > 0 and coup[0] < 7 and coup[1] > 0 and coup[1] < 7:
        coupsDecalage = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # coin haut gauche
    if coup[0] == 0 and coup[1] == 0:
        coupsDecalage = [(0,1),(1,0),(1,1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # coin bas droite
    if coup[0] == 7 and coup[1] == 7:
        coupsDecalage = [(0,-1),(-1,0),(-1,-1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # coin haut droite
    if coup[0] == 7 and coup[1] == 0:
        coupsDecalage = [(-1,0),(0,1),(-1,1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # coin bas gauche
    if coup[0] == 0 and coup[1] == 7:
        coupsDecalage = [(1,-1),(1,0),(0,-1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # cas haut
    if coup[0] == 0:
        coupsDecalage = [(0,1),(1,1),(1,0),(0,-1),(1,-1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True

    
    # cas bas
    if coup[0] == 7:
        coupsDecalage = [(0,1),(-1,1),(0,-1),(-1,-1),(-1,0)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True


    # cas gauche
    if coup[1] == 7:
        coupsDecalage = [(1,0),(0,-1),(-1,-1),(-1,0),(1,-1)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True
    
    # cas droite
    if coup[1] == 0:
        coupsDecalage = [(0,1),(1,1),(1,0),(-1,1),(-1,0)]
        for decalage in coupsDecalage:
            if verifCase(jeu,coup,decalage,joueur,adversaire):
                return True
    
    return False
    
def listeCoupsValides(jeu):
    """jeu->Liste[Coup]
    Retourne une liste des coups valides
    """
    return [(i,j) for i in range(0,8) for j in range(0,8) \
        if estValide(jeu,(i,j))]

def remplir(jeu,caseY,caseX,deltaY,deltaX,joueur):
    """jeu*Coup*Coup*int*int*int->Coup
    Retrouve la case à remplir
    """
    caseYInit=caseY
    caseXInit=caseX

    while(caseX >=0 and 7 >= caseX and caseY >=0 and 7 >= caseY \
        # condition d'arret : quand la prochaine case est vide ou
        # une case correspondant au joueur actuel
        and game.getCaseVal(jeu, caseY+deltaY, caseX+deltaX) != 0 \
        and game.getCaseVal(jeu, caseY+deltaY, caseX+deltaX) != joueur):
        caseY=caseY+deltaY
        caseX=caseX+deltaX
       
    if game.getCaseVal(jeu, caseY+deltaY, caseX+deltaX) == 0:
        caseY=caseYInit
        caseX=caseXInit
     
    return (caseY,caseX)
                
def joueCoup(jeu,coup):
    """jeu*coup->void
    Hypothèse : le coup est valide
    soldat = joueur qui joue le coup"""
    # Choix de nombre pour remplacer
    joueur = game.getJoueur(jeu)
    #if game.getJoueur(jeu)==1:
    #    joueur= 1
    #else: #Le cas où il est égal à 2
    #    joueur= 2
        
    jeu[0][coup[0]][coup[1]]=joueur
    caseY=coup[0]
    caseX=coup[1]

    
    # Changement horizontale gauche
    # cherche dernière case à remplir`
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],0,-1,joueur)
    # remplit tout jusqu'à cette case`
    for i in range(caseX,coup[1]+1):
        jeu[0][coup[0]][i]=joueur
    caseY=coup[0]
    caseX=coup[1]
    
    #Changement horizontale droite       
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],0,1,joueur)
    for i in range(coup[1],caseX+1):
        jeu[0][coup[0]][i]=joueur
    caseY=coup[0]
    caseX=coup[1]

    #changement vertical bas       
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],-1,0,joueur)    
    for i in range(caseY,coup[0]+1):
        jeu[0][i][coup[1]]=joueur
    caseY=coup[0]
    caseX=coup[1]
    
    #changement vertical haut   
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],1,0,joueur) 
    for i in range(coup[0],caseY+1):
        jeu[0][i][coup[1]]=joueur
    caseY=coup[0]
    caseX=coup[1]
    
    diff=coup[0]-coup[1] 
    #Changement haut droite   
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],1,1,joueur)
    #Changement des cases entre les joueurs
    for i in range(coup[0],caseY+1):
        if ((diff-i)<=7 and (diff-i)>=0):
           jeu[0][i][diff-i]=joueur
        else:
            break
    caseY=coup[0]
    caseX=coup[1]

    #Changement bas gauche  
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],-1,-1,joueur)
    #Changement des cases entre les joueurs
    for i in range(caseY,coup[0]+1):
        if ((diff-i)<=7 and (diff-i)>=0):
           jeu[0][i][diff-i]=joueur
        else:
            break       
    caseY=coup[0]
    caseX=coup[1]
    
    somme=coup[0]+coup[1]
    
    #Changement bas droite
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],-1,1,joueur) 
    for i in range(caseY,coup[0]+1):
        jeu[0][i][somme-i]=joueur
    caseY=coup[0]
    caseX=coup[1]

    #Changement haut gauche (vraiment bas gauche)
    (caseY,caseX)=remplir(jeu,coup[0],coup[1],1,-1,joueur)
    #Changement des cases entre les joueurs
    for i in range(coup[0],caseY+1):
        jeu[0][i][somme-i]=joueur
    caseY=coup[0]
    caseX=coup[1]
    
    jeu[3].append(coup)
    changeScore(jeu)
    game.changeJoueur(jeu)

     
def changeScore(jeu):
    """jeu->void
    Met à jour les scores (appelé à la fin de joueCoup)
    """
    score1=0
    score2=0
    for i in range(8):
        for j in range(8):
            if game.getCaseVal(jeu,i,j)==1:
                score1+=1
            if game.getCaseVal(jeu,i,j)==2:
                score2+=1
    jeu[4][0]=score1
    jeu[4][1]=score2
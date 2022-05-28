#!/usr/bin/env python
# -*- coding: utf-8 -*-

# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup:[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:[plateau nat List[coup] List[coup] List[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2
import copy

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2


#Boucle principale


#Fonctions minimales 

def getCopieJeu(jeu):
    """ jeu->jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant (?)
    """ 
    return copy.deepcopy(jeu)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu (plus de coup valide ou trop de coups joués)
    """
    return getCoupsValides(jeu) == [] or len(getCoupsJoues(jeu)) == 100

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    joueur = joueur1
    if jeu[1] == 2: # jeu[1] : joueur à qui c'est le tour de jouer
        joueur = joueur2
    coup = joueur.saisieCoup(jeu)
    
    while not coupValide(jeu,coup):
        print("Coup non valide, recommencez")
        coup = joueur.saisieCoup(jeu)
    return coup

def getCoupsValides(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met à jour la liste des coups valides (c'est à dire si on vient de changer le joueur)
    """
    if jeu[2] is None:
        jeu[2] = game.listeCoupsValides(jeu)
    return jeu[2]

def coupValide(jeu,coup):
   """ jeu*coup*bool->bool
       Retourne vrai si le coup appartient à la liste de coups valides du jeu
       (donc si le coup est valide)
   """
   return coup in getCoupsValides(jeu)

def joueCoup(jeu,coup):
    """jeu*coup->void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese:le coup est valide
        Met à jour tous les élements de la structure jeu 
        La liste des coups valides et remis à 0
    """
    game.joueCoup(jeu,coup)

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste 
        des coups valides None, scores a 0 et joueur = 1)
    """
    return game.initialiseJeu()
    

def getGagnant(jeu):
    """jeu->natif game.getJoueur(jeu) == 2
    Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    # score joueur 1
    score1 = getScore(jeu,1)
    # score joueur 2
    score2 = getScore(jeu,2)

    if score1 < score2:
        return 2
    elif score1 > score2:
        return 1
    else:
        return 0

def affiche(jeu):
    """ jeu->void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer
                    
         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
    # affichage du coup joue
    print("Coup joue = ", end='')
    if len(jeu[3]) == 0:
        print(None)
    else:
        print(jeu[3][-1])
    
    # affichage score
    print("Scores {}, {}".format(jeu[4][0],jeu[4][1]))
    
    # affichage plateau
    # 1e ligne avec indice colonne
    print("   ", end='')
    for i in range(len(jeu[0][0])):
        print("|  {}  ".format(i), end='')
    print('|')
    
    for i in range(len(jeu[0])):
        # affichage tire (affiche en fonction du nombre de colonnes)
        print("---",end='')
        for k in range(len(jeu[0][0])):
            print("------",end='')
        print("-")
        
        # affichage des elements de la ligne
        print(" {} |".format(i), end='')
        for j in range(len(jeu[0][i])):
            print("  {}  |".format(jeu[0][i][j]), end = '')
        print()
        
    # affichage joueur
    print("Joueur {}, a vous de jouer".format(jeu[1]))
    

# Fonctions utiles

def getPlateau(jeu):
    """ jeu  -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def getCoupsJoues(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[3]


def getScores(jeu):
    """ jeu  -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]

def getJoueur(jeu):
    """ jeu  -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]


def changeJoueur(jeu):
    """ jeu  -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    # jeu[1] = int(not(bool(jeu[1]-1)))+1
    if jeu[1] == 1:
        jeu[1] = 2
    else:
        jeu[1] = 1
    jeu[2]=None

def getScore(jeu,joueur):
    """ jeu*nat->int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    return jeu[4][joueur-1]

def getCaseVal(jeu, ligne, colonne):
    """ jeu*nat*nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]
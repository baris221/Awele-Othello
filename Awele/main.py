#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import random
import pickle
import os

import matplotlib.pyplot as plt
import numpy as np
import textwrap

import game
import awele
game.game=awele
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_horizon1
import joueur_minimax
import joueur_alphabeta

def partie(affichage=True, alea=True, nbMax=1000, initJeu=True, jeu = None):
    """bool,bool,int,bool,jeu->int
        Boucle principale du jeu, choix d'afficher et de randomiser
        4 premiers tours. Retourne le joueur gagnant
    """
    i=0
    if initJeu:
        jeu=game.initialiseJeu()
    while not game.finJeu(jeu):
        if alea and i<4:
            coup=joueur_aleatoire.saisieCoup(jeu)
        else:
            coup=game.saisieCoup(jeu)
        if i > nbMax: 
            print("Erreur : atteint limite d'itérations")
            return
        if affichage:
            game.affiche(jeu)
            
        game.joueCoup(jeu,coup)
        i+=1
    jeu = awele.finaliseJeu(jeu) # faut peut-être mettre dans game.py
    #print("Joueur gagnant : {}".format(game.getGagnant(jeu)))
    return game.getGagnant(jeu)

def stats(nbParties,joueur, initJeu = True, jeu = None):
    """ int,int,bool,jeu->int
    Joue nbParties et retourne des statistiques
    """
    nbGagne = 0
    nbNul = 0
    for i in range(nbParties):
        gagnant = partie(False,True,1000, initJeu, jeu)
        if gagnant == joueur:
            nbGagne+=1
        if gagnant == 0:
            nbNul+=1
        #print("Partie jouées : {}".format(i+1))
    return (nbParties, nbGagne, nbNul)

def afficheStats(resStats):
    """ (int*int*int) -> void
    Affiche des statistiques du format retourné par stats
    """
    nbPerdu = resStats[0]-resStats[1]-resStats[2]
    print("Nombre de parties gagnées : {1}/{0}\n\
Nombre de parties nulles : {2}/{0}\n\
Nombre de parties perdues : {3}/{0}".format(resStats[0],resStats[1],resStats[2], nbPerdu))

def statsGraphique(joueur1,joueur2,horizon,nom_fic):
    """module,module,int,str->void
    Génère des statistiques pour les joueurs et l'horizon en entrée,
    les stocke dans des fichiers.
    Le premier joueur doit avoir l'horizon paramétrable
    """
    listeHorizon=[]
    listeResultat=[]
    game.joueur1=joueur1
    game.joueur2=joueur2
    nbParties = 50 # le nombre de parties qu'on utilisera pour les statistiques
    for i in range(1,horizon+1):
        # une itération par horizon (on fait jusqu'à 5 car c'est le dernier horizon)
        #print("Horizon : {}".format(i))
        game.joueur1.horizon=i

        # premier essai pour quand le joueur est joueur 1
        stats1=stats(nbParties,1)
        #print("Quand joueur 1")
        #afficheStats(stats1)

        # On échange les joueurs pour faire la moyenne des taux de victoire
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp
        game.joueur2.horizon=i
        stats2=stats(nbParties,2)
        #print("Quand joueur 2")
        #afficheStats(stats2)

        # On remet les joueurs à l'état de base
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp

        # On ajoute les résultats à une liste (on prend la moyenne des taux de victoire quand on est joueur 1 et quand on est joueur 2)
        listeResultat.append((stats1[1]+stats2[1])/(2*nbParties)*100) #stats[1] est le taux de victoire
        listeHorizon.append(i)
    
    # Enregistrement des données (pour avoir plus de flexibilité lors de la génération des graphiques)
    open_file = open("Donnees/{}Resultat.obj".format(nom_fic), "wb")
    pickle.dump(listeResultat, open_file)
    open_file.close()

def appelsStatsGraphique(nbJeux=10):
    """int->void
    Calcule le nombre d'appels a evaluation dans minimax et alphabeta contre horizon 1 pour comparer les performances.
    Les enregistre dans un fichier.
    """
    game.joueur2 = joueur_horizon1
    matriceAppelsMinimax = []
    matriceAppelsAlphabeta = []
    for k in range(nbJeux):
        # on initialise un jeu global pour que le même jeu soit joué
        initJeu = False
        jeu = game.initialiseJeu()

        game.joueur1=joueur_minimax
        listeAppelsMinimax=[] # liste avec nombre d'appels par horizon
        
        for i in range(1,6):
            game.joueur1.horizon=i
            copieJeu = game.getCopieJeu(jeu)
            stats(1,1,initJeu,copieJeu)
            listeAppelsMinimax.append(game.joueur1.cpt)
            game.joueur1.cpt=0
        
        matriceAppelsMinimax.append(listeAppelsMinimax)

        # compte le nombre d'appels pour alphabeta
        game.joueur1=joueur_alphabeta
        listeAppelsAlphabeta=[] # liste avec nombre d'appels par horizon
        
        for j in range(1,6):
            game.joueur1.horizon=j
            copieJeu = game.getCopieJeu(jeu)
            stats(1,1,initJeu,copieJeu)
            listeAppelsAlphabeta.append(game.joueur1.cpt)
            game.joueur1.cpt=0

        matriceAppelsAlphabeta.append(listeAppelsAlphabeta)

    # moyenne des listes sur nbJeux
    #arrayAppelsMinimax = np.array(matriceAppelsMinimax)
    #arrayAppelsAlphabeta = np.array(matriceAppelsAlphabeta)
    listeAppelsMinimax=np.mean(matriceAppelsMinimax,axis=0)
    listeAppelsAlphabeta=np.mean(matriceAppelsAlphabeta,axis=0)

    # Enregistrement des données
    open_file = open("Donnees/listeAppelsMinimax.obj", "wb")
    pickle.dump(listeAppelsMinimax, open_file)
    open_file.close()

    open_file = open("Donnees/listeAppelsAlphabeta.obj", "wb")
    pickle.dump(listeAppelsAlphabeta, open_file)
    open_file.close()

def lectureListe(nom_fic):
    """str->List[int]
    Lit les données du fichier nom_fic (générées par statsGraphique)
    """
    open_file = open(nom_fic, "rb")
    res=pickle.load(open_file)
    open_file.close()
    return res

def minimaxGraphique():
    """void->void
    Génère un graphique montrant le taux de victoire de minimax contre horizon1 en fonction de l'horizon de minimax
    """
    nom_fic = "minimax"
    # Génération des données
    statsGraphique(joueur_minimax,joueur_horizon1,3,nom_fic) # on fait jusqu'à l'horizon 3 car max avec temps d'exécution bas

    # lecture des fichiers
    listeResultat = lectureListe("Donnees/{}Resultat.obj".format(nom_fic))
    listeHorizon = np.arange(1,4,1)
    
    # génération du graphique
    plt.clf() # initialisation du plot

    plt.plot(listeHorizon,listeResultat)
    plt.xlabel("Horizon de minimax")
    plt.ylabel("Taux de victoire")
    plt.ylim(0,100)
    plt.xticks(listeHorizon)
    t = "Le taux de victoire de minimax contre horizon1 en fonction de l'horizon de minimax (Awélé)"
    plt.title("\n".join(textwrap.wrap(t,70)))
    plt.savefig('Graphiques/minimax_vs_horizon1.png',bbox_inches='tight')

def alphabetaGraphique():
    """void->void
    Génère un graphique montrant le taux de victoire de alphabeta contre horizon1 en fonction de l'horizon de alphabeta
    """
    nom_fic="alphabeta"

    # Génération des données
    statsGraphique(joueur_alphabeta,joueur_horizon1,5,nom_fic) # on fait jusqu'à l'horizon 5 car max avec temps d'exécution bas

    # lecture des fichiers et génération de l'abscisse
    listeResultat = lectureListe("Donnees/{}Resultat.obj".format(nom_fic))
    listeHorizon = np.arange(1,6,1)

    # génération du graphique
    plt.clf() # initialisation du plot

    plt.plot(listeHorizon,listeResultat)
    plt.xlabel("Horizon de alphabeta")
    plt.ylabel("Taux de victoire")
    plt.ylim(0,100)
    plt.xticks(listeHorizon)
    t = "Le taux de victoire de alphabeta contre horizon1 en fonction de l'horizon de alphabeta (Awélé)"
    plt.title("\n".join(textwrap.wrap(t,70)))
    plt.savefig('Graphiques/alphabeta_vs_horizon1.png',bbox_inches='tight')



def appelsGraphique():
    """void->void
    Génère un graphique montrant le nombre d'appels à évaluation moyen sur 10 jeux de minimax vs alphabeta
    (comparaison des performances)
    """
    # Génération des données
    appelsStatsGraphique(100)

    # lecture des fichiers
    listeAppelsMinimax = lectureListe("Donnees/listeAppelsMinimax.obj")
    listeAppelsAlphabeta= lectureListe("Donnees/listeAppelsAlphabeta.obj")
    listeHorizonTime = np.arange(1,6,1) 
    
    # Génération du graphique
    plt.clf() # initialisation du plot

    plt.plot(listeHorizonTime,listeAppelsMinimax,label="minimax")
    plt.plot(listeHorizonTime,listeAppelsAlphabeta,label="alphabeta")
    plt.xlabel("Horizon")
    plt.ylabel("Nombre d'appels à évaluation")
    plt.xticks(listeHorizonTime)
    plt.title("Le nombre d'appels à évaluation dans minimax vs alphabeta (Awélé)")
    plt.legend()
    plt.savefig('Graphiques/appels_minimax_vs_alphabeta.png',bbox_inches='tight')

# initialisation de seed random
random.seed()

# création des répertoires s'ils n'existent pas
directory = ["Donnees","Graphiques"]
for nom_dir in directory:
    if not os.path.exists(nom_dir):
        os.mkdir(nom_dir)

# ne pas exécuter minimaxGraphique ou alphabetaGraphique en même temps que appelsGraphique
minimaxGraphique() # 50 parties par position joueur
alphabetaGraphique() # 50 parties par position joueur
#appelsGraphique() # 100 parties

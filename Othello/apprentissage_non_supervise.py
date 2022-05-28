#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import random
import pickle
import time
import os

import matplotlib.pyplot as plt
import numpy as np

import game
import othello
game.game=othello
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_minimax
import joueur_alphabeta
import joueur_horizon1

def partie(affichage=False, alea=True, nbMax=1000):
    """bool,bool,int->int
        Boucle principale du jeu, choix d'afficher et de randomiser
        4 premiers tours. Retourne le joueur gagnant
    """
    i=0
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
    #print("Joueur gagnant : {}".format(game.getGagnant(jeu)))
    return game.getGagnant(jeu)

def stats(nbParties,joueur):
    """ int,int->int
    Retourne le nombre de parties gagnées
    """
    nbGagne = 0
    nbNul = 0
    for i in range(nbParties):
        gagnant = partie()
        if gagnant == joueur:
            nbGagne+=1
        if gagnant == 0:
            nbNul+=1
        #print("Partie jouées : {}".format(i+1))
    return (nbParties, nbGagne, nbNul)

def afficheStats(resStats):
    """
    int->void
    Affichage du score à partir de resStats
    """
    nbPerdu = resStats[0]-resStats[1]-resStats[2]
    print("Nombre de parties gagnées : {1}/{0}\n\
Nombre de parties nulles : {2}/{0}\n\
Nombre de parties perdues : {3}/{0}".format(resStats[0],resStats[1],resStats[2], nbPerdu))



def apprentissageNonSupervise(nbMax = 100):
    """bool->void
    Effectue un apprentissage non supervisé avec horizon 1 en premier joueur
    et alphabeta ou minimax horizon 3 (ou autre, paramétrable) en Oracle
    """
    cpt = 0 # nombre d'explorations
    epsilon = 1 # initilisation du point optimal
    nbParties = 10 # nombre de parties sur lequel on teste chaque poids
    tauxVictoire = 0 # initialisation du score d'un test des poids
    game.joueur1=joueur_horizon1
    game.joueur2=joueur_alphabeta
    # Initialisation des poids
    game.joueur1.poids = [2,8,-6,4,-5]
    game.joueur2.poids = [2,8,-6,4,-5]

    # Choix de l'horizon
    game.joueur2.horizon=3

    # initialisation de liste de score de test de poids
    listeTauxVictoire=[]

    # initialisation de la liste de temps d'execution
    listeProcessTime = []
    startTime=time.process_time()
    # tant que l'exploration n'est pas achevée ou le score est inférieur à 100%
    while epsilon>0 and tauxVictoire<100 and cpt<nbMax:
        epsilon=epsilon*0.99999999
        i = random.randrange(0,len(game.joueur1.poids))
        # i : le paramètre modifié
        s = random.randrange(-1,1,2)
        # s : choix entre 1 et -1 (changer ou pas signe du paramètre)
        game.joueur1.poids[i] = game.joueur1.poids[i]*s*epsilon # exploration simple
        
        # statistiques pour quand joueur1 est le premier joueur
        stats1 = stats(nbParties,1)
        
        # stats pour quand joueur1 est le deuxième joueur
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp
        stats2 = stats(nbParties,2)
        
        nouvTauxVictoire = (stats1[1] + stats2[1])/(2*nbParties)*100 # moyenne des stats des deux études
        
        # On remets les joueurs à l'état de base
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp

        # si le nouveau taux de victoire est mieux, on ajoute les poids au fichier meilleursPoids (poids.txt) et on ajoute le score à la liste des performances
        if nouvTauxVictoire > tauxVictoire:
            tauxVictoire = nouvTauxVictoire
            with open('poids.txt', 'a') as meilleursPoids:
                meilleursPoids.write(str(game.joueur1.poids)+"\n")
            #print(game.joueur1.poids)
            #print("En tant que premier joueur :")
            #afficheStats(stats1)
            #print("En tant que deuxième joueur :")
            #afficheStats(stats2)
            listeTauxVictoire.append(nouvTauxVictoire)
            listeProcessTime.append(time.process_time()-startTime)
        cpt+=1
        if (cpt%10 == 0):
            print(str(cpt)+"/"+str(nbMax))

        # Enregistrement des données (pour avoir plus de flexibilité lors de la génération des graphiques)
        open_file = open("Donnees/listeTauxVictoire.obj", "wb")
        pickle.dump(listeTauxVictoire, open_file)
        open_file.close()

        open_file = open("Donnees/listeProcessTime.obj", "wb")
        pickle.dump(listeProcessTime, open_file)
        open_file.close()

def lectureListe(nom_fic):
    """str->List[int]
    Lit les données du fichier nom_fic (générées par statsGraphique)
    """
    open_file = open(nom_fic, "rb")
    res=pickle.load(open_file)
    open_file.close()
    return res

def nonSuperviseGraphique():
    """void->void
    Génère un graphique représentant le taux de victoire en fonction du temps d'exécution
    de l'apprentissage
    """
    # génération du graphique
    plt.clf() # initialisation du plot
    
    # lecture des fichiers
    listeTauxVictoire = lectureListe("Donnees/listeTauxVictoire.obj")
    listeProcessTime = lectureListe("Donnees/listeProcessTime.obj")

    plt.plot(listeProcessTime,listeTauxVictoire)
    plt.xlabel("Temps (s)")
    plt.ylabel("Taux de victoire")
    plt.ylim(0,100)
    plt.title("Taux de victoire d'alphabeta en fonction du temps (Othello)")
    plt.savefig('Graphiques/apprentissage_non_supervise.png',bbox_inches='tight')

# initialisation de seed random
random.seed()

# création des répertoires s'ils n'existent pas
directory = ["Donnees","Graphiques"]
for nom_dir in directory:
    if not os.path.exists(nom_dir):
        os.mkdir(nom_dir)

apprentissageNonSupervise(500) # 500 explorations, 10 parties par exploration
nonSuperviseGraphique()
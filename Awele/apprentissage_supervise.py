#!/usr/bin/env python
# -*- coding: utf-8 -*-
import awele
import sys
sys.path.append("..")
import game
import pickle
import os
import textwrap
import random
game.game=awele
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_minimax
import joueur_alphabeta
import joueur_horizon1
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline


def lectureListe(nom_fic):
    """str->List[int]
    Lit les données du fichier nom_fic (générées par statsGraphique)
    """
    open_file = open(nom_fic, "rb")
    res=pickle.load(open_file)
    open_file.close()
    return res

def apprentissageSupervise(nbMax=100):
    """int->void
    Effectue un apprentissage supervisé avec horizon 1 en premier joueur
    et alphabeta horizon 5 en Oracle
    """
    #jeu = game.initialiseJeu()
    alpha = 1 # pas d'apprentissage
    oracle=joueur_alphabeta
    apprenti=joueur_horizon1
    adversaire = joueur_alphabeta
    game.joueur1 = apprenti
    game.joueur2 = adversaire
    apprenti.poids=[2,-1,-1]
    oracle.poids=[2,-1,-1]
    horizonOracle = 5
    oracle.horizon=horizonOracle
    
    nbDesaccord=0
    listeNbAccord=[]
    i = 0
    cpt=0
    cptApprenti=0
    while alpha > 0 and nbMax>cpt:
        i=0
        jeu=game.initialiseJeu()
        joueur_alphabeta.joueur=game.getJoueur(jeu)
        joueur_horizon1.joueur=game.getJoueur(jeu)
        while not game.finJeu(jeu):
            if i<4:
                coup=joueur_aleatoire.saisieCoup(jeu)
                i+=1
                game.joueCoup(jeu,coup)
            else :
                cptApprenti=cptApprenti+1
                listeCoupsValides = game.getCoupsValides(jeu)
                estimationOracle = []
                estimationApprenti = []
                paramOracle = []
                paramApprenti = []
                for coup in listeCoupsValides:
                    estimationOracle.append(oracle.estimation(jeu,coup, horizonOracle))
                    paramOracle.append(oracle.param1)
                    estimationApprenti.append(apprenti.estimation(jeu,coup))
                    paramApprenti.append(apprenti.param1)
                indiceMeilleurCoupOracle = np.argmax(estimationOracle)
                indiceMeilleurCoupApprenti = np.argmax(estimationApprenti)
                if not (indiceMeilleurCoupOracle == indiceMeilleurCoupApprenti):
                    for j in range(len(listeCoupsValides)):
                        evalOptimalApprenti = estimationApprenti[indiceMeilleurCoupOracle]
                        for k in range(len(estimationApprenti)):
                            if evalOptimalApprenti-estimationApprenti[k]<1:
                                for l in range(len(oracle.poids)):
                                    apprenti.poids[l] = apprenti.poids[l]-alpha * (paramApprenti[j][l]-paramOracle[j][l])
                
                    nbDesaccord=nbDesaccord+1 #Augmente un par un en cas différent indice de apprenti et oracle
                    #print(apprenti.poids)
                game.joueCoup(jeu,listeCoupsValides[indiceMeilleurCoupOracle])
                if(game.finJeu(jeu)):
                    break
                game.joueCoup(jeu,adversaire.saisieCoup(jeu))
        cpt+=1
        if (cpt%10 == 0):
            print(str(cpt)+"/"+str(nbMax))
        
        alpha=alpha*0.99999
        nbAccord=cptApprenti-nbDesaccord
        listeNbAccord.append((nbAccord/cptApprenti)*100)
        cptApprenti=0
        nbDesaccord=0
    
    #Enregistrement des données
    open_file = open("Donnees/listeNbAccord.obj", "wb")
    pickle.dump(listeNbAccord, open_file)
    open_file.close()

def apprentissageSuperviseGraphique():
    """
    Génère un graphique représentant le taux de l'accord en fonction du fois d'exécution
    de l'apprentissage
    """
    listeNbAccord=lectureListe("Donnees/listeNbAccord.obj")
    listeNbJeux=np.arange(0,len(listeNbAccord),1) # l'abscisse pour afficher le nombre de parties jouées
    
    # génération du graphique
    plt.clf() # initialisation du plot

    # définition de la taille du graphique
    plt.figure(figsize=(30,6))
    #plt.plot(listeNbJeux,listeNbAccord)

    listeNbJeux_listeNbAccordSplineTout = make_interp_spline(listeNbJeux,listeNbAccord)
    abscisseTout = np.linspace(listeNbJeux[0],listeNbJeux[-1],400)
    ordonneeTout = listeNbJeux_listeNbAccordSplineTout(abscisseTout)
    plt.plot(abscisseTout,ordonneeTout, label = "Données lissées")

    listeNbJeux_listeNbAccordSpline = make_interp_spline(listeNbJeux,listeNbAccord)
    abscisseGeneral = np.linspace(listeNbJeux[0],listeNbJeux[-1],50)
    ordonneeGeneral = listeNbJeux_listeNbAccordSpline(abscisseGeneral)
    plt.plot(abscisseGeneral,ordonneeGeneral,label="Tendance générale")


    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux d'accord (en pourcentage)")
    plt.ylim(0,100)
    plt.xticks(np.arange(listeNbJeux[0],listeNbJeux[-1],step=1000))
    plt.title("Taux d'accord de l'apprenti (horizon1) et l'oracle (alphabeta horizon 3) en fonction du nombre de parties jouées (Awélé)")
    plt.legend()
    plt.savefig('Graphiques/apprentissage_supervise.png',bbox_inches='tight')


directory = ["Donnees","Graphiques"]
for nom_dir in directory:
    if not os.path.exists(nom_dir):
        os.mkdir(nom_dir)

random.seed()
apprentissageSupervise(4000) # 4000 parties
apprentissageSuperviseGraphique()
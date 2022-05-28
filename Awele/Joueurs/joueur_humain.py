#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    coup=input("choisissez une case :")
    while (coup=='' or int(coup)>=6 or int(coup)<0):
            print("Rechoissez votre case")
            coup=input("choisissez une case entre 0 et 5 :")
    
    return (jeu[1]-1,int(coup))
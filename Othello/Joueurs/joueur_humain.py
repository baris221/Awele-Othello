#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    caseX = input("choisissez une  ligne")
    caseY = input("choisissez une colonne")
    while caseX=='' or caseY=='' or int(caseX)>=8 or int(caseX)<0 \
    or int(caseY)>=8 or int(caseY)<0:
        print("pas présent sur plateau")
        caseX = input("choisissez une  ligne")
        caseY = input("choisissez une colonne")
          
    return (int(caseX),int(caseY))
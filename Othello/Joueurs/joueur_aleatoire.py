#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import random

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    listeCoupsVal = game.getCoupsValides(jeu)
    return (random.choice(listeCoupsVal))

# pas besoin de evalCoup car aléatoire
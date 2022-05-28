import sys
sys.path.append("../..")
import game

global poids
poids = [1.9998600041999308, -0.9998600090996368, -0.9997600275979776]

global param1
param1 = []



def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur
    joueur=game.getJoueur(jeu)
    coup = decision(jeu)
    return coup

def dot(v1,v2):
    """ Hypothèse : len(v1)==len(v2)
    """
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def estimation(jeu,coup):
    copie=game.getCopieJeu(jeu)
    game.joueCoup(copie, coup)
    return evaluation(copie)

def evaluation(jeu):
    """jeu->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """
    param=[]
    # différence de score
    diffScores = game.getScore(jeu,joueur)-game.getScore(jeu,3-joueur)
    param.append(diffScores)

    # nombre de cases vides
    nbCasesVides=0
    for i in range(0,6):
        if(game.getCaseVal(jeu,joueur-1,i)==0):
            nbCasesVides=nbCasesVides+1
    param.append(nbCasesVides)

    # nombre de cases vulnerables
    nbCasesVulnerables=0
    for i in range(0,6):
        if(game.getCaseVal(jeu,joueur-1,i)==1 or game.getCaseVal(jeu,joueur-1,i)==2 ):
            nbCasesVulnerables=nbCasesVulnerables+1
    param.append(nbCasesVulnerables)
    
    global param1
    param1=param
       
    return dot(poids,param)

def decision(jeu):
    """jeu->(int,int)
       Elle renvoie le coup qui a meilleur score à evaluation
    """
    #On fait la décision
    listeCoups=game.getCoupsValides(jeu)
    meilleurScore = estimation(jeu,listeCoups[0])
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        scoreEval = estimation(jeu,coup)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup



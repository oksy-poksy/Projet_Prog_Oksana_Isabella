# fichier pour les classes
#on utilise numpy pour la structure de code
from builtins import Exception


class JeuFactice: #architecture du code
    def __init__(self): pass
    def premier_tour(self): pass
    def tour_de_jeu(self, joueur, mat): pass #choisir la case dans laquelle le joueur veut jouer, dans quelle matrixce
    #cette fct doit retiurner la matrice dans laquelle le prochain tour se deroule
    def signe_de_joueur1(self): pass
    def signe_de_joueur2(self): pass
    def reussite_matrice(self, joueur, mat): pass
    #complete la matrice 10
    def fin_jeu(self, joeur): pass


    #Oksana: je me suis dit on devait plus faire une grosse grille, dans laquelle on met les 9 petites
    def __init__(self):
        # État interne (simulé)
        self._grille_principale = None  # etat des 9 matrices (jagné/perdu)
        self._grilles_secondaires = None  # etat des cases




class Exception():
    def __init__(self): pass

    class ErreurClick(Exception): pass

class Matrices:
    def __init__(self): pass

class Pokemons:
    def __init__(self): pass

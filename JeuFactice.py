# fichier pour les classes
#on utilise numpy pour la structure de code
from builtins import Exception


# TODO: idee pour les combats de pokemons: mettre en place un coef multiplicateur pour savoir quel pok gagne

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


    #Oksana: j'ai besoin de ca -----------------------------------------------------------------------------------------
    def __init__(self):
        # État interne (simulé)
        self._grille_principale = None  # etat des 9 matrices (jagné/perdu)
        self._grilles_secondaires = None  # etat des cases

    # TODO: Méthodes pour que l'interface puisse lire l'état des grilles (j'en au besoin pour commencer a coder l'interface)
    #je peux les "utiliser" meme si elles sont vides mais pas tester si mon code fonctionne
    def get_joueur_actuel(self): return 1
    def get_grille_cible(self): return None  #Aucune grille ciblée initialement
    def get_etat_case(self, i_principal, i_secondaire): return ""  # Retourne "" ou "X" ou "O"
    def get_banc_pokemons(self, joueur): return []  # Pour la future sidebar




class Exception():
    def __init__(self): pass

    class ErreurClick(Exception): pass

class Matrices:
    def __init__(self): pass

class Pokemons:
    def __init__(self): pass

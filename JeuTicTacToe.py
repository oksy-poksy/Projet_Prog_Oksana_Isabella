from JeuFactice import JeuFactice
from random import random

class Tictactoe(JeuFactice):
    def __init__(self):
        super().__init__()
        self.plateau={i: [[0,0,0] for k in range(9)] for i in range(1,10)}
        self.J1="O"
        self.J2="X"
        self.jactuel= random(["X","O"])
        self.grille_actu=self.G1

    def premier_tour(self, joueur,grille,case):
        self.grille_actu=self.plateau[grille]

        self.grille_actu[case[1]][case[0]]==self.joueur

    def nomjsp(self, joueur, grille, case):
        self.plateau[grille][case[0]][case[1]] == self.joueur


class Cellule():
    def __init__(self):
        self.valeur = None #X ou O

    def marquer_case(self,joueur):
        self.valeur=joueur

class PetiteGrille():
    def __init__(self):
        self.grille = [[Cellule() for k in range(3)]for i in range(3)]
        self.gagnant = None

    def jouer_coup(self,position, joueur):
        self.grille[position[0]][position[1]]=joueur

    def verifer_victoire(self):
        #lignes
        ligne=True
        colonne=True

        #verif si ligne gagné
        for i in range(len(self.grille)):
            j=0
            while ligne == True and j<len(self.grille)-1 :
                if self.grille[i][j] != self.grille[i][j+1]:
                    ligne=False
                else : j+=1
            if ligne == True:
                return True, self.grille[i][j]

        # verif si colonne gagnéé
            for j in range(len(self.grille)):
                i=0
                while colonne == True and i < len(self.grille) - 1:
                    if self.grille[i][j] != self.grille[i+1][j]:
                        colonne = False
                    else :
                        i+=1
                if colonne==True:
                    return True, self.grille[i][j]

        # verif diagonale gagnée
            if self.grille[0][0]==self.grille[1][1]==self.grille[2][2]:
                return True, self.grille[1][1]
            elif self.grille[2][0] == self.grille[1][1] == self.grille[0][2]:
                return True, self.grille[1][1]
            return False

        def est_plein():
            for i in range(len(self.grille)):
                for j in range(len(self.grille)):
                    if self.grille[i][j]=="":
                        return False
            return True

class GrilleGlobale(PetiteGrille):
    def __init__(self):
        super().__init__()
        self.grille_global = [[PetiteGrille() for i in range(3)] for j in range(3)]
        self.gagnant_global=None

    def verifer_victoire_globale(self):
        ligne = True
        colonne = True

        # verif si ligne gagné
        for i in range(len(self.grille_global)):
            j = 0
            while ligne == True and j < len(self.grille) - 1:
                if self.grille_global[i][j].verifer_victoire() == False:
                    ligne = False
                else:
                    j += 1
            if ligne == True:
                return True, self.grille_global[0][0].verifer_victoire()[1]

            # verif si colonne gagnéé
        for j in range(len(self.grille_global)):
            i = 0
            while colonne == True and i < len(self.grille) - 1:
                if self.grille_global[i][j].verifer_victoire() == False:
                    colonne = False
                else:
                    j += 1
            if colonne == True:
                return True, self.grille_global[0][0].verifer_victoire()[1]

        if self.grille_global[0][0].verifer_victoire() == True and self.grille_global[1][1].verifer_victoire() and self.grille_global[2][2].verifer_victoire():
            return True, self.grille_global[1][1].verifer_victoire()[1]
        elif self.grille_global[2][0].verifer_victoire() == True and self.grille_global[1][1].verifer_victoire() and self.grille_global[0][2].verifer_victoire():
            return True, self.grille_global[1][1].verifer_victoire()[1]
        return False

class Jeu():
    def __init__(self):
        self.plateau = GrilleGlobale()
        self.joueur_actuel=None # a qui le tour
        self.grille_actuelle=None #coordonées de la petite grille



















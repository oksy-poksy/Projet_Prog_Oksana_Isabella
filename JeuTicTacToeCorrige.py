# JeuTicTacToe.py

from JeuFactice import JeuFactice
from random import choice #a la place de random car ca faisiait une erreur

class Tictactoe(JeuFactice):
    def __init__(self):
        super().__init__()

        self.plateau = {i: [[0, 0, 0] for k in range(3)] for i in range(1, 10)}
        self.J1 = "O"
        self.J2 = "X"

        # CORRECTION de l'erreur : utilisation de choice()
        self.jactuel = choice([self.J1, self.J2])
        self.grille_actu = None # self.G1 n'etait pas défini, on l'initialise à None

        self._plateau_ihm = {}
        self._joueur_actuel_signe = self.jactuel  # Synchronisation
        self._grille_cible = None  # Grille ciblée (0 à 8)

    def premier_tour(self, joueur, grille, case):
        self.grille_actu = self.plateau[grille]
        self.grille_actu[case[1]][case[0]] = joueur

    def nomjsp(self, joueur, grille, case):
        # CORRECTION: = au lieu de ==
        self.plateau[grille][case[0]][case[1]] = joueur


    # --- MÉTHODES UTILISÉES PAR L'INTERFACE GRAPHIQUE ---

    def get_joueur_actuel_signe(self):
        """Retourne le signe (X ou O) du joueur actuel"""
        return self._joueur_actuel_signe

    def get_grille_cible(self):
        """Retourne l'indice (0 à 8) de la grille ciblée ou None si libre (IHM)."""
        return self._grille_cible

    def get_etat_case(self, i_principal, i_secondaire):
        """Retourne le signe ('X' ou 'O') à la position ou une chaîne vide (IHM)."""
        return self._plateau_ihm.get((i_principal, i_secondaire), "")

    def jouer_coup_simule(self, i_principal, i_secondaire):
        """
        Simule la logique minimale pour l'affichage (Placement, Changement de Joueur, Grille Cible).
        C'est cette fonction que l'IHM doit appeler.
        """
        if self.get_etat_case(i_principal, i_secondaire) == "":

            is_valid_target = (self._grille_cible is None) or (self._grille_cible == i_principal)

            if is_valid_target:
                self._plateau_ihm[(i_principal, i_secondaire)] = self._joueur_actuel_signe
                self._joueur_actuel_signe = self.J2 if self._joueur_actuel_signe == self.J1 else self.J1
                self._grille_cible = i_secondaire
                return True
        return False

coord_case={(0,0):0,(0,1):1,(0,2):2,(1,0):3,(1,1):4,(1,2):5,(2,0):6,(2,1):7,(2,2):8} #sert à récupérer la coord de la prochaine grille à jouer


class Cellule:
    def __init__(self):
        self.valeur = None  # X ou O

    def marquer_case(self, joueur):
        self.valeur = joueur

    def est_pleine (self):
        if self.valeur is None :
            return False




class PetiteGrille:
    def __init__(self):
        self.grille = [[Cellule() for k in range(3)] for i in range(3)]
        self.gagnant = None

    def jouer_coup(self, position, joueur):
        # Assumons que 'position' est (ligne, colonne)
        self.grille[position[0]][position[1]].marquer_case(joueur)

    def est_plein(self):
        #Vérifie si la petite grille est pleine
        for ligne in self.grille:
            for cellule in ligne:
                if cellule.valeur is None:
                    return False
        return True

    def verifier_victoire(self):
        #Vérifie si la petite grille est gagnée par X ou O, ou s'il y a match nul
        valeurs = [[c.valeur for c in ligne] for ligne in self.grille]

        for ligne in valeurs:
            if ligne[0] is not None and ligne[0] == ligne[1] == ligne[2]:
                self.gagnant = ligne[0]
                return True, ligne[0]

        for j in range(3):
            if valeurs[0][j] is not None and valeurs[0][j] == valeurs[1][j] == valeurs[2][j]:
                self.gagnant = valeurs[0][j]
                return True, valeurs[0][j]

        # Diagonale 1
        if valeurs[0][0] is not None and valeurs[0][0] == valeurs[1][1] == valeurs[2][2]:
            self.gagnant = valeurs[0][0]
            return True, valeurs[0][0]
        # Diagonale 2
        if valeurs[2][0] is not None and valeurs[2][0] == valeurs[1][1] == valeurs[0][2]:
            self.gagnant = valeurs[2][0]
            return True, valeurs[2][0]

        # 4.match nul
        if self.est_plein():
            return True, "NUL"

        return False, None


class GrilleGlobale(PetiteGrille):
    def __init__(self):
        self.grille_global = [[PetiteGrille() for i in range(3)] for j in range(3)]
        self.gagnant_global = None

    def verifier_victoire_globale(self):
        ligne = True
        colonne = True
        #chanfger e verifier seulement avec a grulle jouéé
        # verif si ligne gagné
        for i in range(len(self.grille_global)):
            j = 0
            while ligne == True and j < len(self.grille) - 1:
                if self.grille_global[i][j].verifier_victoire() == False:
                    ligne = False
                else:
                    j += 1
            if ligne == True:
                return True, self.grille_global[0][0].verifier_victoire()[1]

            # verif si colonne gagnéé
        for j in range(len(self.grille_global)):
            i = 0
            while colonne == True and i < len(self.grille) - 1:
                if self.grille_global[i][j].verifier_victoire() == False:
                    colonne = False
                else:
                    j += 1
            if colonne == True:
                return True, self.grille_global[0][0].verifier_victoire()[1]

        if self.grille_global[0][0].verifier_victoire() == True and self.grille_global[1][1].verifier_victoire() and \
                self.grille_global[2][2].verifier_victoire():
            return True, self.grille_global[1][1].verifier_victoire()[1]
        elif self.grille_global[2][0].verifier_victoire() == True and self.grille_global[1][1].verifier_victoire() and \
                self.grille_global[0][2].verifier_victoire():
            return True, self.grille_global[1][1].verifier_victoire()[1]
        return False

    def get_petite_grille(self, grille):
        #grile=(l,c)
        #accéder à la petite grille
        #ligne = grille // 3
        #colonne = (grille% 3)
        return self.grille_globale[grille[0]][grille[1]]

class Jeu():
    def __init__(self):
        self.plateau = GrilleGlobale()
        self.joueur_actuel = None
        self.grille_actuelle = None


    def determiner_premier_joeur(self):
        self.joueur_actuel = choice(["X","O"])

    def changer_joueur(self):
        if self.joueur_actuel=="X":
            self.joueur_actuel="O"
        elif self.joueur_actuel=="O":
            self.joueur_actuel = "X"

    def premier_coup(self,grille,case):
        #grille = (l,c)
        #case = (l,c)
        return self.jouer_coup_global(grille, case)

    def est_coup_valide(self,grille,case):
        pass
    #je ne verifier qu'il clique dans la bonne grille ca cela sera geré par l'interfce


    def jouer_coup_global(self,grille, case):
        if self.est_coup_valide(grille,case):
            coord_prochaine_grille = case

            petite_grille=self.plateau.get_petite_grille(grille)
            petite_grille.jouer_coup(case,self.joueur_actuel)

            petite_grille.verifier_victoire()

            termine, gagnant = self.plateau.verifier_victoire_globale()
            if termine:
                return True

            prochaine_grille = self.plateau.get_petite_grille(case)

            elif prochaine_grille.gagnant==None:
                self.grille_actuelle=prochaine_grille

            else: #la grille est deja pleine et/ou gagné donc le prochain pourra jouer n'importe ou
                self.grille_actuelle=None

            self.changer_joueur()










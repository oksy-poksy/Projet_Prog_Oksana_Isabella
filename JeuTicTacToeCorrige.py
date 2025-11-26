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

    def __repr__(self):
        # Affiche la valeur ou un point si la cellule est vide
        return self.valeur if self.valeur is not None else "."




class PetiteGrille:
    def __init__(self):
        self.grille = [[Cellule() for k in range(3)] for i in range(3)]
        self.gagnant = None

    def get_coords(self,case):
        #accéder à la petite grille
        ligne = case // 3
        colonne = case % 3
        return ligne,colonne


    def jouer_coup(self, case, joueur):
        coord_case=self.get_coords(case)
        self.grille[coord_case[0]][coord_case[1]].marquer_case(joueur)

    def est_plein(self):
        #Vérifie si la petite grille est pleine
        for ligne in self.grille:
            for cellule in ligne:
                if cellule.valeur is None:
                    return False
        return True

    def verifier_victoire(self, case_index):
        case = self.get_coords(case_index)
        casel = case[0]
        casec = case[1]

        joueur = self.grille[casel][casec].valeur

        # Si le coup n'a pas encore de valeur (ce qui ne devrait pas arriver ici), on sort
        if joueur is None:
            return False, None

        # verif colonne
        if self.grille[0][casec].valeur == self.grille[1][casec].valeur == self.grille[2][casec].valeur:
            self.gagnant = self.grille[0][casec].valeur
            return True, self.grille[casel][casec].valeur

        if self.grille[casel][0].valeur == self.grille[casel][1].valeur == self.grille[casel][2].valeur:
            self.gagnant = self.grille[0][casec].valeur
            return True, self.grille[casel][casec].valeur

        if case_index in [0, 2, 4, 6, 8]:
            if self.grille[0][0].valeur == self.grille[1][1].valeur == self.grille[2][2].valeur:
                self.gagnant = self.grille[0][casec].valeur
                return True, self.grille[casel][casec].valeur
            if self.grille[0][2].valeur == self.grille[1][1].valeur == self.grille[2][0].valeur:
                self.gagnant = self.grille[0][casec].valeur
                return True, self.grille[casel][casec].valeur
        return False, None

        # 4.match nul
        if self.est_plein():
            self.gagnant="NUL"
            return True, "NUL"

        return False, None

    def get_case(self,case):
        coord_case=self.get_coords(case)
        return self.grille[coord_case[0]][coord_case[1]]

    def __repr__(self):
        # Affiche le gagnant de la petite grille entre crochets
        gagnant = self.gagnant if self.gagnant is not None else " "
        return f"[{gagnant}]"  # Ex: [X], [O] ou [ ]


class GrilleGlobale(PetiteGrille):
    def __init__(self):
        self.grille_global = [[PetiteGrille() for i in range(3)] for j in range(3)]
        self.gagnant_global = None

    def get_coords_grille(self,grille):
        #accéder à la petite grille
        ligne = grille // 3
        colonne = grille % 3
        return ligne,colonne

    def verifier_victoire_globale(self,grille_index):


        grille_coord = self.get_coords_grille(grille_index)
        if self.get_petite_grille(grille_index).gagnant == None:
            return False, None

        # verif colonne
        if self.grille_global[0][grille_coord[1]].gagnant == self.grille_global[1][grille_coord[1]].gagnant == self.grille_global[2][grille_coord[1]].gagnant:
            self.gagnant_global = self.grille_global[0][grille_coord[1]].gagnant
            return True, self.grille_global[0][grille_coord[1]].gagnant

        if self.grille_global[grille_coord[0]][0].gagnant == self.grille_global[grille_coord[0]][1].gagnant == self.grille_global[grille_coord[0]][2].gagnant:
            self.gagnant_global = self.grille_global[grille_coord[0]][0].gagnant
            return True, self.grille_global[grille_coord[0]][0].gagnant

        if grille_index in [0, 2, 4, 6, 8]:
            if self.grille_global[0][0].gagnant == self.grille_global[1][1].gagnant == self.grille_global[2][2].gagnant:
                self.gagnant_global = self.grille_global[0][0].gagnant
                return True, self.grille_global[0][0].gagnant
            if self.grille_global[0][2].gagnant == self.grille_global[1][1].gagnant == self.grille_global[2][0].gagnant:
                self.gagnant_global = self.grille_global[0][2].gagnant
                return True, self.gagnant_global
        return False, None
    def get_petite_grille(self, grille):
        #grille=1,...,8
        #accéder à la petite grille
        coord_petite_grille=self.get_coords_grille(grille)
        return self.grille_global[coord_petite_grille[0]][coord_petite_grille[1]]

    def __repr__(self):
        output = f"GrilleGlobale (Gagnant: {self.gagnant_global if self.gagnant_global is not None else 'N/A'}):\n"

        # Affiche les petites grilles ligne par ligne, utilisant leur __repr__ ([X], [O], [ ])
        for i, row in enumerate(self.grille_global):
            # row contient 3 objets PetiteGrille
            row_str = " | ".join([repr(pg) for pg in row])
            output += f"{row_str}\n"
            if i < 2:
                output += "-------------------\n"
        return output.strip()

class Jeu():
    def __init__(self):
        self.plateau = GrilleGlobale()
        self.J1="X"
        self.J2="O"
        self.joueur_actuel = None
        self.grille_actuelle = None
        self.premier_coup=False
        self.grille_actuelle_index=None
        self.grille_gagne = []

    def get_coords(self,grille):
        #accéder à la petite grille
        ligne = grille // 3
        colonne = grille % 3
        return ligne,colonne

    def determiner_premier_joeur(self):
        self.joueur_actuel = choice([self.J1,self.J2])

    def changer_joueur(self):
        if self.joueur_actuel=="X":
            self.joueur_actuel="O"
        elif self.joueur_actuel=="O":
            self.joueur_actuel = "X"

    def est_coup_valide(self,grille,case):
        # L'argument 'grille' est l'index de la grille cliquée (0 à 8)

        # 1. Vérification de la grille ciblée (si elle est définie)
        if self.grille_actuelle_index is not None:
            if grille != self.grille_actuelle_index:
                # Si une grille est ciblée et que le coup n'est pas dans cette grille
                return False

        grille_visee = self.plateau.get_petite_grille(grille)

        # 2. Vérification si la petite grille est déjà gagnée/nulle
        # On ne peut pas jouer dans une petite grille déjà terminée.
        if grille_visee.gagnant is not None:
            return False

        # 3. Vérification si la case est déjà occupée
        case_visee = grille_visee.get_case(case)

        # 💡 CORRECTION CRITIQUE : case_visee est un objet Cellule, il faut vérifier sa valeur interne.
        if case_visee.valeur is not None:
            return False  # La case est déjà occupée

        return True

    #je ne verifier qu'il clique dans la bonne grille ca cela sera geré par l'interfce


    def jouer_coup_global(self,grille, case):
        # grille = 1,...,8
        # case = 1,...,8
        if self.joueur_actuel is None:
            self.determiner_premier_joeur()

        if self.est_coup_valide(grille,case)==False:
            return False

        petite_grille=self.plateau.get_petite_grille(grille)
        petite_grille.jouer_coup(case,self.joueur_actuel)
        if petite_grille.verifier_victoire(case):
            self.grille_gagne.append(grille)


        print("Test Cde")
        print(petite_grille)
        termine, gagnant = self.plateau.verifier_victoire_globale(grille)
        print(termine,gagnant)
        if termine:
            self.plateau.gagnant_global= gagnant
            return True

        prochaine_grille = self.plateau.get_petite_grille(case)

        #if prochaine_grille.gagnant==None and not prochaine_grille.est_plein():
        self.grille_actuelle= prochaine_grille
        self.grille_actuelle_index=case
        print(f"prochaine grille gagnat {prochaine_grille.gagnant}")


        if prochaine_grille.gagnant!=None: #la grille est deja pleine et/ou gagné donc le prochain pourra jouer n'importe ou
            #changer sinon ca va beuger avec la verificaiton des est valide
            self.grille_actuelle=None
            self.grille_actuelle_index = None

        self.changer_joueur()
        return True

    def get_etat_case(self,grille,case):
        grille = self.plateau.get_petite_grille(grille)
        ligne, colonne = self.get_coords(case)
        case=grille.grille[ligne][colonne]
        if case.valeur != None :
            return case.valeur
        else :
            return ""

    def __repr__(self):
        output = f"\n--- État Actuel du Jeu ---\n"
        output += f"Joueur Actuel: {self.joueur_actuel}\n"

        cible_index = self.grille_actuelle_index
        cible_texte = f"{cible_index} (Index 0-8)" if cible_index is not None else "LIBRE CHOIX"
        output += f"Grille Ciblée: {cible_texte}\n"

        output += f"--- Plateau Global ---\n"
        output += repr(self.plateau)  # Utilise la surcharge de GrilleGlobale
        return output











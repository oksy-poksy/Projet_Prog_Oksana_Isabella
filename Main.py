import tkinter as tk

"INTERFACE GRAPHIQUE"



# TODO: idée d'albin, mettre une fenetre supplementaire pour mettre les cinématiques des combats de pokemons


class PetitPlateau(tk.Frame):
    def __init__(self, parent, index_principal, controller_callback):
        """Configuration de la Frame (bordure visuelle)"""
        super().__init__(parent, borderwidth=2, relief="groove")
        self.index_principal = index_principal
        self.buttons = {}  # Stockage des 9 boutons cliquables sur les petites grilles

        """Création des 9 boutons clicables sur les petites grilles"""
        for row in range(3):
            for col in range(3):
                index_secondaire = row * 3 + col
            #note pour oksana (moi meme): essayer de trouver une autre méthode que LAMBDA
                bouton = tk.Button(self, text="", width=4, height=2,command=lambda i=index_secondaire: controller_callback(self.index_principal, i))
                bouton.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[index_secondaire] = bouton

        def mettre_a_jour_contenu(self, index_secondaire, contenu): # Mise à jour pour 'X', 'O', ou future Image de Pokémon.
            # TODO: Si 'contenu' est un objet Image, utiliser .config(image=...)
            self.buttons[index_secondaire].config(text=contenu)

        def mettre_en_evidence_next_grille(self, est_cible):
            """Change la couleur si c'est la grille où le joueur DOIT jouer"""
            color = "thistle" if est_cible else "plum"
            self.config(bg=color)




class GrandPlateau(tk.Frame):
    def __init__(self, parent, jeu_factice_instance):
        super().__init__(parent)
        self.jeu = jeu_factice_instance
        self.petits_plateaux = {}

        #Construction de la grille 3x3 de petits plateaux
        for row in range(3):
            for col in range(3):
                index_principal = row * 3 + col
                plateau = PetitPlateau(self, index_principal, self.gerer_plateau_click)
                plateau.grid(row=row, column=col, padx=5, pady=5)
                self.petits_plateaux[index_principal] = plateau

        # Ajout d'une zone pour l'info de jeu (tour, messages d'erreur)
        self.label_info = tk.Label(parent, text="Prêt à jouer!")
        self.label_info.pack(pady=10)

        self.rafraichir_affichage()

    def gerer_plateau_click(self, index_principal, index_secondaire):
        """prend le clic, le donne à la logique, et rafraîchit."""
        joueur = self.jeu.get_joueur_actuel()

        # TODO: Logique pour la phase Pokémon :
        # if self.pokemon_selectionne:
        #    result = self.jeu.tenter_coup(..., pokemon_selectionne)
        # else:
        result = self.jeu.tenter_coup_uttt(joueur, index_principal, index_secondaire)

        if result:
            self.rafraichir_affichage()
        else:
            self.label_info.config(text="Coup invalide. Réessayez.")

    def rafraichir_affichage(self):
        """Récupère l'état du jeu et met à jour tous les boutons/widgets"""
        grille_cible = self.jeu.get_grille_cible()

        for i_principal in range(9):
            # Mise à jour du contenu des cases
            for i_secondaire in range(9):
                contenu = self.jeu.get_etat_case(i_principal, i_secondaire)
                self.petits_plateaux[i_principal].mettre_a_jour_contenu(i_secondaire, contenu)

            # Mise à jour de la grille cible
            self.petits_plateaux[i_principal].mettre_en_evidence(i_principal == grille_cible)

        self.label_info.config(text=f"Tour du Joueur {self.jeu.get_joueur_actuel()}")



class DeroulementJeu:
    def __init__(self): pass
    def run_le_jeu(self): pass




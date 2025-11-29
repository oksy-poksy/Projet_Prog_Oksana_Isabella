import tkinter as tk
from tkinter import messagebox
from JeuFactice import JeuFactice


class UltimateTicTacToeGUI:

    def __init__(self, master):
        self.master = master
        master.title("Project 2026: UTTT X Pokémon")

        # Initialisation du jeu (utilise la classe JeuFactice pour le moment)
        self.jeu = JeuFactice()

        # Configuration de la fenêtre principale
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Conteneurs pour les différentes vues
        self.menu_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)

        # Affichage du menu initial
        self.show_menu()

    # --- 1. Menu d'Ouverture et Choix du Mode de Jeu ---
    def show_menu(self):
        """Affiche le menu de sélection du mode de jeu."""
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        tk.Label(self.menu_frame, text="Ultimate Tic-Tac-Toe X Pokémon", font=("Arial", 24, "bold")).pack(pady=30)

        # Sous-titre
        tk.Label(self.menu_frame, text="Choisissez votre mode de jeu", font=("Arial", 16)).pack(pady=10)

        # Bouton Joueur vs Joueur (Mode par défaut)
        tk.Button(self.menu_frame, text="▶️ Joueur vs Joueur", font=("Arial", 14),
                  command=lambda: self.start_game("JvsJ"),
                  width=30, height=2).pack(pady=10)

        # Bouton Joueur vs IA (Bonus 1/3)
        tk.Button(self.menu_frame, text="🤖 Joueur vs IA (", font=("Arial", 14),
                  command=lambda: self.start_game("JvsIA"),
                  width=30, height=2).pack(pady=10)

        # Bouton IA vs IA (Bonus 3/3)
        tk.Button(self.menu_frame, text="⚔️ IA vs IA (Visualisation)", font=("Arial", 14),
                  command=lambda: self.start_game("IAvsIA"),
                  width=30, height=2).pack(pady=10)

        # Bouton Quitter
        tk.Button(self.menu_frame, text="❌ Quitter", font=("Arial", 14), command=self.master.quit,
                  width=30, height=2).pack(pady=20)

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné."""
        messagebox.showinfo("Mode Sélectionné", f"Démarrage du jeu en mode: {mode}")
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.show_game_interface()

    # --- 2. Grille de Jeu et Éléments Nécessaires ---
    def show_game_interface(self):
        """Configure et affiche l'interface principale du jeu."""
        self.game_frame.pack(fill="both", expand=True)

        # Configuration du layout de la zone de jeu (3 colonnes: Info | Grille | Sidebar/Pokemon)
        self.game_frame.grid_columnconfigure(0, weight=1)  # Colonne infos/score
        self.game_frame.grid_columnconfigure(1, weight=3)  # Colonne Grille UTTT
        self.game_frame.grid_columnconfigure(2, weight=2)  # Colonne Sidebar/Pokémon
        self.game_frame.grid_rowconfigure(0, weight=1)

        # --- A. Colonne d'Informations et Score (Gauche) ---
        info_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.create_info_panel(info_frame)

        # --- B. Grille de Jeu Ultimate Tic-Tac-Toe (Centre) ---
        uttt_frame = tk.Frame(self.game_frame, bg="#A8A8A8", bd=5, relief=tk.SUNKEN)
        uttt_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.create_uttt_grid(uttt_frame)

        # --- C. Sidebar/Panneau Pokémon (Droite) ---
        sidebar_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.create_pokemon_sidebar(sidebar_frame)

        # Mise à jour initiale de l'interface
        self.update_game_state()

    # --- A. Détails du Panneau d'Informations ---
    def create_info_panel(self, parent_frame):
        """Crée les labels d'affichage des informations et du score."""
        tk.Label(parent_frame, text="📊 Informations de Jeu 📊", font=("Arial", 14, "bold")).pack(pady=10)

        # Affichage du joueur actuel
        self.current_player_var = tk.StringVar(value="Joueur Actuel: ")
        tk.Label(parent_frame, textvariable=self.current_player_var, font=("Arial", 12)).pack(pady=5)

        # Affichage de la grille ciblée
        self.target_grid_var = tk.StringVar(value="Grille Ciblée: Aucune")
        tk.Label(parent_frame, textvariable=self.target_grid_var, font=("Arial", 12, "italic")).pack(pady=5)

        # Affichage du Score (simple pour l'exemple)
        tk.Label(parent_frame, text="Score (UTTT Win):", font=("Arial", 12, "underline")).pack(pady=15)
        self.score_j1_var = tk.StringVar(value="Joueur 1 (O): 0")
        tk.Label(parent_frame, textvariable=self.score_j1_var, font=("Arial", 12)).pack()
        self.score_j2_var = tk.StringVar(value="Joueur 2 (X): 0")
        tk.Label(parent_frame, textvariable=self.score_j2_var, font=("Arial", 12)).pack()

        # Bouton de retour au menu
        tk.Button(parent_frame, text="Retour Menu", command=self.show_menu).pack(pady=20)

    # --- B. Détails de la Grille UTTT ---
    def create_uttt_grid(self, parent_frame):
        """Crée la grille 3x3 de 9 petites grilles."""
        # Stockage des boutons pour pouvoir les mettre à jour
        self.buttons = {}

        for i_p in range(3):  # Index Ligne Grille Principale
            for j_p in range(3):  # Index Colonne Grille Principale
                # Création de la petite grille (PetiteGrille Frame)
                small_grid_frame = tk.Frame(parent_frame, bd=1, relief=tk.RIDGE, bg="#DDDDDD")
                # Coordonnées de la grille principale (0-8)
                principal_coords = i_p * 3 + j_p

                # Positionnement de la petite grille dans la grande grille
                small_grid_frame.grid(row=i_p, column=j_p, padx=3, pady=3, sticky="nsew")

                # Configuration des lignes/colonnes de la petite grille pour les boutons
                for r in range(3):
                    small_grid_frame.grid_rowconfigure(r, weight=1)
                for c in range(3): # <-- Ajout de la boucle pour définir 'c'
                    small_grid_frame.grid_columnconfigure(c, weight=1)

                # Création des 9 boutons pour cette petite grille
                self.buttons[principal_coords] = {}
                for i_s in range(3):  # Index Ligne Case Secondaire
                    for j_s in range(3):  # Index Colonne Case Secondaire
                        # Coordonnées de la case dans la petite grille (0-8)
                        secondary_coords = i_s * 3 + j_s

                        button_key = (principal_coords, secondary_coords)

                        # Bouton
                        btn = tk.Button(small_grid_frame, text="", font=("Arial", 10),
                                        width=2, height=1,
                                        command=lambda pc=principal_coords, sc=secondary_coords: self.handle_click(pc,sc))

                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn

    def handle_click(self, principal_coords, secondary_coords):
        """Gère le clic de l'utilisateur sur une case."""
        # ⚠️ C'est ici que vous ferez appel à votre logique de jeu (par exemple, self.jeu.jouer_coup(...))
        # Pour l'instant, c'est juste un affichage de test.
        try:
            current_player = self.jeu.get_joueur_actuel()

            # TODO: Vérifier si le joueur sélectionne un Pokémon
            # TODO: Appeler la méthode du jeu pour placer/défier

            print(f"Clic: Grille Principale {principal_coords}, Case {secondary_coords}")
            self.update_game_state()  # Rafraîchir l'affichage après le coup

        except Exception as e:
            # Utiliser la classe d'exception simulée si nécessaire
            messagebox.showerror("Erreur de Jeu", f"Coup invalide: {e}")

    # --- C. Détails de la Sidebar Pokémon ---
    def create_pokemon_sidebar(self, parent_frame):
        """Crée le panneau pour la sélection du Pokémon et le banc."""
        tk.Label(parent_frame, text="🔥 Banc de Pokémons 🔥", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(parent_frame, text="(Zone de Bonus 2/3 : Filtres Ergonomiques)", font=("Arial", 10, "italic")).pack(
            pady=5)

        # Conteneur pour le banc
        self.pokemon_list_frame = tk.Frame(parent_frame)
        self.pokemon_list_frame.pack(fill="both", expand=True, padx=5, pady=10)

        # Un exemple de zone de défilement (Scrollbar) pour les 60 Pokémons
        canvas = tk.Canvas(self.pokemon_list_frame)
        scrollbar = tk.Scrollbar(self.pokemon_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Liste de Pokémons (simulée)
        tk.Label(scrollable_frame, text="[Affichage des 60 Pokémons ici]", font=("Arial", 12)).pack(pady=5)
        # TODO: C'est ici qu'il faudra itérer sur self.jeu.get_banc_pokemons(current_player)

        # Exemple de bouton de sélection d'un Pokémon
        tk.Button(scrollable_frame, text="Choisir: Pikachu (Force 50)", bg="#FFD700").pack(fill="x", padx=10, pady=2)
        tk.Button(scrollable_frame, text="Choisir: Bulbizarre (Force 45)", bg="#90EE90").pack(fill="x", padx=10, pady=2)
        # ... autres Pokémons ...

    # --- 3. Mise à Jour de l'Interface ---
    def update_game_state(self):
        """Met à jour tous les éléments de l'interface en fonction de l'état du jeu."""

        # 1. Mise à jour des Infos/Score
        current_player = self.jeu.get_joueur_actuel()
        target_grid = self.jeu.get_grille_cible()

        self.current_player_var.set(f"Joueur Actuel: J{current_player} ({'O' if current_player == 1 else 'X'})")

        if target_grid is not None:
            self.target_grid_var.set(f"Grille Ciblée: {target_grid + 1}")  # +1 pour un affichage de 1 à 9
        else:
            self.target_grid_var.set("Grille Ciblée: Aucune (Libre)")

        # 2. Mise à jour de la Grille UTTT
        for principal_coords in range(9):
            for secondary_coords in range(9):
                button_key = (principal_coords, secondary_coords)

                # Utilisation de la méthode simulée
                etat_case = self.jeu.get_etat_case(principal_coords, secondary_coords)
                btn = self.buttons[principal_coords][secondary_coords]

                # Mise à jour du texte
                btn.config(text=etat_case)

                # Mise à jour de la couleur de fond pour la grille ciblée
                if target_grid is not None and principal_coords == target_grid:
                    btn.config(bg="#ADD8E6")  # Bleu clair pour la grille active
                else:
                    btn.config(bg="SystemButtonFace")  # Couleur par défaut


# --- Lancement de l'Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root)
    root.geometry("1000x700")
    root.mainloop()
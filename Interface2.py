import tkinter as tk
from tkinter import messagebox
# Importation de votre classe de jeu réelle/corrigée
from JeuTicTacToe import Tictactoe


class UltimateTicTacToeGUI:
    """Interface graphique pour Ultimate Tic-Tac-Toe X Pokémon."""

    def __init__(self, master):
        self.master = master
        master.title("Project 2026: UTTT X Pokémon")

        # Initialisation du jeu (Utilisation de Tictactoe qui a maintenant la logique d'état)
        self.jeu = Tictactoe()

        # Références aux frames pour l'astuce du carré (initialisation)
        self.uttt_frame = None
        self.center_container = None
        # ... (Le reste de votre __init__ reste inchangé) ...

        # Configuration de la fenêtre principale
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Conteneurs pour les différentes vues
        self.menu_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)

        # Affichage du menu initial
        self.show_menu()

    # --- Astuce Cruciale pour rendre un widget carré ---
    def make_square(self, event):
        """
        Gère l'événement de redimensionnement pour forcer le uttt_frame à rester carré.
        """
        if self.uttt_frame and self.center_container:
            if event:
                width = event.width
                height = event.height
            else:
                width = self.center_container.winfo_width()
                height = self.center_container.winfo_height()
                if width <= 1 and height <= 1:
                    return

            min_dim = min(width, height)

            self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=min_dim, height=min_dim)

    # --- 1. Menu d'Ouverture et Choix du Mode de Jeu ---
    # ... (show_menu reste inchangé) ...
    def show_menu(self):
        """Affiche le menu de sélection du mode de jeu."""
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        tk.Label(self.menu_frame, text="Ultimate Tic-Tac-Toe X Pokémon", font=("Arial", 24, "bold")).pack(pady=30)

        # Sous-titre
        tk.Label(self.menu_frame, text="Choisissez votre mode de jeu", font=("Arial", 16)).pack(pady=10)

        # Bouton Joueur vs Joueur (Mode par défaut)
        tk.Button(self.menu_frame, text="▶️ Joueur vs Joueur (JvJ)", font=("Arial", 14),
                  command=lambda: self.start_game("JvJ"),
                  width=30, height=2).pack(pady=10)

        # Bouton Joueur vs IA (Bonus 1/3)
        tk.Button(self.menu_frame, text="🤖 Joueur vs IA (Aléatoire)", font=("Arial", 14),
                  command=lambda: self.start_game("JvIA"),
                  width=30, height=2).pack(pady=10)

        # Bouton IA vs IA (Bonus 3/3)
        tk.Button(self.menu_frame, text="⚔️ IA vs IA (Visualisation)", font=("Arial", 14),
                  command=lambda: self.start_game("IAvIA"),
                  width=30, height=2).pack(pady=10)

        # Bouton Quitter
        tk.Button(self.menu_frame, text="❌ Quitter", font=("Arial", 14), command=self.master.quit,
                  width=30, height=2).pack(pady=20)

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné. (Fenêtre de confirmation SUPPRIMÉE)"""
        # --- Ligne retirée: messagebox.showinfo("Mode Sélectionné", f"Démarrage du jeu en mode: {mode}")
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.show_game_interface()

    # --- 2. Grille de Jeu et Éléments Nécessaires (Grille Carrée) ---
    def show_game_interface(self):
        """Configure et affiche l'interface principale du jeu."""
        self.game_frame.pack(fill="both", expand=True)

        # Configuration du layout de la zone de jeu (3 colonnes: Info | Grille | Sidebar/Pokemon)
        # Poids ajustés pour recentrer et laisser de la place à la grille: 1 | 5 | 2
        self.game_frame.grid_columnconfigure(0, weight=1)  # Colonne infos/score
        self.game_frame.grid_columnconfigure(1, weight=5)  # Colonne Grille UTTT (dominante)
        self.game_frame.grid_columnconfigure(2, weight=2)  # Colonne Sidebar/Pokémon
        self.game_frame.grid_rowconfigure(0, weight=1)

        # --- A. Colonne d'Informations et Score (Gauche) ---
        info_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.create_info_panel(info_frame)

        # --- B. Grille de Jeu Ultimate Tic-Tac-Toe (Centre) ---
        self.center_container = tk.Frame(self.game_frame)
        self.center_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        self.uttt_frame = tk.Frame(self.center_container, bg="#A8A8A8", bd=5, relief=tk.SUNKEN)

        self.create_uttt_grid(self.uttt_frame)

        # Astuce Carrée
        self.center_container.bind("<Configure>", self.make_square)
        self.master.after(100, lambda: self.make_square(None))

        # --- C. Sidebar/Panneau Pokémon (Droite) ---
        sidebar_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.create_pokemon_sidebar(sidebar_frame)

        self.update_game_state()

    # --- A. Détails du Panneau d'Informations ---
    def create_info_panel(self, parent_frame):
        # ... (Inchangé) ...
        tk.Label(parent_frame, text="📊 Informations de Jeu 📊", font=("Arial", 14, "bold")).pack(pady=10)

        self.current_player_var = tk.StringVar(value="Joueur Actuel: ")
        tk.Label(parent_frame, textvariable=self.current_player_var, font=("Arial", 12)).pack(pady=5)

        self.target_grid_var = tk.StringVar(value="Grille Ciblée: Aucune")
        tk.Label(parent_frame, textvariable=self.target_grid_var, font=("Arial", 12, "italic")).pack(pady=5)

        tk.Label(parent_frame, text="Score (UTTT Win):", font=("Arial", 12, "underline")).pack(pady=15)
        self.score_j1_var = tk.StringVar(value="Joueur 1 (O): 0")
        tk.Label(parent_frame, textvariable=self.score_j1_var, font=("Arial", 12)).pack()
        self.score_j2_var = tk.StringVar(value="Joueur 2 (X): 0")
        tk.Label(parent_frame, textvariable=self.score_j2_var, font=("Arial", 12)).pack()

        tk.Button(parent_frame, text="Retour Menu", command=self.show_menu).pack(pady=20)

    # --- B. Détails de la Grille UTTT (Taille des boutons augmentée pour mieux utiliser l'espace) ---
    def create_uttt_grid(self, parent_frame):
        """Crée la grille 3x3 de 9 petites grilles."""
        self.buttons = {}

        for i in range(3):
            parent_frame.grid_rowconfigure(i, weight=1)
            parent_frame.grid_columnconfigure(i, weight=1)

        for i_p in range(3):
            for j_p in range(3):
                small_grid_frame = tk.Frame(parent_frame, bd=1, relief=tk.RIDGE, bg="#DDDDDD")
                principal_coords = i_p * 3 + j_p

                small_grid_frame.grid(row=i_p, column=j_p, padx=3, pady=3, sticky="nsew")

                for r in range(3):
                    small_grid_frame.grid_rowconfigure(r, weight=1)
                for c in range(3):
                    small_grid_frame.grid_columnconfigure(c, weight=1)

                self.buttons[principal_coords] = {}
                for i_s in range(3):
                    for j_s in range(3):
                        secondary_coords = i_s * 3 + j_s

                        # Augmentation de la taille de la police pour mieux occuper l'espace carré
                        btn = tk.Button(small_grid_frame, text="", font=("Arial", 18, "bold"),
                                        command=lambda pc=principal_coords, sc=secondary_coords: self.handle_click(pc,
                                                                                                                   sc))

                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn

    def handle_click(self, principal_coords, secondary_coords):
        """Gère le clic de l'utilisateur sur une case."""
        try:
            # 💡 Appel de la nouvelle fonction de simulation du jeu
            if self.jeu.jouer_coup_simule(principal_coords, secondary_coords):
                self.update_game_state()  # Rafraîchir l'affichage seulement si le coup est valide
            else:
                messagebox.showerror("Coup Invalide",
                                     "La case est déjà occupée ou vous n'êtes pas dans la bonne grille.")

        except Exception as e:
            messagebox.showerror("Erreur de Jeu", f"Erreur lors du coup: {e}")

    # --- C. Détails de la Sidebar Pokémon (Inchangé) ---
    def create_pokemon_sidebar(self, parent_frame):
        """Crée le panneau pour la sélection du Pokémon et le banc."""
        tk.Label(parent_frame, text="🔥 Banc de Pokémons 🔥", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(parent_frame, text="(Zone de Bonus 2/3 : Filtres Ergonomiques)", font=("Arial", 10, "italic")).pack(
            pady=5)

        self.pokemon_list_frame = tk.Frame(parent_frame)
        self.pokemon_list_frame.pack(fill="both", expand=True, padx=5, pady=10)

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

        tk.Label(scrollable_frame, text="[Affichage des 60 Pokémons ici]", font=("Arial", 12)).pack(pady=5)
        tk.Button(scrollable_frame, text="Choisir: Pikachu (Force 50)", bg="#FFD700").pack(fill="x", padx=10, pady=2)
        tk.Button(scrollable_frame, text="Choisir: Bulbizarre (Force 45)", bg="#90EE90").pack(fill="x", padx=10, pady=2)

    # --- 3. Mise à Jour de l'Interface ---
    def update_game_state(self):
        """Met à jour tous les éléments de l'interface en fonction de l'état du jeu."""

        # 1. Mise à jour des Infos/Score
        current_player_signe = self.jeu.get_joueur_actuel_signe()  # Utilise la nouvelle méthode
        target_grid = self.jeu.get_grille_cible()

        self.current_player_var.set(f"Joueur Actuel: ({current_player_signe})")

        if target_grid is not None:
            self.target_grid_var.set(f"Grille Ciblée: {target_grid + 1}")
        else:
            self.target_grid_var.set("Grille Ciblée: Aucune (Libre)")

        # Le score reste à 0 tant que la vraie logique n'est pas codée.

        # 2. Mise à jour de la Grille UTTT
        for principal_coords in range(9):
            for secondary_coords in range(9):
                # Utilisation de la méthode corrigée/simulée du jeu
                etat_case = self.jeu.get_etat_case(principal_coords, secondary_coords)
                btn = self.buttons[principal_coords][secondary_coords]

                btn.config(text=etat_case)

                # Mise à jour de la couleur de fond pour la grille ciblée
                if target_grid is not None and principal_coords == target_grid:
                    btn.config(bg="#ADD8E6")  # Bleu clair pour la grille active
                elif etat_case != "":
                    btn.config(bg="#F0F0F0")  # Case jouée
                else:
                    btn.config(bg="SystemButtonFace")  # Couleur par défaut


# --- Lancement de l'Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root)
    root.geometry("1000x700")
    root.mainloop()

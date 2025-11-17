import tkinter as tk
from tkinter import messagebox
# Importez votre classe de jeu corrigée (Tictactoe) qui gère l'état
# Assurez-vous que le nom du fichier est correct : JeuTicTacToeCorrige
from JeuTicTacToeCorrige import Tictactoe
import pandas as pd

class UltimateTicTacToeGUI:

    def __init__(self, master):
        # Initialisation principale
        self.master = master
        master.title("Project 2026: UTTT X Pokémon")

        # --- 💡 CHARGEMENT DES DONNÉES POKÉMON ---
        try:
            # Nous trions par l'ID numérique (#) et prenons les 30 premiers
            self.df_pokemons = pd.read_csv("pokemon (1).csv")
            # Filtrer les 30 Pokémons "les plus connus" (par ID #)
            # On retire les méga-évolutions et les doublons pour une liste plus propre
            self.df_populaires = self.df_pokemons[~self.df_pokemons['Name'].str.contains('Mega|Forme', na=False)] \
                .drop_duplicates(subset=['Name']).head(30)

            # Stocker les noms et Totals pour l'affichage
            self.pokemons_populaires = self.df_populaires[['Name', 'Total']].values.tolist()

        except FileNotFoundError:
            messagebox.showerror("Erreur de Fichier",
                                 "Le fichier 'pokemon (1).csv' est introuvable. Veuillez le placer au bon endroit.")
            self.pokemons_populaires = []
        # --- FIN CHARGEMENT DES DONNÉES ---


        self.jeu = Tictactoe()

        # Variables pour l'astuce de la grille carrée
        self.uttt_frame = None
        self.center_container = None
        self.mode_de_jeu = None

        # Configuration de la fenêtre principale
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Conteneurs pour les différentes vues
        self.menu_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)

        # Affichage du menu initial
        self.show_menu()


    def make_square(self, event=None):
        """
        Gère l'événement de redimensionnement pour forcer le uttt_frame à rester carré.
        """
        if self.uttt_frame and self.center_container:
            # Récupère la taille du conteneur parent (center_container)
            if event:
                width = event.width
                height = event.height
            else:
                width = self.center_container.winfo_width()
                height = self.center_container.winfo_height()
                if width <= 1 and height <= 1:
                    return

            # Détermine la plus petite dimension disponible
            min_dim = min(width, height)

            # Place le uttt_frame au centre avec la taille carrée (min_dim x min_dim)
            self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=min_dim, height=min_dim)

    # --- 1. Menu d'Ouverture et Choix du Mode de Jeu ---
    def show_menu(self):
        """Affiche le menu de sélection du mode de jeu."""
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        tk.Label(self.menu_frame, text="Ultimate Tic-Tac-Toe X Pokémon", font=("Arial", 24, "bold")).pack(pady=30)

        # Sous-titre
        tk.Label(self.menu_frame, text="Choisissez votre mode de jeu", font=("Arial", 16)).pack(pady=10)

        # Boutons
        tk.Button(self.menu_frame, text="▶️ Joueur vs Joueur", font=("Arial", 14),
                  command=lambda: self.start_game("JvsJ"),
                  width=30, height=2).pack(pady=10)
        tk.Button(self.menu_frame, text="🤖 Joueur vs IA", font=("Arial", 14),
                  command=lambda: self.start_game("JvsIA"),
                  width=30, height=2).pack(pady=10)
        tk.Button(self.menu_frame, text="⚔️ IA vs IA (Visualisation)", font=("Arial", 14),
                  command=lambda: self.start_game("IAvsIA"),
                  width=30, height=2).pack(pady=10)

        # Bouton Quitter
        tk.Button(self.menu_frame, text="❌ Quitter", font=("Arial", 14), command=self.master.quit,
                  width=30, height=2).pack(pady=20)

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné. (Message de confirmation supprimé)"""
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.show_game_interface()

    # --- 2. Grille de Jeu et Éléments Nécessaires ---
    def show_game_interface(self):
        """Configure et affiche l'interface principale du jeu."""
        self.game_frame.pack(fill="both", expand=True)

        # Configuration du layout (Info:1 | Grille:5 | Sidebar:2)
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=5)  # Grille UTTT prend plus d'espace
        self.game_frame.grid_columnconfigure(2, weight=2)
        self.game_frame.grid_rowconfigure(0, weight=1)

        # --- A. Colonne d'Informations et Score (Gauche) ---
        info_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.create_info_panel(info_frame)

        # --- B. Grille de Jeu Ultimate Tic-Tac-Toe (Centre) ---
        # Conteneur central (pour le centrage et la dimension carrée)
        self.center_container = tk.Frame(self.game_frame)
        self.center_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        # La grille UTTT réelle, qui sera dimensionnée par 'place'
        self.uttt_frame = tk.Frame(self.center_container, bg="#A8A8A8", bd=5, relief=tk.SUNKEN)
        self.create_uttt_grid(self.uttt_frame)

        # CLÉ DE LA GRILLE CARRÉE
        self.center_container.bind("<Configure>", self.make_square)
        self.master.after(100, self.make_square)  # Appel initial

        # --- C. Sidebar/Panneau Pokémon (Droite) ---
        sidebar_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.create_pokemon_sidebar(sidebar_frame) # L'appel fonctionne maintenant

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

        # Affichage du Score
        tk.Label(parent_frame, text="Score (UTTT Win):", font=("Arial", 12, "underline")).pack(pady=15)
        self.score_j1_var = tk.StringVar(value=f"Joueur 1 ({self.jeu.J1}): 0")
        tk.Label(parent_frame, textvariable=self.score_j1_var, font=("Arial", 12)).pack()
        self.score_j2_var = tk.StringVar(value=f"Joueur 2 ({self.jeu.J2}): 0")
        tk.Label(parent_frame, textvariable=self.score_j2_var, font=("Arial", 12)).pack()

        # Bouton de retour au menu
        tk.Button(parent_frame, text="Retour Menu", command=self.show_menu).pack(pady=20)

    # --- B. Détails de la Grille UTTT ---
    def create_uttt_grid(self, parent_frame):
        """Crée la grille 3x3 de 9 petites grilles."""
        self.buttons = {}

        # Configuration des poids pour le uttt_frame
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
            # 💡 CLÉ : Appel de la méthode de simulation du jeu
            if self.jeu.jouer_coup_simule(principal_coords, secondary_coords):
                self.update_game_state()  # Rafraîchir l'affichage seulement si le coup est valide
            else:
                # Fournir une meilleure information en cas de coup invalide
                if self.jeu.get_etat_case(principal_coords, secondary_coords) != "":
                    msg = "La case est déjà occupée."
                elif self.jeu.get_grille_cible() is not None:
                    msg = f"Vous devez jouer dans la Grille {self.jeu.get_grille_cible() + 1}."
                else:
                    msg = "Coup invalide."

                messagebox.showerror("Coup Invalide", msg)


        except Exception as e:
            messagebox.showerror("Erreur de Jeu", f"Erreur critique: {e}")

    # --- C. Détails de la Sidebar Pokémon ---
    # 💡 CORRECTION : La méthode est maintenant correctement indentée au niveau de la classe
    def create_pokemon_sidebar(self, parent_frame):
        """Crée le panneau pour la sélection du Pokémon et le banc."""
        tk.Label(parent_frame, text="🔥 Banc de Pokémons 🔥", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(parent_frame, text="30 Pokémons populaires :", font=("Arial", 10, "italic")).pack(pady=5)

        # Conteneur pour le banc
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

        # 💡 AFFICHAGE DYNAMIQUE DES POKÉMONS (Utilisation de self.pokemons_populaires)
        if self.pokemons_populaires:
            for name, total in self.pokemons_populaires:
                # Création d'un bouton pour chaque Pokémon
                tk.Button(
                    scrollable_frame,
                    text=f"{name} (Force: {total})",
                    # TODO: Ajouter la commande pour sélectionner ce Pokémon lors d'un clic
                    command=lambda p_name=name: print(f"Sélectionné: {p_name}")
                ).pack(fill="x", padx=10, pady=2)
        else:
            tk.Label(scrollable_frame, text="Impossible de charger la liste des Pokémons.", fg="red").pack(pady=5)

    # --- 3. Mise à Jour de l'Interface ---
    def update_game_state(self):
        """Met à jour tous les éléments de l'interface en fonction de l'état du jeu."""

        # 1. Mise à jour des Infos
        current_player_signe = self.jeu.get_joueur_actuel_signe()
        target_grid = self.jeu.get_grille_cible()

        self.current_player_var.set(f"Joueur Actuel: ({current_player_signe})")

        if target_grid is not None:
            self.target_grid_var.set(f"Grille Ciblée: {target_grid + 1}")
        else:
            self.target_grid_var.set("Grille Ciblée: Aucune (Libre)")

        # 2. Mise à jour de la Grille UTTT
        for principal_coords in range(9):
            for secondary_coords in range(9):

                etat_case = self.jeu.get_etat_case(principal_coords, secondary_coords)
                btn = self.buttons[principal_coords][secondary_coords]

                btn.config(text=etat_case)

                # Mise à jour de la couleur de fond pour la grille ciblée
                if target_grid is not None and principal_coords == target_grid:
                    btn.config(bg="#ADD8E6")  # Bleu clair (cible)
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
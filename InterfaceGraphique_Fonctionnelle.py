import tkinter as tk
from tkinter import messagebox
# Importez votre classe de jeu corrigée (Tictactoe) qui gère l'état
from JeuTicTacToeCorrige import Jeu
import pandas as pd


class UltimateTicTacToeGUI:

    def __init__(self, master):
        self.master = master
        master.title("Project 2026: UTTT X Pokémon")

        try: # Tente de charger et filtrer les Pokémons ____________________________ REMPLACER AVEC LE CODE D'ALBIN
            self.df_pokemons = pd.read_csv("pokemon (1).csv")
            self.df_populaires = self.df_pokemons[~self.df_pokemons['Name'].str.contains('Mega|Forme', na=False)] \
                .drop_duplicates(subset=['Name']).head(30)
            self.pokemons_populaires = self.df_populaires[['Name', 'Total']].values.tolist()
        except FileNotFoundError:
            messagebox.showwarning("Fichier Manquant","Le fichier 'pokemon (1).csv' est introuvable. Le panneau Pokémon sera vide.")
            self.pokemons_populaires = []

        self.jeu = Jeu()

        # Variables pour le layout
        self.uttt_frame = None
        self.center_container = None
        self.mode_de_jeu = None

        # Variables pour l'affichage des informations
        self.current_player_var = None
        self.target_grid_var = None
        self.info_panel_target_var = None
        self.score_j1_var = None
        self.score_j2_var = None
        self.buttons = {}

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.menu_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)

        self.show_menu()


    def show_menu(self):
        self.game_frame.pack_forget()

        for widget in self.game_frame.winfo_children(): # Nettoyer l'ancienne interface de jeu
            widget.destroy()

        self.buttons = {} # Réinitialiser les variables de la grille
        self.uttt_frame = None
        self.center_container = None

        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.menu_frame, text="ULTIMATE TIC TAC TOE", font=("Arial", 24, "bold")).pack(pady=30)
        tk.Label(self.menu_frame, text="Choisissez votre mode de jeu", font=("Arial", 16)).pack(pady=10)
        # Boutons
        tk.Button(self.menu_frame, text="Joueur vs Joueur (Classique UTTT)", font=("Arial", 14), command=lambda: self.start_game("JvsJ"), width=40, height=2, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.menu_frame, text="Joueur vs Joueur (Pokémon)", font=("Arial", 14), command=lambda: self.start_game("JvsJ_PKMN"),width=40, height=2, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.menu_frame, text="Joueur vs IA", font=("Arial", 14),command=lambda: self.start_game("JvsIA"),width=40, height=2, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.menu_frame, text="IA vs IA (Visualisation)", font=("Arial", 14),command=lambda: self.start_game("IAvsIA"),width=40, height=2, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.menu_frame, text="Quitter", font=("Arial", 14), command=self.master.quit,width=40, height=2, bg="#FA8072").pack(pady=20)

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné."""
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.jeu = Jeu() # Réinitialiser la simulation de jeu

        if mode == "JvsJ":
            self.show_classic_game_interface()
        else:
            self.show_game_interface()

    def show_game_interface(self):
        self.game_frame.pack(fill="both", expand=True)

        # Configuration du layout (Info:1 | Grille:5 | Sidebar:2)
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=5)
        self.game_frame.grid_columnconfigure(2, weight=2)
        self.game_frame.grid_rowconfigure(0, weight=1)

        # --- A. Colonne d'Informations et Score (Gauche) ---
        info_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.create_info_panel_standard(info_frame)

        # --- B. Grille de Jeu Ultimate Tic-Tac-Toe (Centre, Taille Fixe pour la maquette) ---
        self.center_container = tk.Frame(self.game_frame)
        self.center_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        self.uttt_frame = tk.Frame(self.center_container, bg="#A8A8A8", bd=5, relief=tk.SUNKEN, width=600, height=600)
        self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.uttt_frame.grid_propagate(False)  # Empêcher la grille de changer de taille

        self.create_uttt_grid(self.uttt_frame, font_size=18)
        sidebar_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.create_pokemon_sidebar(sidebar_frame)

        #self.update_game_state()

    def show_classic_game_interface(self):
        """
        Configure et affiche l'interface pour le mode Joueur vs Joueur classique (Layout Corrigé).
        Layout: [Global Info]
                [Info J1 | Grille UTTT Grande et Fixe | Info J2]
        """
        self.game_frame.pack(fill="both", expand=True)
        self.game_frame.config(bg="#FFFFFF")  # Fond blanc uniforme
        self.game_frame.grid_rowconfigure(0, weight=0, minsize=80)
        self.game_frame.grid_rowconfigure(1, weight=1)

        self.game_frame.grid_columnconfigure(0, weight=1, minsize=180)  # J1
        self.game_frame.grid_columnconfigure(1, weight=5)  # Grille
        self.game_frame.grid_columnconfigure(2, weight=1, minsize=180)  # J2

        # Infos Globales au-dessus de la Grille
        global_info_frame = tk.Frame(self.game_frame, bg="#E0FFFF", bd=2, relief=tk.RAISED)  # Bleu clair
        global_info_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.create_global_info_classic(global_info_frame)

        # Panneau J1
        info_j1_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_j1_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.create_player_info_panel_classic(info_j1_frame, "Joueur 1", self.jeu.J1, is_left_panel=True)

        # Grille de Jeu
        self.center_container = tk.Frame(self.game_frame, bg="#FFFFFF")
        self.center_container.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        self.uttt_frame = tk.Frame(self.center_container, bg="#A8A8A8", bd=5, relief=tk.SUNKEN, width=700, height=700)
        self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.uttt_frame.grid_propagate(False)

        self.create_uttt_grid(self.uttt_frame, font_size=28)

        # Panneau J2
        info_j2_frame = tk.Frame(self.game_frame, bd=2, relief=tk.GROOVE)
        info_j2_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        self.create_player_info_panel_classic(info_j2_frame, "Joueur 2", self.jeu.J2, is_left_panel=False)

        # Ajout du bouton de retour au menu sur le panneau de gauche
        tk.Button(info_j1_frame, text="Retour Menu", command=self.show_menu).pack(pady=20, fill="x", side="bottom")

        #self.update_game_state()

    # --- NOUVELLE MÉTHODE : Panneau d'Infos Globales (Mode Classique) ---
    def create_global_info_classic(self, parent_frame):
        """Crée le panneau d'affichage des infos de jeu centrales (Joueur Actuel et Grille Ciblée)."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)

        # Joueur Actuel
        self.current_player_var = tk.StringVar(value="Joueur Actuel: ")
        tk.Label(parent_frame, textvariable=self.current_player_var,
                 font=("Arial", 16, "bold"), bg="#E0FFFF").grid(row=0, column=0, padx=20, pady=5, sticky="e")

        # Grille Ciblée
        self.info_panel_target_var = tk.StringVar(value="Grille Ciblée: Aucune")
        tk.Label(parent_frame, textvariable=self.info_panel_target_var,
                 font=("Arial", 14, "italic"), bg="#E0FFFF").grid(row=0, column=1, padx=20, pady=5, sticky="w")

    # --- A. Détails du Panneau d'Informations (Classique - JvsJ) ---
    def create_player_info_panel_classic(self, parent_frame, player_label, player_sign, is_left_panel):
        """Crée un panneau d'informations simplifié pour un seul joueur (mode JvsJ classique)."""

        inner_frame = tk.Frame(parent_frame)
        inner_frame.pack(expand=True, anchor=tk.CENTER)

        tk.Label(inner_frame, text=f" {player_label} ({player_sign})", font=("Arial", 18, "bold")).pack(pady=20)

        # Les variables current_player_var et info_panel_target_var sont maintenant gérées par create_global_info_classic.

        # Affichage du Score
        tk.Label(inner_frame, text="Score (UTTT Win):", font=("Arial", 14, "underline")).pack(pady=20)

        if is_left_panel:
            self.score_j1_var = tk.StringVar(value=f"{player_sign}: 0")
            tk.Label(inner_frame, textvariable=self.score_j1_var, font=("Arial", 14)).pack()
        else:
            self.score_j2_var = tk.StringVar(value=f"{player_sign}: 0")
            tk.Label(inner_frame, textvariable=self.score_j2_var, font=("Arial", 14)).pack()

    def create_uttt_grid(self, parent_frame, font_size):
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

                        btn = tk.Button(small_grid_frame, text="", font=("Arial", 16, "bold"), command=lambda pc=principal_coords, sc=secondary_coords: self.handle_click(pc,sc), bd=1, relief=tk.FLAT)
                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn


    def update_game_state(self):
        #Mise à jour des Infos
        current_player_signe = self.jeu.joueur_actuel
        target_grid = self.jeu.grille_actuelle
        target_grid_coord= self.jeu.grille_actuelle_index

        if self.current_player_var:
            self.current_player_var.set(f"Joueur Actuel: ({current_player_signe})")

        target_text = f"Grille Ciblée: {target_grid_coord + 1}" if target_grid is not None else "Grille Ciblée: Aucune (Libre)"

        if self.mode_de_jeu == "JvsJ" and self.info_panel_target_var:
            self.info_panel_target_var.set(target_text)
        elif self.target_grid_var:
            self.target_grid_var.set(target_text)

        # 2. Mise à Jour de la Grille UTTT
        for principal_coords in range(9):
            for secondary_coords in range(9):

                if principal_coords in self.buttons and secondary_coords in self.buttons[principal_coords]:

                    etat_case = self.jeu.get_etat_case(principal_coords,secondary_coords)
                    btn = self.buttons[principal_coords][secondary_coords]

                    btn.config(text=etat_case)

                    # Mise à jour de la couleur de fond pour la grille ciblée et jouée
                    if target_grid is not None and principal_coords == target_grid_coord:
                        btn.config(bg="#ADD8E6")  # Bleu clair (cible)
                    # 💡 CORRECTION : Utilisation de la couleur de fond du bouton, pas du panneau, pour éviter l'expansion
                    elif etat_case !=None:
                        # Couleur pour les cases jouées (sans relief spécifique pour ne pas changer la taille)
                        bg_color = "#C0C0C0" if etat_case == self.jeu.J1 else "#D3D3D3"
                        btn.config(bg=bg_color,
                                   relief=tk.SUNKEN)  # Utilisation de SUNKEN pour un léger effet visuel sans déformer la grille
                    else:
                        btn.config(bg="SystemButtonFace", relief=tk.FLAT)  # Couleur par défaut et FLAT

    # --- C. Détails de la Sidebar Pokémon ---
    def create_pokemon_sidebar(self, parent_frame):
        """Crée le panneau pour la sélection du Pokémon et le banc."""
        tk.Label(parent_frame, text="🔥 Banc de Pokémons 🔥", font=("Arial", 14, "bold")).pack(pady=10)

        # Afficher la liste de Pokémons uniquement dans les modes qui en ont besoin
        if self.mode_de_jeu in ["JvsJ_PKMN", "JvsIA", "IAvsIA"]:
            tk.Label(parent_frame, text="30 Pokémons populaires :", font=("Arial", 10, "italic")).pack(pady=5)

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

            if self.pokemons_populaires:
                for name, total in self.pokemons_populaires:
                    tk.Button(
                        scrollable_frame,
                        text=f"{name} (Force: {total})",
                        command=lambda p_name=name: print(f"Sélectionné: {p_name}")
                    ).pack(fill="x", padx=10, pady=2)
            else:
                tk.Label(scrollable_frame,
                         text="Impossible de charger la liste des Pokémons. (Fichier pokemon (1).csv manquant)",
                         fg="red", wraplength=180).pack(pady=5)
        else:
            # Message pour le mode classique qui n'a pas de banc
            tk.Label(parent_frame, text="Ce mode de jeu n'utilise pas de Pokémons.", font=("Arial", 12)).pack(pady=20)

    def handle_click(self, principal_coords, secondary_coords):
        """Gère le clic de l'utilisateur sur une case (appelle la simulation de JeuTicTacToeCorrige)."""
        try:
            if self.jeu.jouer_coup_global(principal_coords, secondary_coords):

                self.update_game_state()

            else:

                if self.jeu.get_etat_case(principal_coords, secondary_coords) != None:
                    msg = "La case est déjà occupée."
                elif self.jeu.grille_actuelle is not None:
                    msg = f"Vous devez jouer dans la Grille {self.jeu.grille_actuelle_index + 1}."
                else:
                    msg = "Coup invalide."
                messagebox.showerror("Coup Invalide", msg)
        except Exception as e:
            messagebox.showerror("Erreur de Jeu", f"Erreur critique: {e}")

    # --- 4. Mise à Jour de l'Interface ---
    def update_game_state(self):
        """Met à jour tous les éléments de l'interface en fonction de l'état du jeu."""

        # 1. Mise à jour des Infos
        current_player_signe = self.jeu.joueur_actuel
        target_grid = self.jeu.grille_actuelle
        target_grid_coord=self.jeu.grille_actuelle_index
        print(current_player_signe)
        print(target_grid)
        print(target_grid_coord)

        if self.current_player_var:
            self.current_player_var.set(f"Joueur Actuel: ({current_player_signe})")

        target_text = f"Grille Ciblée: {target_grid_coord+ 1}" if target_grid is not None else "Grille Ciblée: Aucune (Libre)"

        if self.mode_de_jeu == "JvsJ" and self.info_panel_target_var:
            self.info_panel_target_var.set(target_text)
        elif self.target_grid_var:
            self.target_grid_var.set(target_text)

        # 2. Mise à jour de la Grille UTTT
        for principal_coords in range(9):
            for secondary_coords in range(9):

                if principal_coords in self.buttons and secondary_coords in self.buttons[principal_coords]:

                    etat_case = self.jeu.get_etat_case(principal_coords, secondary_coords)

                    btn = self.buttons[principal_coords][secondary_coords]

                    btn.config(text=etat_case)

                    # Mise à jour de la couleur de fond pour la grille ciblée
                    if target_grid is not None and principal_coords == target_grid:
                        btn.config(bg="#ADD8E6")  # Bleu clair (cible)
                    elif etat_case != None:
                        # Couleur pour les cases jouées
                        bg_color = "#C0C0C0" if etat_case == self.jeu.J1 else "#D3D3D3"
                        btn.config(bg=bg_color)
                    else:
                        btn.config(bg="SystemButtonFace")  # Couleur par défaut



if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.state('zoomed') # Tente d'utiliser 'zoomed' (Windows/X11) pour maximiser en laissant la barre des tâches
    except tk.TclError:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

    app = UltimateTicTacToeGUI(root)
    root.mainloop()



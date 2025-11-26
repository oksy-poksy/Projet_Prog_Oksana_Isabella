import tkinter as tk
from tkinter import messagebox
from JeuTicTacToeCorrige import Jeu
import pandas as pd
from PIL import Image, ImageTk #TENTATIVE


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
        self.menu_frame.pack_forget()
        self.game_frame.pack_forget()

        # Réinitialisation des poids du gestionnaire grid sur les conteneurs parents
        self.master.grid_columnconfigure(0, weight=0, minsize=0)
        self.master.grid_rowconfigure(0, weight=0, minsize=0)

        for i in range(3):
            self.game_frame.grid_columnconfigure(i, weight=0, minsize=0)
        for j in range(2):
            self.game_frame.grid_rowconfigure(j, weight=0, minsize=0)

        # Destruction des widgets enfants pour le nettoyage
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Réinitialisation des variables de jeu
        self.buttons = {}
        self.uttt_frame = None
        self.center_container = None

        image_path = "Menu_Image_Rogne.jpg"

        background_label = None
        try:
            original_image = Image.open(image_path)
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            resized_image = original_image.resize((width, height))

            # Affectation à la variable d'instance pour éviter la suppression
            self.bg_image = ImageTk.PhotoImage(resized_image)

            # Placement du Label de fond
            background_label = tk.Label(self.menu_frame, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        except FileNotFoundError:
            messagebox.showwarning("Erreur Image",
                                   f"Le fichier image '{image_path}' est introuvable. Fond gris utilisé.")
            self.bg_image = None
        except Exception as e:
            messagebox.showwarning("Erreur Image", f"Erreur lors du chargement de l'image : {e}")
            self.bg_image = None

        self.menu_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # If we have a background image, draw title/subtitle on a Canvas so there is no white box behind text
        if background_label is not None and hasattr(self, 'bg_image') and self.bg_image is not None:
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.menu_canvas = tk.Canvas(self.menu_frame, width=width, height=height, highlightthickness=0)
            self.menu_canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
            self.menu_canvas.pack(fill='both', expand=True)

            # Title and subtitle drawn on canvas (no opaque background)
            self.menu_canvas.create_text(width/2, 80, text="ULTIMATE TIC TAC TOE", font=("Arial", 24, "bold"), fill='white')
            self.menu_canvas.create_text(width/2, 120, text="Choisissez votre mode de jeu", font=("Arial", 16), fill='white')

            # Create buttons as normal widgets but placed on the canvas so they float above the image
            btn_w = 400
            btn_h = 48
            start_y = 250
            gap = 70

            b1 = tk.Button(self.menu_canvas, text="Joueur vs Joueur (Classique UTTT)", font=("Arial", 14), command=lambda: self.start_game("JvsJ"), bg="#FFA07A")
            self.menu_canvas.create_window(width/2, start_y + 0*gap, window=b1, width=btn_w, height=btn_h)
            b2 = tk.Button(self.menu_canvas, text="Joueur vs Joueur (Pokémon)", font=("Arial", 14), command=lambda: self.start_game("JvsJ_PKMN"), bg="#FFA07A")
            self.menu_canvas.create_window(width/2, start_y + 1*gap, window=b2, width=btn_w, height=btn_h)
            b3 = tk.Button(self.menu_canvas, text="Joueur vs IA", font=("Arial", 14), command=lambda: self.start_game("JvsIA"), bg="#FFA07A")
            self.menu_canvas.create_window(width/2, start_y + 2*gap, window=b3, width=btn_w, height=btn_h)
            b4 = tk.Button(self.menu_canvas, text="IA vs IA (Visualisation)", font=("Arial", 14), command=lambda: self.start_game("IAvsIA"), bg="#FFA07A")
            self.menu_canvas.create_window(width/2, start_y + 3*gap, window=b4, width=btn_w, height=btn_h)

            bq = tk.Button(self.menu_canvas, text="Quitter", font=("Arial", 14), command=self.master.quit, bg="#FA8072")
            self.menu_canvas.create_window(width/2, start_y + 4*gap + 60, window=bq, width=btn_w, height=btn_h)
        else:
            # fallback when no background image: use regular widgets
            container_for_widgets = self.menu_frame
            tk.Label(container_for_widgets, text="ULTIMATE TIC TAC TOE", font=("Arial", 24, "bold"), fg='red').pack(pady=30)
            tk.Label(container_for_widgets, text="Choisissez votre mode de jeu", font=("Arial", 16), fg='red').pack(pady=10)

            # Boutons
            tk.Button(container_for_widgets, text="Joueur vs Joueur (Classique UTTT)", font=("Arial", 14), command=lambda: self.start_game("JvsJ"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Joueur vs Joueur (Pokémon)", font=("Arial", 14), command=lambda: self.start_game("JvsJ_PKMN"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Joueur vs IA", font=("Arial", 14), command=lambda: self.start_game("JvsIA"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="IA vs IA (Visualisation)", font=("Arial", 14), command=lambda: self.start_game("IAvsIA"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Quitter", font=("Arial", 14), command=self.master.quit, width=40, height=2, bg="#FA8072").pack(pady=120)

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné."""
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.jeu = Jeu() # Réinitialiser la simulation de jeu
        # Utiliser l'interface classique (fond et layout UTTT) pour tous les modes
        self.show_classic_game_interface()

    def show_game_interface(self):
        self.game_frame.pack(fill="both", expand=True)

        # Configuration du layout (Info:1 | Grille:5 | Sidebar:2)
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=5)
        self.game_frame.grid_columnconfigure(2, weight=2)
        self.game_frame.grid_rowconfigure(0, weight=1)

        # --- A. Colonne d'Informations et Score (Gauche) ---
        info_frame = tk.Frame(self.game_frame, bd=0, relief=tk.FLAT)
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

        self.update_game_state()

    def show_classic_game_interface(self):

        self.game_frame.pack(fill="both", expand=True)

        # --- 1. Charger et Placer l'Image de Fond sur un Canvas ---
        game_bg_image_path = "prairie_horizontale.jpg"
        try:
            original_game_image = Image.open(game_bg_image_path)
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            resized_game_image = original_game_image.resize((width, height), Image.LANCZOS)
            self.game_bg_photo = ImageTk.PhotoImage(resized_game_image)

            # Utiliser un Canvas pour dessiner l'image de fond et le texte par-dessus
            self.main_game_canvas = tk.Canvas(self.game_frame, width=width, height=height, highlightthickness=0)
            self.main_game_canvas.create_image(0, 0, image=self.game_bg_photo, anchor='nw')
            self.main_game_canvas.pack(fill="both", expand=True)

            # Créer des textes sur le Canvas (pas de fond opaque)
            self.canvas_current_text_id = self.main_game_canvas.create_text(width/2, 28, text="", font=("Arial", 14, "bold"), fill="black")
            self.canvas_target_text_id = self.main_game_canvas.create_text(width/2 + 260, 28, text="", font=("Arial", 12, "italic"), fill="black")

            # Textes joueurs gauche/droite (initialement vides)
            self.canvas_j1_id = self.main_game_canvas.create_text(width*0.12, height/2, text="", font=("Arial", 14), fill="black", anchor='n')
            self.canvas_j2_id = self.main_game_canvas.create_text(width*0.88, height/2, text="", font=("Arial", 14), fill="black", anchor='n')

            # Créer et placer la zone centrale (grille) en tant que widget sur le Canvas
            self.center_container = tk.Frame(self.main_game_canvas)
            # Définir la taille de la fenêtre contenant la grille
            center_w, center_h = 700, 700
            center_x, center_y = width/2, height/2
            self.main_game_canvas.create_window(center_x, center_y, window=self.center_container, width=center_w, height=center_h)

            # Grille UTTT (gardée comme Frame pour conserver la logique actuelle)
            self.uttt_frame = tk.Frame(self.center_container, bg="light sky blue", bd=5, relief=tk.SUNKEN, width=center_w, height=center_h)
            self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.uttt_frame.grid_propagate(False)
            self.create_uttt_grid(self.uttt_frame, font_size=28)

            # Bouton Retour Menu : petit bouton placé sur le Canvas (en bas à gauche)
            self.return_button = tk.Button(self.main_game_canvas, text="Retour Menu", font=("Arial", 14) , command=self.show_menu, bg="sea green", fg="white")
            self.main_game_canvas.create_window(width*0.12, height-110, window=self.return_button, width=160, height=36)

        except FileNotFoundError:
            messagebox.showwarning("Erreur Image", f"Le fichier image '{game_bg_image_path}' est introuvable. Fond bleu clair utilisé.")
            return
        except Exception as e:
            messagebox.showwarning("Erreur Image", f"Erreur critique lors du chargement de l'image : {e}")
            return

        self.update_game_state() # Mettre à jour l'affichage initial


    def create_global_info_classic(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)

        # Joueur Actuel
        self.current_player_var = tk.StringVar(value="Joueur Actuel: ")
        tk.Label(parent_frame, textvariable=self.current_player_var, font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="e")

        # Grille Ciblée
        self.info_panel_target_var = tk.StringVar(value="Grille Ciblée: Aucune")
        tk.Label(parent_frame, textvariable=self.info_panel_target_var, font=("Arial", 14, "italic")).grid(row=0, column=1, padx=20, pady=5, sticky="w")

    #étails du Panneau d'Informations (Classique - JvsJ)
    def create_player_info_panel_classic(self, parent_frame, player_label, player_sign, is_left_panel):
        inner_frame = tk.Frame(parent_frame)
        inner_frame.pack(expand=True, anchor=tk.CENTER)

        tk.Label(inner_frame, text=f" {player_label} ({player_sign})", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(inner_frame, text="Score (UTTT Win):", font=("Arial", 14, "underline")).pack(pady=20)

        if is_left_panel:
            self.score_j1_var = tk.StringVar(value=f"{player_sign}: 0")
            tk.Label(inner_frame, textvariable=self.score_j1_var, font=("Arial", 14)).pack()
        else:
            self.score_j2_var = tk.StringVar(value=f"{player_sign}: 0")
            tk.Label(inner_frame, textvariable=self.score_j2_var, font=("Arial", 14)).pack()

    def create_uttt_grid(self, parent_frame, font_size):
        self.buttons = {}

        self.small_grid_frames = {}
        for i in range(3):
            parent_frame.grid_rowconfigure(i, weight=1)
            parent_frame.grid_columnconfigure(i, weight=1)

        for i in range(3):
            parent_frame.grid_rowconfigure(i, weight=1)
            parent_frame.grid_columnconfigure(i, weight=1)

        for i_p in range(3):
            for j_p in range(3):
                small_grid_frame = tk.Frame(parent_frame, bd=3, relief=tk.RIDGE, bg="white")
                principal_coords = i_p * 3 + j_p
                self.small_grid_frames[principal_coords] = small_grid_frame

                small_grid_frame.grid(row=i_p, column=j_p, padx=3, pady=3, sticky="nsew")

                for r in range(3):
                    small_grid_frame.grid_rowconfigure(r, weight=1)
                for c in range(3):
                    small_grid_frame.grid_columnconfigure(c, weight=1)

                self.buttons[principal_coords] = {}
                for i_s in range(3):
                    for j_s in range(3):
                        secondary_coords = i_s * 3 + j_s
                        btn = tk.Button(small_grid_frame, text="", font=("Arial",font_size), command=lambda pc=principal_coords, sc=secondary_coords: self.handle_click(pc,sc),bg="white", bd=1, relief=tk.SUNKEN, width=1, height=1)
                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn


    def handle_click(self, principal_coords, secondary_coords):
        """Gère le clic de l'utilisateur sur une case """
        try:
            if self.jeu.jouer_coup_global(principal_coords, secondary_coords):
                self.update_game_state()

            else:
                if self.jeu.get_etat_case(principal_coords, secondary_coords) != "":
                    msg = "La case est déjà occupée."
                if self.jeu.grille_actuelle != self.jeu.plateau.get_petite_grille(principal_coords):
                    msg = f"Vous devez jouer dans la Grille {self.jeu.grille_actuelle_index + 1}."
                else:
                    msg = "Coup invalide."
                messagebox.showerror("Coup Invalide", msg)
        except Exception as e:
            messagebox.showerror("Erreur de Jeu", f"Erreur critique: {e}")

    def update_game_state(self):
        current_player_signe = self.jeu.joueur_actuel
        #target_grid = self.jeu.grille_actuelle
        target_grid_index = self.jeu.grille_actuelle_index
        #print("target_grid", target_grid)


        if self.current_player_var:
            self.current_player_var.set(f"Joueur Actuel: ({current_player_signe})")

        target_text = f"Grille Ciblée: {target_grid_index + 1}" if target_grid_index is not None else "Grille Ciblée: Aucune (Libre)"

        if self.mode_de_jeu == "JvsJ" and self.info_panel_target_var:
            self.info_panel_target_var.set(target_text)
        elif self.target_grid_var:
            self.target_grid_var.set(target_text)
        # --- Mise à jour des textes sur le Canvas (inchangé) ---
        target_text = f"Grille Ciblée: {target_grid_index + 1}" if target_grid_index is not None else "Grille Ciblée: Aucune (Libre)"

        if hasattr(self, 'main_game_canvas'):
            try:
                current_text = f"Joueur Actuel: ({current_player_signe})"
                self.main_game_canvas.itemconfig(self.canvas_current_text_id, text=current_text)
                self.main_game_canvas.itemconfig(self.canvas_target_text_id, text=target_text)

                j1_score = self.score_j1_var.get() if self.score_j1_var else f"{self.jeu.J1}: 0"
                j2_score = self.score_j2_var.get() if self.score_j2_var else f"{self.jeu.J2}: 0"
                j1_text = f"Joueur 1 ({self.jeu.J1})\n\nScore:\n{j1_score}"
                j2_text = f"Joueur 2 ({self.jeu.J2})\n\nScore:\n{j2_score}"

                if j1_text:
                    self.main_game_canvas.itemconfig(self.canvas_j1_id, text=j1_text)
                if j2_text:
                    self.main_game_canvas.itemconfig(self.canvas_j2_id, text=j2_text)
            except Exception:
                pass

        # --- Mise à Jour de la Grille UTTT et de la Surbrillance ---
        for principal_coords in range(9):

            if principal_coords in self.small_grid_frames:
                frame = self.small_grid_frames[principal_coords]

                # 1. État par défaut: Blanc, Cadre RIDGE normal
                frame.config(bg="light sky blue", bd=3, relief=tk.RIDGE)

                if target_grid_index is None:
                    # 2. Libre Choix: Surligner toutes les grilles non gagnées en Light Sky Blue
                    petite_grille = self.jeu.plateau.get_petite_grille(principal_coords)
                    if petite_grille.gagnant is None:
                        frame.config(bg="light sky blue", bd=4, relief=tk.RIDGE)

                elif principal_coords == target_grid_index:
                    # 3. Grille Ciblée : Light Sky Blue et Cadre NOIR (avant l'astuce highlightbackground)
                    frame.config(bg="black", bd=3, relief=tk.RAISED, highlightbackground="black", highlightcolor="black")

            # --- Gestion des cases individuelles (boutons) ---
            for secondary_coords in range(9):

                if principal_coords in self.buttons and secondary_coords in self.buttons[principal_coords]:

                    etat_case = self.jeu.get_etat_case(principal_coords, secondary_coords)
                    btn = self.buttons[principal_coords][secondary_coords]

                    btn.config(text=etat_case)

                    if target_grid_index is not None and principal_coords == target_grid_index:
                        # Case dans la grille ciblée : Fond Light Sky Blue, relief FLAT
                        btn.config(bg="light sky blue", relief=tk.FLAT, fg="black")

                    elif etat_case != "":
                        # Case jouée (X ou O)
                        bg_color = "#C0C0C0" if etat_case == self.jeu.J1 else "#D3D3D3"
                        btn.config(bg=bg_color, relief=tk.SUNKEN)
                    else:
                        # État par défaut (Non jouée, non ciblée) : Blanc
                        btn.config(bg="white", relief=tk.FLAT)



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
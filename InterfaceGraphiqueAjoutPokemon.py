import tkinter as tk
from tkinter import messagebox
from JeuTicTacToeCorrige import Jeu
import pandas as pds
from PIL import Image, ImageTk  # TENTATIVE
from random import choice, choices
import os
FILENAME = "images_pokemon"
import requests
from CraftInterfacepokemon import download_and_name_pokemon_images

class IAJoueur:

    def __init__(self, jeu, signe):
        self.jeu = jeu
        self.signe = signe

    def obtenir_coup_aleatoire(self):
        coups_valides = self.obtenir_coups_valides()

        if not coups_valides:
            return None

        return choice(coups_valides)

    def obtenir_coups_valides(self):
        coups_valides = []
        if self.jeu.grille_actuelle_index is not None: # Déterminer les grilles jouables
            grilles_jouables = [self.jeu.grille_actuelle_index] # Une grille est ciblée, on ne peut jouer que dans celle-ci
        else:
            grilles_jouables = []
            for i in range(9):
                petite_grille = self.jeu.plateau.get_petite_grille(i)
                if petite_grille.gagnant is None:
                    grilles_jouables.append(i)

        # Pour chaque grille jouable, trouver les cases libres
        for grille_index in grilles_jouables:
            petite_grille = self.jeu.plateau.get_petite_grille(grille_index)
            for case_index in range(9):
                case = petite_grille.get_case(case_index)
                if case.valeur is None:
                    coups_valides.append((grille_index, case_index)) # Si la case est vide, c'est un coup valide

        return coups_valides


class IAIntelligente(IAJoueur):
    """IA heuristique pour Ultimate Tic-Tac-Toe :
    - gagne la petite grille si possible
    - bloque l'adversaire si nécessaire
    - préfère envoyer l'adversaire dans une grille pleine/gagnée
    - sinon centre > coins > côtés
    """
    def __init__(self, jeu, signe):
        super().__init__(jeu, signe)
        # poids paramétrables, on mets des "recompences" à l'IA selon les differents goals qu'elle accomplit
        self.weights = {
            'penalize_full_target': 200, #quand une grosse case est remplie par l'adversaire, il perd 200 points
            'penalize_adv_win_target': 80,
            'center_bonus': 12,
            'corner_bonus': 6,
            'side_bonus': 2,
            'empty_cell_penalty': 2,
            'control_new_grid_bonus': 500,
            'global_win_bonus': 10000,
            'opponent_immediate_threat_penalty': 400,
        }

    def obtenir_coup_aleatoire(self):
        coups = self.obtenir_coups_valides()
        if not coups:
            return None

        adv = self.jeu.J1 if self.signe == self.jeu.J2 else self.jeu.J2

        # 1) Jouer victoire locale si possible
        for g, c in coups:
            if self._coup_gagne_petite_grille(g, c, self.signe):
                return (g, c)

        # 2) Bloquer victoire locale de l'adversaire, ne garder QUE les coups qui empêchent réellement la victoire
        for g, c in coups:
            if self._adversaire_peut_gagner_dans_grille(g, adv):
                # chercher les coups dans cette grille qui empêchent l'adversaire de gagner
                blocking_moves = [ (gg, cc) for gg, cc in coups if gg == g and not self._simule_coup_laisse_adversaire_gagner(gg, cc, adv) ]
                if blocking_moves:
                    return blocking_moves[0]

        # 3) Heuristique de scoring globale pour choisir le meilleur coup
        # Eviter d'envoyer l'adversaire vers une petite grille pleine/gagnée (qui lui donne un "choix libre")
        # Eviter d'envoyer l'adversaire vers une grille où il peut gagner immédiatement
        # Favoriser centre puis coins
        best = None
        best_score = -10_000
        for g, c in coups:
            score = 0
            cible = self.jeu.plateau.get_petite_grille(c)
            if (cible.gagnant is not None or cible.est_plein()) and self._adversaire_peut_gagner_dans_grille(c, adv): # Penaliser si le coup envoie l'adversaire vers une petite grille déjà terminée (libre choix)
                score -= self.weights['penalize_full_target']
            if self._adversaire_peut_gagner_dans_grille(c, adv): # Penaliser si l'adversaire peut gagner immédiatement dans la grille cible
                score -= self.weights['penalize_adv_win_target']
            if c == 4: # Petites préférences: centre > coins > sides
                score += self.weights['center_bonus']
            elif c in (0, 2, 6, 8):
                score += self.weights['corner_bonus']
            else:
                score += self.weights['side_bonus']
            if g == 4: # Bonus si le move se place dans le centre de la petite grille jouée (valeur positionnelle)
                score += 2

            empty_cells = sum(1 for i in range(9) if cible.get_case(i).valeur is None)  # Ne pénaliser les grilles très libres que si l'adversaire y a une menace
            if self._adversaire_peut_gagner_dans_grille(c, adv):
                score -= empty_cells * self.weights['empty_cell_penalty']
            if c == g:
                score += 3
            if self._simule_mouvement_gagne_globale(g, c, self.signe): # Bonus si le coup permet de gagner la grande grille
                score += self.weights['global_win_bonus']
            if self._opponent_has_immediate_threat(adv, simulate_move=(g, c)): # Pénaliser si, après notre coup, l'adversaire a une menace immédiate sur le tour suivant
                score -= self.weights['opponent_immediate_threat_penalty']
            if score > best_score:
                best_score = score
                best = (g, c)

        if best is not None:
            return best

        return choice(coups)

    def _coup_gagne_petite_grille(self, grille_index, case_index, signe):
        pg = self.jeu.plateau.get_petite_grille(grille_index)
        return self._existe_coup_gagnant(pg, case_index, signe)

    def _existe_coup_gagnant(self, petite_grille, case_index, signe):
        coords = petite_grille.get_coords(case_index)
        r, c = coords

        grid = [[cell.valeur for cell in row] for row in petite_grille.grille] # lecture rapide des valeurs
        grid[r][c] = signe

        for i in range(3): # lignes
            if grid[i][0] == grid[i][1] == grid[i][2] == signe:
                return True
        for j in range(3): # colonnes
            if grid[0][j] == grid[1][j] == grid[2][j] == signe:
                return True
        if grid[0][0] == grid[1][1] == grid[2][2] == signe: # diagonales
            return True
        if grid[0][2] == grid[1][1] == grid[2][0] == signe:
            return True
        return False

    def _adversaire_peut_gagner_dans_grille(self, grille_index, signe_adv):
        pg = self.jeu.plateau.get_petite_grille(grille_index)
        for case_index in range(9):
            if pg.get_case(case_index).valeur is None:
                if self._existe_coup_gagnant(pg, case_index, signe_adv):
                    return True
        return False

    def _simule_coup_laisse_adversaire_gagner(self, grille_index, case_index, signe_adv):
        """Retourne True si, en jouant (grille_index, case_index) en notre faveur,
        l'adversaire aurait ensuite un coup gagnant dans la même petite grille.
        (utilisé pour vérifier si un coup bloque réellement).
        """
        pg = self.jeu.plateau.get_petite_grille(grille_index)
        cell = pg.get_case(case_index)
        if cell.valeur is not None:
            return True

        original = cell # Simuler le coup
        cell.valeur = self.signe
        try:
            for ci in range(9): # Vérifier si l'adversaire a maintenant une case gagnante
                if pg.get_case(ci).valeur is None:
                    if self._existe_coup_gagnant(pg, ci, signe_adv):
                        return True
            return False
        finally:
            cell.valeur = original # Revenir à l'état initial

    def _simule_mouvement_gagne_globale(self, grille_index, case_index, signe):
        """Simule brièvement le coup et renvoie True si cela cause une victoire globale."""
        plateau = self.jeu.plateau
        pg = plateau.get_petite_grille(grille_index)
        cell = pg.get_case(case_index)
        if cell.valeur is not None:
            return False

        original_val = cell.valeur
        original_gagnant = pg.gagnant
        try:
            cell.valeur = signe
            termine, gagnant = pg.verifier_victoire(case_index)
            if termine:
                pg.gagnant = gagnant
            # maintenant vérifier victoire globale sur cette grille
            termine_glob, gagnant_glob = plateau.verifier_victoire_globale(grille_index)
            return termine_glob
        finally:
            cell.valeur = original_val
            pg.gagnant = original_gagnant

    def _opponent_has_immediate_threat(self, signe_adv, simulate_move=None):
        """Retourne True si l'adversaire dispose d'un coup gagnant immédiat.
        Si simulate_move=(g,c) fourni, on simule d'abord ce coup.
        """
        # Simuler notre coup si demandé
        sim_cell = None
        sim_pg = None
        if simulate_move is not None:
            g, c = simulate_move
            sim_pg = self.jeu.plateau.get_petite_grille(g)
            sim_cell = sim_pg.get_case(c)
            if sim_cell.valeur is not None:
                sim_cell = None
            else:
                sim_cell.valeur = self.signe

        try:
            # construire une IA simple pour l'adversaire afin d'obtenir ses coups valides
            adv_ia = IAJoueur(self.jeu, signe_adv)
            adv_coups = adv_ia.obtenir_coups_valides()
            for gg, cc in adv_coups:
                pg = self.jeu.plateau.get_petite_grille(gg)
                if pg.get_case(cc).valeur is None:
                    if self._existe_coup_gagnant(pg, cc, signe_adv):
                        return True
                    # vérifier si ce coup mène à victoire globale
                    # on simule temporairement
                    cell = pg.get_case(cc)
                    orig = cell.valeur
                    orig_gagnant = pg.gagnant
                    try:
                        cell.valeur = signe_adv
                        termine, gagn = pg.verifier_victoire(cc)
                        if termine:
                            pg.gagnant = gagn
                        terme_glob, _ = self.jeu.plateau.verifier_victoire_globale(gg)
                        if terme_glob:
                            return True
                    finally:
                        cell.valeur = orig
                        pg.gagnant = orig_gagnant
            return False
        finally:
            if sim_cell is not None:
                sim_cell.valeur = None


class UltimateTicTacToeGUI:

    def __init__(self, master):
        self.master = master
        master.title("Project 2026: UTTT X Pokémon")

        try:  # Tente de charger et filtrer les Pokémons ____________________________ REMPLACER AVEC LE CODE D'ALBIN
            self.pokemons= self._obtenir_pokemon()
            self.pokemons_names = self.pokemons.index.values.tolist()
        except FileNotFoundError:
            messagebox.showwarning("Fichier Manquant",
                                   "Le fichier 'pokemon.csv' est introuvable. Le panneau Pokémon sera vide.")
            self.pokemons = []

        self.jeu = Jeu()

        # Variables pour le layout
        self.uttt_frame = None
        self.center_container = None
        self.mode_de_jeu = None

        # Variables pour l'IA
        self.ia_joueur = None
        self.humain_signe = None
        self.ia_mode = None
        self.ia_turn_pending = False

        #varaibe pour les pokémons
        self.pokemon_image_refs_j1 = []
        self.pokemon_image_refs_j2 = []
        self.current_pokemon=""
        self.placed_pokemon=dict()
        self.player_available_pokemon={"X":[],"Y":[]}
        self.game_phase_pokemon="" #3 phases : selection du pokemon, placement du pokemon, combat


        # Variables pour l'affichage des informations
        self.current_player_var = None
        self.target_grid_var = None
        self.info_panel_target_var = None
        self.score_j1_var = None
        self.score_j2_var = None
        self.buttons = {}
        self.small_grid_frames = {}
        self.grilles_gagnees = {}  # Track les grilles gagnées et leur gagnant
        self.winner_labels = {}
        self.gagnant_global = None  # Track le gagnant global

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.menu_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)

        self.show_menu()

    def show_menu(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack_forget()

        self.master.grid_columnconfigure(0, weight=0, minsize=0) # Réinitialisation des poids du gestionnaire grid sur les conteneurs parents
        self.master.grid_rowconfigure(0, weight=0, minsize=0)

        for i in range(3):
            self.game_frame.grid_columnconfigure(i, weight=0, minsize=0)
        for j in range(2):
            self.game_frame.grid_rowconfigure(j, weight=0, minsize=0)

        for widget in self.game_frame.winfo_children(): # Destruction des widgets enfants pour le nettoyage
            widget.destroy()
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        self.buttons = {} # Réinitialisation des variables de jeu
        self.uttt_frame = None
        self.center_container = None

        image_path = "Menu_Image_Rogne.jpg"

        background_label = None
        try:
            original_image = Image.open(image_path)
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            resized_image = original_image.resize((width, height))

            self.bg_image = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self.menu_frame, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        except FileNotFoundError:
            messagebox.showwarning("Erreur Image",f"Le fichier image '{image_path}' est introuvable. Fond gris utilisé.")
            self.bg_image = None
        except Exception as e:
            messagebox.showwarning("Erreur Image", f"Erreur lors du chargement de l'image : {e}")
            self.bg_image = None

        self.menu_frame.pack(fill="both", expand=True, padx=0, pady=0)

        if background_label is not None and hasattr(self, 'bg_image') and self.bg_image is not None:
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.menu_canvas = tk.Canvas(self.menu_frame, width=width, height=height, highlightthickness=0)
            self.menu_canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
            self.menu_canvas.pack(fill='both', expand=True)

            self.menu_canvas.create_text(width / 2, 80, text="ULTIMATE TIC TAC TOE", font=("Arial", 24, "bold"),fill='white')
            self.menu_canvas.create_text(width / 2, 120, text="Choisissez votre mode de jeu", font=("Arial", 16),fill='white')
            btn_w = 400
            btn_h = 48
            start_y = 250
            gap = 70

            b1 = tk.Button(self.menu_canvas, text="Joueur vs Joueur (Classique UTTT)", font=("Arial", 14),command=lambda: self.start_game("JvsJ"), bg="#FFA07A")
            self.menu_canvas.create_window(width / 2, start_y + 0 * gap, window=b1, width=btn_w, height=btn_h)
            b2 = tk.Button(self.menu_canvas, text="Joueur vs Joueur (Pokémon)", font=("Arial", 14),command=lambda: self.start_game("JvsJ_PKMN"), bg="#FFA07A")
            self.menu_canvas.create_window(width / 2, start_y + 1 * gap, window=b2, width=btn_w, height=btn_h)
            b3 = tk.Button(self.menu_canvas, text="Joueur vs IA (Aléatoire)", font=("Arial", 14),command=lambda: self.start_game("JvsIA_Aleatoire"), bg="#FFA07A")
            self.menu_canvas.create_window(width / 2, start_y + 2 * gap, window=b3, width=btn_w, height=btn_h)
            b3i = tk.Button(self.menu_canvas, text="Joueur vs IA (Intelligente)", font=("Arial", 14),command=lambda: self.start_game("JvsIA_Intelligente"), bg="#FFA07A")
            self.menu_canvas.create_window(width / 2, start_y + 3 * gap, window=b3i, width=btn_w, height=btn_h)
            b4 = tk.Button(self.menu_canvas, text="IA vs IA (Visualisation)", font=("Arial", 14),command=lambda: self.start_game("IAvsIA"), bg="#FFA07A")
            self.menu_canvas.create_window(width / 2, start_y + 4 * gap, window=b4, width=btn_w, height=btn_h)

            bq = tk.Button(self.menu_canvas, text="Quitter", font=("Arial", 14), command=self.master.quit, bg="#FA8072")
            self.menu_canvas.create_window(width / 2, start_y + 5 * gap + 60, window=bq, width=btn_w, height=btn_h)
        else:
            container_for_widgets = self.menu_frame
            tk.Label(container_for_widgets, text="ULTIMATE TIC TAC TOE", font=("Arial", 24, "bold"), fg='red').pack(pady=30)
            tk.Label(container_for_widgets, text="Choisissez votre mode de jeu", font=("Arial", 16), fg='red').pack(pady=10)

            # Boutons
            tk.Button(container_for_widgets, text="Joueur vs Joueur (Classique UTTT)", font=("Arial", 14),command=lambda: self.start_game("JvsJ"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Joueur vs Joueur (Pokémon)", font=("Arial", 14),command=lambda: self.start_game("JvsJ_PKMN"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Joueur vs IA (Aléatoire)", font=("Arial", 14),command=lambda: self.start_game("JvsIA_Aleatoire"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Joueur vs IA (Intelligente)", font=("Arial", 14),command=lambda: self.start_game("JvsIA_Intelligente"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="IA vs IA (Visualisation)", font=("Arial", 14),command=lambda: self.start_game("IAvsIA"), width=40, height=2, bg="#FFA07A").pack(pady=10)
            tk.Button(container_for_widgets, text="Quitter", font=("Arial", 14), command=self.master.quit, width=40,height=2, bg="#FA8072").pack(pady=120)

    def _obtenir_pokemon(self):
        df2 = pds.read_csv("Pokemon.csv", index_col="Name")
        df3 = df2[-df2["Type 1"].isin(
            ["Normal", "Flying", "Dragon", "Poison", "Ghost", "Fairy", "Fighting", "Ice", "Dark", "Steel", "Psychic",
             "Bug"])]

        return df3

    def start_game(self, mode):
        """Lance le jeu dans le mode sélectionné."""
        self.mode_de_jeu = mode
        self.menu_frame.pack_forget()
        self.jeu = Jeu()  # Réinitialiser la simulation de jeu
        self.grilles_gagnees = {}  # Réinitialiser le tracking des grilles gagnées
        self.gagnant_global = None  # Réinitialiser le gagnant global

        # Initialiser l'IA pour les modes JvsIA (aléatoire ou intelligente)
        self.ia_player1 = None
        self.ia_player2 = None
        self.ai_vs_ai_running = False

        if isinstance(mode, str) and mode.startswith("JvsJ_PKMN"):
            self.show_pokemon_interface()

        if isinstance(mode, str) and mode.startswith("JvsIA"):
            self.jeu.determiner_premier_joeur()
            # Le joueur humain prend le signe du premier joueur
            self.humain_signe = self.jeu.joueur_actuel
            ia_signe = self.jeu.J2 if self.humain_signe == self.jeu.J1 else self.jeu.J1
            # Créer l'IA demandée
            if mode == "JvsIA_Intelligente":
                self.ia_joueur = IAIntelligente(self.jeu, ia_signe)
                self.ia_mode = "intelligente"
            else:
                self.ia_joueur = IAJoueur(self.jeu, ia_signe)
                self.ia_mode = "aleatoire"
            self.ia_turn_pending = False

        elif mode == "IAvsIA":
            self.jeu.determiner_premier_joeur()
            # Assurer que J1 et J2 sont définis dans le moteur
            self.ia_player1 = IAIntelligente(self.jeu, self.jeu.J1)
            self.ia_player2 = IAJoueur(self.jeu, self.jeu.J2)
            self.ia_joueur = None
            self.ia_mode = "IAvsIA"
            self.ia_turn_pending = False
            self.ai_vs_ai_running = True

        else:
            self.ia_joueur = None
            self.ia_mode = None

        if mode == "JvsJ_PKMN":
            self.show_pokemon_interface()
            return

        self.show_classic_game_interface()
        if getattr(self, 'ai_vs_ai_running', False): # Si IA vs IA, lancer la boucle d'exécution automatisée
            # délai pour que l'interface soit rendue
            self.master.after(500, self.ia_vs_ia_step)

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

            # Créer des textes sur le Canvas
            self.canvas_current_text_id = self.main_game_canvas.create_text(width / 2, 18, text="",font=("Arial", 28, "bold"), fill="black")
            self.canvas_target_text_id = self.main_game_canvas.create_text(width / 2 + 500, 18, text="",font=("Arial", 20), fill="black")

            # Label indiquant quel contrôleur contrôle J1 / J2 (IA/Humain)
            self.canvas_ai_info_id = self.main_game_canvas.create_text(width / 2, 60, text="",font=("Arial", 24, "italic"), fill="darkblue")

            # Textes joueurs gauche/droite (initialement vides)
            self.canvas_j1_id = self.main_game_canvas.create_text(width * 0.12, height / 3, text="", font=("Arial", 26),fill="black", anchor='n')
            self.canvas_j2_id = self.main_game_canvas.create_text(width * 0.88, height / 3, text="", font=("Arial", 26),fill="black", anchor='n')

            # Créer et placer la zone centrale (grille) en tant que widget sur le Canvas
            self.center_container = tk.Frame(self.main_game_canvas)
            # Définir la taille de la fenêtre contenant la grille
            center_w, center_h = 700, 700
            center_x, center_y = width / 2, height / 2
            self.main_game_canvas.create_window(center_x, center_y, window=self.center_container, width=center_w,height=center_h)

            # Grille UTTT (gardée comme Frame pour conserver la logique actuelle)
            self.uttt_frame = tk.Frame(self.center_container, bg="light sky blue", bd=5, relief=tk.SUNKEN,width=center_w, height=center_h)
            self.uttt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.uttt_frame.grid_propagate(False)
            self.create_uttt_grid(self.uttt_frame, font_size=28)

            # Bouton Retour Menu : petit bouton placé sur le Canvas (en bas à gauche)
            self.return_button = tk.Button(self.main_game_canvas, text="Retour Menu", font=("Arial", 14),command=self.show_menu, bg="sea green", fg="white")
            self.main_game_canvas.create_window(width * 0.12, height - 135, window=self.return_button, width=160,height=36)

        except FileNotFoundError:
            messagebox.showwarning("Erreur Image",f"Le fichier image '{game_bg_image_path}' est introuvable. Fond bleu clair utilisé.")
            return
        except Exception as e:
            messagebox.showwarning("Erreur Image", f"Erreur critique lors du chargement de l'image : {e}")
            return

        self.update_game_state(self.main_game_canvas)  # Mettre à jour l'affichage initial

    def show_pokemon_interface(self):

        self.game_frame.pack(fill="both", expand=True)
        game_bg_image_path = "fond_ecran_pokemon.jpg"
        try:
            original_game_image = Image.open(game_bg_image_path)
            width, height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            resized_game_image_pokemon = original_game_image.resize((width, height), Image.LANCZOS)
            self.game_bg_photo_pokemon = ImageTk.PhotoImage(resized_game_image_pokemon)

            # Utiliser un Canvas pour dessiner l'image de fond et le texte par-dessus
            self.main_game_canvas = tk.Canvas(self.game_frame, width=width, height=height, highlightthickness=0)
            self.main_game_canvas.create_image(0, 0, image=self.game_bg_photo_pokemon, anchor='nw')
            self.main_game_canvas.pack(fill="both", expand=True)

            # Créer des textes sur le Canvas
            self.canvas_current_text_id = self.main_game_canvas.create_text(width / 2, 18, text="",font=("Arial", 28, "bold"), fill="black")
            self.canvas_target_text_id = self.main_game_canvas.create_text(width / 2 + 500, 18, text="",font=("Arial", 20), fill="black")

            # Textes joueurs gauche/droite (initialement vides)
            self.canvas_j1_id = self.main_game_canvas.create_text(width * 0.12, height / 3, text="", font=("Arial", 26),fill="black", anchor='n')
            self.canvas_j2_id = self.main_game_canvas.create_text(width * 0.88, height / 3, text="", font=("Arial", 26),fill="black", anchor='n')

            # Créer et placer la zone centrale (grille) en tant que widget sur le Canvas
            self.center_container = tk.Frame(self.main_game_canvas)
            # Définir la taille de la fenêtre contenant la grille
            center_w, center_h = 700, 700
            center_x, center_y = width / 2, height / 2
            self.main_game_canvas.create_window(center_x, center_y, window=self.center_container, width=center_w,height=center_h)

            # Grille UTTT (gardée comme Frame pour conserver la logique actuelle)
            self.uttt_frame_poke = tk.Frame(self.center_container, bg="light sky blue", bd=5, relief=tk.SUNKEN,width=center_w, height=center_h)
            self.uttt_frame_poke.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.uttt_frame_poke.grid_propagate(False)
            self.create_uttt_grid_pokemon(self.uttt_frame_poke, font_size=28)

            # Bouton Retour Menu : petit bouton placé sur le Canvas (en bas à gauche)
            self.return_button = tk.Button(self.main_game_canvas, text="Retour Menu", font=("Arial", 14),command=self.show_menu, bg="sea green", fg="white")
            self.main_game_canvas.create_window(width * 0.12, height - 135, window=self.return_button, width=160,height=36)

        except FileNotFoundError:
            messagebox.showwarning("Erreur Image",f"Le fichier image '{game_bg_image_path}' est introuvable. Fond bleu clair utilisé.")
            return
        except Exception as e:
            messagebox.showwarning("Erreur Image", f"Erreur critique lors du chargement de l'image : {e}")
            return

        """Affiche deux grilles de 10 Pokémons aléatoires (5x2) de chaque côté de la grille UTTT."""

        # 1. Préparation des variables et constantes
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()

        # Réinitialisation des références d'images
        self.pokemon_image_refs_j1 = []
        self.pokemon_image_refs_j2 = []

        if not os.path.exists(FILENAME):
            os.makedirs(FILENAME)


        # Sélectionne 20 Pokémon (avec répétition si la liste est courte)
        if len(self.pokemons_names) < 20:
            selected_pokemon = choices(self.pokemons_names, k=20)
        else:
            selected_pokemon = choices(self.pokemons_names, k=20)

        poke_j1_names = selected_pokemon[:10]
        poke_j2_names = selected_pokemon[10:]

        # 3. Définition de la mise en page des grilles
        grid_width, grid_height = 250, 650  # Taille de chaque grille
        cols, rows = 2, 5

        # Positions centrées verticalement et décalées horizontalement
        center_x_j1 = width * 0.12  # Gauche
        center_x_j2 = width * 0.88  # Droite
        center_y = height / 2

        # --- Fonction interne pour créer une grille de Pokémon ---
        def create_pokemon_grid(canvas, x, y, frame_w, frame_h, pokemon_names_list, image_ref_list):

            grid_frame = tk.Frame(canvas, bg="#F0F8FF", bd=3, relief=tk.GROOVE)  # Fond bleu très clair
            #canvas.create_window(x, y, window=grid_frame, width=frame_w, height=frame_h, anchor=tk.CENTER)

            poke_w, poke_h = 90, 90

            for i, pokemon in enumerate(pokemon_names_list):
                try:
                    # Tente de télécharger l'image (si elle n'existe pas)
                    #download_and_name_pokemon_images(pokemon)

                    row = i // cols
                    col = i % cols

                    # Nettoyage du nom pour trouver le fichier local (identique à la fonction de téléchargement)
                    cleaned_name = pokemon.replace(' ', '_').replace('.', '')
                    image_poke_path = os.path.join(FILENAME, f"{cleaned_name}.png")

                    if not os.path.exists(image_poke_path):
                        pokeball = "pokeball.png"
                        image_poke_path = os.path.join(FILENAME, pokeball)


                    poke_image_original = Image.open(image_poke_path)
                    resized_image = poke_image_original.resize((poke_w, poke_h))
                    poke_image_tk = ImageTk.PhotoImage(resized_image)

                    # Stocker la référence pour empêcher le garbage collector
                    image_ref_list.append(poke_image_tk)

                    # Créer le Label avec l'image et le nom en dessous
                    poke_but = tk.Button(grid_frame,image=poke_image_tk,text=pokemon,compound=tk.TOP,font=("Webgdings", 10),bg="#F0F8FF")
                    poke_but.config(command=lambda p=pokemon,b=poke_but: self.select_pokemon(p, self.jeu.joueur_actuel,b))


                    poke_but.image = poke_image_tk #essentiel maitenant les images s'affichent !!!
                    poke_but.text = pokemon
                    poke_but.grid(row=row, column=col, padx=0, pady=0)

                    # Configurer les poids des lignes/colonnes
                    grid_frame.grid_columnconfigure(col, weight=1)
                    grid_frame.grid_rowconfigure(row, weight=1)

                except Exception as e:
                    # En cas d'erreur de chargement ou autre, afficher un placeholder
                    print(f"Erreur d'affichage/téléchargement pour {pokemon}: {e}")
                    row, col = i // cols, i % cols
                    tk.Label(grid_frame, text=f"{pokemon} (Erreur)", font=("Arial", 10), bg="red").grid(row=row,
                                                                                                        column=col,
                                                                                                        padx=2, pady=2,
                                                                                                        sticky="nsew")
            canvas.create_window(x, y, window=grid_frame, width=frame_w, height=frame_h, anchor=tk.CENTER)

        # 4. Création des deux grilles sur le canvas principal
        try:
            # Grille J1 (Gauche)
            create_pokemon_grid(self.main_game_canvas, center_x_j1, center_y, grid_width, grid_height, poke_j1_names,
                                self.pokemon_image_refs_j1)

            # Grille J2 (Droite)
            create_pokemon_grid(self.main_game_canvas, center_x_j2, center_y, grid_width, grid_height, poke_j2_names,
                                self.pokemon_image_refs_j2)

        except Exception as e:
            messagebox.showwarning("Erreur Pokémon Interface",
                                   f"Erreur critique lors de la création des grilles : {e}. Les grilles ne s'afficheront pas.")
            return
        self.update_game_state(self.main_game_canvas)  # Mettre à jour l'affichage initial

    def jouer_coup_ia(self):
        """Exécute le coup de l'IA"""
        if not self.ia_joueur:
            self.ia_turn_pending = False
            return

        try:
            # Obtenir un coup aléatoire
            coup = self.ia_joueur.obtenir_coup_aleatoire()

            if coup is None:
                messagebox.showerror("Erreur IA", "Aucun coup valide disponible!")
                self.ia_turn_pending = False
                return

            grille_index, case_index = coup

            # Jouer le coup
            if self.jeu.jouer_coup_global(grille_index, case_index):
                # Vérifier si une grille a été gagnée après ce coup
                petite_grille = self.jeu.plateau.get_petite_grille(grille_index)
                if petite_grille.gagnant is not None:
                    self.grilles_gagnees[grille_index] = petite_grille.gagnant

                # Vérifier si le jeu global est terminé
                    if self.jeu.plateau.gagnant_global is not None:
                        # Mettre à jour l'état de l'UI d'abord, puis afficher la dialogue de victoire
                        self.gagnant_global = self.jeu.plateau.gagnant_global
                        self.update_game_state(self.main_game_canvas)
                        # Laisser le temps au canvas de se rafraîchir avant la messagebox
                        self.master.after(180, lambda g=self.gagnant_global: messagebox.showinfo("Partie Terminée", f"Joueur {g} a remporté le match !"))
                    else:
                        self.update_game_state(self.main_game_canvas)

            self.ia_turn_pending = False
        except Exception as e:
            messagebox.showerror("Erreur IA", f"Erreur lors du coup de l'IA: {e}")
            self.ia_turn_pending = False

    def ia_vs_ia_step(self):
        """Une étape de la boucle IA vs IA : joue le coup de l'IA dont c'est le tour, met à jour, et programme l'étape suivante."""
        if not getattr(self, 'ai_vs_ai_running', False):
            return

        # Sécurité : s'arrêter si partie terminée
        if self.jeu.plateau.gagnant_global is not None:
            self.ai_vs_ai_running = False
            return

        current = self.jeu.joueur_actuel
        # Choisir quelle IA doit jouer selon le signe du joueur actuel
        if current == self.ia_player1.signe:
            ai = self.ia_player1
        else:
            ai = self.ia_player2

        try:
            coup = ai.obtenir_coup_aleatoire()
            if coup is None:
                self.ai_vs_ai_running = False
                return

            grille_index, case_index = coup
            played = self.jeu.jouer_coup_global(grille_index, case_index)
            if played:
                petite_grille = self.jeu.plateau.get_petite_grille(grille_index)
                if petite_grille.gagnant is not None:
                    self.grilles_gagnees[grille_index] = petite_grille.gagnant

                if self.jeu.plateau.gagnant_global is not None:
                    self.gagnant_global = self.jeu.plateau.gagnant_global
                    self.update_game_state(self.main_game_canvas)
                    self.master.after(180, lambda g=self.gagnant_global: messagebox.showinfo("Partie Terminée", f"Joueur {g} a remporté le match !"))
                else:
                    self.update_game_state(self.main_game_canvas)

            # Programmer le prochain coup
            if self.jeu.plateau.gagnant_global is None:
                self.master.after(300, self.ia_vs_ia_step)
            else:
                self.ai_vs_ai_running = False

        except Exception as e:
            messagebox.showerror("Erreur IA", f"Erreur durant IA vs IA: {e}")
            self.ai_vs_ai_running = False

    def create_global_info_classic(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)

        # Joueur Actuel
        self.current_player_var = tk.StringVar(value="Joueur Actuel: ")
        tk.Label(parent_frame, textvariable=self.current_player_var, font=("Arial", 18, "bold")).grid(row=0, column=0,
                                                                                                      padx=20, pady=5,
                                                                                                      sticky="e")

        # Grille Ciblée
        self.info_panel_target_var = tk.StringVar(value="Grille Ciblée: Aucune")
        tk.Label(parent_frame, textvariable=self.info_panel_target_var, font=("Arial", 16, "italic")).grid(row=0,
                                                           column=1,
                                                           padx=20,
                                                           pady=5,
                                                           sticky="w")

    # étails du Panneau d'Informations (Classique - JvsJ)
    def create_player_info_panel_classic(self, parent_frame, player_label, player_sign, is_left_panel):
        inner_frame = tk.Frame(parent_frame)
        inner_frame.pack(expand=True, anchor=tk.CENTER)

        tk.Label(inner_frame, text=f" {player_label} ({player_sign})", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(inner_frame, text="Score (UTTT Win):", font=("Arial", 16, "underline")).pack(pady=20)

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
                        btn = tk.Button(small_grid_frame, text="", font=("Arial", font_size),
                                        command=lambda pc=principal_coords, sc=secondary_coords: self.handle_click(pc,sc),bg="white", bd=1, relief=tk.SUNKEN, width=1, height=1)

                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn

    def create_uttt_grid_pokemon(self, parent_frame, font_size):
        self.buttons = {}
        self.small_grid_frames = {}
        for i in range(3):
            parent_frame.grid_rowconfigure(i, weight=1)
            parent_frame.grid_columnconfigure(i, weight=1)

        for i in range(3):
            parent_frame.grid_rowconfigure(i,weight=1) #retirer weight=1
            parent_frame.grid_columnconfigure(i,weight=1) #retirer weight=1

        for i_p in range(3):
            for j_p in range(3):
                small_grid_frame = tk.Frame(parent_frame, bd=3, relief=tk.RIDGE, bg="white")
                principal_coords = i_p * 3 + j_p
                self.small_grid_frames[principal_coords] = small_grid_frame

                small_grid_frame.grid(row=i_p, column=j_p, padx=3, pady=3, sticky="nsew")

                for r in range(3):
                    small_grid_frame.grid_rowconfigure(r,weight=1)
                for c in range(3):
                    small_grid_frame.grid_columnconfigure(c,weight=1)

                self.buttons[principal_coords] = {}
                for i_s in range(3):
                    for j_s in range(3):
                        secondary_coords = i_s * 3 + j_s
                        btn = tk.Button(small_grid_frame, text="", font=("Arial", font_size),bg="white", bd=1, relief=tk.SUNKEN, width=1, height=1)
                        btn.config(command=lambda pc=principal_coords, sc=secondary_coords, b = btn : self.handle_click_pokemon(pc,sc,b))

                        btn.grid(row=i_s, column=j_s, sticky="nsew", padx=1, pady=1)
                        self.buttons[principal_coords][secondary_coords] = btn

    def handle_click(self, principal_coords, secondary_coords):
        """Gère le clic de l'utilisateur sur une case """
        # Empêcher les clics si c'est le tour de l'IA
        if self.ia_turn_pending:
            messagebox.showinfo("Tour de l'IA", "Veuillez attendre le tour de l'IA...")
            return

        # En mode JvsIA, empêcher de jouer si ce n'est pas le tour du joueur humain
        if self.ia_joueur and self.jeu.joueur_actuel != self.humain_signe:
            messagebox.showinfo("Tour de l'IA", "Ce n'est pas votre tour!")
            return

        try:
            if self.jeu.jouer_coup_global(principal_coords, secondary_coords):
                # Vérifier si une grille a été gagnée après ce coup
                petite_grille = self.jeu.plateau.get_petite_grille(principal_coords)
                if petite_grille.gagnant is not None:
                    self.grilles_gagnees[principal_coords] = petite_grille.gagnant

                # Vérifier si le jeu global est terminé
                if self.jeu.plateau.gagnant_global is not None:
                    self.gagnant_global = self.jeu.plateau.gagnant_global
                    messagebox.showinfo("Partie Terminée", f"Joueur {self.gagnant_global} a remporté le match !")

                self.update_game_state(self.main_game_canvas)

                # Si mode JvsIA et c'est le tour de l'IA, programmer son coup
                if self.ia_joueur and self.jeu.joueur_actuel == self.ia_joueur.signe:
                    self.ia_turn_pending = True
                    self.master.after(500, self.jouer_coup_ia)
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

    def update_game_state(self, canva):

        current_player_signe = self.jeu.joueur_actuel
        target_grid_index = self.jeu.grille_actuelle_index

        # --- Mise à jour des textes sur le Canvas (inchangé) ---
        target_text = f"Grille Ciblée: {target_grid_index + 1}" if target_grid_index is not None else "Grille Ciblée: Aucune (Libre)"

        if hasattr(self, 'main_game_canvas'):

            try:
                current_text = f"Joueur Actuel: ({current_player_signe})"
                canva.itemconfig(self.canvas_current_text_id, text=current_text)
                canva.itemconfig(self.canvas_target_text_id, text=target_text)

                # Construire le texte décrivant qui contrôle chaque signe
                ai_info_text = ""
                if getattr(self, 'ai_vs_ai_running', False) or self.mode_de_jeu == "IAvsIA":
                    j1_role = "IA Intelligente" if isinstance(getattr(self, 'ia_player1', None), IAIntelligente) else "IA Aléatoire"
                    j2_role = "IA Intelligente" if isinstance(getattr(self, 'ia_player2', None), IAIntelligente) else "IA Aléatoire"
                    ai_info_text = f"J1 ({self.jeu.J1}): {j1_role}   —   J2 ({self.jeu.J2}): {j2_role}"
                elif self.ia_joueur is not None and isinstance(self.mode_de_jeu, str) and self.mode_de_jeu.startswith("JvsIA"):
                    ia_type = "IA Intelligente" if self.ia_mode == "intelligente" else "IA Aléatoire"
                    ia_signe = self.ia_joueur.signe
                    if ia_signe == self.jeu.J1:
                        ai_info_text = f"J1 ({self.jeu.J1}): {ia_type}    —    J2 ({self.jeu.J2}): Humain"
                    else:
                        ai_info_text = f"J1 ({self.jeu.J1}): Humain    —    J2 ({self.jeu.J2}): {ia_type}"

                # Mettre à jour le label si le canvas existe
                if hasattr(self, 'canvas_ai_info_id'):
                    self.main_game_canvas.itemconfig(self.canvas_ai_info_id, text=ai_info_text)

                # Compter les grilles gagnées par chaque joueur
                j1_wins = sum(1 for winner in self.grilles_gagnees.values() if winner == self.jeu.J1)
                j2_wins = sum(1 for winner in self.grilles_gagnees.values() if winner == self.jeu.J2)

                j1_score = f"{self.jeu.J1}: {j1_wins}"
                j2_score = f"{self.jeu.J2}: {j2_wins}"
                j1_text = f"Joueur 1 ({self.jeu.J1})\n\nScore:\n{j1_score}"
                j2_text = f"Joueur 2 ({self.jeu.J2})\n\nScore:\n{j2_score}"

                if j1_text:
                   canva.itemconfig(self.canvas_j1_id, text=j1_text)
                if j2_text:
                    canva.itemconfig(self.canvas_j2_id, text=j2_text)
            except Exception:
                pass

        # --- Mise à Jour de la Grille UTTT et de la Surbrillance ---
        for principal_coords in range(9):

            if principal_coords in self.small_grid_frames:
                frame = self.small_grid_frames[principal_coords]
                petite_grille = self.jeu.plateau.get_petite_grille(principal_coords)

                # Vérifier si cette grille a été gagnée
                if principal_coords in self.grilles_gagnees:
                    gagnant = self.grilles_gagnees[principal_coords]
                    frame.config(bg="DarkSeaGreen3", bd=5, relief=tk.SUNKEN) # Grille gagnée : fond gris avec le signe du gagnant
                    # Au lieu de détruire la structure interne (qui modifie le layout),
                    # on place un label par-dessus la petite grille pour garder la taille
                    existing = self.winner_labels.get(principal_coords)

                    if existing is None:
                        winner_label = tk.Label(frame, text=gagnant, font=("Arial", 72, "bold"),bg="LightSkyBlue1" if gagnant == self.jeu.J1 else "DarkSeaGreen3", fg="black")
                        winner_label.place(relx=0, rely=0, relwidth=1, relheight=1) # place par dessus pour remplir exactement le frame sans toucher au grid parent
                        winner_label.lift()
                        self.winner_labels[principal_coords] = winner_label
                    else:
                        existing.config(text=gagnant, bg="LightSkyBlue1" if gagnant == self.jeu.J1 else "DarkSeaGreen3")
                elif target_grid_index is None:
                    print("1")
                    if petite_grille.gagnant is None:
                        frame.config(bg="light sky blue", bd=4, relief=tk.RIDGE)
                    else:
                        frame.config(bg="white", bd=5, relief=tk.SUNKEN)

                elif principal_coords == target_grid_index:
                    print("2")
                    frame.config(bg="black", bd=3, relief=tk.RAISED, highlightbackground="black",highlightcolor="black")
                else:
                    print("3")
                    frame.config(bg="light sky blue", bd=3, relief=tk.RIDGE) # Grilles non ciblées

            # --- Gestion des cases individuelles (boutons) - uniquement si grille non gagnée ---
            if principal_coords not in self.grilles_gagnees:
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
                            bg_color = "LightSkyBlue1" if etat_case == self.jeu.J1 else "DarkSeaGreen3"
                            btn.config(bg=bg_color, relief=tk.SUNKEN)
                        else:
                            btn.config(bg="white", relief=tk.FLAT)

    def select_pokemon(self, pokemon_name, signe_joueur, button):
        self.current_selected_pokemon = pokemon_name
        print(f" current_pokemon: {self.current_selected_pokemon}")
        button.config(bg="blue")
        self.game_phase_pokemon="PLACEMENT POKEMON"
        print(f"Phase mise à jour à: {self.game_phase_pokemon}")


    def handle_click_pokemon(self, principal_coords, secondary_coords, button):

        try:
            if self.jeu.jouer_coup_global(principal_coords, secondary_coords):
                # Vérifier si une grille a été gagnée après ce coup
                petite_grille = self.jeu.plateau.get_petite_grille(principal_coords)
                if petite_grille.gagnant is not None:
                    self.grilles_gagnees[principal_coords] = petite_grille.gagnant

                # Vérifier si le jeu global est terminé
                if self.jeu.plateau.gagnant_global is not None:
                    self.gagnant_global = self.jeu.plateau.gagnant_global
                    messagebox.showinfo("Partie Terminée", f"Joueur {self.gagnant_global} a remporté le match !")

                self.update_game_state(self.main_game_canvas)

                # Si mode JvsIA et c'est le tour de l'IA, programmer son coup
                if self.ia_joueur and self.jeu.joueur_actuel == self.ia_joueur.signe:
                    self.ia_turn_pending = True
                    self.master.after(500, self.jouer_coup_ia)
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


        current_player_signe = self.jeu.joueur_actuel
        print("current player", current_player_signe)
        if self.game_phase_pokemon == "PLACEMENT POKEMON":

            #POKEMON MIS DANS LA CASE
            poke_w, poke_h = 80,80
            image_poke_path = os.path.join(FILENAME, f"{self.current_selected_pokemon}.png")

            #gestion des pokeballs
            if not os.path.exists(image_poke_path):
                pokeball = "pokeball.png"
                image_poke_path= os.path.join(FILENAME, pokeball)

            poke_image_original = Image.open(image_poke_path)
            resized_image = poke_image_original.resize((poke_w, poke_h))
            poke_image_tk = ImageTk.PhotoImage(resized_image)

            #enlever la lettre et mettre que la couleur bg(background) si cela fonctionne car sur mac les boutons ne se colorent pas
            button.config(text = current_player_signe,image=poke_image_tk,compound=tk.CENTER,font=("Arial", 60, "bold"),bg="salmon1" if current_player_signe == "X" else "steel blue",fg="salmon1" if current_player_signe == "X" else "steel blue")
            button.image = poke_image_tk
            button.text= current_player_signe


if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.state('zoomed')  # Tente d'utiliser 'zoomed' (Windows/X11) pour maximiser en laissant la barre des tâches
    except tk.TclError:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

    app = UltimateTicTacToeGUI(root)
    root.mainloop()

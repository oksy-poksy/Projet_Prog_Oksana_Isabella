import pandas as pds
import requests
import os
import tkinter as tk
from PIL import Image, ImageTk
from random import choices

root = tk.Tk()
root.state('zoomed')


def _obtenir_pokemon():
    df2 = pds.read_csv("Pokemon.csv", index_col="Name")
    df3 = df2[-df2["Type 1"].isin(
        ["Normal", "Flying", "Dragon", "Poison", "Ghost", "Fairy", "Fighting", "Ice", "Dark", "Steel", "Psychic",
         "Bug"])]
    return df3

pokemon=_obtenir_pokemon()
print(pokemon)

CSV_FILE = "Pokemon.csv"
FILENAME = "images_pokemon"
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"
SPRITE_URL_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
cleaned_names=[]
pokemon_names= pokemon.index.values.tolist()

def get_pokemon_id_from_name(pokemon_name):
    cleaned_name = pokemon_name.lower().replace(' ', '_').replace('.', '')
    try:
        reponse = requests.get(POKEAPI_URL +pokemon_name)
        reponse.raise_for_status()  # Lève une exception si le statut HTTP est 4xx ou 5xx
        data = reponse.json()
        return (data['id'])
    except requests.exceptions.RequestException as e:
    # Gérer les Pokémons introuvables ou les erreurs de connexion
    # print(f"Impossible de trouver l'ID pour {name} ({e})")
        None
    # L'ID est directement dans la réponse


def download_and_name_pokemon_images(pokemon_name):
    # Obtenir l'ID
    poke_id = get_pokemon_id_from_name(pokemon_name)

    if poke_id:
        # 2. Construire l'URL de l'image (sprite standard)
        image_url = f"{SPRITE_URL_BASE}{poke_id}.png"

        # 3. Définir le nom du fichier local
        # On utilise le nom du DataFrame pour le nommage local
        filename = os.path.join(FILENAME, f"{pokemon_name.replace(' ', '_').replace('.', '')}.png")
        if os.path.exists(filename):
            print(f"Image {pokemon_name} existe déjà dans {FILENAME}. Téléchargement ignoré.")
            return
        # 4. Télécharger l'image
        try:
            img_response = requests.get(image_url)
            img_response.raise_for_status()

            with open(filename, 'wb') as f:
                f.write(img_response.content)
                # print(f"Image téléchargée: {pokemon_name}")

        except requests.exceptions.RequestException as e:
            print(f"Échec du téléchargement de l'image pour {pokemon_name} (ID {poke_id}): {e}")

        else:
            print(f"ID non trouvé pour {pokemon_name}. Image ignorée.")

    print("\nTéléchargement terminé.")

pokemon_image_refs=[] #besoin d'un attribut global sinon les images ne s'affichent pas

def interfacePokemon():
    image_path = "prairie_horizontale.jpg"
    try:
        original_image = Image.open(image_path)
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        resized_image = original_image.resize((width, height))

        global menu_canvas_global
        menu_canvas_global = tk.Canvas(root, width=width, height=height, highlightthickness=0)
        menu_canvas_global.pack(fill="both", expand=True)

        global bg_image_global
        bg_image_global = ImageTk.PhotoImage(resized_image)
        menu_canvas_global.create_image(0, 0, image=bg_image_global, anchor=tk.NW)
    except:
        pass

    try :
        list_pokemon = choices(pokemon_names,k=10)
        grid_frame = tk.Frame(menu_canvas_global)
        rows = 5
        cols = 2
        for i, pokemon in enumerate(list_pokemon):
            download_and_name_pokemon_images(pokemon)
            row = i // cols
            col = i % cols

            image_poke_path = os.path.join("images_pokemon", f"{pokemon}.png")
            poke_image_original = Image.open(image_poke_path)

            poke_width, poke_height = 100, 100
            resized_image = poke_image_original.resize((poke_width, poke_height))
            poke_image_tk = ImageTk.PhotoImage(resized_image)
            global pokemon_image_refs
            pokemon_image_refs.append(poke_image_tk)

            poke_label = tk.Label(grid_frame, image=poke_image_tk, text=pokemon, compound=tk.TOP, bg="white")
            poke_label.grid(row=row, column=col, padx=5, pady=5)

        menu_canvas_global.create_window(width / 2, height / 2, window=grid_frame, anchor=tk.CENTER)
    except:
        pass

def telecharger_image_pokeball():
    image_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"

    filename = os.path.join(FILENAME, "pokeball.png")
    try:
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(img_response.content)
            # print(f"Image téléchargée: {pokemon_name}")
    except:
        print("pas marché")


telecharger_image_pokeball()

interfacePokemon()
root.mainloop()

"""
def show_pokemon_interface(self):

    #1. Selection de pokémons aléatoires
    poke_j1_name = choices(self.pokemons,10 )
    temp_list = [p for p in self.pokemons if p != poke_j1_name]
    poke_j2_name = choices(temp_list)

    # 2. Définition des constantes de position
    width = self.master.winfo_screenwidth()
    height = self.master.winfo_screenheight()

    # Positions (gauche/droite) et tailles
    ball_size_largeur = 320  # Taille de la Pokéball (diamètre en pixels)
    ball_size_hauteur = 220
    pokeball_y = height / 10 * 2  # Position verticale (en bas du centre)

    # Coordonnées des centres des Pokéballs
    center_x_j1 = width * 0.12
    center_x_j2 = width * 0.88

    # --- J1 : Côté Gauche ---

    # 3. Tentative de chargement des images (Simulation)
    try:
        # SIMULATION : Utiliser des images génériques/fictives car les chemins exacts ne sont pas connus

        # --- Image de la Pokéball ---
        original_ball = Image.open("pokeball.png")
        resized_ball = original_ball.resize((ball_size_largeur, ball_size_hauteur))
        self.pokeball_photo = ImageTk.PhotoImage(resized_ball)

        # --- Image du Pokémon J1 ---
        # Supposons qu'on utilise un fichier d'image Pokémon générique basé sur son nom
        #poke_j1_path = f"pokemon_images/{poke_j1_name}.png"
        #original_pokemon_j1 = Image.open(poke_j1_path)
        #resized_pokemon_j1 = original_pokemon_j1.resize((int(ball_size * 0.7), int(ball_size * 0.7)))
        #self.pokemon_j1_photo = ImageTk.PhotoImage(resized_pokemon_j1)

        # --- Image du Pokémon J2 ---
        #poke_j2_path = f"pokemon_images/{poke_j2_name}.png"
        #original_pokemon_j2 = Image.open(poke_j2_path)
        #resized_pokemon_j2 = original_pokemon_j2.resize((int(ball_size * 0.7), int(ball_size * 0.7)))
        #self.pokemon_j2_photo = ImageTk.PhotoImage(resized_pokemon_j2)

    except FileNotFoundError as e:
        # En cas d'échec du chargement d'image (très probable sans les fichiers)
        messagebox.showwarning("Erreur Pokémon",
                                   f"Fichier image manquant pour l'interface Pokémon: {e.filename}. Affichage désactivé.")
        return
    except Exception as e:
        messagebox.showwarning("Erreur Pokémon",
                                   f"Erreur lors du traitement d'image Pokémon: {e}. Affichage désactivé.")
        return

    # 4. Dessin sur le Canvas

    # --- J1 (Gauche) ---
    # Pokéball
    self.main_game_canvas.create_image(center_x_j1, pokeball_y, image=self.pokeball_photo, anchor=tk.CENTER)
    # Pokémon (légèrement décalé pour le positionnement)
    #self.main_game_canvas.create_image(center_x_j1, pokeball_y, image=self.pokemon_j1_photo, anchor=tk.CENTER)
    # Nom du Pokémon (sous la Pokéball)
    #self.main_game_canvas.create_text(center_x_j1, pokeball_y + ball_size / 2 + 10, text=poke_j1_name,font=("Arial", 18, "bold"), fill="black")

    # --- J2 (Droite) ---
    # Pokéball
    self.main_game_canvas.create_image(center_x_j2, pokeball_y, image=self.pokeball_photo, anchor=tk.CENTER)
    # Pokémon
    #self.main_game_canvas.create_image(center_x_j2, pokeball_y, image=self.pokemon_j2_photo, anchor=tk.CENTER)
    #Nom du Pokémon
    #self.main_game_canvas.create_text(center_x_j2, pokeball_y + ball_size / 2 + 10, text=poke_j2_name,font=("Arial", 18, "bold"), fill="black")

    # Mise à jour des noms de joueurs J1/J2 sur le Canvas
    j1_text = f"Joueur 1 ({self.jeu.J1})\n\nPokémon: \n\nScore:\n{self.jeu.J1}: 0"
    j2_text = f"Joueur 2 ({self.jeu.J2})\n\nPokémon: \n\nScore:\n{self.jeu.J2}: 0"

    self.main_game_canvas.itemconfig(self.canvas_j1_id, text=j1_text)
    self.main_game_canvas.itemconfig(self.canvas_j2_id, text=j2_text)
"""
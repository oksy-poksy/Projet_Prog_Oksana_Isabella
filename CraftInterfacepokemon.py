import pandas as pds
import requests
import os
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from random import choice


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

def combat_pokemon(df3,pok_j1,pok_j2):
    hp = df3["HP"]
    att = df3["Attack"]
    defense = df3["Defense"]
    speed = df3["Speed"]

    pv_pok_j1 = hp.loc[pok_j1]
    pv_pok_j2 = hp.loc[pok_j2]
    att_pok_j1 = att.loc[pok_j1]
    att_pok_j2 = att.loc[pok_j2]
    def_pok_j1 = defense.loc[pok_j1]
    def_pok_j2 = defense.loc[pok_j2]
    speed_pok_j1 = speed.loc[pok_j1]
    speed_pok_j2 = speed.loc[pok_j2]
    type_pok_j1 = df3.loc[pok_j1, "Type 1"]
    type_pok_j2 = df3.loc[pok_j2, "Type 1"]

    avantage = {"Fire": "Grass", "Water": "Fire", "Grass": "Ground", "Ground": "Rock", "Rock": "Electric",
                "Electric": "Water"}
    # mettre fleche sur interface si possible ex: fleche vers haut rouge type avantageux
    tour = 1
    while pv_pok_j1 > 0 and pv_pok_j2 > 0:
        esquive_J1 = np.random.binomial(1, speed_pok_j1 / 300)
        esquive_J2 = np.random.binomial(1, speed_pok_j2 / 300)
        if avantage.get(type_pok_j2) == type_pok_j1:

            tour += 1
            print(f'Tour: {tour}')
            if esquive_J1 == 1:
                print(f'{pok_j1} à ésquivé')
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')
            else:

                pv_pok_j1 = pv_pok_j1 - ((att_pok_j2 / def_pok_j1) * 13 * 1.35)
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            if esquive_J2 == 1:
                print(f'{pok_j2} à esquivé')
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')
            else:
                pv_pok_j2 = pv_pok_j2 - ((att_pok_j1 / def_pok_j2) * 13)
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')

        elif avantage.get(type_pok_j1) == type_pok_j2:
            tour += 1
            print(f'Tour: {tour}')
            if esquive_J1 == 1:
                print(f'{pok_j1} à ésquivé')
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')
            else:

                pv_pok_j1 = pv_pok_j1 - ((att_pok_j2 / def_pok_j1) * 13)
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            if esquive_J2 == 1:
                print(f'{pok_j2} à esquivé')
                print(f'il reste {pv_pok_j1} HP à {pok_j1}')
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')
            else:
                pv_pok_j2 = pv_pok_j2 - ((att_pok_j1 / def_pok_j2) * 13 * 1.35)
                print(f'il reste {pv_pok_j2} HP à {pok_j2}')

        else:
            tour += 1
            print(f'Tour: {tour}')

        if esquive_J1 == 1:
            print(f'{pok_j1} à ésquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:

            pv_pok_j1 = pv_pok_j1 - ((att_pok_j2 / def_pok_j1) * 13)
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
        if esquive_J2 == 1:
            print(f'{pok_j2} à esquivé')
            print(f'il reste {pv_pok_j1} HP à {pok_j1}')
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')
        else:
            pv_pok_j2 = pv_pok_j2 - ((att_pok_j1 / def_pok_j2) * 13)
            print(f'il reste {pv_pok_j2} HP à {pok_j2}')

    if pv_pok_j1 < pv_pok_j2 and pv_pok_j2 > 0:
        return pok_j2
        print(f'{pok_j2} à gagné')
    elif pv_pok_j1 > pv_pok_j2 and pv_pok_j1 > 0:
        return pok_j1
        print(f'{pok_j1} à gagné')
    elif pv_pok_j1 <= 0 and pv_pok_j2 <= 0:
        return choice([pok_j2,pok_j1])
        print("Match Nul")


telecharger_image_pokeball()
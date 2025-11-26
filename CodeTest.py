# test_jeu.py
from JeuTicTacToeCorrige import Jeu


def afficher_plateau_console(jeu):
    """Affiche l'état du plateau global sur la console."""
    print("\n" + "=" * 40)
    print(f"Joueur Actuel : {jeu.joueur_actuel}")
    cible = jeu.grille_actuelle_index
    print(f"Grille Ciblée (Index 0-8) : {cible if cible is not None else 'LIBRE CHOIX'}")
    print("=" * 40)

    # Affichage 3x3 des petites grilles
    plateau_affichable = []

    # Récupérer l'état de chaque case pour l'affichage
    for i_grille in range(9):
        ligne_grille = []
        for i_case in range(9):
            etat = jeu.get_etat_case(i_grille, i_case)
            ligne_grille.append(etat if etat != "" else ".")  # Afficher '.' pour les cases vides
        plateau_affichable.append(ligne_grille)

    # Afficher le plateau UTTT
    for i_row in range(3):
        for k_row in range(3):
            ligne_affichage = []
            for i_col in range(3):
                i_grille = i_row * 3 + i_col

                # Récupère les symboles pour la ligne k_row de la petite grille i_grille
                symbols = plateau_affichable[i_grille][k_row * 3: k_row * 3 + 3]

                # Ajoute l'affichage de cette petite grille
                ligne_affichage.append(" ".join(symbols))

            # Afficher la ligne complète des 3 petites grilles
            print(f"| {' | '.join(ligne_affichage)} |")

        # Séparateur entre les grandes lignes
        if i_row < 2:
            print("-" * 40)


def simuler_coups():
    """Simule une séquence de coups pour tester la logique."""

    # 1. Initialisation du Jeu
    jeu = Jeu()
    jeu.determiner_premier_joeur()  # Assure que le premier joueur est défini
    print("--- DÉBUT DE LA SIMULATION ---")
    afficher_plateau_console(jeu)

    # Séquence de coups [Index_Grille, Index_Case] (0-8, 0-8)
    # Les coups sont choisis pour tester le ciblage et la victoire
    coups_a_tester = [
        [4, 4],  # Coup 1 : Grille 4, Case 4 -> Cible Grille 4
        [4, 0],  # Coup 2 : Grille 4, Case 0 -> Cible Grille 0
        [0, 1],  # Coup 3 : Grille 0, Case 1 -> Cible Grille 1
        [1, 2],  # Coup 4 : Grille 1, Case 2 -> Cible Grille 2
        [2, 2],  # Coup 5 : Grille 2, Case 2 -> Cible Grille 2 (Grille 2 était déjà ciblée)
        [2, 4],  # Coup 6 : Grille 2, Case 4 -> Cible Grille 4
        [4, 8],  # Coup 7 : Grille 4, Case 8 -> Cible Grille 8
    ]

    for i, (grille, case) in enumerate(coups_a_tester):
        print(f"\n--- Tour {i + 1} : Jouer dans Grille {grille}, Case {case} ---")

        resultat = jeu.jouer_coup_global(grille, case)
        if resultat is True:
            afficher_plateau_console(jeu)
        else:
            print(f"🛑 Coup {i + 1} INVALIDE (grille: {grille}, case: {case}).")

            # Exemple de test d'un coup invalide (case déjà jouée)
            # if i == 0:
            #    jeu.jouer_coup_global(4, 4) # Tente de rejouer la même case

        if jeu.plateau.gagnant_global:
            print(f"\n🎉 JEU TERMINÉ ! Gagnant global : {jeu.plateau.gagnant_global}")
            break


# Lancer la simulation
if __name__ == "__main__":
    # N'oubliez pas d'appliquer les corrections de la réponse précédente
    # dans JeuTicTacToeCorrige.py avant de lancer ce test !
    simuler_coups()
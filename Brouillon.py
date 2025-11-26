def jouer_coup(self, grille_index, case_index):
    """
    Joue un coup
    grille_index: 0-8 (quelle petite grille)
    case_index: 0-8 (quelle case dans la petite grille)
    """
    if not self.est_coup_valide(grille_index, case_index):
        return False

    # Convertir les index en coordonnées
    grille_ligne = grille_index // 3
    grille_colonne = grille_index % 3
    case_ligne = case_index // 3
    case_colonne = case_index % 3

    # Jouer le coup
    petite_grille = self.plateau.grille_globale[grille_ligne][grille_colonne]
    petite_grille.jouer_coup((case_ligne, case_colonne), self.joueur_actuel)

    # Vérifier si la petite grille est gagnée
    petite_grille.verifier_victoire()

    # Marquer que le premier coup a été joué
    self.premier_coup_joue = True

    # Déterminer la prochaine grille
    prochaine_grille = self.plateau.get_petite_grille(case_index)

    # Si la prochaine grille est déjà gagnée ou pleine, le joueur peut choisir n'importe où
    if prochaine_grille.gagnant is not None:
        self.grille_actuelle = None
    else:
        self.grille_actuelle = case_index

    # Changer de joueur
    self.changer_joueur()

    return True
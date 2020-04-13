import networkx as nx


MSG1 = "L'argument 'joueurs' n'est pas itérable."
MSG2 = "L'itérable de joueurs en contient un nombre différent de deux."
MSG3 = "Le nombre de murs qu'un joueur peut placer est plus grand que 10, ou négatif."
MSG4 = "La position d'un joueur est invalide."
MSG5 = "L'argument 'murs' n'est pas un dictionnaire lorsque présent."
MSG6 = "Le total des murs placés et plaçables n'est pas égal à 20."
MSG7 = "La position d'un mur est invalide."
MSG8 = "Le numéro du joueur est autre que 1 ou 2."
MSG9 = "La position est invalide (en dehors du damier)."
MSG10 ="La position est invalide pour l'état actuel du jeu."
MSG11 = "La partie est déjà terminée."
MSG13 = "Un mur occupe déjà cette position."
MSG14 = "La position est invalide pour cette orientation."
MSG15 = "Le joueur a déjà placé tous ses murs."

# TODO: Définissez votre classe QuoridorError ici.

class QuoridorError(Exception):
    """type QuoridorError"""

class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Attributes:
        état (dict): état du jeu tenu à jour.
        TODO: Identifiez les autres attribut de votre classe

    Examples:
        >>> q.Quoridor()
    """
    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].

        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """
        try:
            assert isinstance(joueurs, list)
        except AssertionError:
            raise QuoridorError(MSG1)
        if len(joueurs) > 2:
            raise QuoridorError(MSG2)
        if murs is not None and not isinstance(murs, dict):
            raise QuoridorError(MSG5)
        self.partie = {
            "joueurs": [
                {"nom": "", "murs": 0, "pos": tuple()},
                {"nom": "", "murs": 0, "pos": tuple()},
            ],
            "murs": {
                "horizontaux": [], "verticaux": []
            }
        }
        self.initialiser_joueur(joueurs[0], 0)
        self.initialiser_joueur(joueurs[1], 1)
        if murs:
            self.partie["murs"] = murs
        self.analyser(self.partie)

    def initialiser_joueur(self, joueur, index):
        """init joueur"""
        if isinstance(joueur, str):
            self.partie["joueurs"][index]["nom"] = joueur
            self.partie["joueurs"][index]["pos"] = (5, 1) if index == 0 else (5, 9)
            self.partie["joueurs"][index]["murs"] = 10
        elif isinstance(joueur, dict):
            self.partie["joueurs"][index]["nom"] = joueur["nom"]
            self.partie["joueurs"][index]["pos"] = joueur["pos"]
            self.partie["joueurs"][index]["murs"] = joueur["murs"]
        else:
            raise QuoridorError(MSG1)

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        return afficher_damier_ascii(self.partie)

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): Le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        numero = (1, 2)
        if joueur not in numero:
            raise QuoridorError(MSG8)
        if position[0] < 1 or position[0] > 9 or position[1] < 1 or position[1] > 9:
            raise QuoridorError(MSG9)
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.partie['joueurs']],
            self.partie['murs']['horizontaux'],
            self.partie['murs']['verticaux']
        )
        pos = self.partie["joueurs"][joueur-1]["pos"]
        if position not in list(graphe.successors(pos)):
            raise QuoridorError(MSG10)
        self.partie["joueurs"][joueur-1]["pos"] = position

    def état_partie(self):
        """Produire l'état actuel de la partie.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de tuple (x, y) uniquement.

        Examples:

            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ],
                'murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }

            où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
            au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
            associée à sa position sur le damier. Une position est représentée par un tuple
            de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

            Les murs actuellement placés sur le damier sont énumérés dans deux listes de
            positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
            est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
            situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
            mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        pass

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.
            
        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        pass

    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        joueur1, joueur2 = (self.partie["joueurs"][i] for i in (0, 1))
        pos1 = joueur1["pos"]
        pos2 = joueur2["pos"]
        if pos1[1] == 9:
            return joueur1["nom"]
        elif pos2[1] == 1:
            return joueur2["nom"]
        else:
            return False

    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        numero = (1, 2)
        ortn = ("horizontal", "vertical")
        cd = position
        if joueur not in numero:
            raise QuoridorError(MSG8)
        if orientation not in ortn:
            raise QuoridorError(MSG14)
        if self.partie["joueurs"][joueur-1]["murs"] == 0:
            raise QuoridorError(MSG15)
        if orientation == "horizontal":
            for pos in self.partie["murs"]["horizontaux"]:
                if (cd[0] == pos[0]-1 or cd[0] == pos[0] or cd[0] == pos[0]+1) and cd[1] == pos[1]:
                    raise QuoridorError(MSG14)
            self.partie["joueurs"][joueur-1]["murs"] -= 1
            self.partie["murs"]["horizontaux"].append(position)
        elif orientation == "vertical":
            for pos in self.partie["murs"]["verticaux"]:
                if (cd[1] == pos[1]-1 or cd[1] == pos[1] or cd[1] == pos[1]+1) and cd[0] == pos[0]:
                    raise QuoridorError(MSG14)
            self.partie["joueurs"][joueur-1]["murs"] -= 1
            self.partie["murs"]["verticaux"].append(position)
        for vert in self.partie["murs"]["verticaux"]:
            for hori in self.partie["murs"]["horizontaux"]:
                if vert == (hori[0]+1, hori[1]-1):
                    raise QuoridorError(MSG14)
        self.analyser(self.partie)

    def analyser(self, partie):
        """
            Validation des positions et des murs
        """
        places = len(partie["murs"]["horizontaux"]) + len(partie["murs"]["verticaux"])
        placables = partie["joueurs"][0]["murs"] + partie["joueurs"][1]["murs"]
        if places + placables != 20:
            raise QuoridorError(MSG6)
        for joueurs in partie["joueurs"]:
            if joueurs["murs"] > 10 or joueurs["murs"] < 0:
                raise QuoridorError(MSG3)
            if joueurs["pos"][0] < 1 or joueurs["pos"][0] > 9:
                raise QuoridorError(MSG9)
            if joueurs["pos"][1] < 1 or joueurs["pos"][1] > 9:
                raise QuoridorError(MSG9)
        if partie["joueurs"][0]["pos"] == partie["joueurs"][1]["pos"]:
            raise QuoridorError(MSG10)
        for absc, ordo in partie["murs"]["horizontaux"]:
            if absc < 1 or absc > 8 or ordo < 2 or ordo > 9:
                raise QuoridorError(MSG7)
        for absc, ordo in partie["murs"]["verticaux"]:
            if absc < 2 or absc > 9 or ordo < 1 or ordo > 8:
                raise QuoridorError(MSG7)

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.

    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.

    Args:
        joueurs (List[Tuple]): une liste des positions (x,y) des joueurs.
        murs_horizontaux (List[Tuple]): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (List[Tuple]): une liste des positions (x,y) des murs verticaux.

    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

def afficher_damier_ascii(dictio):
    """Affiche le damier"""
    nom = [dictio['joueurs'][i]['nom'] for i in range(2)]
    affichage = ''
    affichage += f'Légende: 1={nom[0]}, 2={nom[1]}'+'\n'
    affichage += 3*" "+35*"-"+'\n'
    resultat = []
    index = 10
    for i in range(9):
        resultat.append(['.' if i%4 == 0 else " " for i in range(33)])
        resultat.append([" " for _ in range(35)])
    resultat.pop(-1)
    player = dictio["joueurs"][0]
    bot = dictio["joueurs"][1]
    horizontaux = dictio["murs"]["horizontaux"]
    verticaux = dictio["murs"]["verticaux"]
    resultat[17-2*player["pos"][1]+1][4*(player["pos"][0]-1)] = str(1)
    resultat[17-2*bot["pos"][1]+1][4*(bot["pos"][0]-1)] = str(2)
    for horizontal in horizontaux:
        resultat[17-2*horizontal[1]+2][4*(horizontal[0]-1):4*(horizontal[0]-1)+5+2] = 7*"-"
    for vertical in verticaux:
        j = 0
        for i in range(3):
            toggle = 1 if j == 1 else 0
            resultat[17-2*(vertical[1]+i)+1+j][4*(vertical[0]-2)+2+toggle] = chr(124)
            j += 1
    for i, j in enumerate(resultat, 1):
        if i%2:
            index -= 1
            affichage += str(index)+" "+chr(124)+" "+''.join(j)+" "+chr(124)+'\n'
        else:
            affichage += 2*" "+chr(124)+''.join(j)+chr(124)+'\n'
    affichage += f'{"--"+ chr(124)+35*"-"}'+'\n'
    affichage += f'{2*" "+chr(124)+" "}'
    for i in range(1, 10):
        affichage += f'{str(i)+3*" "}'
    affichage += '\n'
    return affichage

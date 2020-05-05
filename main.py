''' Main.py  '''
import argparse
from api import initialiser_partie
from quoridor import Quoridor
from quoridorx import QuoridorX

def analyser_commande():
    """Parser les valeurs """
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 1')
    parser.add_argument('idul', help=' IDUL du joueur.')
    parser.add_argument('-l', '--lister',
                        help='Lister les identifiants de vos 20 dernières parties.',
                        action='store_true')
    parser.add_argument('-a', '--automatique', help='Activer le mode automatique.',
                        action='store_true')
    parser.add_argument('-x', '--graphique', help='Activer le mode graphique.',
                        action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    PARSER = analyser_commande()
    IDF, ETAT = initialiser_partie(PARSER.idul)
    if PARSER.automatique and not PARSER.graphique:
        MATCH = Quoridor(ETAT["joueurs"])
        while 1:
            MATCH.jouer_auto_console(IDF)
    elif PARSER.graphique and not PARSER.automatique:
        MATCH = QuoridorX(ETAT["joueurs"])
        while 1:
            COORD = tuple(map(int, input('Coordonnees du coup  x, y: ').strip().split(',')))
            DEPL = input('Type de coup MH, MV ou D: ')
            MATCH.jouer_manuel_graph(IDF, DEPL, COORD)
    else:
        print("grpahique et auto")
        MATCH = QuoridorX(ETAT["joueurs"])
        while 1:
            MATCH.jouer_auto_graph(IDF)

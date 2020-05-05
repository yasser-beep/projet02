"""module quoridorx"""
import turtle
from quoridor  import Quoridor

class QuoridorX(Quoridor):
    """class quoridorx: jouer graphiquement"""
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs=None)
        self.dessin_joueur = turtle.Turtle()
        self.screen = turtle.Screen()

    def jouer_auto_graph(self, idf):
        """fonction"""
        pass

    def jouer_manuel_graph(self, idf, typef, pos):
        """fonction"""
        pass
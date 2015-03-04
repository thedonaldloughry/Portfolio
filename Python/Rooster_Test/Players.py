import playerOne, events, sys, pygame, glob, math

class SetPlayers(object):
    """ Creates two clones of Player 1, and sets unique images and control schemes
    to each player."""
    def __init__(self, surf):
        self.surf = surf

    def CreatePlayers(self):
        self.PLAYERONE = playerOne.character(self.surf)
        self.PLAYERONE.x = 100
        self.PLAYERONE.y = 300



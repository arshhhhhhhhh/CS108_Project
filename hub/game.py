import sys
import numpy as np
import pygame
player1 = sys.argv[1]
player2 = sys.argv[2]
class Game:
    def __init__(self, n, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn_of_player = 1
        self.board_size = n
        self.board = np.zeros((self.board_size, self.board_size))
    def switch_turn(self):
        if self.turn_of_player == 1:
            self.turn_of_player = 2
        else:
            self.turn_of_player = 1
    def current_player(self):
        if self.turn_of_player == 1:
            return self.player1
        else:
            return self.player2
    def check_win(self):
        pass
game = Game(3, player1, player2)

import os
import sys

sys.path.append(os.path.join(sys.path[0], 'games'))

import numpy as np
import pygame

player1 = sys.argv[1]
player2 = sys.argv[2]

class Game:
    def __init__(self, n, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = 1
        self.next_player = 2
        self.board_size = n
        self.board = np.zeros((self.board_size, self.board_size))
    def switch_turn(self):
        self.current_player, self.next_player = self.next_player, self.current_player
    def get_current_player(self):
        if self.current_player == 1:
            return self.player1
        else:
            return self.player2
    def check_win(self):
        pass

game = Game(3, player1, player2)

from games import connect4
from games import tictactoe
from games import othello

pygame.init()
screen = pygame.display.set_mode((1470, 956))
pygame.display.set_caption("Welcome to GameSphere Hub: " + player1 + " vs " + player2)
menu_bg = pygame.image.load('images/menu.png').convert()
menu_bg = pygame.transform.scale(menu_bg, (1470, 956))
tictactoe_button = pygame.image.load('images/play_tictactoe.png').convert_alpha()
tictactoe_rect = tictactoe_button.get_rect()
tictactoe_rect.bottomleft = (105, 830)
othello_button = pygame.image.load('images/play_othello.png').convert_alpha()
othello_rect = othello_button.get_rect()
othello_rect.bottomleft = (560, 830)
connect4_button = pygame.image.load('images/play_connect4.png').convert_alpha()
connect4_rect = connect4_button.get_rect()
connect4_rect.bottomleft = (1015, 830)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(menu_bg, (0, 0))
    screen.blit(tictactoe_button, tictactoe_rect)
    screen.blit(othello_button, othello_rect)
    screen.blit(connect4_button, connect4_rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if tictactoe_rect.collidepoint(event.pos):
            print("Starting Tic Tac Toe game...")
            # Start Tic Tac Toe game
        elif othello_rect.collidepoint(event.pos):
            print("Starting Othello game...")
            # Start Othello game
        elif connect4_rect.collidepoint(event.pos):
            print("Starting Connect 4 game...")
            # Start Connect 4 game
    pygame.display.update()

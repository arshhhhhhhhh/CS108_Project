import sys
import numpy as np
import pygame
from game import Game
from datetime import datetime
from numpy.lib.stride_tricks import sliding_window_view
class tictactoe(Game):
    def __init__(self, player1, player2, screen) -> None:
        super().__init__(10, player1, player2)
        self.set_game(screen)
    
    def set_game(self, screen):
        self.load_assets(screen)
        self.pieces = {1: 0, 2: 0}
        self.grid = [
            [pygame.Rect(col*60 + 437, row*60 + 225, 60, 60) for col in range(10)]
            for row in range(10)
        ]
        self.win_cell = None
        self.win_type = None
        self.x_image = pygame.image.load('images/tictactoe/cross.png').convert_alpha()
        self.o_image = pygame.image.load('images/tictactoe/nought.png').convert_alpha()
        self.piece_images = {1: self.x_image, 2: self.o_image}
        self.tictactoe_bg = pygame.image.load('images/tictactoe/bg.png').convert()
        self.reset_button = pygame.Rect(60, 749, 286, 61)
        self.main_menu_button = pygame.Rect(1124, 749, 286, 61)
        self.win_h = pygame.image.load('images/tictactoe/h.png').convert_alpha()
        self.win_v = pygame.image.load('images/tictactoe/v.png').convert_alpha()
        self.win_d1 = pygame.image.load('images/tictactoe/d1.png').convert_alpha()
        self.win_d2 = pygame.image.load('images/tictactoe/d2.png').convert_alpha()
        self.h_rect = self.win_h.get_rect()
        self.v_rect = self.win_v.get_rect()
        self.d1_rect = self.win_d1.get_rect()
        self.d2_rect = self.win_d2.get_rect()

    def check_win(self, r, c):
        #draw
        if self.pieces[1]+self.pieces[2]==100:
            self.result = 0
            return
        b = (self.board == self.next_player).astype(int)
        #horizontal
        row = b[r, :]
        windows = sliding_window_view(row, 5)
        sums = windows.sum(axis=1)
        if np.any(sums == 5):
            self.win_cell = (r, int(np.argmax(sums == 5) + 2))
            self.win_type = "h"
            self.result = self.next_player
            return
        #vertical
        col = b[:, c]
        windows = sliding_window_view(col, 5)
        sums = windows.sum(axis=1)
        if np.any(sums == 5):
            self.win_cell = (int(np.argmax(sums == 5) + 2), c)
            self.win_type = "v"
            self.result = self.next_player
            return
        #diagonal1
        diag1 = np.diagonal(b, offset=c-r)
        if len(diag1) >= 5:
            windows = sliding_window_view(diag1, 5)
            sums = windows.sum(axis=1)
            if np.any(sums == 5):
                i = np.argmax(sums == 5)
                if r >= c:
                    self.win_cell = (r-c+i+2, i+2)
                else:
                    self.win_cell = (i+2, c-r+i+2)
                self.win_type = "d1"
                self.result = self.next_player
                return
        #diagonal2
        diag2 = np.diagonal(np.fliplr(b), offset=(9-c)-r)
        if len(diag2) >= 5:
            windows = sliding_window_view(diag2, 5)
            sums = windows.sum(axis=1)
            if np.any(sums == 5):
                i = np.argmax(sums == 5)
                if r+c >= 10:
                    self.win_cell = (r+c-9+i+2, 9-i-2)
                else:
                    self.win_cell = (i+2, r+c-i-2)
                    print(self.win_cell)
                self.win_type = "d2"
                self.result = self.next_player
                return

    def update_board(self, r, c):
        if self.board[r][c] == 0:
            self.board[r][c] = self.current_player
            self.pieces[self.current_player] += 1
            self.switch_turn()
            return True
        else:
            return False
    
    def draw_board(self):
        self.screen.blit(self.tictactoe_bg, (0, 0))
        for r in range(10):
            for c in range(10):
                if self.board[r][c] != 0:
                    self.screen.blit(self.piece_images[self.board[r][c]], self.grid[r][c])
        if self.result == -1:
            self.screen.blit(self.turn_images[self.current_player], (0, 0))
        else:
            self.screen.blit(self.result_images[self.result], (0, 0))
        p1_count_str = f"{self.pieces[1]:02d}"
        p2_count_str = f"{self.pieces[2]:02d}"
        p1_name = self.name_font.render(self.player1.upper(), True, (255, 255, 255))
        p2_name = self.name_font.render(self.player2.upper(), True, (255, 255, 255))
        p1_count = self.count_font.render(p1_count_str, True, (255, 255, 255))
        p2_count = self.count_font.render(p2_count_str, True, (255, 255, 255))
        p1_name_rect = p1_name.get_rect()
        p2_name_rect = p2_name.get_rect()
        p1_count_rect = p1_count.get_rect()
        p2_count_rect = p2_count.get_rect()
        p1_name_rect.center = (200, 385)
        p2_name_rect.center = (1270, 385)
        p1_count_rect.center = (200, 535)
        p2_count_rect.center = (1270, 535)
        self.screen.blit(p1_name, p1_name_rect)
        self.screen.blit(p2_name, p2_name_rect)
        self.screen.blit(p1_count, p1_count_rect)
        self.screen.blit(p2_count, p2_count_rect)
        if self.win_cell != None:
            (r,c) = self.win_cell
            x = 437+c*60
            y = 225+r*60
            if self.win_type == "h":
                self.h_rect.center = (x+30,y+30)
                self.screen.blit(self.win_h, self.h_rect)
            elif self.win_type == "v":
                self.v_rect.center = (x+30,y+30)
                self.screen.blit(self.win_v, self.v_rect)
            elif self.win_type == "d1":
                self.d1_rect.center = (x+30,y+30)
                self.screen.blit(self.win_d1, self.d1_rect)
            elif self.win_type == "d2":
                self.d2_rect.center = (x+30,y+30)
                self.screen.blit(self.win_d2, self.d2_rect)

    def get_clicked_cell(self, pos):
        for i in range(10):
            for j in range(10):
                if self.grid[i][j].collidepoint(pos):
                    return (i, j)
        return None
        
    def start_tictactoe(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_button.collidepoint(event.pos):
                        self.board = np.zeros((self.board_size, self.board_size))
                        self.pieces = {1: 0, 2: 0}
                        self.result = -1
                        self.current_player = 1
                        self.next_player = 2
                        self.win_cell = None
                        self.win_type = None
                        continue
                    elif self.main_menu_button.collidepoint(event.pos):
                        return
                    elif self.result == -1:
                        cell = self.get_clicked_cell(event.pos)
                        if cell is not None:
                            r, c = cell
                            if self.update_board(r, c):
                                self.check_win(r, c)
            self.draw_board()
            cell = self.get_clicked_cell(pygame.mouse.get_pos())
            if cell is not None:
                if self.board[cell[0]][cell[1]] == 0 and self.result == -1:
                    self.screen.blit(self.piece_images[self.current_player], self.grid[cell[0]][cell[1]])
            if self.result != -1 and self.appended == 0:
                self.appended = 1
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y")
                if self.result == 1:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player1},{self.player2},{timestamp},TicTacToe\n")
                elif self.result == 2:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player2},{self.player1},{timestamp},TicTacToe\n")
            pygame.display.update()
            clock.tick(60)

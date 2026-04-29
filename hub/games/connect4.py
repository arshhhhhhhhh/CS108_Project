import sys
import numpy as np
import pygame
from game import Game
from datetime import datetime
from numpy.lib.stride_tricks import sliding_window_view
class connect4(Game):
    def __init__(self, player1, player2, screen) -> None:
        super().__init__(7, player1, player2)
        self.set_game(screen)
    
    def set_game(self, screen):
        #load assets and initialize game variables
        self.load_assets(screen)
        self.pieces = {1: 0, 2: 0}
        self.grid = [
            [pygame.Rect(col*86 + 434, row*86 + 224, 86, 86) for col in range(7)]
            for row in range(7)
        ]
        self.win_cell = None
        self.win_type = None
        self.blue_disc = pygame.image.load('images/connect4/blue.png').convert_alpha()
        self.pink_disc = pygame.image.load('images/connect4/pink.png').convert_alpha()
        self.discs = {1: self.blue_disc, 2: self.pink_disc}
        self.connect4_bg = pygame.image.load('images/connect4/bg.png').convert()
        self.win_h = pygame.image.load('images/connect4/h.png').convert_alpha()
        self.win_v = pygame.image.load('images/connect4/v.png').convert_alpha()
        self.win_d1 = pygame.image.load('images/connect4/d1.png').convert_alpha()
        self.win_d2 = pygame.image.load('images/connect4/d2.png').convert_alpha()
        self.h_rect = self.win_h.get_rect()
        self.v_rect = self.win_v.get_rect()
        self.d1_rect = self.win_d1.get_rect()
        self.d2_rect = self.win_d2.get_rect()

    def check_win(self, r, c):
        #check for draw
        if self.pieces[1]+self.pieces[2]==49:
            self.result = 0
            return
        b = (self.board == self.next_player).astype(int)
        #check horizontal
        row = b[r, :]
        windows = sliding_window_view(row, 4)
        sums = windows.sum(axis=1)
        if np.any(sums == 4):
            self.win_cell = (r, int(np.argmax(sums == 4) + 2))
            self.win_type = "h"
            self.result = self.next_player
            return
        #check vertical
        col = b[:, c]
        windows = sliding_window_view(col, 4)
        sums = windows.sum(axis=1)
        if np.any(sums == 4):
            self.win_cell = (int(np.argmax(sums == 4) + 2), c)
            self.win_type = "v"
            self.result = self.next_player
            return
        #check diagonal1
        diag1 = np.diagonal(b, offset=c-r)
        if len(diag1) >= 4:
            windows = sliding_window_view(diag1, 4)
            sums = windows.sum(axis=1)
            if np.any(sums == 4):
                i = np.argmax(sums == 4)
                if r >= c:
                    self.win_cell = (r-c+i+2, i+2)
                else:
                    self.win_cell = (i+2, c-r+i+2)
                self.win_type = "d1"
                self.result = self.next_player
                return
        #check diagonal2
        diag2 = np.diagonal(np.fliplr(b), offset=(6-c)-r)
        if len(diag2) >= 4:
            windows = sliding_window_view(diag2, 4)
            sums = windows.sum(axis=1)
            if np.any(sums == 4):
                i = np.argmax(sums == 4)
                if r+c >= 6:
                    self.win_cell = (r+c-6+i+2, 6-i-2)
                else:
                    self.win_cell = (i+2, r+c-i-2)
                self.win_type = "d2"
                self.result = self.next_player
                return

    def get_lowest(self, c):
        #return the lowest empty row in the specified column, or None if the column is full
        if c is None:
            return None
        for r in range(6, -1, -1):
            if self.board[r][c] == 0:
                return r
        return None
    
    def update_board(self, c):
        #update the board with the current player's move in the specified column if possible and switch turns
        r = self.get_lowest(c)
        if r != None:
            self.board[r][c] = self.current_player
            self.pieces[self.current_player] += 1
            self.switch_turn()
            return True
        else:
            return False
        
    def draw_board(self):
        #display the board and pieces on the screen
        self.screen.blit(self.connect4_bg, (0, 0))
        for r in range(7):
            for c in range(7):
                if self.board[r][c] != 0:
                    self.screen.blit(self.discs[self.board[r][c]], self.grid[r][c])
        
        #display current turn or result
        if self.result == -1:
            self.screen.blit(self.turn_images[self.current_player], (0, 0))
        else:
            self.screen.blit(self.result_images[self.result], (0, 0))
        
        #display player names and piece counts
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
        
        #display winning line if there is a winner
        if self.win_cell != None:
            (r,c) = self.win_cell
            x = 434+c*86
            y = 224+r*86
            if self.win_type == "h":
                self.h_rect.center = (x,y+43)
                self.screen.blit(self.win_h, self.h_rect)
            elif self.win_type == "v":
                self.v_rect.center = (x+43,y)
                self.screen.blit(self.win_v, self.v_rect)
            elif self.win_type == "d1":
                self.d1_rect.center = (x,y)
                self.screen.blit(self.win_d1, self.d1_rect)
            elif self.win_type == "d2":
                self.d2_rect.center = (x+86,y)
                self.screen.blit(self.win_d2, self.d2_rect)

    def get_column(self, pos):
        #return the column corresponding to the position of mouse click
        for r in range(7):
            for c in range(7):
                if self.grid[r][c].collidepoint(pos):
                    return c
        return None
    
    def start_connect4(self):
        #main game loop to handle events and update the screen accordingly
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
                        col = self.get_column(event.pos)
                        row = self.get_lowest(col)
                        if col is not None:
                            if self.update_board(col):
                                self.check_win(row, col)
            self.draw_board()
            col = self.get_column(pygame.mouse.get_pos())
            if col is not None:
                row = self.get_lowest(col)
                if row is not None and self.result == -1:
                    self.screen.blit(self.discs[self.current_player], self.grid[row][col])
            if self.result != -1 and self.appended == 0:
                self.appended = 1
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y")
                if self.result == 1:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player1},{self.player2},{timestamp},Connect4\n")
                elif self.result == 2:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player2},{self.player1},{timestamp},Connect4\n")
            pygame.display.flip()
            clock.tick(60)

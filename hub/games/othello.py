import sys
import numpy as np
import pygame
from datetime import datetime
from game import Game
class othello(Game):
    def __init__(self, player1, player2, screen) -> None:
        super().__init__(8, player1, player2)
        self.set_board(screen=screen)
        self.update_valid_pos()
    
    def set_board(self, screen):
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        self.player1_pieces = 2
        self.player2_pieces = 2
        self.load_assets(screen)
        self.grid = [
            [pygame.Rect(col*75 + 437, row*75 + 225, 75, 75) for col in range(8)]
            for row in range(8)
        ]
        self.black_disc = pygame.image.load('images/othello/black.png').convert_alpha()
        self.white_disc = pygame.image.load('images/othello/white.png').convert_alpha()
        self.discs = {1: self.black_disc, 2: self.white_disc}
        self.othello_bg = pygame.image.load('images/othello/bg.png').convert()
        self.reset_button = pygame.Rect(60, 749, 286, 61)
        self.main_menu_button = pygame.Rect(1124, 749, 286, 61)

    def update_valid_pos(self):
        self.valid_moves = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != self.current_player:
                    continue
                for c in range(8):
                    if self.board[i][c] != 0 or c == j or j-c == 1 or j-c == -1:
                        continue
                    value = 1
                    for x in self.board[i, min(c, j)+1:max(c, j)]:
                        if x != self.next_player:
                            value = 0
                            break
                    if value == 1:
                        self.valid_moves.add(((i, c), (i, j), "horizontal"))
                for r in range(8):
                    if self.board[r][j] != 0 or r == i or r-i == 1 or r-i == -1:
                        continue
                    value = 1
                    for x in self.board[min(r, i)+1:max(r, i), j]:
                        if x != self.next_player:
                            value = 0
                            break
                    if value == 1:
                        self.valid_moves.add(((r, j), (i, j), "vertical"))
                for t in range(-7, 8):
                    if i+t < 0 or i+t > 7 or j+t < 0 or j+t > 7 or t == 0 or t == 1 or t == -1:
                        continue
                    if self.board[i+t][j+t] != 0:
                        continue
                    value = 1
                    for x in range(min(t, 0)+1, max(t, 0)):
                        if self.board[i+x][j+x] != self.next_player:
                            value = 0
                            break
                    if value == 1:
                        self.valid_moves.add(((i+t, j+t), (i, j), "diagonal1"))
                for t in range(-7, 8):
                    if i+t < 0 or i+t > 7 or j-t < 0 or j-t > 7 or t == 0 or t == 1 or t == -1:
                        continue
                    if self.board[i+t][j-t] != 0:
                        continue
                    value = 1
                    for x in range(min(t, 0)+1, max(t, 0)):
                        if self.board[i+x][j-x] != self.next_player:
                            value = 0
                            break
                    if value == 1:
                        self.valid_moves.add(((i+t, j-t), (i, j), "diagonal2"))
        
    def check_valid_move(self, r, c):
        moves = []
        for move in self.valid_moves:
            if move[0] == (r, c):
                moves.append(move[1]) 
        return moves         

    def update_board(self, r, c):
        if len(self.check_valid_move(r, c)) == 0:
            return 0
        for move in self.check_valid_move(r, c):
            self.board[r][c] = self.current_player
            sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0
            dr = sign(move[0] - r)
            dc = sign(move[1] - c)
            i, j = r + dr, c + dc
            while (i, j) != move:
                self.board[i][j] = self.current_player
                i += dr
                j += dc
            self.player1_pieces = 0
            self.player2_pieces = 0
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 1:
                        self.player1_pieces += 1
                    elif self.board[i][j] == 2:
                        self.player2_pieces += 1
        self.switch_turn()
        self.update_valid_pos()
        #print(self.valid_moves)
        return 1

    def check_win(self):
        if self.player1_pieces + self.player2_pieces == 64:
            if self.player1_pieces > self.player2_pieces:
                self.result = 1
                return 1
            elif self.player2_pieces > self.player1_pieces:
                self.result = 2
                return 2
            else:
                self.result = 0
                return 0

        if self.current_player == 1 and self.player1_pieces == 0:
            self.result = 2
            return 2
        elif self.current_player == 2 and self.player2_pieces == 0:
            self.result = 1
            return 1

        if len(self.valid_moves) == 0:
            self.switch_turn()
            self.update_valid_pos()
            if len(self.valid_moves) == 0:
                if self.player1_pieces > self.player2_pieces:
                    self.result = 1
                    return 1
                elif self.player2_pieces > self.player1_pieces:
                    self.result = 2
                    return 2
                else:
                    self.result = 0
                    return 0
            #self.switch_turn()
            #self.update_valid_pos()
        return -1
    
    def draw_board(self):
        self.screen.blit(self.othello_bg, (0, 0))
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.screen.blit(self.discs[self.board[i][j]], self.grid[i][j])
        if self.result == -1:
            self.screen.blit(self.turn_images[self.current_player], (0, 0))
        else:
            self.screen.blit(self.result_images[self.result], (0, 0))
        p1_count_str = f"{self.player1_pieces}"
        p2_count_str = f"{self.player2_pieces}"
        if self.player1_pieces < 10:
            p1_count_str = "0" + p1_count_str
        if self.player2_pieces < 10:
            p2_count_str = "0" + p2_count_str
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
    
    def get_clicked_cell(self, pos):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j].collidepoint(pos):
                    return (i, j)
        return None
    
    def start_othello(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_button.collidepoint(event.pos):
                        self.board = np.zeros((self.board_size, self.board_size))
                        self.set_board(self.screen)
                        self.current_player = 1
                        self.next_player = 2
                        self.update_valid_pos()
                        self.result = -1
                        continue
                    elif self.main_menu_button.collidepoint(event.pos):
                        return
                    cell = self.get_clicked_cell(event.pos)
                    if cell is not None:
                        r, c = cell
                        if self.update_board(r, c) == 1:
                            self.check_win()
            
            self.draw_board()
            cell = self.get_clicked_cell(pygame.mouse.get_pos())
            if cell is not None:
                if (cell[0], cell[1]) in [move[0] for move in self.valid_moves]:
                    self.screen.blit(self.discs[self.current_player], self.grid[cell[0]][cell[1]])
            if self.result != -1 and self.appended == 0:
                self.appended = 1
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y")
                if self.result == 1:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player1},{self.player2},{timestamp},Othello\n")
                elif self.result == 2:
                    with open('history.csv', 'a') as f:
                        f.write(f"{self.player2},{self.player1},{timestamp},Othello\n")
            pygame.display.flip()
            clock.tick(60)
                            
                
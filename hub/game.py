import sys
import numpy as np
import pygame


class Game:
    def __init__(self, n, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = 1
        self.next_player = 2
        self.board_size = n
        self.board = np.zeros((self.board_size, self.board_size))
        self.result = -1
        self.appended = 0
    def load_assets(self, screen):
        self.screen = screen
        self.turn_images = {1: pygame.image.load('images/player1_turn.png').convert_alpha(),
                            2: pygame.image.load('images/player2_turn.png').convert_alpha()}
        self.result_images = {1: pygame.image.load('images/win_1.png').convert_alpha(),
                              2: pygame.image.load('images/win_2.png').convert_alpha(),
                              0: pygame.image.load('images/draw.png').convert_alpha()}
        self.rect = pygame.Rect(0, 0, 1470, 956)
        self.name_font = pygame.font.Font('AudioWide-Regular.ttf', 45)
        self.count_font = pygame.font.Font('AudioWide-Regular.ttf', 120)
    def switch_turn(self):
        self.current_player, self.next_player = self.next_player, self.current_player
    def get_current_player(self):
        if self.current_player == 1:
            return self.player1
        else:
            return self.player2
    def check_win(self):
        pass

def get_rect(pos, rect):
    for r in rect:
        if r.collidepoint(pos):
            return r
    return None

def main_menu(player1, player2, screen, clock):
    menu_bg = pygame.image.load('images/menu.png').convert()
    #menu_bg = pygame.transform.scale(menu_bg, (1470, 956))
    tictactoe_rect = pygame.Rect(105, 340, 350, 345)
    othello_rect = pygame.Rect(560, 340, 350, 345)
    connect4_rect = pygame.Rect(1015, 340, 350, 345)
    switch_turn_rect = pygame.Rect(105, 725, 350, 105)
    leaderboard_rect = pygame.Rect(560, 725, 350, 105)
    exit_rect = pygame.Rect(1015, 725, 350, 105)
    rectangles = [tictactoe_rect, othello_rect, connect4_rect, switch_turn_rect, leaderboard_rect, exit_rect]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = get_rect(event.pos, rectangles)
                if button == exit_rect:
                    print("Exiting GameSphere Hub. Goodbye!")
                    pygame.quit()
                    sys.exit()
                elif button == switch_turn_rect:
                    print("Switching turns between players...")
                    player1, player2 = player2, player1
                    pygame.display.set_caption("Welcome to GameSphere Hub: " + player1 + " vs " + player2)
                    continue
                elif button == leaderboard_rect:
                    print("Displaying leaderboard...")
                    # Display leaderboard (not implemented in this code snippet)
                    continue
                elif button == tictactoe_rect:
                    print("Starting Tic Tac Toe game...")
                    # Start Tic Tac Toe game
                    from games.tictactoe import tictactoe
                    game = tictactoe(player1, player2, screen)
                    game.start_tictactoe()
                    pygame.event.clear()
                    game = None
                    continue   
                elif button == othello_rect:
                    print("Starting Othello game...")
                    # Start Othello game
                    from games.othello import othello
                    game = othello(player1, player2, screen)
                    game.start_othello()
                    pygame.event.clear()
                    game = None
                elif button == connect4_rect:
                    print("Starting Connect 4 game...")
                    # Start Connect 4 game
                    from games.connect4 import connect4
                    game = connect4(player1, player2, screen)
                    game.start_connect4()
                    pygame.event.clear()
                    game = None
        
        screen.blit(menu_bg, (0, 0))
        pygame.display.update()
        clock.tick(60)
    
if __name__ == "__main__":
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    pygame.init()
    screen = pygame.display.set_mode((1470, 956))
    pygame.display.set_caption("Welcome to GameSphere Hub: " + player1 + " vs " + player2)
    clock = pygame.time.Clock()
    main_menu(player1, player2, screen, clock)

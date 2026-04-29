import os
import sys

sys.path.append(os.path.join(sys.path[0], 'games'))

import numpy as np
import pygame
import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import MaxNLocator
from collections import Counter
import subprocess

player1 = sys.argv[1]
player2 = sys.argv[2]

class Game:
    def __init__(self, n, player1, player2):
        #Initialize game state
        self.player1 = player1
        self.player2 = player2
        self.current_player = 1
        self.next_player = 2
        self.board_size = n
        self.board = np.zeros((self.board_size, self.board_size))
        self.result = -1
        self.appended = 0

    def load_assets(self, screen):
        #Load common assets for all games
        self.screen = screen
        self.turn_images = {1: pygame.image.load('images/player1_turn.png').convert_alpha(),
                            2: pygame.image.load('images/player2_turn.png').convert_alpha()}
        self.result_images = {1: pygame.image.load('images/win_1.png').convert_alpha(),
                              2: pygame.image.load('images/win_2.png').convert_alpha(),
                              0: pygame.image.load('images/draw.png').convert_alpha()}
        self.rect = pygame.Rect(0, 0, 1470, 956)
        self.name_font = pygame.font.Font('AudioWide-Regular.ttf', 45)
        self.count_font = pygame.font.Font('AudioWide-Regular.ttf', 120)
        self.reset_button = pygame.Rect(60, 749, 286, 61)
        self.main_menu_button = pygame.Rect(1124, 749, 286, 61)

    def switch_turn(self):
        #switch turns between players
        self.current_player, self.next_player = self.next_player, self.current_player

    def check_win(self):
        #Winning condition implemented in each game subclass
        pass


def get_rect(pos, rect):
    #Check if mouse click is within any of the given rectangles and return the rectangle if so
    for r in rect:
        if r.collidepoint(pos):
            return r
    return None


def main_menu(player1, player2, screen, clock):
    #Load main menu assets and define button rectangles
    menu_bg = pygame.image.load('images/menu.png').convert()
    tictactoe_rect = pygame.Rect(105, 340, 350, 345)
    othello_rect = pygame.Rect(560, 340, 350, 345)
    connect4_rect = pygame.Rect(1015, 340, 350, 345)
    switch_turn_rect = pygame.Rect(105, 725, 350, 105)
    leaderboard_rect = pygame.Rect(560, 725, 350, 105)
    exit_rect = pygame.Rect(1015, 725, 350, 105)
    rectangles = [tictactoe_rect, othello_rect, connect4_rect, switch_turn_rect, leaderboard_rect, exit_rect]

    while True:
        #Event loop for main menu
        for event in pygame.event.get():
            #Handle quitting and button clicks
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = get_rect(event.pos, rectangles)
                if button == exit_rect:
                    #for exiting the game
                    print("Exiting GameSphere Hub. Goodbye!")
                    pygame.quit()
                    sys.exit()
                elif button == switch_turn_rect:
                    #Switch turns between players for the game
                    print("Switching turns between players...")
                    player1, player2 = player2, player1
                    pygame.display.set_caption("Welcome to GameSphere Hub: " + player1 + " vs " + player2)
                    continue
                elif button == leaderboard_rect:
                    #Display the leaderboard and statistics visualisation
                    print("Displaying leaderboard...")
                    if leaderboard(screen, clock):
                        visualise(screen, clock)
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


def leaderboard(screen, clock):
    #Display the leaderboard window
    leaderboard_bg = pygame.image.load('images/leaderboard.png').convert()
    rects = [pygame.Rect(505, 365, 460, 80), pygame.Rect(505, 465, 460, 80), pygame.Rect(505, 565, 460, 80), pygame.Rect(1030, 209, 45, 45)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = get_rect(event.pos, rects)
                if button == rects[3]:
                    return 0
                elif button is not None:
                    m = rects.index(button)
                    subprocess.run(["bash", "leaderboard.sh", str(m)])
                    return 1
        screen.blit(leaderboard_bg, (0, 0))
        pygame.display.update()
        clock.tick(60)
                
def visualise(screen, clock):
    plt.close("all")
    #  Font Setup 
    font_path = "Audiowide-Regular.ttf"
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()

    #  Custom Colors 
    pink = "#EB1E84"
    blue = "#49CCFB"
    violet = "#7216D3"

    # Read history data from CSV
    with open("history.csv", "r") as f:
        if not f.read().strip():
            print("No game history found. Returning to main menu.")
            return
        f.seek(0)
        reader = csv.reader(f, delimiter=",")
        winners = []
        games = []

        for row in reader:
            if len(row) == 4:
                winners.append(row[0].upper())
                games.append(row[3].upper())


    #Bar Graph 
    win_counts = Counter(winners)
    top5 = win_counts.most_common(5)

    if top5:
        players, counts = zip(*top5)

        # Alternate pink and blue bars
        bar_colors = []
        for i in range(len(players)):
            if i % 2 == 0:
                bar_colors.append(pink)
            else:
                bar_colors.append(blue)

        plt.figure(1, facecolor="black")
        ax1 = plt.gca()
        ax1.set_facecolor("black")

        #Setting the labels and title of the bar graph
        plt.bar(players, counts, color=bar_colors)
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(f"TOP {len(top5)} PLAYERS BY WIN COUNT", color="white", fontsize=20)
        plt.xlabel("PLAYERS", color="white", fontsize=16)
        plt.ylabel("WINS", color="white", fontsize=16)

        ax1.tick_params(colors="white")

        for spine in ax1.spines.values():
            spine.set_color("white")

        plt.savefig("images/top5_players.png")


    #Pie Chart 
    game_counts = Counter(games)

    if game_counts:
        labels, sizes = zip(*game_counts.items())
        pie_colors = [blue, violet, pink]

        plt.figure(2, facecolor="black")
        ax2 = plt.gca()
        ax2.set_facecolor("black")

        #displaying the pie chart and title
        plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct="%1.1f%%",
            textprops={
                "color": "white",
                "fontproperties": font_prop,
                "fontsize": 16
            }
        )
        plt.title(
            "MOST PLAYED GAMES BY FREQUENCY",
            color="white",
            fontproperties=font_prop,
            fontsize=20
        )

        plt.savefig("images/game_distribution.png")

    #Display the visualisations in pygame window
    stats_bg = pygame.image.load('images/game_stats.png').convert()
    top5 = pygame.image.load('images/top5_players.png').convert()
    top5 = pygame.transform.scale(top5, (640, 480))
    distribution = pygame.image.load('images/game_distribution.png').convert()
    distribution = pygame.transform.scale(distribution, (640, 480))
    main_menu_rect = pygame.Rect(105, 725, 350, 105)
    exit_rect = pygame.Rect(1015, 725, 350, 105)
    rects = [main_menu_rect, exit_rect]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = get_rect(event.pos, rects)
                if button == exit_rect:
                    print("Exiting GameSphere Hub. Goodbye!")
                    pygame.quit()
                    sys.exit()
                elif button == main_menu_rect:
                    return
        screen.blit(stats_bg, (0, 0))
        screen.blit(top5, (55, 187))
        screen.blit(distribution, (775, 187))
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    #Initialize players, pygame, and start the main menu loop
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    pygame.init()
    screen = pygame.display.set_mode((1470, 956))
    pygame.display.set_caption("Welcome to GameSphere Hub: " + player1 + " vs " + player2)
    clock = pygame.time.Clock()
    main_menu(player1, player2, screen, clock)

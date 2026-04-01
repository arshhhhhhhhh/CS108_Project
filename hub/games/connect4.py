def place_piece(r,c):
    for r_t in range(r, len(game.board)):
        if game.board[r_t][c] == 0:
            game.board[r_t][c] = game.turn_of_player
            return 1
    return 0

def check_win():
    for r in range(game.board_size):
        for c in range(game.board_size - 3):
            if np.all(game.board[r][c:c+4] == game.turn_of_player):
                return 1
    for c in range(game.board_size):
        for r in range(game.board_size - 3):
            if np.all(game.board[r:r+4, c] == game.turn_of_player):
                return 1
    for r in range(game.board_size - 3):
        for c in range(game.board_size - 3):
            if np.all(np.diag(game.board[r:r+4, c:c+4]) == game.turn_of_player):
                return 1
    for r in range(3, game.board_size):
        for c in range(game.board_size - 3):
            if np.all(np.diag(np.fliplr(game.board[r-3:r+1, c:c+4])) == game.turn_of_player):
                return 1
    return 0

def check_draw():
    if np.all(game.board != 0):
        return 1
    return 0

def reset_game():
    game.board = np.zeros((game.board_size, game.board_size))
    game.turn_of_player = 1
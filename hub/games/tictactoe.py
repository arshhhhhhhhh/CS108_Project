def place_piece(r, c):
    if(game .board[r][c] == 0):
        game.board[r][c] = game.turn_of_player
        return 1
    else:
        return 0

def check_win():
    for i in range(game.board_size):
        if np.all(game.board[i] == game.turn_of_player):
            return 1
        if np.all(game.board[:, i] == game.turn_of_player):
            return 1
    if np.all(np.diag(game.board) == game.turn_of_player):
        return 1
    if np.all(np.diag(np.fliplr(game.board)) == game.turn_of_player):
        return 1
    return 0

def check_draw():
    if np.all(game.board != 0):
        return 1
    return 0

def reset_game():
    game.board = np.zeros((game.board_size, game.board_size))
    game.turn_of_player = 1

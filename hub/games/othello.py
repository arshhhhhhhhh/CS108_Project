from game import Game
class othello(Game):
    def __init__(self, player1, player2) -> None:
        super().__init__(8, player1, player2)
        self.set_board()
        self.update_valid_pos()
        print(self.valid_moves)

    def set_board(self):
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.player1_pieces = 2
        self.player2_pieces = 2

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
        for move in self.valid_moves:
            if move[0] == (r, c):
                return move[1]
        return 0          

    def update_board(self, r, c):
        move = self.check_valid_move(r, c)
        if move == 0:
            return 0
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
        print(self.valid_moves)
        return 1

    def turn_pass(self):
        if len(self.valid_moves) == 0:
            self.switch_turn()
            self.update_valid_pos()
            return 1
        return 0

    def check_win(self):
        if self.player1_pieces + self.player2_pieces == 64:
            if self.player1_pieces > self.player2_pieces:
                return 1
            elif self.player2_pieces > self.player1_pieces:
                return 2
            else:
                return 0
        
        if self.current_player == 1 and self.player1_pieces == 0:
            return 2
        elif self.current_player == 2 and self.player2_pieces == 0:
            return 1

        if self.turn_pass() == 1:
            if self.turn_pass() == 1:
                if self.player1_pieces > self.player2_pieces:
                    return 1
                elif self.player2_pieces > self.player1_pieces:
                    return 2
                else:
                    return 0
            else:
                self.switch_turn()
                self.update_valid_pos()
        return -1
    

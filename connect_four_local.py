import game_view as gv

BOARD_X = 7
BOARD_Y = 6

def setup_board():
    board = [["E" for i in range(BOARD_X)] for j in range(BOARD_Y)]
    return board

def down_check_win(x, y, board, turn):
    has_won = True
    for temp_y in range(y, y + 4):
        if (temp_y >= len(board)) or (board[temp_y][x] != turn[0]):
            has_won = False
            break
    if (has_won):
        return True

def left_check_win(x, y, board, turn):
    has_won = True
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0) or (board[y][temp_x] != turn[0]):
            has_won = False
            break
    if (has_won):
        return True

def right_check_win(x, y, board, turn):
    has_won = True
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0])) or (board[y][temp_x] != turn[0]):
            has_won = False
            break
    if (has_won):
        return True

def topleft_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0 or temp_y < 0) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        temp_y -= 1
    if (has_won):
        return True

def topright_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0]) or temp_y < 0) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        temp_y -= 1
    if (has_won):
        return True

def bottomleft_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0 or temp_y >= len(board)) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        temp_y += 1
    if (has_won):
        return True

def bottomright_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0]) or temp_y >= len(board)) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        temp_y += 1
    if (has_won):
        return True

class Game:
    def __init__(self, board):
        self.turn = "Red"
        self.board = board
    
    def get_turn(self):
        return self.turn

    def toggle_turn(self):
        if self.turn == "Red":
            self.turn = "Yellow"
        else:
            self.turn = "Red"
    
    def get_board(self):
        return self.board

    def check_win(self, x, y):
        if down_check_win(x, y, self.board, self.get_turn()):
            return True
        if left_check_win(x, y, self.board, self.get_turn()):
            return True
        if right_check_win(x, y, self.board, self.get_turn()):
            return True
        if topleft_check_win(x, y, self.board, self.get_turn()):
            return True
        if topright_check_win(x, y, self.board, self.get_turn()):
            return True
        if bottomleft_check_win(x, y, self.board, self.get_turn()):
            return True
        if bottomright_check_win(x, y, self.board, self.get_turn()):
            return True
        return False

    def dropped_token(self, x, game_view):
        y = 0
        running = True
        while running:
            if (y + 1 < len(self.board) and (self.board[y + 1][x] == "E")):
                y += 1
            else:
                running = False
        if self.board[y][x] == "E":
            self.board[y][x] = self.turn[0]
            game_view.update_button(x, y)
            has_won = self.check_win(x, y)
            if has_won:
                game_view.display_winner(self.turn)
                game_view.disable_all_drop_buttons()
                return False
            else:
                self.toggle_turn()
            return True
        return False

def main():
    board = setup_board()
    game = Game(board)
    gv.GameView(game)

if __name__ == "__main__":
    main()
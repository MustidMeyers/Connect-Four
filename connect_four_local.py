import game_view as gv

BOARD_X = 7
BOARD_Y = 6

def setup_board():
    board = [["E" for i in range(BOARD_X)] for j in range(BOARD_Y)]
    return board

def down_check_win(x, y, board, turn):
    has_won = True
    won_tuples = []
    for temp_y in range(y, y + 4):
        if (temp_y >= len(board)) or (board[temp_y][x] != turn[0]):
            has_won = False
            break
        won_tuples.append((x, temp_y))
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def left_check_win(x, y, board, turn):
    has_won = True
    won_tuples = []
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0) or (board[y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, y))
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def right_check_win(x, y, board, turn):
    has_won = True
    won_tuples = []
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0])) or (board[y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, y))
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def topleft_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    won_tuples = []
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0 or temp_y < 0) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, temp_y))
        temp_y -= 1
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def topright_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    won_tuples = []
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0]) or temp_y < 0) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, temp_y))
        temp_y -= 1
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def bottomleft_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    won_tuples = []
    for temp_x in range(x, x - 4, -1):
        if (temp_x < 0 or temp_y >= len(board)) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, temp_y))
        temp_y += 1
    if (has_won):
        return True, won_tuples
    return False, won_tuples

def bottomright_check_win(x, y, board, turn):
    has_won = True
    temp_y = y
    won_tuples = []
    for temp_x in range(x, x + 4):
        if (temp_x >= len(board[0]) or temp_y >= len(board)) or (board[temp_y][temp_x] != turn[0]):
            has_won = False
            break
        won_tuples.append((temp_x, temp_y))
        temp_y += 1
    if (has_won):
        return True, won_tuples
    return False, won_tuples

checks = [down_check_win,left_check_win,right_check_win,topleft_check_win,topright_check_win,
            bottomleft_check_win,bottomright_check_win]

class Game:
    def __init__(self, board, menu):
        self.turn = "Red"
        self.board = board
        self.menu = menu
    
    def back_to_menu(self):
        if self.menu is None:
            import main_menu
            main_menu.main()
        else:
            self.menu.reset()

    def get_turn(self):
        return self.turn

    def toggle_turn(self):
        if self.turn == "Red":
            self.turn = "Yellow"
        else:
            self.turn = "Red"
    
    def get_board(self):
        return self.board

    def check_win(self, xi, yi):
        for x in range(xi - 3, xi + 4):
            for y in range(yi - 3, yi + 4):
                if (y >= 0 and y < len(self.board) and x >= 0 and x < len(self.board[0])):
                    if self.board[y][x] == self.turn[0]:
                        for check in checks:
                            win_check = check(x, y, self.board, self.get_turn())
                            if win_check[0]:
                                return True, win_check[1]
        return False, []

    def check_draw(self):
        draw = True
        for square in self.board[0]:
            if square == "E":
                draw = False
        return draw

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
            has_won, row_tuples = self.check_win(x, y)
            if has_won:
                game_view.display_winner(self.turn, self, row_tuples)
                game_view.disable_all_drop_buttons()
                return False
            else:
                if self.check_draw():
                    game_view.display_draw(self)
                    return False
                else:
                    self.toggle_turn()
            return True
        return False
    
    def restart(self):
        main(self.menu)


def main(menu):
    board = setup_board()
    game = Game(board, menu)
    gv.GameView(game)

if __name__ == "__main__":
    main(None)
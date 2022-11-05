import game_view as gv

BOARD_X = 7
BOARD_Y = 6

def setup_board():
    board = [["E" for i in range(BOARD_X)] for j in range(BOARD_Y)]
    return board

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
        pass

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
            self.check_win(x, y)
            self.toggle_turn()
            return True
        return False

def main():
    board = setup_board()
    game = Game(board)
    game_view = gv.GameView(game)

if __name__ == "__main__":
    main()
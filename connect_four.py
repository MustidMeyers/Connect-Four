import tkinter as tk
import tkinter.font as font
from functools import partial

BOARD_X = 7
BOARD_Y = 6
EMPTY_BG = "grey"
EMPTY_FG = "black"
YELLOW_BG = "yellow"
YELLOW_FG = "black"
RED_BG = "red"
RED_FG = "black"
BUTTON_HEIGHT = 5
BUTTON_WIDTH = 13

def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.
    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.destroy()
    return geometry

def get_center_pos():
    geometry = get_curr_screen_geometry()
    x, y = geometry.split("+")[0].split("x")
    return int(x) // 4, int(y) // 10

def setup_board():
    board = [["E" for i in range(BOARD_X)] for j in range(BOARD_Y)]
    return board

def update_button(button: tk.Button, player: str):
    if player == "Y":
        button.configure(background = YELLOW_BG, foreground = YELLOW_FG)
    elif player == "R":
        button.configure(background = RED_BG, foreground = RED_FG)
    else:
        button.configure(background = EMPTY_BG, foreground = EMPTY_FG)

def setup_board_view(board, window: tk.Tk):
    buttons = [[] for i in range(len(board[0]))]
    for y in range(len(board)):
        for x in range(len(board[0])):
            temp_button = tk.Button(window, height = 5, width = 13)
            temp_button.grid(row = y, column = x)
            buttons[y].append(temp_button)

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

    def dropped_token(self, x):
        print(f"Dropped in {x}")


class GameView:
    def __init__(self, game: Game):
        self.buttons = [[] for i in range(len(self.game.get_board()[0]))]
        self.game = game
        self.drop_buttons = []
        self.main_window = tk.Tk()
        self.default_font = font.Font(family = "Helvetica", size = 20, weight = "bold")
        self.turn_label = tk.Label(self.main_window, text = f"{self.game.get_turn()} player's turn", font = self.default_font)
        self.turn_label.pack()
        spacer = tk.Label(self.main_window, font = self.default_font)
        spacer.pack()
        self.drop_canvas = tk.Canvas(self.main_window)
        self.drop_canvas.pack()
        self.setup_drop_buttons(self.game.get_board())
        spacer = tk.Label(self.main_window, font = self.default_font)
        spacer.pack()
        self.board_canvas = tk.Canvas(self.main_window)
        self.board_canvas.pack()
        self.setup_board_view(self.game.get_board())
        self.main_window.mainloop()
    
    def setup_drop_buttons(self, board):
        for x in range(len(board[0])):
            temp_button = tk.Button(self.drop_canvas, height = BUTTON_HEIGHT, width = BUTTON_WIDTH,
                                    command = partial(self.pressed_drop_button, x), cursor = "hand2")
            temp_button.grid(row = 0, column = x)
            self.drop_buttons.append(temp_button)

    def setup_board_view(self, board):
        for y in range(len(board)):
            for x in range(len(board[0])):
                temp_button = tk.Button(self.board_canvas, height = BUTTON_HEIGHT, width = BUTTON_WIDTH)
                temp_button["state"] = "disabled"
                temp_button.grid(row = y, column = x)
                self.buttons[y].append(temp_button)
    
    def pressed_drop_button(self, x):
        self.game.dropped_token(x)
        self.update_turn_label()
    
    def update_turn_label(self):
        self.turn_label.configure(text = f"{self.game.get_turn()} player's turn")

def main():
    board = setup_board()
    game = Game()
    game_view = GameView(board, game)
    # main_window = tk.Tk()
    # turn_label = tk.Label(main_window, text = "Player's turn")
    # turn_label.pack()
    # board_canvas = tk.Canvas(main_window)
    # board_canvas.pack()
    # setup_board_view(board, board_canvas)
    # main_window.mainloop()

if __name__ == "__main__":
    main()
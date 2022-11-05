import tkinter as tk
import tkinter.font as font
from functools import partial
import connect_four as cf

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

def get_colour_for_token(turn):
    if turn[0] == "Y":
        return YELLOW_BG, YELLOW_FG
    elif turn[0] == "R":
        return RED_BG, RED_FG
    else:
        return EMPTY_BG, EMPTY_FG

class GameView:
    def __init__(self, game: cf.Game):
        self.game = game
        self.buttons = [[] for i in range(len(self.game.get_board()[0]))]
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
    
    def disable_all_drop_buttons(self):
        for button in self.drop_buttons:
            button.configure(cursor = "")
            button["state"] = "disabled"

    def display_winner(self, turn):
        self.turn_label.configure(text = f"{turn} player won!")

    def update_button(self, x, y):
        bg, fg = get_colour_for_token(self.game.get_turn())
        self.buttons[y][x].configure(background = bg, foreground = fg)
        # if self.game.get_turn()[0] == "Y":
        #     self.buttons[y][x].configure(background = YELLOW_BG, foreground = YELLOW_FG)
        # elif self.game.get_turn()[0] == "R":
        #     self.buttons[y][x].configure(background = RED_BG, foreground = RED_FG)
        # else:
        #     self.buttons[y][x].configure(background = EMPTY_BG, foreground = EMPTY_FG)

    def pressed_drop_button(self, x):
        is_okay_drop = self.game.dropped_token(x, self)
        if is_okay_drop:
            self.update_turn_label()
    
    def update_turn_label(self):
        self.turn_label.configure(text = f"{self.game.get_turn()} player's turn")
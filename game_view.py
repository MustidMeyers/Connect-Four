import tkinter as tk
import tkinter.font as font
from functools import partial

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
    def __init__(self, game):
        self.game = game
        self.buttons = [[] for i in range(len(self.game.get_board()[0]))]
        self.drop_buttons = []
        self.main_window = tk.Tk()
        self.main_window.title("Connect 4")
        self.default_font = font.Font(family = "Helvetica", size = 20, weight = "bold")
        self.turn_label = tk.Label(self.main_window, text = f"{self.game.get_turn()} player's turn", font = self.default_font)
        self.turn_label.pack()
        spacer = tk.Label(self.main_window, font = self.default_font)
        spacer.pack()
        self.drop_canvas = tk.Canvas(self.main_window)
        self.drop_canvas.pack()
        self.setup_drop_buttons(self.game.get_board())
        self.setup_drop_bindings()
        self.spacer1 = tk.Label(self.main_window, font = self.default_font)
        self.spacer1.pack()
        self.board_canvas = tk.Canvas(self.main_window)
        self.board_canvas.pack()
        self.setup_board_view(self.game.get_board())
        self.main_window.mainloop()
    
    def setup_drop_bindings(self):
        self.drop_buttons[0].bind("<Enter>", func = lambda e: self.set_drop_button_colour(0))
        self.drop_buttons[0].bind("<Leave>", func = lambda e: self.drop_buttons[0].configure(background = "SystemButtonFace"))
        self.drop_buttons[1].bind("<Enter>", func = lambda e: self.set_drop_button_colour(1))
        self.drop_buttons[1].bind("<Leave>", func = lambda e: self.drop_buttons[1].configure(background = "SystemButtonFace"))
        self.drop_buttons[2].bind("<Enter>", func = lambda e: self.set_drop_button_colour(2))
        self.drop_buttons[2].bind("<Leave>", func = lambda e: self.drop_buttons[2].configure(background = "SystemButtonFace"))
        self.drop_buttons[3].bind("<Enter>", func = lambda e: self.set_drop_button_colour(3))
        self.drop_buttons[3].bind("<Leave>", func = lambda e: self.drop_buttons[3].configure(background = "SystemButtonFace"))
        self.drop_buttons[4].bind("<Enter>", func = lambda e: self.set_drop_button_colour(4))
        self.drop_buttons[4].bind("<Leave>", func = lambda e: self.drop_buttons[4].configure(background = "SystemButtonFace"))
        self.drop_buttons[5].bind("<Enter>", func = lambda e: self.set_drop_button_colour(5))
        self.drop_buttons[5].bind("<Leave>", func = lambda e: self.drop_buttons[5].configure(background = "SystemButtonFace"))
        self.drop_buttons[6].bind("<Enter>", func = lambda e: self.set_drop_button_colour(6))
        self.drop_buttons[6].bind("<Leave>", func = lambda e: self.drop_buttons[6].configure(background = "SystemButtonFace"))

    def set_drop_button_colour(self, i):
        bg, fg = get_colour_for_token(self.game.get_turn())
        self.drop_buttons[i].configure(background = bg, foreground = fg)

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

    def display_winner(self, turn, game, won_tuples):
        self.turn_label.configure(text = f"{turn} player won!")
        self.drop_canvas.pack_forget()
        self.spacer1.pack_forget()
        self.spacer1.pack()
        for x, y in won_tuples:
            self.buttons[y][x].configure(background = "green")
        game_over_buttons_canvas = tk.Canvas(self.main_window)
        game_over_buttons_canvas.pack()
        play_again_button = tk.Button(game_over_buttons_canvas, text = "Play again?", font = self.default_font,
                                        command = partial(self.play_again, game), cursor = "hand2")
        play_again_button.grid(row = 0, column = 0)
        menu_button = tk.Button(game_over_buttons_canvas, text = "Main menu", font = self.default_font,
                                command = partial(self.goto_menu, game), cursor = "hand2")
        menu_button.grid(row = 0, column = 1)
    
    def goto_menu(self, game):
        self.main_window.destroy()
        game.back_to_menu()

    def play_again(self, game):
        self.main_window.destroy()
        game.restart()


    def update_button(self, x, y):
        bg, fg = get_colour_for_token(self.game.get_turn())
        self.buttons[y][x].configure(background = bg, foreground = fg)

    def pressed_drop_button(self, x):
        is_okay_drop = self.game.dropped_token(x, self)
        if is_okay_drop:
            self.set_drop_button_colour(x)
            self.update_turn_label()
    
    def update_turn_label(self):
        self.turn_label.configure(text = f"{self.game.get_turn()} player's turn")
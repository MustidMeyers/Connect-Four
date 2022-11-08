import tkinter as tk
import tkinter.font as font
import connect_four_local as cfl
from functools import partial

class Menu:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("500x500")
        self.main_window.title("Connect 4 Menu")
        text_font = font.Font(family = "Helvetica", size = 20, weight = "bold")
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        welcome_label = tk.Label(self.main_window, text = "Welcome to Connect 4", font = text_font)
        welcome_label.pack()
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        play_local_button = tk.Button(self.main_window, text = "Play local", font = text_font,
                                        command=self.start_local, cursor = "hand2")
        play_local_button.pack()
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        play_local_button = tk.Button(self.main_window, text = "Play via socket", font = text_font,
                                        command=self.start_socket, cursor = "hand2")
        play_local_button.pack()
        spacer = tk.Label(self.main_window, font = text_font)
        spacer.pack()
        play_local_button = tk.Button(self.main_window, text = "Quit", font = text_font,
                                        command=quit, cursor = "hand2")
        play_local_button.pack()
        self.main_window.mainloop()
    
    def reset(self):
        self.__init__()

    def start_socket(self):
        pass

    def start_local(self):
        self.main_window.destroy()
        cfl.main(self)
    

def main():
    Menu()

if __name__ == "__main__":
    main()
""" Simply tetris game """
import arcade

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800

class Tetris(arcade.Window):
    """ main game class """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

def main():
    """ main function to initialize game """
    # open window
    window = Tetris(WINDOW_WIDTH, WINDOW_HEIGHT, "Tetris")
    arcade.run()

if __name__ == "__main__":
    main()
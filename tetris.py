""" Simply tetris game """
import arcade
import random
# Settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
# horizontal movement speed (the higher the value, the slower it moves)
MOVE_SPEED = 4
# The size of single square
BLOCKS_SCALE = 20
# BLOCKS WIDTH COORDINATE
I_BLOCK = ((0, 0), (1, 0), (2, 0), (-1,0))
J_BLOCK = ((0, 0), (1, 0), (-1, 0), (-1,1))
L_BLOCK = ((0, 0), (1, 0), (-1, 0), (1,1))
O_BLOCK = ((0, 0), (1, 0), (0, 1), (1,1))
S_BLOCK = ((0, 0), (-1, 0), (0, 1), (1,1))
T_BLOCK = ((0, 0), (-1, 0), (1, 0), (0,1))
Z_BLOCK = ((0, 1), (1, 1), (1, 0), (2,0))

class Block():
    """ create and hold actual block """
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 + BLOCKS_SCALE / 2
        self.y = WINDOW_HEIGHT / 2 + BLOCKS_SCALE / 2
        # randomly selects the type of block
        random_number = random.randint(0,6)
        if random_number == 0:
            self.type_of_block = I_BLOCK
        elif random_number == 1:
            self.type_of_block = J_BLOCK
        elif random_number == 2:
            self.type_of_block = L_BLOCK
        elif random_number == 3:
            self.type_of_block = O_BLOCK
        elif random_number == 4:
            self.type_of_block = S_BLOCK
        elif random_number == 5:
            self.type_of_block = T_BLOCK
        elif random_number == 6:
            self.type_of_block = Z_BLOCK

    def rotate(self):
        """ rotate the block """
        new_position = []
        for elem in self.type_of_block:
            new_position.append((elem[1], elem[0] * -1))
        # overwrite the positions of the squares in the block with new ones
        self.type_of_block = new_position

    def move_left(self):
        self.x -= BLOCKS_SCALE

    def move_right(self):
        self.x += BLOCKS_SCALE

    def on_draw(self):
        """ drow the block """
        for elem in self.type_of_block:
            arcade.draw_rectangle_filled(
                                        center_x= self.x + elem[0] * BLOCKS_SCALE,
                                        center_y= self.y + elem[1] * BLOCKS_SCALE,
                                        width= BLOCKS_SCALE,
                                        height= BLOCKS_SCALE,
                                        color= arcade.csscolor.WHITE)        

class Tetris(arcade.Window):
    """ main game class """
    # list of all squares which you have no control
    squares_list = []
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.move_left = False
        self.move_right = False
        # if it reaches MOVE_SPEED, the move will be made
        self.move_timer = 0
        # crate block
        self.block = Block()

    def on_key_press(self, symbol: int, modifiers: int):
        # rotate the block
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.block.rotate()
        # move left
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.move_left = True
        # move right
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.move_right = True

    def on_key_release(self, symbol: int, modifiers: int):
        # stop moving left
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.move_left = False
            self.move_timer = 0
        # stop moving right
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.move_right = False
            self.move_timer = 0

    def update(self, delta_time: float):
        # reset movement speed counter
        if self.move_timer == MOVE_SPEED:
            self.move_timer = 0
        # move left
        if self.move_left == True:
            if self.move_timer == 0:
                self.block.move_left()
            self.move_timer += 1
        # move right
        if self.move_right == True:
            if self.move_timer == 0:
                self.block.move_right()
            self.move_timer += 1

    def on_draw(self):
        arcade.start_render()
        self.block.on_draw()

def main():
    """ main function to initialize game """
    # open window
    window = Tetris(WINDOW_WIDTH, WINDOW_HEIGHT, "Tetris")
    arcade.run()

if __name__ == "__main__":
    main()
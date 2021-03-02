""" Simply tetris game """
import arcade
import random
# Settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
# horizontal movement speed (the higher the value, the slower it moves)
MOVE_SPEED = 4
FALL_SPEED = 5
# The size of single square
BLOCKS_SCALE = 20
# BLOCKS WIDTH COORDINATE (x, y)
I_BLOCK = ((0, 0), (1, 0), (2, 0), (-1,0))
J_BLOCK = ((0, 0), (1, 0), (-1, 0), (-1,1))
L_BLOCK = ((0, 0), (1, 0), (-1, 0), (1,1))
O_BLOCK = ((0, 0), (1, 0), (0, 1), (1,1))
S_BLOCK = ((0, 0), (-1, 0), (0, 1), (1,1))
T_BLOCK = ((0, 0), (-1, 0), (1, 0), (0,1))
Z_BLOCK = ((0, 1), (1, 1), (1, 0), (2,0))

def round_y(y):
    """ round y position off block """
    return round(y / BLOCKS_SCALE) * BLOCKS_SCALE

class Block():
    """ create and hold actual block """
    # list of all squares which you have no control
    squares_list = []
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 + BLOCKS_SCALE / 2
        self.y = WINDOW_HEIGHT
        self.can_move_left = True
        self.can_move_right = True
        # if square is on ground change to True
        self.square_on_ground = False
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
            new_position.append((elem[1], -elem[0]))
        # overwrite the positions of the squares in the block with new ones
        self.type_of_block = new_position

    def move_left(self):
        if self.can_move_left:
            self.x -= BLOCKS_SCALE

    def move_right(self):
        if self.can_move_right:
            self.x += BLOCKS_SCALE

    def on_ground(self):
        """ checks if a square is on the ground, if so moves all squares to square_list """
        for square in self.type_of_block:
            position_x = self.x + square[0] * BLOCKS_SCALE
            position_y = self.y + square[1] * BLOCKS_SCALE
            # if square is on the bottom off the screen
            if position_y <= BLOCKS_SCALE:
                self.square_on_ground = True
                break

            for sq in self.squares_list:
                # if square is on the other square from square_list
                if position_x == sq[0]:
                    if position_y <= sq[1] + BLOCKS_SCALE and position_y > sq[1]:
                        self.square_on_ground = True
                        break
        
        if self.square_on_ground:
            # move all square from block to square_list and delet object 
            for square in self.type_of_block:
                Block.squares_list.append([self.x + square[0] * BLOCKS_SCALE, round_y(self.y + square[1] * BLOCKS_SCALE)])

    def update(self):
        self.on_ground()
        # block fall down
        if not self.square_on_ground:
            self.y -= FALL_SPEED

    def on_draw(self):
        self.can_move_left = True
        self.can_move_right = True
        """ drow the block """
        # draw all square where you can't move
        for square in self.squares_list:
            arcade.draw_rectangle_filled(
                                        center_x= square[0],
                                        center_y= square[1],
                                        width= BLOCKS_SCALE,
                                        height= BLOCKS_SCALE,
                                        color= arcade.csscolor.WHITE)            

        # draw all square in the block where you can move 
        for square in self.type_of_block:
            position_x = self.x + square[0] * BLOCKS_SCALE
            position_y = self.y + square[1] * BLOCKS_SCALE
            arcade.draw_rectangle_filled(
                                        center_x= position_x,
                                        center_y= position_y,
                                        width= BLOCKS_SCALE,
                                        height= BLOCKS_SCALE,
                                        color= arcade.csscolor.WHITE)        
            # disable movement if any block is next to the wall
            if self.x - BLOCKS_SCALE / 2 + square[0] * BLOCKS_SCALE == 0:
                self.can_move_left = False
            if self.x + BLOCKS_SCALE / 2 + square[0] * BLOCKS_SCALE == WINDOW_WIDTH:
                self.can_move_right = False
            # disable movement if any block is next to the other square
            for sq in self.squares_list:
                if position_y <= sq[1] + BLOCKS_SCALE / 2 and position_y >= sq[1] - BLOCKS_SCALE / 2:
                    if position_x == sq[0] - BLOCKS_SCALE:
                        self.can_move_right = False
                    if position_x == sq[0] + BLOCKS_SCALE:
                        self.can_move_left = False

class Tetris(arcade.Window):
    """ main game class """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.move_left = False
        self.move_right = False
        self.move_down = False
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
        # move down
        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.move_down = True

    def on_key_release(self, symbol: int, modifiers: int):
        # stop moving left
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.move_left = False
            self.move_timer = 0
        # stop moving right
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.move_right = False
            self.move_timer = 0
        # stop moving down
        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.move_down = False

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

        self.block.update()
        # if block is on ground make new object
        if self.block.square_on_ground:
            self.block = Block()

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
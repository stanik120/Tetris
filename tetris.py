"""
Simply tetris game.

    File name: tetris.py
    Author: Stanik
    Email: stanik@tuta.io
    GitHub: https://github.com/stanik120
    License: GPL 3
    Python Version: 3.9.1
    
"""
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
    """ round y position of block """
    return round(y / BLOCKS_SCALE) * BLOCKS_SCALE

class Block():
    """ create and hold actual block """
    # list of all squares which you have no control
    squares_list = []
    point = 0
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 + BLOCKS_SCALE / 2
        self.y = WINDOW_HEIGHT
        self.can_move_left = True
        self.can_move_right = True
        self.move_down = False
        self.color = None
        # if square is on ground change to True
        self.square_on_ground = False
        # randomly selects the type of block
        random_number = random.randint(0,6)
        if random_number == 0:
            self.type_of_block = I_BLOCK
            self.color = arcade.csscolor.BLUE
        elif random_number == 1:
            self.type_of_block = J_BLOCK
            self.color = arcade.csscolor.RED
        elif random_number == 2:
            self.type_of_block = L_BLOCK
            self.color = arcade.csscolor.YELLOW
        elif random_number == 3:
            self.type_of_block = O_BLOCK
            self.color = arcade.csscolor.GREEN
        elif random_number == 4:
            self.type_of_block = S_BLOCK
            self.color = arcade.csscolor.ORANGE
        elif random_number == 5:
            self.type_of_block = T_BLOCK
            self.color = arcade.csscolor.HOTPINK
        elif random_number == 6:
            self.type_of_block = Z_BLOCK
            self.color = arcade.csscolor.PURPLE

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

    def line_check(self):
        """ checks if any line is full, if so removes squares from it and adds points """
        square_line_count = {}
        # create key in square_line_count dictionary for other line and add to them count of all square in this line
        for square in Block.squares_list:
            if square[1] in square_line_count:
                square_line_count[square[1]] += 1
            else:
                square_line_count[square[1]] = 1
        # check count of square in line if is full delet square from square_list and add point and move all other square to the bootom
        for k, v in square_line_count.items():
            if v == WINDOW_WIDTH / BLOCKS_SCALE:
                square_to_remove = []
                for square in Block.squares_list:
                    if square[1] == k:
                        square_to_remove.append(square)                        
                    # move square from top of the deleted square to the bootom
                    if square[1] > k:
                        square[1] -= BLOCKS_SCALE
                # remove square
                for square in square_to_remove:
                    Block.squares_list.remove(square)
                Block.point += 1

    def on_ground(self):
        """ checks if a square is on the ground, if so moves all squares to square_list """
        for square in self.type_of_block:
            position_x = self.x + square[0] * BLOCKS_SCALE
            position_y = self.y + square[1] * BLOCKS_SCALE
            # if square is on the bottom of the screen
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
                Block.squares_list.append([self.x + square[0] * BLOCKS_SCALE, round_y(self.y + square[1] * BLOCKS_SCALE), self.color])
            self.line_check()

    def update(self):
        self.on_ground()
        # block fall down
        if not self.square_on_ground:
            if self.move_down:
                self.y -= FALL_SPEED * 2
            else:
                self.y -= FALL_SPEED

    def on_draw(self):
        """ drow the block """
        # draw point text
        arcade.draw_text(
                        text = str(self.point),
                        start_x = 10,
                        start_y = WINDOW_HEIGHT - 25,
                        color = arcade.csscolor.WHITE,
                        font_size = BLOCKS_SCALE,
                        bold = True)
        self.can_move_left = True
        self.can_move_right = True
        # draw all square where you can't move
        for square in self.squares_list:
            arcade.draw_rectangle_filled(
                                        center_x= square[0],
                                        center_y= square[1],
                                        width= BLOCKS_SCALE,
                                        height= BLOCKS_SCALE,
                                        color= square[2])

        # draw all square in the block where you can move 
        for square in self.type_of_block:
            position_x = self.x + square[0] * BLOCKS_SCALE
            position_y = self.y + square[1] * BLOCKS_SCALE
            arcade.draw_rectangle_filled(
                                        center_x= position_x,
                                        center_y= position_y,
                                        width= BLOCKS_SCALE,
                                        height= BLOCKS_SCALE,
                                        color= self.color)        
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
        self.game_over = False
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
            self.block.move_down = True
        # game over
        if self.game_over and symbol == arcade.key.ENTER:
            Block.squares_list.clear()
            Block.point = 0
            self.game_over = False
            self.block = Block()

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
            self.block.move_down = False

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
        if not self.game_over:
            self.block.update()
        # if block is on ground make new object
        if not self.game_over and self.block.square_on_ground:
            if self.block.y == WINDOW_HEIGHT:
                self.game_over = True
                del(self.block)
            else:
                self.block = Block()
            
    def on_draw(self):
        arcade.start_render()
        if not self.game_over:
            self.block.on_draw()
        if self.game_over:
            arcade.draw_text(
                text = "Game Over",
                start_x = 0,
                start_y = WINDOW_HEIGHT / 2,
                font_size = BLOCKS_SCALE * 2,
                color = arcade.csscolor.GREEN,
                bold = True,
                width = WINDOW_WIDTH,
                align = "center"
                )
            arcade.draw_text(
                text = f"You got {Block.point} points",
                start_x = 0,
                start_y = WINDOW_HEIGHT / 2 - BLOCKS_SCALE * 2,
                font_size = BLOCKS_SCALE * 2,
                color = arcade.csscolor.GREEN,
                bold = True,
                width = WINDOW_WIDTH,
                align = "center"
                )

def main():
    """ main function to initialize game """
    # open window
    window = Tetris(WINDOW_WIDTH, WINDOW_HEIGHT, "Tetris")
    arcade.run()

if __name__ == "__main__":
    main()

"""
Better Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
This is slightly better than sprite_move_keyboard.py example
in how it works, but also slightly more complex.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard_better
"""

import arcade
import random

# File Paths for Player and Field Images; You can change them to what you want
COMPUTER_PATH = "/Users/udbhav/Desktop/"

STARTING_MENU_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/StartingMenuImage.jpg"
CLOSING_MENU_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/GameOverScreenImage.jpg"
FIELD_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/FootballBackgroundImage1.jpeg"
PLAYER1_OPTION1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/image4.png"
PLAYER1_OPTION2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/image5.png"
PLAYER2_OPTION1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/image1.png"
PLAYER2_OPTION2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TestingRunningImages/image2.png"

# Image File Paths for Player Images
BLF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue1.png"
BLF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue2.png"
BRF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/BluePlayerAnimationFacingRightFrame1.png"
BRF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/BluePlayerAnimationFacingRightFrame2.png"
RLF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/RedPlayerAnimationFacingRightFrame1.png"
RLF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red2.png"
RRF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red1.png"
RRF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/RedPlayerAnimationFacingRightFrame2.png"

player1_color = ""
player2_color = ""

# Keep track of who won
winning_player = ""
player1_final_score = 0
player2_final_score = 0

FIELD_WIDTH = 4862  # 1500, 2431, 4862  width = height * 2.43111831
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000  # 617, 1000  height = width / 0.411333333333
SCREEN_TITLE = "1v1 Football Run"

# Quarter Duration
SECONDS_PER_QUARTER = 120

FRAMES_PER_QUARTER = SECONDS_PER_QUARTER * 60

# Fumble Chance
FUMBLE_CHANCE = 2
# Keep track of which direction they are facing
LEFT_DIRECTION = 0
RIGHT_DIRECTION = 1

# Powerups
SPEED_BOOST_DURATION = 60

SPRITE_SCALING = SCREEN_HEIGHT/1000

MOVEMENT_SPEED = 4 #4 #2.5
PIXELS_FOR_FIRST_DOWN = FIELD_WIDTH/(12.7118644068/1.5)
TIME_BETWEEN_PLAYS = 200

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second image being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Player(arcade.Sprite):

    def __init__(self, color, direction, player_number):
        super().__init__()
        color == "red"
        self.direction = direction
        self.walk_textures = []

        self.time_interval = 0
        self.player_number = player_number
        self.cur_texture = 0
        self.scale = SPRITE_SCALING
        if player_number == 1:
            if color == "red":
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red"
            else:
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue"
            for i in range(2):
                texture = load_texture_pair(f"{main_file_name}{i+1}.png")
                self.walk_textures.append(texture)
            self.texture = self.walk_textures[0][direction]
        else:
            if color == "red":
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red"
            else:
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue"
            for i in range(2):
                texture = load_texture_pair(f"{main_file_name}{i+1}.png")
                self.walk_textures.append(texture)
            self.texture = self.walk_textures[0][direction]

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > FIELD_WIDTH - 1:
            self.right = FIELD_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        self.update_animation()

    def update_animation(self):
        if self.time_interval == 0:
            self.time_interval = 10
            if self.change_x < 0:
                self.direction = LEFT_DIRECTION

                self.cur_texture += 1
                if self.cur_texture > 1:
                    self.cur_texture = 0

                self.texture = self.walk_textures[self.cur_texture][LEFT_DIRECTION]
                return
            if self.change_x > 0:
                self.direction = RIGHT_DIRECTION

                self.cur_texture += 1
                if self.cur_texture > 1:
                    self.cur_texture = 0

                self.texture = self.walk_textures[self.cur_texture][RIGHT_DIRECTION]
                return
            if self.change_y != 0:
                self.cur_texture += 1
                if self.cur_texture > 1:
                    self.cur_texture = 0
                self.texture = self.walk_textures[self.cur_texture][self.direction]
        else:
            self.time_interval -= 1

    def reset_animations(self):
        if self.player_number == 1:
            self.texture = self.walk_textures[0][0]
        else:
            self.texture = self.walk_textures[0][1]

class ClosingMenu(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(CLOSING_MENU_IMAGE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.window.set_mouse_visible(True)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

        if player1_final_score > player2_final_score:
            arcade.draw_text("Player1 Wins!", 865, 821,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
        elif player1_final_score < player2_final_score:
            arcade.draw_text("Player2 Wins!", 865, 821,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
        else:
            arcade.draw_text("It's a Tie!", 865, 821,
                             arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Close Game", 383, 211,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Play Again", 1197, 211,
                         arcade.color.WHITE, font_size=50, anchor_x="center")



    def on_mouse_press(self, x, y, button, modifiers):
        global player1_selected_option
        global player2_selected_option

        if 699 > x > 67 and 288 > y > 135:

            arcade.close_window()

        elif 1531 > x > 863 and 288 > y > 135:

            game_view = StartingMenu()
            self.window.show_view(game_view)

class StartingMenu(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(STARTING_MENU_IMAGE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)




    def on_mouse_press(self, x, y, button, modifiers):
        global player1_color
        global player2_color
        global player_selection_combo
        if 489 > x > 254 and 617 > y > 436:
            player1_color = "blue"
            player2_color = "red"

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif 489 > x > 254 and 407 > y > 226:
            player1_color = "red"
            player2_color = "blue"

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif 1395 > x > 1160 and 615 > y > 437:
            player1_color = "red"
            player2_color = "blue"

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif 1395 > x > 1160 and 410 > y > 228:
            player1_color = "blue"
            player2_color = "red"

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__()

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Camera
        self.camera = None
        self.gui_camera = None

        # Variables that will hold sprite lists
        self.player_list = None

        # For Tracking Player Speed
        self.player1_movement_speed = MOVEMENT_SPEED
        self.player2_movement_speed = MOVEMENT_SPEED


        # Set up the player info
        self.player_sprite = None
        self.player_sprite2 = None
        self.background = None

        # Used for Animation
        self.player1_current_frame = None
        self.player2_current_frame = None

        # Make the scene
        self.scene = None

        # Keep track of player turn and time
        self.player_turn = 0
        self.down_number = 1
        self.pixels_left = PIXELS_FOR_FIRST_DOWN
        self.time_marker = 0
        self.position_for_first_down = None

        # Used for Touchdown Text and Turnover Text
        self.did_player1_touchdown = False
        self.did_player2_touchdown = False
        self.is_there_turnover = False
        self.is_there_fumble = False
        self.is_player1_tackled = False
        self.is_player2_tackled = False

        # Keeping Track of non-boosting movement speed
        self.player1_non_boosting_movement_speed = MOVEMENT_SPEED
        self.player2_non_boosting_movement_speed = MOVEMENT_SPEED

        # Yards Left
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.v_pressed = False
        self.m_pressed = False

        # Boost
        self.is_player1_boosting = False
        self.is_player2_boosting = False
        self.player1_boost_left = SPEED_BOOST_DURATION
        self.player2_boost_left = SPEED_BOOST_DURATION

        # Use Height and Width to track variables.
        self.left_end_of_endzone = int(FIELD_WIDTH / 34.8837209)
        self.right_end_of_endzone = int(FIELD_WIDTH - self.left_end_of_endzone)
        self.pixels_for_5_yards = int(FIELD_WIDTH / (12.7118644068 * 2))
        self.player1_touchdown = self.left_end_of_endzone + PIXELS_FOR_FIRST_DOWN/1.5
        self.player2_touchdown = self.right_end_of_endzone - PIXELS_FOR_FIRST_DOWN/1.5
        self.player2_pos_on_first_and_goal = [int(self.player1_touchdown - (FIELD_WIDTH / 500)), int(SCREEN_HEIGHT / 2)]
        self.player1_pos_on_first_and_goal = [int(self.player2_touchdown + (FIELD_WIDTH / 500)), int(SCREEN_HEIGHT / 2)]

        # Set Player Position
        # Positioning the Players: Player1's turn on Offense
        self.P1_P1T_START_X = self.player2_touchdown
        self.P1_P1T_START_Y = int(SCREEN_HEIGHT / 2)
        self.P2_P1T_START_X = self.player2_touchdown - self.pixels_for_5_yards
        self.P2_P1T_START_Y = int(SCREEN_HEIGHT / 2)

        # Positioning the Players: Player2's turn on Offense
        self.P1_P2T_START_X = self.player1_touchdown + self.pixels_for_5_yards
        self.P1_P2T_START_Y = int(SCREEN_HEIGHT / 2)
        self.P2_P2T_START_X = self.player1_touchdown
        self.P2_P2T_START_Y = int(SCREEN_HEIGHT / 2)

        # Track the score
        self.player1_score = 0
        self.player2_score = 0

        # Set up the time factor
        self.quarter_number = 1
        self.frames_left_in_quarter = FRAMES_PER_QUARTER

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Initialize the Scene
        self.scene = arcade.Scene()

        # Create sprite List
        self.scene.add_sprite_list("Player")

        # Camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Set up the Background
        self.background = arcade.load_texture(FIELD_IMAGE)

        # Set up the player
        self.player_sprite = Player(player1_color,
                                    LEFT_DIRECTION, 1)
        self.player1_current_frame = 1
        self.player_sprite2 = Player(player2_color,
                                    RIGHT_DIRECTION, 2)
        self.player2_current_frame = 3

        self.player_list.append(self.player_sprite)
        self.player_list.append(self.player_sprite2)
        self.scene.add_sprite("Player", self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite2)

        # Start Positions based on which player's turn it is
        if self.player_turn == 0:
            self.position_for_first_down = self.P1_P1T_START_X - PIXELS_FOR_FIRST_DOWN
            self.player_sprite.center_x = self.P1_P1T_START_X
            self.player_sprite.center_y = self.P1_P1T_START_Y
            self.player_sprite2.center_x = self.P2_P1T_START_X
            self.player_sprite2.center_y = self.P2_P1T_START_Y
        else:
            self.position_for_first_down = self.P2_P2T_START_X + PIXELS_FOR_FIRST_DOWN
            self.player_sprite.center_x = self.P1_P2T_START_X
            self.player_sprite.center_y = self.P1_P2T_START_Y
            self.player_sprite2.center_x = self.P2_P2T_START_X
            self.player_sprite2.center_y = self.P2_P2T_START_Y

    def if_player1_tackled(self, player1_x_coordinate):
        # Create a delay in the game
        self.time_marker = TIME_BETWEEN_PLAYS

        # Set player position after being hit
        self.player_sprite.center_x = player1_x_coordinate
        self.player_sprite.center_y = int(SCREEN_HEIGHT / 2)


        # Check for touchdown
        if player1_x_coordinate <= self.player1_touchdown:
            self.player1_boost_left = SPEED_BOOST_DURATION
            self.player2_boost_left = SPEED_BOOST_DURATION
            self.did_player1_touchdown = True
            self.player1_score += 7
            self.player_turn = 1
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # Check if first down is necessary
        elif self.position_for_first_down >= player1_x_coordinate:
            # If we are within 10 yards of the endzone
            if (player1_x_coordinate - PIXELS_FOR_FIRST_DOWN) <= self.player1_touchdown:
                self.position_for_first_down = self.player1_touchdown
                self.pixels_left = player1_x_coordinate - self.player1_touchdown
                self.down_number = 1

                # Set player2's position right on the endzone
                self.player_sprite2.center_x = self.player2_pos_on_first_and_goal[0]
                self.player_sprite2.center_y = self.player2_pos_on_first_and_goal[1]
            # If the player is not within 10 yards of the endzone.
            else:
                self.position_for_first_down = player1_x_coordinate - PIXELS_FOR_FIRST_DOWN
                self.pixels_left = PIXELS_FOR_FIRST_DOWN
                self.down_number = 1

                # Set player2's position 5 yards back
                self.player_sprite2.center_x = player1_x_coordinate - self.pixels_for_5_yards
                self.player_sprite2.center_y = int(SCREEN_HEIGHT / 2)

        # If it is not first down or touchdown, the down number increases.
        else:
            if self.down_number == 4:
                self.player_turn = 1
                self.down_number = 1
                self.pixels_left = PIXELS_FOR_FIRST_DOWN
                self.is_there_turnover = True
                self.setup()
            else:
                self.down_number += 1
                self.pixels_left = player1_x_coordinate - self.position_for_first_down

                # Set player2's position 5 yards back
                self.player_sprite2.center_x = player1_x_coordinate - self.pixels_for_5_yards
                self.player_sprite2.center_y = int(SCREEN_HEIGHT / 2)

    def if_player2_tackled(self, player2_x_coordinate):
        # Create a delay in the game
        self.time_marker = TIME_BETWEEN_PLAYS

        # Set player position after being hit
        self.player_sprite2.center_x = player2_x_coordinate
        self.player_sprite2.center_y = int(SCREEN_HEIGHT / 2)

        # Check for touchdown®
        if player2_x_coordinate >= self.player2_touchdown:
            self.player1_boost_left = SPEED_BOOST_DURATION
            self.player2_boost_left = SPEED_BOOST_DURATION
            self.did_player2_touchdown = True
            self.player2_score += 7
            self.player_turn = 0
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # Check if first down is necessary
        elif self.position_for_first_down <= player2_x_coordinate:
            if (player2_x_coordinate + PIXELS_FOR_FIRST_DOWN) >= self.player2_touchdown:
                self.position_for_first_down = self.player2_touchdown
                self.pixels_left = self.player2_touchdown - player2_x_coordinate
                self.down_number = 1

                # Set player1's position some yards behind the end zone
                self.player_sprite.center_x = self.player1_pos_on_first_and_goal[0]
                self.player_sprite.center_y = self.player1_pos_on_first_and_goal[1]
            else:
                self.position_for_first_down = player2_x_coordinate + PIXELS_FOR_FIRST_DOWN
                self.pixels_left = PIXELS_FOR_FIRST_DOWN
                self.down_number = 1

                # Set player1's position 5 yards in front
                self.player_sprite.center_x = player2_x_coordinate + self.pixels_for_5_yards
                self.player_sprite.center_y = int(SCREEN_HEIGHT / 2)

        # If it is not first down or touchdown, the down number increases.
        else:
            if self.down_number == 4:
                self.player_turn = 0
                self.down_number = 1
                self.pixels_left = PIXELS_FOR_FIRST_DOWN
                self.is_there_turnover = True
                self.setup()
            else:
                self.down_number += 1
                self.pixels_left = self.position_for_first_down - player2_x_coordinate

                # Set player1's position 5 yards in front
                self.player_sprite.center_x = player2_x_coordinate + self.pixels_for_5_yards
                self.player_sprite.center_y = int(SCREEN_HEIGHT / 2)

    def player1_turn(self):
        random_num = random.randint(1, 2)
        if random_num == 2:
            self.player1_movement_speed -= MOVEMENT_SPEED/300

        if self.player1_movement_speed <= 0:
            self.player1_movement_speed = 0
            self.player1_non_boosting_movement_speed = self.player1_movement_speed


        # Update the player
        self.player_list.update()
        self.frames_left_in_quarter -= 1

        # Check if player has been tackled and get the coordinates
        is_hit = arcade.check_for_collision(self.player_sprite, self.player_sprite2)
        player1_x_coordinate = self.player_sprite.center_x

        # Check for our of bounds
        if self.player_sprite.center_y > (
                SCREEN_HEIGHT - int(SCREEN_HEIGHT / 16.6666666)) or self.player_sprite.center_y < int(
                SCREEN_HEIGHT / 16.6666666):
            self.if_player1_tackled(player1_x_coordinate)


        # Check if the player scored a touchdown without being tackled
        if player1_x_coordinate <= self.player1_touchdown:
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            self.player1_boost_left = SPEED_BOOST_DURATION
            self.player2_boost_left = SPEED_BOOST_DURATION
            self.did_player1_touchdown = True
            self.player1_score += 7
            self.player_turn = 1
            self.down_number = 1
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # If the player has been hit, and if so, if their y_coordinate are close enough for tackling to be possible
        if is_hit is True and abs(self.player_sprite.center_y - self.player_sprite2.center_y) < self.pixels_for_5_yards/5:
            self.if_player1_tackled(player1_x_coordinate)



    def player2_turn(self):
        random_num = random.randint(1, 2)
        if random_num == 2:
            self.player2_movement_speed -= MOVEMENT_SPEED / 300

        if self.player2_movement_speed <= 0:
            self.player2_movement_speed = 0
            self.player2_non_boosting_movement_speed = self.player2_movement_speed

        self.player_list.update()
        self.frames_left_in_quarter -= 1

        # Check if player has been tackled and get the coordinates
        is_hit = arcade.check_for_collision(self.player_sprite, self.player_sprite2)
        player2_x_coordinate = self.player_sprite2.center_x

        # Check for our of bounds
        if self.player_sprite2.center_y > (
                SCREEN_HEIGHT - int(SCREEN_HEIGHT / 16.6666666)) or self.player_sprite2.center_y < int(
            SCREEN_HEIGHT / 16.6666666):
            self.if_player2_tackled(player2_x_coordinate)

        # Check if the player scored a touchdown without being tackled
        if player2_x_coordinate >= self.player2_touchdown:
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            self.player1_boost_left = SPEED_BOOST_DURATION
            self.player2_boost_left = SPEED_BOOST_DURATION
            self.did_player2_touchdown = True
            self.player2_score += 7
            self.player_turn = 0
            self.down_number = 1
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # If the player has been hit, and if so, if their y_coordinate are close enough for tackling to be possible
        if is_hit is True and abs(self.player_sprite2.center_y - self.player_sprite.center_y) < self.pixels_for_5_yards/5:
            self.if_player2_tackled(player2_x_coordinate)


    def center_camera_to_player(self):
        if (self.player_turn == 0):
            screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)

            # Don't let camera travel past 0
            if screen_center_x < 0:
                screen_center_x = 0
            elif self.player_sprite.center_x + self.camera.viewport_width / 2 > FIELD_WIDTH:
                screen_center_x = FIELD_WIDTH - self.camera.viewport_width

            player_centered = screen_center_x, 0

            self.camera.move_to(player_centered)
        else:
            screen_center_x = self.player_sprite2.center_x - (self.camera.viewport_width / 2)

            # Don't let camera travel past 0
            if screen_center_x < 0:
                screen_center_x = 0
            elif self.player_sprite2.center_x + self.camera.viewport_width / 2 > FIELD_WIDTH:
                screen_center_x = FIELD_WIDTH - self.camera.viewport_width

            player_centered = screen_center_x, 0

            self.camera.move_to(player_centered)



    def text_changer(self, num):
        if num == 1:
            return "1st"
        elif num == 2:
            return "2nd"
        elif num == 3:
            return "3rd"
        else:
            return "4th"

    def player1_touchdown_text(self):
        arcade.draw_text(
            "Player1 Touchdown",
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-200,
            arcade.csscolor.INDIANRED,
            50,
            anchor_x="center",
            font_name="arial"
        )

    def player2_touchdown_text(self):
        arcade.draw_text(
            "Player2 Touchdown",
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-200,
            arcade.csscolor.INDIANRED,
            50,
            anchor_x="center",
            font_name= "arial"
        )

    def time_calculator(self):
        seconds = self.frames_left_in_quarter / 60
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds}"
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.window.clear()

        # Activate the Camera
        self.camera.use()

        # Draw the Background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            FIELD_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Draw the players
        self.scene.draw()

        # Activate the Gui Camera to draw stationary things.
        self.gui_camera.use()


        # Draw the score and Down Number and Yards
        score_text = f"Score: {self.player1_score} - {self.player2_score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        if (self.pixels_left < PIXELS_FOR_FIRST_DOWN/10):
            yards_left = "inches"
        else:
            yards_left = int(self.pixels_left / (PIXELS_FOR_FIRST_DOWN / 15))
        down_text = f"{self.text_changer(self.down_number)} & {yards_left}"
        arcade.draw_text(
            down_text,
            10,
            SCREEN_HEIGHT - 20,
            arcade.csscolor.WHITE,
            18
        )
        player_turn_text = f"Player {self.player_turn + 1} Posession"
        arcade.draw_text(
            player_turn_text,
            300,
            SCREEN_HEIGHT - 20,
            arcade.csscolor.WHITE,
            18
        )
        quarter_number_text = f"{self.text_changer(self.quarter_number)} Quarter  {self.time_calculator()}"
        arcade.draw_text(
            quarter_number_text,
            600,
            SCREEN_HEIGHT - 20,
            arcade.csscolor.WHITE,
            18
        )

        if self.did_player1_touchdown:
            self.player1_touchdown_text()
        elif self.did_player2_touchdown:
            self.player2_touchdown_text()
        elif self.is_there_turnover:
            self.turnover_text()
        if self.is_there_fumble:
            self.print_if_fumble()

        if self.time_marker > 150:
            self.print_time_delay("3...")
        elif self.time_marker > 100:
            self.print_time_delay("2...")
        elif self.time_marker > 50:
            self.print_time_delay("1...")
        elif self.time_marker > 0:
            self.print_time_delay("Go!")

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

    def turnover_text(self):
        arcade.draw_text(
            "Turnover",
            600,
            SCREEN_HEIGHT - 300,
            arcade.csscolor.AQUAMARINE,
            50
        )

    def update_player_speed(self):



        # Calculate speed based on the keys pressed

        self.player_sprite.change_x = 0

        self.player_sprite.change_y = 0

        self.player_sprite2.change_x = 0

        self.player_sprite2.change_y = 0



        if self.up_pressed and not self.down_pressed:

            self.player_sprite.change_y = self.player1_movement_speed

        elif self.down_pressed and not self.up_pressed:

            self.player_sprite.change_y = -self.player1_movement_speed

        if self.left_pressed and not self.right_pressed:

            self.player_sprite.change_x = -self.player1_movement_speed

        elif self.right_pressed and not self.left_pressed:

            self.player_sprite.change_x = self.player1_movement_speed

        if self.w_pressed and not self.s_pressed:

            self.player_sprite2.change_y = self.player2_movement_speed

        elif self.s_pressed and not self.w_pressed:

            self.player_sprite2.change_y = -self.player2_movement_speed

        if self.a_pressed and not self.d_pressed:

            self.player_sprite2.change_x = -self.player2_movement_speed

        elif self.d_pressed and not self.a_pressed:

            self.player_sprite2.change_x = self.player2_movement_speed

    def on_update(self, delta_time = 1/60):
        """ Movement and game logic """
        if self.player1_boost_left <= 0:
            self.w_pressed = False
        if self.player2_boost_left <= 0:
            self.v_pressed = False

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        if self.frames_left_in_quarter == 0:
            if self.quarter_number == 4:

                global player1_final_score
                global player2_final_score
                player1_final_score = self.player1_score
                player2_final_score = self.player2_score

                game_view = ClosingMenu()
                self.window.show_view(game_view)
            else:
                self.quarter_number += 1
                self.frames_left_in_quarter = FRAMES_PER_QUARTER

        if self.time_marker != 0:

            if self.player_turn == 0:
                self.player1_movement_speed = MOVEMENT_SPEED - MOVEMENT_SPEED / 10
                self.player2_movement_speed = MOVEMENT_SPEED
            else:
                self.player1_movement_speed = MOVEMENT_SPEED
                self.player2_movement_speed = MOVEMENT_SPEED - MOVEMENT_SPEED / 10
            self.time_marker -= 1
            self.player_sprite.reset_animations()
            self.player_sprite2.reset_animations()
            self.is_player2_boosting = False
            self.is_player1_boosting = False

        elif self.player_turn == 0:
            self.did_player1_touchdown = False
            self.did_player2_touchdown = False
            self.is_there_turnover = False
            self.is_there_fumble = False
            self.is_player1_tackled = False
            self.is_player2_tackled = False

            self.player1_turn()

        else:
            self.did_player1_touchdown = False
            self.did_player2_touchdown = False
            self.is_there_turnover = False
            self.is_there_fumble = False
            self.is_player1_tackled = False
            self.is_player2_tackled = False

            self.player2_turn()

        self.center_camera_to_player()

    def print_time_delay(self, text):
        arcade.draw_text(
            text,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 700,
            arcade.csscolor.CORNFLOWER_BLUE,
            50,
            anchor_x="center",
            font_name="arial"
        )

    def print_if_fumble(self):
        if self.player_turn == 0:
            x_coordinate = self.player_sprite.center_x + 50
            y_coordinate = self.player_sprite.center_y
        else:
            x_coordinate = self.player_sprite2.center_x + 50
            y_coordinate = self.player_sprite2.center_y
        arcade.draw_text(
            "Fumble",
            x_coordinate,
            y_coordinate,
            arcade.csscolor.CORNFLOWER_BLUE,
            18,
            anchor_x="center",
            font_name="arial"
        )

    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """


        if key == arcade.key.UP:

            self.up_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.DOWN:

            self.down_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.LEFT:

            self.left_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.RIGHT:

            self.right_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.W:

            self.w_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.S:

            self.s_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.A:

            self.a_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.D:

            self.d_pressed = True
            self.update_player_speed()
            return

        elif key == arcade.key.M:

            self.m_pressed = True
            self.update_player_speed()

        elif key == arcade.key.V:

            self.v_pressed = True
            self.update_player_speed()



    def on_key_release(self, key, modifiers):

        """Called when the user releases a key. """



        if key == arcade.key.UP:

            self.up_pressed = False

            self.update_player_speed()

        elif key == arcade.key.DOWN:

            self.down_pressed = False

            self.update_player_speed()

        elif key == arcade.key.LEFT:

            self.left_pressed = False

            self.update_player_speed()

        elif key == arcade.key.RIGHT:

            self.right_pressed = False

            self.update_player_speed()

        elif key == arcade.key.W:

            self.w_pressed = False

            self.update_player_speed()

        elif key == arcade.key.S:

            self.s_pressed = False

            self.update_player_speed()

        elif key == arcade.key.A:

            self.a_pressed = False

            self.update_player_speed()

        elif key == arcade.key.D:

            self.d_pressed = False

            self.update_player_speed()




def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartingMenu()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
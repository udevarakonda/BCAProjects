"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SCREEN_WIDTH = 1594
SCREEN_HEIGHT = 891
SCREEN_TITLE = "Track Attack!"

FIELD_WIDTH = 1594
FIELD_HEIGHT = 891

WINNER = None

import arcade
import random

# File Paths for Player and Field Images; You can change them to what you want
COMPUTER_PATH = "/Users/udbhav/Desktop/"

player1_color = "blue"
player2_color = "red"
LEFT_DIRECTION = 0
RIGHT_DIRECTION = 1
current_event_distance = 0
current_level = 1
SPRITE_SCALING = SCREEN_HEIGHT / 1000

STARTING_MENU_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TugOfWarImages/StartingScreenTugOfWar.png"

FIELD_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TugOfWarImages/TugOfWarBackground.png"
ROPE_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TugOfWarImages/TugOfWarRopeImage.png"

PLAYER1_WIN = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TugOfWarImages/TugOfWarPlayer1Win.png"
PLAYER2_WIN = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TugOfWarImages/TugOfWarPlayer2Win.png"

# Image File Paths for Player Images
BLF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue1.png"
BLF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue2.png"
BRF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/BluePlayerAnimationFacingRightFrame1.png"
BRF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/BluePlayerAnimationFacingRightFrame2.png"
RLF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/RedPlayerAnimationFacingRightFrame1.png"
RLF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red2.png"
RRF1 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red1.png"
RRF2 = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/RedPlayerAnimationFacingRightFrame2.png"


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

        global current_event_distance
        if current_event_distance == 100:
            self.scale = SPRITE_SCALING
        elif current_event_distance == 200:
            self.scale = SPRITE_SCALING * 0.75
        elif current_event_distance == 400:
            self.scale = SPRITE_SCALING * 0.50
        if player_number == 1:
            if color == "red":
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red"
            else:
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue"
            for i in range(2):
                texture = load_texture_pair(f"{main_file_name}{i + 1}.png")
                self.walk_textures.append(texture)
            self.texture = self.walk_textures[0][direction]
        else:
            if color == "red":
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Red"
            else:
                main_file_name = "/Users/udbhav/Desktop/MidyearProjectFootball/source_code/FutbolImages/ActualRunningAnimationImages/Blue"
            for i in range(2):
                texture = load_texture_pair(f"{main_file_name}{i + 1}.png")
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
            self.time_interval = 8
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


class StartingMenu(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(STARTING_MENU_IMAGE)
        arcade.set_viewport(0, FIELD_WIDTH-1, 0, FIELD_HEIGHT-1)

    def on_draw(self):
        self.window.clear()
        self.texture.draw_sized(FIELD_WIDTH / 2, FIELD_HEIGHT / 2,
                                FIELD_WIDTH, FIELD_HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = RulesMenu()
        self.window.show_view(game_view)


class RulesMenu(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()

        arcade.draw_text("Tug O' War", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press the correct letter to gain power", self.window.width / 2, self.window.height - 110,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Pressing the wrong letter makes you lose power", self.window.width / 2, self.window.height - 210,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Drag the other team to the center line to win!", self.window.width / 2, self.window.height - 310,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

class EndingScreen(arcade.View):
    def __init__(self):
        global WINNER
        super().__init__()
        if WINNER == "player1":
            self.texture = arcade.load_texture(PLAYER1_WIN)
        else:
            self.texture = arcade.load_texture(PLAYER2_WIN)

        arcade.set_viewport(0, FIELD_WIDTH - 1, 0, FIELD_HEIGHT - 1)

    def on_draw(self):
        self.window.clear()
        self.texture.draw_sized(FIELD_WIDTH / 2, FIELD_HEIGHT / 2, FIELD_WIDTH, FIELD_HEIGHT)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 701 > x > 128 and 442 > y > 262:
            # Play Again Button

            game_view = StartingMenu()
            self.window.show_view(game_view)

        elif 1505 > x > 932 and 442 > y > 262:
            # Quit Button
            arcade.close_window()

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Camera
        self.camera = None
        self.gui_camera = None

        # Variables that will hold sprite lists
        self.player1_list = None
        self.player2_list = None

        # Power
        self.player1_power = 0
        self.player2_power = 0

        # Set up the player info
        self.player1_sprite1 = None
        self.player1_sprite2 = None
        self.player1_sprite3 = None
        self.player1_sprite4 = None
        self.player1_sprite5 = None

        self.player2_sprite1 = None
        self.player2_sprite2 = None
        self.player2_sprite3 = None
        self.player2_sprite4 = None
        self.player2_sprite5 = None

        self.background = None
        self.rope = None


        # Used for Animation
        self.player1_sprite1_current_frame = None
        self.player1_sprite2_current_frame = None
        self.player1_sprite3_current_frame = None
        self.player1_sprite4_current_frame = None
        self.player1_sprite5_current_frame = None

        self.player2_sprite1_current_frame = None
        self.player2_sprite2_current_frame = None
        self.player2_sprite3_current_frame = None
        self.player2_sprite4_current_frame = None
        self.player2_sprite5_current_frame = None

        # Make the scene
        self.scene = None

        # Timer
        self.timer = None

        # Level
        self.level = current_level

        # Letters
        self.letters_player1 = ["Q", "W", "A", "S", "Z", "X"]
        self.letters_player2 = ["U", "I", "J", "K", "N", "M"]
        self.current_letter_player1 = "Q"
        self.current_letter_player2 = "U"


        # Timer
        self.stopwatch = 0

        # Interval
        self.interval = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Sprite lists
        self.player1_list = arcade.SpriteList()
        self.player2_list = arcade.SpriteList()

        # Initialize the Scene
        self.scene = arcade.Scene()

        # Create sprite List
        self.scene.add_sprite_list("Rope")
        self.scene.add_sprite_list("Player1")
        self.scene.add_sprite_list("Player2")

        # Set up the Background
        self.background = arcade.load_texture(FIELD_IMAGE)

        # Set up the players

        # Player 1
        self.player1_sprite1 = Player(player1_color, RIGHT_DIRECTION, 1)
        self.player1_sprite1_current_frame = 1
        self.player1_list.append(self.player1_sprite1)
        self.scene.add_sprite("Player1", self.player1_sprite1)

        self.player1_sprite2 = Player(player1_color, RIGHT_DIRECTION, 1)
        self.player1_sprite2_current_frame = 1
        self.player1_list.append(self.player1_sprite2)
        self.scene.add_sprite("Player1", self.player1_sprite2)

        self.player1_sprite3 = Player(player1_color, RIGHT_DIRECTION, 1)
        self.player1_sprite3_current_frame = 1
        self.player1_list.append(self.player1_sprite3)
        self.scene.add_sprite("Player1", self.player1_sprite3)

        self.player1_sprite4 = Player(player1_color, RIGHT_DIRECTION, 1)
        self.player1_sprite4_current_frame = 1
        self.player1_list.append(self.player1_sprite4)
        self.scene.add_sprite("Player1", self.player1_sprite4)

        self.player1_sprite5 = Player(player1_color, RIGHT_DIRECTION, 1)
        self.player1_sprite5_current_frame = 1
        self.player1_list.append(self.player1_sprite5)
        self.scene.add_sprite("Player1", self.player1_sprite5)

        # Player 2
        self.player2_sprite1 = Player(player2_color, LEFT_DIRECTION, 1)
        self.player2_sprite1_current_frame = 1
        self.player2_list.append(self.player2_sprite1)
        self.scene.add_sprite("Player2", self.player2_sprite1)

        self.player2_sprite2 = Player(player2_color, LEFT_DIRECTION, 1)
        self.player2_sprite2_current_frame = 1
        self.player2_list.append(self.player2_sprite2)
        self.scene.add_sprite("Player2", self.player2_sprite2)

        self.player2_sprite3 = Player(player2_color, LEFT_DIRECTION, 1)
        self.player2_sprite3_current_frame = 1
        self.player2_list.append(self.player2_sprite3)
        self.scene.add_sprite("Player2", self.player2_sprite3)

        self.player2_sprite4 = Player(player2_color, LEFT_DIRECTION, 1)
        self.player2_sprite4_current_frame = 1
        self.player2_list.append(self.player2_sprite4)
        self.scene.add_sprite("Player2", self.player2_sprite4)

        self.player2_sprite5 = Player(player2_color, LEFT_DIRECTION, 1)
        self.player2_sprite5_current_frame = 1
        self.player2_list.append(self.player2_sprite5)
        self.scene.add_sprite("Player2", self.player2_sprite5)

        # Rope
        self.rope = arcade.Sprite(ROPE_IMAGE, 1)
        self.scene.add_sprite("Rope", self.rope)

        self.timer = 180

        self.position_players()

        self.stopwatch = 0

    def position_players(self):
        self.player1_sprite1.center_x = 340
        self.player1_sprite1.center_y = 235

        self.player1_sprite2.center_x = 380
        self.player1_sprite2.center_y = 235

        self.player1_sprite3.center_x = 420
        self.player1_sprite3.center_y = 235

        self.player1_sprite4.center_x = 460
        self.player1_sprite4.center_y = 235

        self.player1_sprite5.center_x = 500
        self.player1_sprite5.center_y = 235

        self.player2_sprite1.center_x = 1160
        self.player2_sprite1.center_y = 235

        self.player2_sprite2.center_x = 1200
        self.player2_sprite2.center_y = 235

        self.player2_sprite3.center_x = 1240
        self.player2_sprite3.center_y = 235

        self.player2_sprite4.center_x = 1280
        self.player2_sprite4.center_y = 235

        self.player2_sprite5.center_x = 1320
        self.player2_sprite5.center_y = 235

        self.rope.center_x = 812
        self.rope.center_y = 235



    def stopwatch_timer(self):
        minutes = int(self.stopwatch / 30)
        seconds = self.stopwatch - (minutes*30)
        return f"{minutes}.{seconds}"

    def on_draw(self):
        """
        Render the screen.
        """

        # Clear the screen
        self.window.clear()

        # Draw the Background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            FIELD_WIDTH, FIELD_HEIGHT,
                                            self.background)

        # Draw the players
        self.scene.draw()
        self.rope.update()

        player1_current_letter = f"Player 1: Press {self.current_letter_player1}"
        player2_current_letter = f"Player 2: Press {self.current_letter_player2}"
        arcade.draw_text(
            player1_current_letter,
            350,
            800,
            arcade.csscolor.BLACK,
            25
        )
        arcade.draw_text(
            player2_current_letter,
            1226,
            800,
            arcade.csscolor.BLACK,
            25
        )

        # # Distance Text
        # global current_event_distance
        # distance_text = f"{current_event_distance}m race"
        # arcade.draw_text(
        #     distance_text,
        #     1300,
        #     350,
        #     arcade.csscolor.BLACK,
        #     18,
        # )
        #
        #
        # # Level
        # level_text = f"Level {self.level}"
        # arcade.draw_text(
        #     level_text,
        #     10,
        #     350,
        #     arcade.csscolor.BLACK,
        #     18,
        # )
        #
        # timer_text = ""
        # if self.timer > 0:
        #     timer_text = f"{int(self.timer/60)}"
        # else:
        #     timer_text = ""
        # arcade.draw_text(
        #     timer_text,
        #     FIELD_WIDTH / 2,
        #     FIELD_HEIGHT / 2,
        #     arcade.csscolor.BLACK,
        #     50,
        # )
        #
        # press_text = f"Press {self.current_letter}"
        # arcade.draw_text(
        #     press_text,
        #     750,
        #     350,
        #     arcade.csscolor.BLACK,
        #     18,
        # )

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

    # def game_logic(self):


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.check_winner()

        self.player1_list.update()
        self.player2_list.update()


    def update_players(self):
        power = self.player2_power - self.player1_power
        self.player1_sprite1.change_x = power
        self.player1_sprite2.change_x = power
        self.player1_sprite3.change_x = power
        self.player1_sprite4.change_x = power
        self.player1_sprite5.change_x = power

        self.player2_sprite1.change_x = power
        self.player2_sprite2.change_x = power
        self.player2_sprite3.change_x = power
        self.player2_sprite4.change_x = power
        self.player2_sprite5.change_x = power

        self.rope.change_x = power



    def change_player1_letter(self):
        random_int = random.randint(0, 5)
        self.current_letter_player1 = self.letters_player1[random_int]

    def change_player2_letter(self):
        random_int = random.randint(0, 5)
        self.current_letter_player2 = self.letters_player2[random_int]


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.Q:
            if self.current_letter_player1 == "Q":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()
        if key == arcade.key.W:
            if self.current_letter_player1 == "W":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()
        if key == arcade.key.A:
            if self.current_letter_player1 == "A":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()
        if key == arcade.key.S:
            if self.current_letter_player1 == "S":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()
        if key == arcade.key.Z:
            if self.current_letter_player1 == "Z":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()
        if key == arcade.key.X:
            if self.current_letter_player1 == "X":
                self.player1_power += 0.5
            else:
                self.player1_power -= 0.5
            self.change_player1_letter()
            self.update_players()

        if key == arcade.key.U:
            if self.current_letter_player2 == "U":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()
        if key == arcade.key.I:
            if self.current_letter_player2 == "I":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()
        if key == arcade.key.J:
            if self.current_letter_player2 == "J":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()
        if key == arcade.key.K:
            if self.current_letter_player2 == "K":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()
        if key == arcade.key.N:
            if self.current_letter_player2 == "N":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()
        if key == arcade.key.M:
            if self.current_letter_player2 == "M":
                self.player2_power += 0.5
            else:
                self.player2_power -= 0.5
            self.change_player2_letter()
            self.update_players()


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if self.timer <= 0:
            random_int = random.randint(1, 8)
            self.current_letter = self.letters[random_int]

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def check_winner(self):
        global WINNER
        if self.player1_sprite5.center_x > 812:
            WINNER = "player2"
            game_view = EndingScreen()
            self.window.show_view(game_view)
        elif self.player2_sprite1.center_x < 812:
            WINNER = "player1"
            game_view = EndingScreen()
            self.window.show_view(game_view)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartingMenu()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
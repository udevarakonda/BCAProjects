"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 377
SCREEN_TITLE = "Track Attack!"

FIELD_WIDTH = 1500
FIELD_HEIGHT = 377

import arcade
import random

# File Paths for Player and Field Images; You can change them to what you want
COMPUTER_PATH = "/Users/udbhav/Desktop/"

player1_color = "blue"
ai_color = "red"
LEFT_DIRECTION = 0
RIGHT_DIRECTION = 1
current_event_distance = 0
current_level = 5
SPRITE_SCALING = SCREEN_HEIGHT / 628

WINNING_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/winscreen_trackAttack.png"
CLOSING_MENU_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/endscreen_trackAttack.png"
STARTING_MENU_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/StartingMenuImage.png"
FIELD_IMAGE = COMPUTER_PATH + "MidyearProjectFootball/source_code/FutbolImages/TrackBackground.png"
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
        print(self.scale)
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
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(STARTING_MENU_IMAGE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, FIELD_WIDTH - 1, 0, FIELD_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        self.texture.draw_sized(FIELD_WIDTH / 2, FIELD_HEIGHT / 2,
                                FIELD_WIDTH, FIELD_HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        if 700 > x > 156 and 253 > y > 173:
            # 100m Button

            game_view = Hundred_Meter_Rules()
            self.window.show_view(game_view)

        if 1358 > x > 814 and 253 > y > 173:
            # 200m Button

            game_view = Two_Hundred_Meter_Rules()
            self.window.show_view(game_view)

        elif 1022 > x > 479 and 141 > y > 61:
            # 400m Button

            game_view = Four_Hundred_Meter_Rules()
            self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

class WinningMenu(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(WINNING_IMAGE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, FIELD_WIDTH - 1, 0, FIELD_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        self.texture.draw_sized(FIELD_WIDTH / 2, FIELD_HEIGHT / 2,
                                FIELD_WIDTH, FIELD_HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        if 628 > x > 104 and 204 > y > 104:
            # Play Again Button

            game_view = StartingMenu()
            self.window.show_view(game_view)

        elif 1359 > x > 841 and 204 > y > 104:
            # Quit Button
            arcade.close_window()



    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

class ClosingMenu(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(CLOSING_MENU_IMAGE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, FIELD_WIDTH - 1, 0, FIELD_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        self.texture.draw_sized(FIELD_WIDTH / 2, FIELD_HEIGHT / 2,
                                FIELD_WIDTH, FIELD_HEIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        if 628 > x > 104 and 204 > y > 104:
            # Play Again Button

            game_view = StartingMenu()
            self.window.show_view(game_view)

        elif 1359 > x > 841 and 204 > y > 104:
            # Quit Button
            arcade.close_window()



    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))

class Hundred_Meter_Rules(arcade.View):
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

        arcade.draw_text("100m", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press the correct letter to speed up", self.window.width / 2, self.window.height - 110,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Pressing the wrong letter slows you down", self.window.width / 2, self.window.height - 210,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Beat all five levels to win!", self.window.width / 2, self.window.height - 310,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global current_event_distance

        current_event_distance = 100
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))


class Two_Hundred_Meter_Rules(arcade.View):
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

        arcade.draw_text("200m", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press the correct letter to speed up", self.window.width / 2, self.window.height - 110,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Pressing the wrong letter slows you down", self.window.width / 2, self.window.height - 210,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Beat all five levels to win!", self.window.width / 2, self.window.height - 310,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global current_event_distance

        current_event_distance = 200
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))


class Four_Hundred_Meter_Rules(arcade.View):
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

        arcade.draw_text("400m", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press the correct letter to speed up", self.window.width / 2, self.window.height - 110,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Pressing the wrong letter slows you down", self.window.width / 2, self.window.height - 210,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

        arcade.draw_text("Beat all five levels to win!", self.window.width / 2, self.window.height - 310,
                         arcade.color.WHITE, font_size=12, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global current_event_distance

        current_event_distance = 400
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     print(str(x) + " " + str(y))


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
        self.player_list = None
        self.AI_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_sprite2 = None
        self.background = None

        # 7 AIs
        self.AI_1 = None
        self.AI_2 = None
        self.AI_3 = None
        self.AI_4 = None
        self.AI_5 = None
        self.AI_6 = None
        self.AI_7 = None

        # Used for Animation
        self.player1_current_frame = None
        self.AI_1_current_frame = None
        self.AI_2_current_frame = None
        self.AI_3_current_frame = None
        self.AI_4_current_frame = None
        self.AI_5_current_frame = None
        self.AI_6_current_frame = None
        self.AI_7_current_frame = None

        # Make the scene
        self.scene = None

        # Timer
        self.timer = None

        # Level
        self.level = current_level

        # Letters
        self.letters = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        self.current_letter = "A"

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.AI_list = arcade.SpriteList()

        # Initialize the Scene
        self.scene = arcade.Scene()

        # Create sprite List
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("AI")

        # Set up the Background
        self.background = arcade.load_texture(FIELD_IMAGE)

        # Set up the player
        self.player_sprite = Player(player1_color,
                                    LEFT_DIRECTION, 1)
        self.player1_current_frame = 1

        self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up the AIs
        self.AI_1 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_1_current_frame = 1
        self.scene.add_sprite("AI", self.AI_1)
        self.AI_list.append(self.AI_1)

        self.AI_2 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_2_current_frame = 1
        self.scene.add_sprite("AI", self.AI_2)
        self.AI_list.append(self.AI_2)

        self.AI_3 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_3_current_frame = 1
        self.scene.add_sprite("AI", self.AI_3)
        self.AI_list.append(self.AI_3)

        self.AI_4 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_4_current_frame = 1
        self.scene.add_sprite("AI", self.AI_4)
        self.AI_list.append(self.AI_4)

        self.AI_5 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_5_current_frame = 1
        self.scene.add_sprite("AI", self.AI_5)
        self.AI_list.append(self.AI_5)

        self.AI_6 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_6_current_frame = 1
        self.scene.add_sprite("AI", self.AI_6)
        self.AI_list.append(self.AI_6)

        self.AI_7 = Player(ai_color,
                           LEFT_DIRECTION, 1)
        self.AI_7_current_frame = 1
        self.scene.add_sprite("AI", self.AI_7)
        self.AI_list.append(self.AI_7)

        self.timer = 180

        self.position_players_and_ai()
        self.assign_speeds()

    def position_players_and_ai(self):
        self.AI_1.center_x = 1450
        self.AI_1.center_y = 340

        self.AI_2.center_x = 1450
        self.AI_2.center_y = 290

        self.AI_3.center_x = 1450
        self.AI_3.center_y = 250

        self.player_sprite.center_x = 1450
        self.player_sprite.center_y = 210

        self.AI_4.center_x = 1450
        self.AI_4.center_y = 170

        self.AI_5.center_x = 1450
        self.AI_5.center_y = 130

        self.AI_6.center_x = 1450
        self.AI_6.center_y = 90

        self.AI_7.center_x = 1450
        self.AI_7.center_y = 50

    def assign_speeds(self):

        self.player_sprite.change_x = -3 * self.adjust_speeds_for_distance()

        for x in self.AI_list:
            random_int = random.randint(4, 30)
            x.change_x = -3 - ((random_int/30)*(self.level/2))
            x.change_x *= self.adjust_speeds_for_distance()



    def adjust_speeds_for_distance(self):
        global current_event_distance
        # print(current_event_distance)

        if current_event_distance == 100:
            return 1
        elif current_event_distance == 200:
            return 0.5
        else:
            return 0.25


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

        # Activate the Gui Camera to draw stationary things.

        # Distance Text
        global current_event_distance
        distance_text = f"{current_event_distance}m race"
        arcade.draw_text(
            distance_text,
            1300,
            350,
            arcade.csscolor.BLACK,
            18,
        )

        # Level
        level_text = f"Level {self.level}"
        arcade.draw_text(
            level_text,
            10,
            350,
            arcade.csscolor.BLACK,
            18,
        )

        timer_text = ""
        if self.timer > 0:
            timer_text = f"{int(self.timer/60)}"
        else:
            timer_text = ""
        arcade.draw_text(
            timer_text,
            FIELD_WIDTH / 2,
            FIELD_HEIGHT / 2,
            arcade.csscolor.BLACK,
            50,
        )

        press_text = f"Press {self.current_letter}"
        arcade.draw_text(
            press_text,
            750,
            350,
            arcade.csscolor.BLACK,
            18,
        )

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        print(str(x) + " " + str(y))

    # def game_logic(self):

    def check_winner(self):
        if self.player_sprite.center_x < 50:
            if self.level == 5:
                game_view = WinningMenu()
                self.window.show_view(game_view)

            self.level += 1
            self.setup()
        else:
            for x in self.AI_list:
                if x.center_x < 50:
                    game_view = ClosingMenu()
                    self.window.show_view(game_view)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.check_winner()

        if self.timer <= 0:
            self.player_list.update()
            self.AI_list.update()
        else:
            self.timer -= 1


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        interval = 0.3 * self.adjust_speeds_for_distance()

        if self.timer <= 0:
            if key == arcade.key.A:
                if self.current_letter == "A":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.S:
                if self.current_letter == "S":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.D:
                if self.current_letter == "D":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.F:
                if self.current_letter == "F":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.G:
                if self.current_letter == "G":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.H:
                if self.current_letter == "H":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.J:
                if self.current_letter == "J":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.K:
                if self.current_letter == "K":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

            if key == arcade.key.L:
                if self.current_letter == "L":
                    self.player_sprite.change_x -= interval
                else:
                    self.player_sprite.change_x += interval

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
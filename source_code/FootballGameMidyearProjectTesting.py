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

FRAME = 0

PLAYER_STARTING_TURN = 0

SCREEN_WIDTH = 4862  # 1500, 2431. 4862  width = height * 2.43111831
SCREEN_HEIGHT = 1000  # 617, 1000  height = width / 0.411333333333
SCREEN_TITLE = "1v1 Football Run"

# Window Screen Width:
WINDOW_WIDTH = 1600

SPRITE_SCALING = SCREEN_HEIGHT/2000

MOVEMENT_SPEED = 2 #2
PIXELS_FOR_FIRST_DOWN = SCREEN_WIDTH/12.7118644068
TIME_BETWEEN_PLAYS = 200

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Player(arcade.Sprite):

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(WINDOW_WIDTH, height, title)

        # Camera
        self.camera = None
        self.gui_camera = None

        # Variables that will hold sprite lists
        self.player_list = None


        # Set up the player info
        self.quarterback1 = None
        self.quarterback2 = None
        self.background = None

        # Make the scene
        self.scene = None
        self.scene2 = None

        # Keep track of player turn and time
        self.player_turn = PLAYER_STARTING_TURN
        self.down_number = 1
        self.pixels_left = PIXELS_FOR_FIRST_DOWN
        self.time_marker = 0
        self.position_for_first_down = None
        self.line_of_scrimmage = None

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

        # Use Height and Width to track variables.
        self.left_end_of_endzone = int(SCREEN_WIDTH / 34.8837209)
        self.right_end_of_endzone = int(SCREEN_WIDTH - self.left_end_of_endzone)
        self.pixels_for_5_yards = int(SCREEN_WIDTH / (12.7118644068 * 2))
        self.player1_touchdown = self.left_end_of_endzone + PIXELS_FOR_FIRST_DOWN
        self.player2_touchdown = self.right_end_of_endzone - PIXELS_FOR_FIRST_DOWN
        self.player2_pos_on_first_and_goal =[int(self.player1_touchdown - (SCREEN_WIDTH / 500)), int(SCREEN_HEIGHT / 2)]
        self.player1_pos_on_first_and_goal =[int(self.player2_touchdown + (SCREEN_WIDTH / 500)), int(SCREEN_HEIGHT / 2)]

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

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Create Offense and Defense Dictionaries
        self.player1_offense_list = []
        self.player2_defense_list = []

        self.player2_offense_list = []
        self.player1_defense_list = []

        # Create Offense on Both Sides
        self.player1_offense1 = None
        self.player1_offense2 = None
        self.player1_offense3 = None
        self.player1_offense4 = None
        self.player1_offense5 = None
        self.player1_offense6 = None
        self.player1_offense7 = None
        self.player1_offense8 = None
        self.player1_offense9 = None
        self.player1_offense10 = None

        self.player2_offense1 = None
        self.player2_offense2 = None
        self.player2_offense3 = None
        self.player2_offense4 = None
        self.player2_offense5 = None
        self.player2_offense6 = None
        self.player2_offense7 = None
        self.player2_offense8 = None
        self.player2_offense9 = None
        self.player2_offense10 = None

        # Create Defense on Both Sides
        self.player1_defense1 = None
        self.player1_defense2 = None
        self.player1_defense3 = None
        self.player1_defense4 = None
        self.player1_defense5 = None
        self.player1_defense6 = None
        self.player1_defense7 = None
        self.player1_defense8 = None
        self.player1_defense9 = None
        self.player1_defense10 = None

        self.player2_defense1 = None
        self.player2_defense2 = None
        self.player2_defense3 = None
        self.player2_defense4 = None
        self.player2_defense5 = None
        self.player2_defense6 = None
        self.player2_defense7 = None
        self.player2_defense8 = None
        self.player2_defense9 = None
        self.player2_defense10 = None

        self.current_running_player = None

        # Make variable to keep track of if quarterback has thrown the ball or not
        self.is_thrown = False

        # Number of Frame
        self.frame = 0

    def create_offense(self):
        # Create Offense on Both Sides
        self.player1_offense1 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense1)
        self.player1_offense2 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense2)
        self.player1_offense3 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense3)
        self.player1_offense4 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense4)
        self.player1_offense5 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense5)
        self.player1_offense6 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense6)
        self.player1_offense7 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense7)
        self.player1_offense8 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense8)
        self.player1_offense9 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense9)
        self.player1_offense10 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player1_offense_list.append(self.player1_offense10)

        self.player2_offense1 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense1)
        self.player2_offense2 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense2)
        self.player2_offense3 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense3)
        self.player2_offense4 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense4)
        self.player2_offense5 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense5)
        self.player2_offense6 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense6)
        self.player2_offense7 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense7)
        self.player2_offense8 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense8)
        self.player2_offense9 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense9)
        self.player2_offense10 = Player(":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player2_offense_list.append(self.player2_offense10)

    def create_defense(self):
        # Create Defense on Both Sides
        self.player1_defense1 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense1)
        self.player1_defense2 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense2)
        self.player1_defense3 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense3)
        self.player1_defense4 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense4)
        self.player1_defense5 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense5)
        self.player1_defense6 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense6)
        self.player1_defense7 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense7)
        self.player1_defense8 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense8)
        self.player1_defense9 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense9)
        self.player1_defense10 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player1_defense_list.append(self.player1_defense10)

        self.player2_defense1 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense1)
        self.player2_defense2 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense2)
        self.player2_defense3 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense3)
        self.player2_defense4 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense4)
        self.player2_defense5 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense5)
        self.player2_defense6 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense6)
        self.player2_defense7 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense7)
        self.player2_defense8 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense8)
        self.player2_defense9 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense9)
        self.player2_defense10 = Player(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING)
        self.player2_defense_list.append(self.player2_defense10)


    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Initialize the scenes, which will be used to draw either offense
        self.scene = arcade.Scene()
        self.scene2 = arcade.Scene()

        # Create sprite Lists
        self.scene.add_sprite_list("Quarterback")
        self.scene2.add_sprite_list("Quarterback")

        self.scene.add_sprite_list("Offense")
        self.scene.add_sprite_list("Defense")

        self.scene2.add_sprite_list("Offense")
        self.scene2.add_sprite_list("Defense")

        # Camera
        self.camera = arcade.Camera(WINDOW_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(WINDOW_WIDTH, SCREEN_HEIGHT)

        # Set up the Background
        self.background = arcade.load_texture(":resources:images/backgrounds/FootballBackgroundImage1.jpeg")

        # Set up the player
        self.quarterback1 = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                   SPRITE_SCALING)
        self.quarterback2 = Player(":resources:images/animated_characters/male_person/malePerson_idle.png",
                                   SPRITE_SCALING)

        self.player_list.append(self.quarterback1)
        self.player_list.append(self.quarterback2)
        self.scene.add_sprite("Quarterback", self.quarterback1)
        self.scene2.add_sprite("Quarterback", self.quarterback2)

        # Create offense and defense
        self.create_offense()
        self.create_defense()

        # Line of Scrimmage
        # Line of Scrimmage
        if self.player_turn == 0:
            self.line_of_scrimmage = self.player2_touchdown
        else:
            self.line_of_scrimmage = self.player1_touchdown

        # Position offense and defense


        # Start Positions based on which player's turn it is
        if self.player_turn == 0:
            self.position_for_first_down = self.P1_P1T_START_X - PIXELS_FOR_FIRST_DOWN
            self.quarterback1.center_x = self.P1_P1T_START_X
            self.quarterback1.center_y = self.P1_P1T_START_Y
            self.quarterback2.center_x = self.P2_P1T_START_X
            self.quarterback2.center_y = self.P2_P1T_START_Y
            self.setup_player1_offense()
        else:
            self.position_for_first_down = self.P2_P2T_START_X + PIXELS_FOR_FIRST_DOWN
            self.quarterback1.center_x = self.P1_P2T_START_X
            self.quarterback1.center_y = self.P1_P2T_START_Y
            self.quarterback2.center_x = self.P2_P2T_START_X
            self.quarterback2.center_y = self.P2_P2T_START_Y
            self.setup_player2_offense()


    def setup_player1_offense(self):
        # For loop to set up offense
        for x in range(10):
            # Setup player1_offense
            self.scene.add_sprite("Offense", self.player1_offense_list[x])
            # Formula to calculate where on the field the offensive player should be
            self.player1_offense_list[x].center_x = self.quarterback1.center_x - self.pixels_for_5_yards / 2.5
            self.player1_offense_list[x].center_y = ((SCREEN_HEIGHT - (SCREEN_HEIGHT / 16.675675675 * 2)) / 15)\
                                                    * (x + 1) + (self.pixels_for_5_yards)

            # Setup player2_defense
            self.scene.add_sprite("Defense", self.player2_defense_list[x])
            self.player2_defense_list[x].center_x = self.player1_offense_list[x].center_x \
                                                    - self.pixels_for_5_yards / 2.5
            self.player2_defense_list[x].center_y = self.player1_offense_list[x].center_y

    def setup_player2_offense(self):
        # For loop to set up offense
        for x in range(10):
            # Setup player1_offense
            self.scene2.add_sprite("Offense", self.player2_offense_list[x])
            # Formula to calculate where on the field the offensive player should be
            self.player2_offense_list[x].center_x = self.quarterback2.center_x + self.pixels_for_5_yards / 2.5
            self.player2_offense_list[x].center_y = ((SCREEN_HEIGHT - (SCREEN_HEIGHT / 16.675675675 * 2)) / 15) \
                                                    * (x + 1) + (self.pixels_for_5_yards)

            # Setup player2_defense
            self.scene2.add_sprite("Defense", self.player1_defense_list[x])
            self.player1_defense_list[x].center_x = self.player2_offense_list[x].center_x \
                                                    + self.pixels_for_5_yards / 2.5
            self.player1_defense_list[x].center_y = self.player2_offense_list[x].center_y

    def quarterback1_moving(self):
        pass

    def wide_receivers_moving(self):
        pass

    def offensive_line_1_moving(self):
        for x in range(1, 9):
            offense = self.player1_offense_list[x]
            defense = self.player2_defense_list[x]



            if defense.center_x < self.quarterback1.center_x:
                defense.change_x = MOVEMENT_SPEED/2
                print(self.player2_defense_list[x].change_x)
            else:
                defense.change_x = -MOVEMENT_SPEED/2
            if defense.center_y < self.quarterback1.center_y:
                defense.change_y = MOVEMENT_SPEED/2
            else:
                defense.change_y = -MOVEMENT_SPEED/2

            offense.change_x = -defense.change_x
            offense.change_y = -defense.change_y

            hit_list = arcade.check_for_collision_with_list(defense, self.scene["Offense"])
            if len(hit_list) > 0:
                random_int = random.randint(1, 150)
                if random_int == 73:
                    for player in hit_list:
                        player.center_x = defense.center_x - self.pixels_for_5_yards / 2.5
                else:
                    offense.change_x = 0
                    offense.change_y = 0
                    defense.change_x = 0
                    defense.change_y = 0

            offense.update()
            defense.update()

    def player2_defense_swarming_quarterback(self):
        pass

    def quarterback1_throw(self):
        if not self.is_thrown:
            self.offensive_line_1_moving()
            self.player_list.update()
            if self.quarterback1.center_x < self.line_of_scrimmage:
                self.player1_run(self.quarterback1)
                self.is_thrown = True
                self.current_running_player = self.quarterback1

        else:
            self.player1_run(self.current_running_player)




    def set_player1_offense_after_tackle(self):
        # For loop to set up offense
        for x in range(10):
            # Setup player1_offense
            # Formula to calculate where on the field the offensive player should be
            self.player1_offense_list[x].center_x = self.quarterback1.center_x - self.pixels_for_5_yards / 5
            self.player1_offense_list[x].center_y = ((SCREEN_HEIGHT - (SCREEN_HEIGHT / 16.675675675 * 2)) / 15) \
                                                    * (x + 1) + (self.pixels_for_5_yards)

            # Setup player2_defense
            self.player2_defense_list[x].center_x = self.player1_offense_list[x].center_x \
                                                    - self.pixels_for_5_yards / 2.5
            self.player2_defense_list[x].center_y = self.player1_offense_list[x].center_y

    def player1_run(self, running_player):
        # Update the player
        running_player.update()

        # Check if player has been tackled and get the coordinates
        is_hit = arcade.check_for_collision_with_list(running_player, self.scene["Defense"])
        player1_x_coordinate = running_player.center_x

        # Check if the player scored a touchdown without being tackled
        if player1_x_coordinate <= self.player1_touchdown:
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            self.player1_score += 6
            self.player_turn = 1
            self.down_number = 1
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # If the player has been hit, and if so, if their y_coordinate are close enough for tackling to be possible
        if len(is_hit) > 0:
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            # Set player position after being hit
            self.quarterback1.center_x = player1_x_coordinate
            self.quarterback1.center_y = int(SCREEN_HEIGHT / 2)


            # Check for touchdown
            if player1_x_coordinate <= self.player1_touchdown:
                self.player1_score += 6
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
                        # self.quarterback2.center_x = self.player2_pos_on_first_and_goal[0]
                        # self.quarterback2.center_y = self.player2_pos_on_first_and_goal[1]
                    self.set_player1_offense_after_tackle()
                # If the player is not within 10 yards of the endzone.
                else:
                    self.position_for_first_down = player1_x_coordinate - PIXELS_FOR_FIRST_DOWN
                    self.pixels_left = PIXELS_FOR_FIRST_DOWN
                    self.down_number = 1

                    # Set player2's position 5 yards back
                        # self.quarterback2.center_x = player1_x_coordinate - self.pixels_for_5_yards
                        # self.quarterback2.center_y = int(SCREEN_HEIGHT / 2)
                    self.set_player1_offense_after_tackle()

            # If it is not first down or touchdown, the down number increases.
            else:
                if self.down_number == 4:
                    self.player_turn = 1
                    self.down_number = 1
                    self.pixels_left = PIXELS_FOR_FIRST_DOWN
                    self.setup()
                else:
                    self.down_number += 1
                    self.pixels_left = player1_x_coordinate - self.position_for_first_down

                    # Set player2's position 5 yards back
                        # self.quarterback2.center_x = player1_x_coordinate - self.pixels_for_5_yards
                        # self.quarterback2.center_y = int(SCREEN_HEIGHT / 2)
                    self.set_player1_offense_after_tackle()


    def player2_run(self):
        # Update the player
        self.player_list.update()

        # Check if player has been tackled and get the coordinates
        is_hit = arcade.check_for_collision(self.quarterback1, self.quarterback2)
        player2_x_coordinate = self.quarterback2.center_x

        # Check if the player scored a touchdown without being tackled
        if player2_x_coordinate >= self.player2_touchdown:
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            self.player2_score += 6
            self.player_turn = 0
            self.down_number = 1
            self.pixels_left = PIXELS_FOR_FIRST_DOWN
            self.setup()

        # If the player has been hit, and if so, if their y_coordinate are close enough for tackling to be possible
        if is_hit is True and abs(self.quarterback2.center_y - self.quarterback1.center_y) < int(SCREEN_HEIGHT/41.133333):
            # Create a delay in the game
            self.time_marker = TIME_BETWEEN_PLAYS

            # Set player position after being hit
            self.quarterback2.center_x = player2_x_coordinate
            self.quarterback2.center_y = int(SCREEN_HEIGHT / 2)

            # Check for touchdown®
            if player2_x_coordinate >= self.player2_touchdown:
                self.player2_score += 6
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
                    self.quarterback1.center_x = self.player1_pos_on_first_and_goal[0]
                    self.quarterback1.center_y = self.player1_pos_on_first_and_goal[1]
                else:
                    self.position_for_first_down = player2_x_coordinate + PIXELS_FOR_FIRST_DOWN
                    self.pixels_left = PIXELS_FOR_FIRST_DOWN
                    self.down_number = 1

                    # Set player1's position 5 yards in front
                    self.quarterback1.center_x = player2_x_coordinate + self.pixels_for_5_yards
                    self.quarterback1.center_y = int(SCREEN_HEIGHT / 2)

            # If it is not first down or touchdown, the down number increases.
            else:
                if self.down_number == 4:
                    self.player_turn = 0
                    self.down_number = 1
                    self.pixels_left = PIXELS_FOR_FIRST_DOWN
                    self.setup()
                else:
                    self.down_number += 1
                    self.pixels_left = self.position_for_first_down - player2_x_coordinate

                    # Set player1's position 5 yards in front
                    self.quarterback1.center_x = player2_x_coordinate + self.pixels_for_5_yards
                    self.quarterback1.center_y = int(SCREEN_HEIGHT / 2)


    def center_camera_to_player(self):
        if (self.player_turn == 0):
            screen_center_x = self.quarterback1.center_x - (self.camera.viewport_width / 2)

            # Don't let camera travel past 0
            if screen_center_x < 0:
                screen_center_x = 0
            elif self.quarterback1.center_x + self.camera.viewport_width / 2 > SCREEN_WIDTH:
                screen_center_x = SCREEN_WIDTH - self.camera.viewport_width

            player_centered = screen_center_x, 0

            self.camera.move_to(player_centered)
        else:
            screen_center_x = self.quarterback2.center_x - (self.camera.viewport_width / 2)

            # Don't let camera travel past 0
            if screen_center_x < 0:
                screen_center_x = 0
            elif self.quarterback2.center_x + self.camera.viewport_width / 2 > SCREEN_WIDTH:
                screen_center_x = SCREEN_WIDTH - self.camera.viewport_width

            player_centered = screen_center_x, 0

            self.camera.move_to(player_centered)

    def down_text_changer(self):
        if self.down_number == 1:
            return "1st"
        elif self.down_number == 2:
            return "2nd"
        elif self.down_number == 3:
            return "3rd"
        else:
            return "4th"

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()

        # Activate the Camera
        self.camera.use()

        # Draw the Background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Draw the players
        if self.player_turn == 0:
            self.scene.draw()
        else:
            self.scene2.draw()

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
        if (self.pixels_left < 11.8):
            yards_left = "inches"
        else:
            yards_left = int(self.pixels_left / (PIXELS_FOR_FIRST_DOWN / 10))
        down_text = f"{self.down_text_changer()} & {yards_left}"
        arcade.draw_text(
            down_text,
            10,
            SCREEN_HEIGHT - 20,
            arcade.csscolor.WHITE,
            18
        )
        player_turn_text = f"Player {self.player_turn + 1} turn"
        arcade.draw_text(
            player_turn_text,
            300,
            SCREEN_HEIGHT - 20,
            arcade.csscolor.WHITE,
            18
        )

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        print(str(x) + " " + str(y))


    def update_player_speed(self):



        # Calculate speed based on the keys pressed

        self.quarterback1.change_x = 0

        self.quarterback1.change_y = 0

        self.quarterback2.change_x = 0

        self.quarterback2.change_y = 0



        if self.up_pressed and not self.down_pressed:

            self.quarterback1.change_y = MOVEMENT_SPEED

        elif self.down_pressed and not self.up_pressed:

            self.quarterback1.change_y = -MOVEMENT_SPEED

        if self.left_pressed and not self.right_pressed:

            self.quarterback1.change_x = -MOVEMENT_SPEED

        elif self.right_pressed and not self.left_pressed:

            self.quarterback1.change_x = MOVEMENT_SPEED

        if self.w_pressed and not self.s_pressed:

            self.quarterback2.change_y = MOVEMENT_SPEED

        elif self.s_pressed and not self.w_pressed:

            self.quarterback2.change_y = -MOVEMENT_SPEED

        if self.a_pressed and not self.d_pressed:

            self.quarterback2.change_x = -MOVEMENT_SPEED

        elif self.d_pressed and not self.a_pressed:

            self.quarterback2.change_x = MOVEMENT_SPEED


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        if self.time_marker != 0:
            self.time_marker -= 1
        elif self.player_turn == 0:
            self.quarterback1_throw()
        else:
            self.quarterback2_throw()
        self.center_camera_to_player()


    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """



        if key == arcade.key.UP:

            self.up_pressed = True

            self.update_player_speed()

        elif key == arcade.key.DOWN:

            self.down_pressed = True

            self.update_player_speed()

        elif key == arcade.key.LEFT:

            self.left_pressed = True

            self.update_player_speed()

        elif key == arcade.key.RIGHT:

            self.right_pressed = True

            self.update_player_speed()

        elif key == arcade.key.W:

            self.w_pressed = True

            self.update_player_speed()

        elif key == arcade.key.S:

            self.s_pressed = True

            self.update_player_speed()

        elif key == arcade.key.A:

            self.a_pressed = True

            self.update_player_speed()

        elif key == arcade.key.D:

            self.d_pressed = True

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
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
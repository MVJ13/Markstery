import cocos                                # Cocos2d is a framework for building 2D games, graphical applications, interactive demos, and more. By importing cocos, you can access its various classes and functions for creating and managing scenes, layers, sprites, and other game elements.
from cocos.director import director         # The director is a singleton object that manages the game loop, scenes, and transitions. It is responsible for running the main loop of the application, switching between scenes, and handling the overall flow of the game.
from pyglet.window import mouse             # The mouse module provides constants and functions for handling mouse input events, such as detecting mouse button presses and mouse movements.
from cocos.scenes import *                  # The scenes module in Cocos2d provides various scene classes, such as Scene, TransitionScene, FadeTransition, etc., which are used to manage different screens or levels in a game. By importing everything from this module, you can easily use these scene classes in your game.
from random import randint, shuffle         # This imports the randint and shuffle functions from the random module. The random module is part of Python's standard library and provides functions for generating random numbers and performing random operations. randint generates a random integer within a specified range, while shuffle randomly reorders the elements of a list.
import pyglet                               # Pyglet is a cross-platform windowing and multimedia library for Python, which Cocos2d uses for its underlying graphics and windowing operations. By importing pyglet, you can access its functionalities for handling windows, rendering graphics, playing sounds, and processing user input.


# This needs to be on the top, otherwise the DisplayController won't work
director.init(width=1024, height=576, caption="Markstery: Memory Card Matching Game!")
director.window.pop_handlers()
director.window.set_location(400, 200)
#
img = image = pyglet.resource.image("res/sprites/markstery_1000x.png")
director.window.set_icon(img)
#
#
#
#
#
#==================== ALL GAME LAYERS ====================#
class CardLayer(cocos.layer.Layer):   # Inheritance # This defines CardLayer as a subclass of cocos.layer.Layer. Layer is a base class in Cocos2d for creating different layers in a scene.
    is_event_handler = True                         # This attribute indicates that the layer will handle events, such as mouse clicks. Setting this to True allows the layer to respond to events like mouse presses.
    def __init__(self, image_path):                 # The constructor method initializes the CardLayer object.
        super().__init__()                          # Calls the constructor of the parent class 
        self.clicked = False                        # Initializes a flag to track whether the card has been clicked.
        self.spr = cocos.sprite.Sprite(image_path, anchor=(0, 0))       # Creates a sprite for the card's front image using the provided image_path. The anchor point is set to (0, 0), meaning the sprite's position will be relative to its bottom-left corner.
        self.name = image_path.split("/")[2].split(".")[0]              # Extracts the card's name from the file path. This assumes a specific directory structure for the image files.
        #
        self.back = cocos.sprite.Sprite('res/sprites/markstery_100x_w_white_bckgrd.png', anchor=(0, 0))         # Creates a sprite for the card's back image. The back image is initially visible to hide the front image.
        #
        self.add(self.spr)              # Adds the front and back sprites to the layer. By adding both, the back image will be on top, hiding the front image until the card is clicked.
        self.add(self.back)
        #
    def card_clicked(self, x, y):
        return x < self.spr.x + self.spr.width and x > self.spr.x and y < self.spr.y + self.spr.height and y > self.spr.y
    #
    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.card_clicked(x, y) and len(CardController.cards_clicked) < 2:    # Checks if the card was clicked and if fewer than two cards are currently clicked (to limit selection to two cards at a time).
                self.clicked = True
                self.back.visible = False
            #
            else:
                self.clicked = False
        #
        if self.clicked and self not in CardController.cards_clicked:       # Checks if the card was clicked and if it hasn't already been added to the list of clicked cards.
            CardController.cards_clicked.append(self)
            CardController.check_cards()
#
#
#
#===== Card Controller =====#
class CardController():                 # Encapsulation
    #
    cards_clicked = []
    pairs = 0
    #
    def __init__(self):
        #   6  x=3, y=2
        #  12  x=4, y=3
        #  20  x=5, y=4
        #  24  x=6, y=4
        
        self.level1 = 6 
        self.level2 = 12
        self.level3 = 20
        self.level4 = 24
        #
        self.current_level = self.level4
        #
        path = "res/sprites/"
        files = [path + "a_card.png", path + "c_card.png", path + "e_card.png",
                 path + "f_card.png", path + "i_card.png", path + "n_card.png",
                 path + "p_card.png", path + "q_card.png", path + "b_card.png",
                 path + "d_card.png", path + "o_card.png", path + "r_card.png"]
        #
        random_list = []
        #
        for i in range(self.current_level // 2):
            r = randint(0, len(files) - 1)
            if files[r] not in random_list:
                random_list.append(files[r])
                random_list.append(files[r])
            #    
            else:
                while files[r] in random_list:
                    r = randint(0, len(files) - 1)
                random_list.append(files[r])
                random_list.append(files[r])
                #
        shuffle(random_list)
        #
        positions = self.calc_positions()
        #
        for i, file in enumerate(random_list):
            card = CardLayer(file)
            card.spr.image_anchor_x = 0
            card.spr.image_anchor_y = 0
            card.spr.position = positions[i]
            card.back.position = card.spr.position
            DisplayController.game_display.add(card)
    #
    def calc_positions(self):
        xx, yy = 0, 0
        if self.current_level == self.level1:
            xx, yy = 3, 2
        #
        elif self.current_level == self.level2:
            xx, yy = 4, 3
        #
        elif self.current_level == self.level3:
            xx, yy = 5, 4
        #
        elif self.current_level == self.level4:
            xx, yy = 6, 4
        #
        positions = []
        x_offset = 50
        y_offset = 50
        #
        for x in range(xx):
            for y in range(yy):
                positions.append((x_offset, y_offset))
                y_offset += 120
            #
            x_offset += 120
            y_offset = 50
        #
        return positions


    @staticmethod                       # This decorator indicates that flip_cards_back is a static method, meaning it can be called on the class itself without needing an instance.
    def flip_cards_back(dt):            # The method accepts a parameter dt, which stands for delta time, a common parameter passed by scheduling functions to denote elapsed time.
        for card in CardController.cards_clicked:
            card.back.visible = True
        CardController.cards_clicked = []  # need to set this here also

    @staticmethod
    def remove_cards(dt):               # remove_cards(dt): Similar to flip_cards_back, this method also takes dt as a parameter.
        DisplayController.game_display.remove(CardController.cards_clicked[0])
        DisplayController.game_display.remove(CardController.cards_clicked[1])
        CardController.cards_clicked = [] # need to set this here also

    @staticmethod
    def check_cards():                  # This method does not take any parameters and is responsible for checking the clicked cards for a match.
        if len(CardController.cards_clicked) == 2:
            if CardController.cards_clicked[0].name == CardController.cards_clicked[1].name:
                CardController.pairs += 1
                pyglet.clock.schedule_once(CardController.remove_cards, 0.5)
            #
            else:
                pyglet.clock.schedule_once(CardController.flip_cards_back, 0.5)
        #
        if CardController.pairs == 12:
            CardController.pairs = 0
            GameDisplay.game_finished = True
            DisplayController.change_display(DisplayController.winning_display)
#
#
#
#
#
#==================== ALL MENUS LAYERS ====================#
class MainMenu(cocos.menu.Menu):                    # Defines MainMenu as a subclass of cocos.menu.Menu, which is used to create menus in Cocos2d.
    def __init__(self):                             # The constructor method initializes the MainMenu object.
        super().__init__('MARKSTERT GAME!')         # Calls the parent class (cocos.menu.Menu) constructor with the title "MARKSTERT GAME!".
        #
        items = []
        #
        items.append(cocos.menu.MenuItem('Start The Game', self.start_game))        # Adds a menu item labeled "Start The Game" that triggers the start_game method when selected.
        items.append(cocos.menu.MenuItem('Quit', self.quit_game))
        #
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())
    #
    def start_game(self):                               # This method is invoked when the "Start The Game" menu item is selected.
        DisplayController.change_display(DisplayController.game_display)        # Calls the change_display method of DisplayController to switch the current display to the game screen. It assumes DisplayController is a class responsible for managing different screens or displays in the game, and game_display is the attribute representing the game screen.
    #
    def quit_game(self):                                # This method is invoked when the "Quit" menu item is selected.
        director.window.close()
#
#
#
#===== Button =====#
class Button(cocos.layer.Layer):                    # Polymorphism
    is_event_handler = True
    def __init__(self, pos):
        super().__init__()
        self.spr = cocos.sprite.Sprite('res/sprites/back_btn_w_trnsp.png')
        #
        self.spr.position = pos
        #
        self.add(self.spr)
    #
    def button_clicked(self, x, y):
        return x > self.spr.x - (self.spr.width//2) and x < self.spr.x + (self.spr.width // 2) and \
               y > self.spr.y - (self.spr.height//2) and y < self.spr.y + (self.spr.height // 2)
    #
    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.button_clicked(x, y):
                DisplayController.change_display(DisplayController.start_display)
    #
    def on_mouse_motion(self, x, y, dx, dy):
        if self.button_clicked(x, y):
            self.spr.scale = 1.2
        #
        else:
            self.spr.scale = 1
#
#
#
#===== Timer =====#
class Timer(cocos.layer.Layer):

    # variable
    current_time = ""
    time_start = None
    time_stop = None
    #
    def __init__(self):
        super().__init__()
        self.label = cocos.text.Label(font_name="Times New Roman", font_size=26,
                                 anchor_x="center", anchor_y="center")
        self.start_time = 0
        #
        self.label.position = 874, 276
        self.add(self.label)

        # Assigns the method to the class variable.
        Timer.time_start = self.run_counting 
        Timer.time_stop = self.stop_counting
    #
    #
    def timer(self, dt):                    #  Method to update the timer every dt seconds.
        if GameDisplay.game_finished:
            self.stop_counting()
            self.start_time = 0
            GameDisplay.game_finished = False
        #
        else:                                               # If the game is not finished, formats the time (self.start_time) into minutes and seconds, updates the current_time variable, updates the label text with the formatted time, and increments the start time.
            mins, secs = divmod(self.start_time, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            Timer.current_time = time_format
            self.label.element.text = time_format
            self.start_time += 1
    #
    def run_counting(self):
        self.schedule_interval(self.timer, 1.0)         # Method to start the timer.
    #
    def stop_counting(self):                            # Method to stop the timer.
        self.unschedule(self.timer)
#
#
#
#
#
#==================== ALL DISPLAY LAYERS ====================#
#
#
#
#===== StartDisplay =====#
class StartDisplay(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        #
        menu = MainMenu()
        #
        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))       # Adds a semi-transparent color layer to the scene, creating a dim background.

        self.add(menu)
#
#
#
#===== GameDisplay =====#
class GameDisplay(cocos.scene.Scene):
    #
    game_finished = False
    #
    def __init__(self):
        super().__init__()
        #
        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))       # Adds a semi-transparent color layer to the scene, creating a dim background.
        self.add(Button(pos=(874, 376)))
        self.add(Timer())
#
#
#
#===== Win Display =====#
class WinningDisplay(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))       # Adds a semi-transparent color layer to the scene, creating a dim background.
        self.add(Button(pos=(512, 156)))

        self.add(cocos.text.Label("Congratulations!", font_name="Times New Roman", font_size=26,
                                      anchor_x="center", anchor_y="center", position=(512,300)))

        self.score = cocos.text.Label("click the button back to Main Menu", font_name="Times New Roman", font_size=22,
                                     anchor_x="center", anchor_y="center", position=(512, 220))

        self.add(self.score)

    def on_exit(self):
        super().on_exit()
#
#
#
#
#
#==================== ALL DISPLAY ====================#
class DisplayController:                    # Encapsulation
    #
    start_display = StartDisplay()
    game_display = GameDisplay()
    winning_display = WinningDisplay()
    #
    active_display = start_display
    #
    @staticmethod                   # static method, meaning it can be called on the class itself without needing an instance.
    def change_display(scene):
        DisplayController.active_display = scene
        if DisplayController.active_display == DisplayController.game_display:
            CardController()
            Timer.time_start()
        #
        elif DisplayController.active_display == DisplayController.start_display:
            for child in DisplayController.game_display.get_children():
                if hasattr(child, 'name'):
                    child.kill()
        #
        director.replace(FlipX3DTransition(DisplayController.active_display, duration=2))


if __name__ == "__main__":
    director.run(DisplayController.active_display)
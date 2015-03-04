import pygame, playerOne, events, math


class TestObj(object):
    pass                # Create an object on the screen that can be hit and lose
                        # health points if within the range of player1's attacking
                        # hitbox (define a box-like border around the center of the
                        # circle which, when the circle's center is within the border
                        # of the attack box, takes away health points).

#### INITIALIZATION VALUES #####################################################
h=400
w = 800
screen = pygame.display.set_mode((w,h))
mousePos = pygame.mouse.get_pos()           # Gets the initial mouse position.

player1 = playerOne.character(screen)       # Creates the player. This should
                                            # eventually be a part of its own module.
pos = 0                                     # Sets position value to 0. (See playerOne module.)
gameOn = True
info = "STILL"                              # Initializes at standing still.
clock = pygame.time.Clock()                 # Clock object.
EVENTS = events.getEvent(player1,screen,clock)  # Event handling object.
################################################################################

#### GAME LOOP #################################################################
while EVENTS.gameOn:
    mousePos = pygame.mouse.get_pos()       # Updates the mouse position.
    posList = list(mousePos)                # Attempting to cast mousePos to the "list" type.
    EVENTS.Run(mousePos)                    # Runs the event handling method of EVENTS.
    player1.hitBox(posList)                 # Temporary debugging module for hit, given the list version of mousePos as the "enemy" position.
                                            # detection.



    player1.update(EVENTS.pos, EVENTS.info) # Updates the events of player1 and
                                            # what the player is doing.
    pygame.display.update()                 # Updates the screen.

pygame.quit()                               # Quits the game.

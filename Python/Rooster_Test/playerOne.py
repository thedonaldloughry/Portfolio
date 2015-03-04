import pygame, sys, glob, math

class character:
    """Defines the properties of a character on-screen. In the initialization are
    all of the essential attributes, including animation variables, position variables,
    health point statistics, trigonometry variables, and everything necessary for
    Cartesian movement. If you find something inefficient about the animation cycling,
    please don't hesitate to tweak it a little, because I felt that the system used
    here may not be the best. It works for now, so I'll leave it there."""
    def __init__(self, surf):
        self.x = 200
        self.y = 300
        self.surf = surf
        self.ani_fps_init=3
        self.ani_fps=self.ani_fps_init
        self.ani = glob.glob("rooster/walking s0000.png")
        self.ani.sort()
        self.ani_pos=0
        self.ani_max = len(self.ani)-1
        self.img = pygame.image.load(self.ani[0])
        self.move = 0
        self.mouseAngle = 0     # AS ALWAYS, IN RADIANS!!!
        self.hitRad = 20
        self.Health = 100
        self.position = [self.x, self.y]

    def hitBox(self, mousePos):
        """This function, called in the Players module, contains information pertaining to each characters
        'hit box'. This should record the player's distance from all other players, and in the case where
        another player is close enough to you and holding the 'attack' button, this function should take away
        from the current player's health points."""
        theoreticalPoint = (mousePos[0],mousePos[1])
        position = (self.x, self.y)
        distanceBetween = math.sqrt(((theoreticalPoint[0] - self.x)**2) + ((theoreticalPoint[1] - self.y)**2))
        pygame.draw.line(self.surf, (255,0,0), theoreticalPoint, (self.x, self.y),  3)
        if distanceBetween <= 30:
            print("BEJEEZUS!!!!!!!!!!!!!")
        #pygame.draw.circle(self.surf, (0,0,0), (self.x, self.y), self.hitRad)

    def update(self, pos, direct):
        """Handles which animations get loaded with respect to your current angle from the mouse cursor.
        A little note for me: the part of the string that has 'rooster' in it should eventually be changed to
        a variable, and other types of images should be loaded for sprites. At first, this will be hard-coded,
        but eventually this will be a part of the 'player select' menu module. This function also cycles through
        loaded images and blits them to the screen."""

        if direct == "STILL":
            pass

        if direct == "UP":
            self.ani = glob.glob("rooster/walking n0*")

        if direct == "DOWN":
            self.ani = glob.glob("rooster/walking s0*")

        if direct == "LEFT":
            self.ani = glob.glob("rooster/walking w*")

        if direct == "RIGHT":
            self.ani = glob.glob("rooster/walking e*")

        if direct == "UPRIGHT":
            self.ani = glob.glob("rooster/walking ne*")

        if direct == "UPLEFT":
            self.ani = glob.glob("rooster/walking nw*")

        if direct == "DOWNRIGHT":
            self.ani = glob.glob("rooster/walking se*")

        if direct == "DOWNLEFT":
            self.ani = glob.glob("rooster/walking sw*")

        self.position[0] = self.x
        self.position[1] = self.y


        self.ani.sort()
        self.ani_max = len(self.ani)-1

        if pos != 0:
            self.ani_fps-=1
            if self.move == 1:
                self.x+=pos
            elif self.move == 2:
                self.y+=pos
            elif self.move == 3:
                self.x += pos
                self.y -= pos
            elif self.move == 4:
                self.x -= pos
                self.y -= pos
            elif self.move == 5:
                self.x += pos
                self.y += pos

            if self.ani_fps == 0:
                self.img = pygame.transform.rotate(pygame.image.load(self.ani[self.ani_pos]), self.mouseAngle)
                self.ani_fps = self.ani_fps_init
                if self.ani_pos == self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos+=1

        halfWidth = self.img.get_width() // 2
        halfHeight = self.img.get_height() // 2
        self.surf.blit(pygame.transform.rotate(self.img, int(self.mouseAngle)), (self.x - halfWidth, self.y - halfHeight))



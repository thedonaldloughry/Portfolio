import pygame, math

class getEvent(object):         # re-write to inherit the playerOne class. mainV4 is starting to lag.
    """Gets all events and player angle relative to mouse position."""
    def __init__(self, playerOne, surf, clockObj):
        self.playerOne = playerOne
        self.pos = 0
        self.info = "STILL"
        self.gameOn = True
        self.surf = surf
        self.clockObj = clockObj
        self.mouseAngle = 0     # IN RADIANS
        #self.attackAngle = 0    # ALSO IN RADIANS
    def Run(self, mPosition):
        self.surf.fill((255,255,255))
        self.clockObj.tick(60)

        #### ANGLE LOGIC #######################################################
        O = self.playerOne.y - mPosition[1]
        A = mPosition[0] - self.playerOne.x

        self.mouseAngle = math.degrees(math.atan2(O , A))
        attackO = math.sin(math.radians(self.mouseAngle)) * self.playerOne.hitRad
        attackA = math.cos(math.radians(self.mouseAngle)) * self.playerOne.hitRad

        print((attackA, attackO))


        if self.mouseAngle < 0:
            self.mouseAngle = 360 + (self.mouseAngle)
        #print(self.mouseAngle)
        ########################################################################

        pygame.event.pump()

        event = pygame.event.get()

        for evt in event:
            if evt.type == pygame.QUIT:
                self.gameOn = False

        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            self.gameOn = False

        #### TEST FOR ATTACKING ANIMATION ANGLE ################################

        if key[pygame.K_i]:
            pygame.draw.circle(self.surf, (255,0,0), (int(self.playerOne.x + attackA), int((self.playerOne.y + 5) - attackO)) , 20, 3)

        ########################################################################

        if key[pygame.K_w]:
            self.pos = -1
            self.playerOne.move = 2

        if key[pygame.K_s]:
            self.pos = 1
            self.playerOne.move = 2

        if key[pygame.K_a]:
            self.pos = -1
            self.playerOne.move = 1

        if key[pygame.K_d]:
            self.pos = 1
            self.playerOne.move = 1

        if key[pygame.K_w] and key[pygame.K_d]:
            self.pos = 1
            self.playerOne.move = 3

        if key[pygame.K_w] and key[pygame.K_a]:
            self.pos = 1
            self.playerOne.move = 4

        if key[pygame.K_s] and key[pygame.K_d]:
            self.pos = 1
            self.playerOne.move = 5

        if key[pygame.K_s] and key[pygame.K_a]:
            self.pos = -1
            self.playerOne.move = 3

        if not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_a] and not key[pygame.K_d]:
            self.pos = 0
            self.info = "STILL"
            if 30 < self.mouseAngle <= 60:
                self.playerOne.img = pygame.image.load("rooster/walking ne0000.png")
            if 60 < self.mouseAngle <= 120:
                self.playerOne.img = pygame.image.load("rooster/walking n0000.png")
            if 120 < self.mouseAngle <= 150:
                self.playerOne.img = pygame.image.load("rooster/walking nw0000.png")
            if 150 < self.mouseAngle <= 210:
                self.playerOne.img = pygame.image.load("rooster/walking w0000.png")
            if 210 < self.mouseAngle <= 240:
                self.playerOne.img = pygame.image.load("rooster/walking sw0000.png")
            if 240 < self.mouseAngle <= 300:
                self.playerOne.img = pygame.image.load("rooster/walking s0000.png")
            if 300 < self.mouseAngle <= 330:
                self.playerOne.img = pygame.image.load("rooster/walking se0000.png")
            if 330 < self.mouseAngle <= 0 or 0 < self.mouseAngle <= 30:
                self.playerOne.img = pygame.image.load("rooster/walking e0000.png")


        if 30 < self.mouseAngle <= 60:
            self.info = "UPRIGHT"
        if 60 < self.mouseAngle <= 120:
            self.info = "UP"
        if 120 < self.mouseAngle <= 150:
            self.info = "UPLEFT"
        if 150 < self.mouseAngle <= 210:
            self.info = "LEFT"
        if 210 < self.mouseAngle <= 240:
            self.info = "DOWNLEFT"
        if 240 < self.mouseAngle <= 300:
            self.info = "DOWN"
        if 300 < self.mouseAngle <= 330:
            self.info = "DOWNRIGHT"
        if 330 < self.mouseAngle <= 0 or 0 < self.mouseAngle <= 30:
            self.info = "RIGHT"



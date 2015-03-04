import pygame
import math2d
import random
import BigDict
import copy
import world

class Entity(object):
    """ A Generic thing that is draw on the screen.
        Some common things:
            1. Sprite
            2. Position
            3. Size
        We will create derived classes from this for:
            Players
            Enemies
            Loot
            Pressure Plates
            ...
    """
    def __init__(self, pos, spriteName, spriteDBase):
        self.state = 0      # When 0, alive. When 1, dying. When 2, it is dead, and needs to be removed
        self.spriteDB = spriteDBase  # Needed for creating projectiles
        self.sprite = spriteDBase.get(spriteName)
        if not isinstance(pos, math2d.Vector2):     # Making sure the position of this Entity is a Vector2 object
            self.pos = math2d.Vector2(pos[0], pos[1])   # WORLD position of the bottom-middle of the character (feet when standing)
        else:
            self.pos = pos
        self.size = 20      # Radius of the bounding circle (centered at self.pos) used for wall / trap hit-detection
                            #       Normal size of (nearly) all entities is set here
        self.hitRadius = 5  # The radius of the circle used for weapons
        self.damageScale = 25   # Multiplied by the weapon damage factor
                            #    ^^^ These two are placed here to be used for projectiles and the Player

    def render(self, surf, cameraPos):
        """ Draw a blobby shadow underneath the character """
        # We might need to replace this with a "shadow" image; the corners
        #     of the rectangular surface appear around the circle as-is
        tempS = pygame.Surface((self.size * 2, self.size * 2))   # Create an off-screen, semi-transparent (soon) surface
        tempS.fill((255,255,255))                                # Temporary?
        tempS.set_alpha(64)                                      # Arbitrary number for transparency; lower numbers = more transparent
        tempS.set_colorkey((255,255,255))

        pygame.draw.circle(tempS, (0,0,0), (self.size, self.size), self.size)       # Draws the shadow
        surf.blit(tempS, (self.pos[0] - cameraPos[0] - self.size, self.pos[1] - cameraPos[1] - self.size))   # Blit the shadow to the screen at self.pos

    def update(self, dT):
        """ Do any pertinent updates """
        pass

class Projectile(Entity):
    """ A class for projectiles. Whenever a projectile is fired, create
        a projectile object. """
    def __init__(self, pos, spriteName, spriteDBase, firingWeapon, direction, shooter, atkType):
        Entity.__init__(self, pos, spriteName, spriteDBase)
        # NOTE: The position of the projectile is the point used for hit detection (the middle, front edge based on direction)
        self.range = firingWeapon[6]
        self.distTravelled = 0          # The amount of distance the projectile has already travelled
        self.speed = 500 * firingWeapon[7]
        if atkType == "Normal":
            self.damage = firingWeapon[4]
        elif atkType == "Power":
            self.damage = firingWeapon[5]
        self.direction = direction      # W = 0, E = 1...
        self.shooter = shooter          # The object that fired this projectile - so the projectile doesn't hit the one that shot it
        self.firingWeapon = firingWeapon[0]
        self.drawOffset = math2d.Vector2(0, 0)

        # self.drawOffset is the distance from self.pos to the top left corner of the sprite
        if self.direction == 0 and self.firingWeapon == "Bow":
            # Already facing correct direction; no rotation needed
            self.drawOffset = math2d.Vector2(0, self.sprite.get_height() // 2)

        elif self.direction == 1 and self.firingWeapon == "Bow":
            self.sprite = pygame.transform.rotate(self.sprite, 180)
            self.drawOffset = math2d.Vector2(self.sprite.get_width(), self.sprite.get_height() // 2)

        elif self.direction == 2 and self.firingWeapon == "Bow":
            self.sprite = pygame.transform.rotate(self.sprite, -90)
            self.drawOffset = math2d.Vector2(self.sprite.get_width() // 2, 0)

        elif self.direction == 3 and self.firingWeapon == "Bow":
            self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.drawOffset = math2d.Vector2(self.sprite.get_width() // 2, self.sprite.get_height())

        elif self.firingWeapon == "MagicStaff":
            self.drawOffset = math2d.Vector2(32, 32)

    def render(self, surf, cameraPos):
        surf.blit(self.sprite, (int(self.pos[0] - self.drawOffset[0] - cameraPos[0]), int(self.pos[1] - self.drawOffset[1] - cameraPos[1])))
        ####### TEMPORARY #######
##        pygame.draw.circle(surf, (255,0,0), (int(self.pos[0] - cameraPos[0]), int(self.pos[1] - cameraPos[1])), self.hitRadius)

    def update(self, dT, checkList, world):
        """ Updates the projectile. Performs the following:
                1: Move the projectile in the correct direction
                2: Determine how far the projectile has travelled
                    - If it has travelled the maximum range, change its state to 2 (dead)
                3: Check to see if the projectile hits anything """
        displacement = self.speed * dT      # This is the amount of distance the projectile has moved

        ####### Move the projectile #######
        if self.direction == 0:             # West
            self.pos[0] -= displacement
        elif self.direction == 1:           # East
            self.pos[0] += displacement
        elif self.direction == 2:           # North
            self.pos[1] -= displacement
        elif self.direction == 3:           # South
            self.pos[1] += displacement

        self.distTravelled += displacement  # Add to the total distance travelled by the projectile
        if self.distTravelled >= self.range: # The projectile has moved its maximum range
            self.state = 2
        # If this gets code stomped again, someone dies
        if not (world.isSpotWalkable((self.pos[0]), (self.pos[1]))):
            self.state = 2

        for obj in checkList:
            # Does the actual hit detection for this projectile
            if obj == self.shooter:  # Don't hit yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1] - 10)
                distance = distance.length()

                if distance < obj.size + self.hitRadius:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    obj.health -= self.damage * self.damageScale
                    self.state = 2

class Mover(Entity):
    """ A generic class of any entity that moves.
        Some common things:
            1. Has the ability to move
            2. Has a health attribute
            3. Able to perform actions (such as attack)
            4. Able to trigger (most/all) traps
        We will create derived classes from this for:
            1. Player
            2. Enemy
    """
    def __init__(self, pos, spriteName, spriteDBase):
        Entity.__init__(self, pos, spriteName, spriteDBase)
        self.name = spriteName
        self.speed = 200             # The speed of the Mover, in pixels per second - normal speed is set here
        self.tempSpeed = self.speed  # If the speed of the object changes, this changes - NOT self.speed
        self.health = 100.0          # The health this object has - Will be changed later to reflect what class the player is (maybe?)
        self.maxHealth = 100         # The maximum health this object can have
        self.curAction = 0           # Walk, BeingHit, Falling, Idle, Dying
        self.drawDirection = 0       # W, E, N, S
        self.curFrame = 0
        self.animDelay = 0.15        # The amount of time an object is in the same frame until it changes
        self.frameTime = 0.0         # The amount of time this object has been in the same frame
        self.projList = []           # A list of projectiles fired by this Mover
        self.lastHitByPlayer = False # Though only used for the player, the entire Mover update method would have to be copied if
                                     #     this was ONLY in the Player class. This is why there is an isinstance check in update
    def changeAction(self, newAction):
        if self.state == 0:
            self.curAction = newAction
            if (newAction != 0):         # Makes sure it's not walking, so it doesn't reset the animation
                self.curFrame = 0        # As the action changes, the new action
                                         #    starts from the first frame
    def changeDrawDirection(self, newDir):
        """ Directions are as follows:
            W = 0
            E = 1
            N = 2
            S = 3 """
        if self.state == 0:
            if newDir != self.drawDirection:
                self.drawDirection = newDir

            if (self.curAction != 0):
                self.curFrame = 0        # As the direction changes, the action
                                         #    starts from the first frame
    def update(self, dT, checkList, world):
        """ Modify curFrame (every self.animDelay seconds), wrapping around to
         0 if we're at the end of the animation (use self.curAction) """
        if self.health <= 0:
            self.health = 0              # To stop health from going negative if strange things happen
            if self.state == 0:
                self.death()

        if self.health > self.maxHealth:
            self.health = self.maxHealth # Your health cannot exceed its maximum

        self.frameTime += dT             # Increment self.frameTime based on the time that has passed

        for proj in self.projList:
            if proj.state == 2:          # The projectile is dead and needs to be removed
                self.projList.remove(proj)
                continue                 # Don't try to update the projectile afer it's been removed
            proj.update(dT, checkList, world)

        if self.frameTime >= self.animDelay:
            self.curFrame += 1
            self.frameTime = 0           # Reset self.frameTime if the frame changes
            if self.curFrame >= 4:
                self.curFrame = 0
                self.frameTime = 0       # Reset self.frameTime if the frame changes
                if self.state == 1:      # If the object has gone through the "Dying" animation...
                    if not self.lastHitByPlayer and isinstance(self, Player):
                        self.respawn(world)
                    else:
                        self.state = 2   # ... change its state to "Dead"

        self.tempSpeed = self.speed      # If tempSpeed is changed, set it back to the original speed

    def death(self):
        """ Handles the death of the mover. Changes self.curAction to 4 (dying) and self.state to 1.
            Update changes the state of the object to 2 when it's done dying """
        if isinstance(self, Player):
            if self.weapon[0] == "Sword":
                self.appPtr.sounds["exploding head"].play()
            else:
                self.appPtr.sounds["death"].play()
        self.curAction = 4    # The "Dying" action
        self.state = 1        # State is now "Dying"
        self.curFrame = 0
        self.frameTime = 0

    def fall(self):
        """ Handles the death of the mover, IF they have fallen into a pit. """
        self.curAction = 2    # The "Falling" action
        self.state = 1
        self.curFrame = 0
        self.frameTime = 0

    def render(self, surf, cameraPos):
        """ Draw the blobby shadow (from Entity.render), then draw the current
            sprite on top of it. Also, draws a green health bar above the current sprite
            whose width is dependent on self.health. """
        # Draws the shadow by using the render method of the Entity base class
        Entity.render(self, surf, cameraPos)
        # Draws the correct sprite on top of the shadow; for the rect argument,
        #   the first argument is the current column, the second argument is the
        #   currentAction (which determines which group of 4 rows to use) and which
        #   direction (which determines which of the 4 rows to use). Each sprite is 64x64
        surf.blit(self.sprite, (self.pos[0] - 32 - cameraPos[0], self.pos[1] - 64 - cameraPos[1]), (self.curFrame * 64,
            self.curAction * 256 + self.drawDirection * 64, 64,64))
        # Render all projectiles associated with this object
        for proj in self.projList:
            proj.render(surf, cameraPos)
        # Health bar
        pygame.draw.rect(surf, (0,0,0), (self.pos[0] - 49 - cameraPos[0], self.pos[1] - 65 - cameraPos[1], 102, 4))
        pygame.draw.rect(surf, (0,255,0), (self.pos[0] - 48 - cameraPos[0], self.pos[1] - 64 - cameraPos[1], self.health, 2))

class Player(Mover):
    """ A player-controlled entity. Able to access Loot. Able to trigger all traps.
        Has a weapon dictionary-attribute that includes:
            Weapon Type
            Range
            Attack Damage
            Power-Attack Type
            Power-Attack Recharge Rate
            Power-Attack Damage
        which will change as the player changes weapons."""
    def __init__(self, pos, spriteName, spriteDBase, app):
        Mover.__init__(self, pos, spriteName, spriteDBase)
        self.is_attacking = False  # True when the ANIMATION for the attack is going (actually checking for hits)
        self.atkCooldown = 1.0     # Determines when the player can attack. 1.0 is ready (percentage)
        self.is_p_atk = False      # True when the ANIMATION for the p atk is going (checking for hits)
        self.paCharge = 1.0        # Determines when the player can use a power attack. 1.0 is fully charged (percentage)
        self.pAttackColor = (0,0,255)
        self.hand_action = 1       # Initially idle; works just like curAction does for rendering the knight, just for the hands
                                   # Additional note: THIS NUMBER DOES NOT DIFFERENTIATE between attacking and otherwise
        self.hand_frameTime = 0.0  # The amount of time the current hand frame has been shown - used with self.animDelay
        self.hand_frame = 0        # The current frame for the hands
        self.walkDmgTimer = 1.0    # When at 1.0, walking on an enemy will cause damage; if less than that, temporary invuln from this kind of dmg
        self.lastHitByPlayer = False # Set to True if the player is hit by another player, until hit by something other than a player (including ALL traps)
        # For self.weapon: Spritename, attackType, Cooldown (seconds), Power Cooldown (seconds), Damage, Power Damage, Range (pixels), Proj. Speed, hitPtList
        self.weapon = BigDict.BigDict["Pickups"]["Weapons"]["Melee"][0]  # Sets self.weapon to the Sword list
        self.weaponSprite = spriteDBase.get(self.weapon[0])
        self.handSprite = spriteDBase.get("hands")
        #Sound attributes
        self.appPtr = app
        self.lavaBool = False

    def onMove(self, dT, horiz, vert, w):#Does this junk even do anything? Lol
        """ horiz and vert are both floats between -1.0 and 1.0.  Change self.pos """
        if self.state == 0:
            if (w.isSpotWalkable((self.pos[0]) + horiz * (self.size + self.tempSpeed * dT), (self.pos[1]))):
                self.pos[0] += horiz * self.tempSpeed * dT
            if (w.isSpotWalkable((self.pos[0]), (self.pos[1]) + vert * (self.size + self.tempSpeed * dT))):
                self.pos[1] += vert * self.tempSpeed * dT
            # Keeping these ^^^ as two separate if statements. Prevents "sticky" walls when pressing more than 1 direction.

    def walkEnemyDmg(self, checkList):
        """ Check against the checkList to see if you are standing on an enemy. If so,
            cause damage to the player and set self.walkDmgTimer to 0.0. This will be incremented
            in the update method back up to 1.0. """
        if self.state == 0:
            if self.walkDmgTimer < 1.0:
                return None      # If the timer is not full, no damage is taken, nothing happens
            for ene in checkList:
                if isinstance(ene, Enemy):
                    distance = (ene.pos - self.pos).length()        # Gets distance between player pos and enemby pos.
                    if distance > ene.size + self.size:             # If the length is greater than both radius combine. No collision
                        continue
                    else:
                        self.lastHitByPlayer = False
                        self.health -= ene.damage                   # Cause damage (Health points take 5.0 damage points)
                        self.appPtr.sounds[random.choice(("hit1", "hit2", "hit3"))].play()
                        self.walkDmgTimer = 0.0                     # Resets self.walkDmgTimer back to 0.0
                        if self.health < 0:                         # Health cannot be negative.
                            self.health = 0
                        return None                                 # Once you within contact of an enemy stop checking.

    def walkLootCheck(self, checkList):
        """ Check to see if the player has walked over any loot. If so, check to see what type of loot,
            and call the correct method from there. """
        if self.state == 0:
            for loot in checkList:
                if isinstance(loot, Loot):

                    distance = (loot.pos - self.pos).length()
                    if distance > loot.size + self.size:
                        continue
                    else:
                        print("Here")
                        loot.state = 2
                        # Type check to see if it is a weapon or a potion
                        if loot.action == "heal":
                            self.appPtr.sounds["health"].play()
                            self.health += loot.value
                        elif loot.action == "changeClass":
                            self.appPtr.sounds["pickup"].play()
                            self.pickUpWeapon(loot)

    def attack(self, checkList):
        """ checkList is the list of objects to test for a hit.
            Check to see if the player hits anything.
            If there is a hit, handle it. """
        if self.state == 0:
            if self.is_p_atk or self.atkCooldown < 1.0:
                return None         # If the player is already attacking or on cooldown, nothing will happen.

            self.is_attacking = True
            self.atkCooldown = 0.0  # Needs to recharge back up to 1 before it can be used again
            self.hand_frame = 0

            if self.weapon[0] == "Sword" or self.weapon[0] == "StrongSword":
                self.swordAttack(checkList)

            elif self.weapon[0] == "Scythe":
                self.scytheAttack(checkList)

            elif self.weapon[0] == "Bow":
                self.bowAttack(checkList)

            elif self.weapon[0] == "MagicStaff":
                self.staffAttack(checkList)

    def playHitSound(self, obj):
            if isinstance(obj, Player):
                self.appPtr.sounds[random.choice(("hit1", "hit2", "hit3"))].play()
                obj.lastHitByPlayer = True
            elif obj.name == "slime" or obj.name == "slime00cas" or obj.name == "slime00des":
                self.appPtr.sounds["slime hit"].play()
            elif obj.name == "Skeleton Archer":
                self.appPtr.sounds["skeleton hit"].play()
            elif obj.name == "ghost":
                self.appPtr.sounds["ghost hit"].play()
            else: #bomb
                self.appPtr.sounds[random.choice(("bomb hit1", "bomb hit2", "bomb hit3"))].play()

    def scytheAttack(self, checkList):
        """ The hit detection if using a SCYTHE. """
        self.appPtr.sounds["Scythe"].play()
        for obj in checkList:
######### HIT DETECTION FOR hitPtFar! ############
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.hitPtFar[0], obj.pos[1] - self.hitPtFar[1] - 10)
                distance = distance.length()

                if distance < obj.size + self.hitRadius:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[4] * self.damageScale // 2

        for obj in checkList:
######### HIT DETECTION FOR hitPtNear! ###########
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.hitPtNear[0], obj.pos[1] - self.hitPtNear[1] - 10)
                distance = distance.length()

                if distance < obj.size + self.hitRadius:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[4] * self.damageScale // 2

    def swordAttack(self, checkList):
        """ The hit detection if using a SWORD. """
        self.appPtr.sounds["sword"].play()
        for obj in checkList:
######### HIT DETECTION FOR hitPtFar! ############
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.hitPtFar[0], obj.pos[1] - self.hitPtFar[1] - 10)
                distance = distance.length()

                if distance < obj.size + self.hitRadius:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[4] * self.damageScale // 2  # Only the tip of the sword has hit; the full damage is applied if both points hit the target

        for obj in checkList:
######### HIT DETECTION FOR hitPtNear! ###########
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.hitPtNear[0], obj.pos[1] - self.hitPtNear[1] - 10)
                distance = distance.length()

                if distance < obj.size + self.hitRadius:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[4] * self.damageScale // 2  # Only the middle of the sword has hit; the full damage is applied if both points hit the target

    def bowAttack(self, checkList):
        """ Hit detection for the BOW. Creates a projectile that handles all hit detection """
        ####### Finding the position of the new projectile #######
        if self.drawDirection == 0:
            projPos = math2d.Vector2(self.pos[0] - 64, self.pos[1] - 20)
        elif self.drawDirection == 1:
            projPos = math2d.Vector2(self.pos[0] + 64, self.pos[1] - 20)
        elif self.drawDirection == 2:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] - 64)
        elif self.drawDirection == 3:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] + 64)

        self.appPtr.sounds["arrow"].play()
        newProjectile = Projectile(projPos, "arrow", self.spriteDB, self.weapon, self.drawDirection, self, "Normal")
        self.projList.append(newProjectile)

    def staffAttack(self, checkList):
        """ Hit detection for the STAFF. Creates a projectile that handles all hit detection """
        ####### Finding the position of the new projectile #######
        self.appPtr.sounds["staff"].play()
        if self.drawDirection == 0:
            projPos = math2d.Vector2(self.pos[0] - 64, self.pos[1] - 20)
        elif self.drawDirection == 1:
            projPos = math2d.Vector2(self.pos[0] + 64, self.pos[1] - 20)
        elif self.drawDirection == 2:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] - 64)
        elif self.drawDirection == 3:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] + 64)

        newProjectile = Projectile(projPos, "Blue projectile", self.spriteDB, self.weapon, self.drawDirection, self, "Normal")
        self.projList.append(newProjectile)

    def swordP_Attack(self, checkList):
        for obj in checkList:
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):

                if self.drawDirection == 0:         # Facing West
                    if obj.pos[0] > self.pos[0]:    # If the object is to your right, skip it
                        continue
                elif self.drawDirection == 1:       # Facing East
                    if obj.pos[0] < self.pos[0]:    # If the object is to your left, skip it
                        continue
                elif self.drawDirection == 2:       # Facing North
                    if obj.pos[1] > self.pos[1]:    # If the object is below you, skip it
                        continue
                elif self.drawDirection == 3:       # Facing South
                    if obj.pos[1] < self.pos[1]:    # If the object is above you, skip it
                        continue

                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1])
                distance = distance.length()

                # 96 is the distance the Scythe reaches (192/2)
                if distance < 96:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[5] * self.damageScale

    def scytheP_Attack(self, checkList):
        for obj in checkList:
            if obj == self:    # Don't check hits against yourself
                continue
            if isinstance(obj, Player) or isinstance(obj, Enemy):
                # Calculates the distance (scalar) between the hit point and the object
                distance = math2d.Vector2(obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1])
                distance = distance.length()

                # 96 is the distance the Scythe reaches (192/2)
                if distance < 96:        # If the object is hit, handle the hit (below)
                    if isinstance(obj, Player):
                        obj.lastHitByPlayer = True
                    self.playHitSound(obj)
                    obj.health -= self.weapon[5] * self.damageScale

    def bowP_Attack(self, checkList):
        if self.drawDirection == 0:
            projPos = math2d.Vector2(self.pos[0] - 64, self.pos[1] - 20)
        elif self.drawDirection == 1:
            projPos = math2d.Vector2(self.pos[0] + 64, self.pos[1] - 20)
        elif self.drawDirection == 2:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] - 64)
        elif self.drawDirection == 3:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] + 64)

        newProjectile = Projectile(projPos, "flaming_arrow", self.spriteDB, self.weapon, self.drawDirection, self, "Power")
        self.projList.append(newProjectile)

    def staffP_Attack(self, checkList):
        if self.drawDirection == 0:
            projPos = math2d.Vector2(self.pos[0] - 64, self.pos[1] - 20)
        elif self.drawDirection == 1:
            projPos = math2d.Vector2(self.pos[0] + 64, self.pos[1] - 20)
        elif self.drawDirection == 2:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] - 64)
        elif self.drawDirection == 3:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] + 64)

        newProjectile = Projectile(projPos, "purple projectile", self.spriteDB, self.weapon, self.drawDirection, self, "Power")
        self.projList.append(newProjectile)

    def p_attack(self, checkList = None):
        """ checkList is the list of objects to test for a hit.
            Check to see if the player hits anything.
            If there is a hit, handle it. """
        if self.state == 0:
            if self.is_attacking or self.paCharge < 1.0:
                return None                       # If the player is already attacking or on cooldown, nothing will happen.

            self.paCharge = 0.0                   # Needs to recharge back up to 1 before it can be used again
            self.pAttackColor = (0,0,255)
            self.is_p_atk = True
            self.hand_frame = 0

            if self.weapon[0] == "Sword" or self.weapon[0] == "StrongSword":
                self.appPtr.sounds["sword"].play()
                self.swordP_Attack(checkList)
            elif self.weapon[0] == "Scythe":
                self.appPtr.sounds["Scythe"].play()
                self.scytheP_Attack(checkList)

            elif self.weapon[0] == "Bow":
                self.appPtr.sounds["arrow"].play()
                self.bowP_Attack(checkList)

            elif self.weapon[0] == "MagicStaff":
                self.appPtr.sounds["staff"].play()
                self.staffP_Attack(checkList)

    def pickUpWeapon(self, newWeapon):
        self.weapon = newWeapon.value[1]
        self.weaponSprite = self.spriteDB.get(self.weapon[0])
        if newWeapon.value[0] == "Melee":
            self.name = "Knight"
            self.sprite = self.spriteDB.get("Knight")
        elif newWeapon.value[0] == "Ranged":
            self.name = "Archer"
            self.sprite = self.spriteDB.get("Archer")
        elif newWeapon.value[0] == "Magic":
            self.name = "Mage"
            self.sprite = self.spriteDB.get("Mage")

    def update(self, dT, checkList, w):
        Mover.update(self, dT, checkList, w)

        if self.is_attacking:         # Attacking
            self.hand_action = 0

        elif self.is_p_atk:           # P-attacking
            self.hand_action = 1

        elif self.curAction == 0:     # Walking
            self.hand_action = 0

        elif self.curAction == 3:     # Idle
            self.hand_action = 1

        self.hand_frameTime += dT     # Add to the hand frame timer

        if self.paCharge < 1.0:
            self.paCharge += dT / self.weapon[3]     # Divide dT by the cooldown to increase paCharge by a percentage
        else:
            self.pAttackColor = (255,0,255)          # Not even sure what this is, but I think it's necessary for GUI things

        if self.atkCooldown < 1.0:
            self.atkCooldown += dT / self.weapon[2]  # Divide dT by the cooldown of the attack to increase by percentage

        if self.walkDmgTimer < 1.0:
            self.walkDmgTimer += dT   # Increment the damage timer for walking over enemies

        if self.hand_frameTime >= self.animDelay:
            self.hand_frame += 1      # Change to the next hand frame
            self.hand_frameTime = 0   # Reset the timer to 0
            if self.hand_frame < 4:
                if self.weapon[0] == "Sword" or self.weapon[0] == "StrongSword":
                    self.hitPtFar = math2d.Vector2(self.weapon[8][self.drawDirection][self.hand_frame][0][0] + self.pos[0],
                                                   self.weapon[8][self.drawDirection][self.hand_frame][0][1] + self.pos[1])
                    self.hitPtNear = math2d.Vector2(self.weapon[8][self.drawDirection][self.hand_frame][1][0] + self.pos[0],
                                                    self.weapon[8][self.drawDirection][self.hand_frame][1][1] + self.pos[1])
                if self.weapon[0] == "Scythe":
                    self.hitPtNear = math2d.Vector2(self.weapon[8][self.drawDirection][self.hand_frame][0][0] + self.pos[0],
                                                    self.weapon[8][self.drawDirection][self.hand_frame][0][1] + self.pos[1])
                    self.hitPtFar = math2d.Vector2(self.weapon[8][self.drawDirection][self.hand_frame][1][0] + self.pos[0],
                                                   self.weapon[8][self.drawDirection][self.hand_frame][1][1] + self.pos[1])
            if self.hand_frame >= 4:
                self.hand_frame = 0   # Reset back to the first frame
                self.hand_frameTime = 0
                self.is_attacking = False
                self.is_p_atk = False

        trapCheck = (w.isSpotTrap((self.pos[0]), (self.pos[1])-5))
        if trapCheck != -1 and self.state == 0:
            #Pit
            if trapCheck == 0:
                self.lastHitByPlayer = False
                self.fall()
                self.appPtr.sounds["fall"].play()
            #Spikes
            elif trapCheck == 1:
                if self.walkDmgTimer >= 1:
                    if self.lavaBool == True:
                        self.appPtr.sounds["lava"].stop()
                        self.lavaBool = False
                    self.appPtr.sounds["spike"].play()
                    self.lastHitByPlayer = False
                    self.health -= 10
                    self.appPtr.sounds[random.choice(("hit1", "hit2", "hit3"))].play()
                    self.walkDmgTimer = 0
                    self.speed = 75
            #Lava
            if trapCheck == 2:
                if self.lavaBool == False:
                    self.appPtr.sounds["lava"].play()
                    self.lavaBool = True
                if self.walkDmgTimer >= 1:
                    self.lastHitByPlayer = False
                    self.health -= 20
                    self.appPtr.sounds[random.choice(("hit1", "hit2", "hit3"))].play()
                    self.walkDmgTimer = 0
                    self.speed = 75
        else:
            self.speed = 200
            self.appPtr.sounds["lava"].stop()
            self.lavaBool = False
        for obj in checkList:
            if isinstance(obj, Enemy):
                if obj.AI == "chase":
                    obj.visibles = checkList

    def respawn(self,world):
        spawnPoints = copy.deepcopy(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
        self.state = 0                      # Revert the state of the player to 0 (normal)
        self.health = 100                   # Return the player to full health
        spawnIndex = random.randint(0, len(spawnPoints) - 1)
        self.pos = spawnPoints[spawnIndex]  # Put the player's position at the chosen spawnPoint (randomly picked from possible spawnPoints)
        self.pos = math2d.Vector2(self.pos[0], self.pos[1])   # To make sure position is a vector, not a tuple
        if not world.isSpotWalkable(self.pos[0], self.pos[1], "normal") or world.isSpotTrap(self.pos[0], self.pos[1]-5)!=-1:
            print("Trying respawn again, you got stuck in a wall or trap!")
            self.respawn(world)
        self.weapon = BigDict.BigDict["Pickups"]["Weapons"]["Melee"][0]  # Sets self.weapon to the Sword list
        self.weaponSprite = self.spriteDB.get(self.weapon[0])
        self.sprite = self.spriteDB.get("Human")
        self.name = "Human"

    def render(self, surf, cameraPos):
        if self.drawDirection == 2:                 # If the player is facing up...
            self.render_hand(surf, cameraPos)       # render the hands first
            Mover.render(self, surf, cameraPos)     # ...and the player is on top of the hands

        else:                                       # If the player is facing right/down/left...
            Mover.render(self, surf, cameraPos)     # render the player first
            self.render_hand(surf, cameraPos)       # ...and the hands are on top of the player

    def render_hand(self, surf, cameraPos):
        """ Renders the hands """
        if self.is_attacking or self.is_p_atk:      # If the player is attacking or power attacking, render the weapon

            surf.blit(self.weaponSprite, (self.pos[0] - 96 - cameraPos[0], self.pos[1] - 96 - cameraPos[1]), (self.hand_frame * 192,
                    self.hand_action * 768 + self.drawDirection * 192, 192, 192))
##            try:    # A strange error was occuring; this is to handle that error
##                    # Draw the red dot at the tip of the sword, using the point list
##                if self.weapon[0] == "Sword" or self.weapon[0] == "StrongSword" or self.weapon[0] == "Scythe":
##                    pygame.draw.circle(surf, (255,0,0), (int(self.hitPtFar[0] - cameraPos[0]), int(self.hitPtFar[1] - cameraPos[1])), self.hitRadius)
##                    pygame.draw.circle(surf, (255,0,0), (int(self.hitPtNear[0] - cameraPos[0]), int(self.hitPtNear[1] - cameraPos[1])), self.hitRadius)
##
##            except: # To handle the strange error case where hitPtFar was not defined before this was called
##                pass

        else:
            surf.blit(self.handSprite, (self.pos[0] - 96 - cameraPos[0], self.pos[1] - 96 - cameraPos[1]), (self.hand_frame * 192 + 3,
                self.hand_action * 768 + self.drawDirection * 192 + 3, 192, 192))

class Enemy(Mover):
    """ A NPC entity. Unable to access Loot. Able to trigger [most?] traps. """
    def __init__(self, pos, sprite, spriteDBase):
        Mover.__init__(self, pos, sprite, spriteDBase)
        self.spriteName = sprite
        self.duration = random.randint(1,5)         # Randomly determines how long the enemy will maintain the same action
        self.direction = random.randint(0,4)        # Picks a random direction.
        self.visibles = []

    def randMove(self, dT, w):
        """ Randomly moves the enemy in a direction for a duration, using self.duration and self.direction """
        self.duration -= dT

        if self.direction == 0:     # If moving west: go left.
            if (w.isSpotWalkable((self.pos[0]) - 16 + self.tempSpeed * dT, (self.pos[1]), "enemy") or (self.spriteName == "ghost" and self.pos[0] > 0)):
                self.pos[0] -= self.tempSpeed * dT
                self.changeDrawDirection(0)
        elif self.direction == 1:   # If moving east: go right.
            if (w.isSpotWalkable((self.pos[0]) + 32 + self.tempSpeed * dT, (self.pos[1]), "enemy") or (self.spriteName == "ghost" and self.pos[0] < w.worldWidthT)):
                self.pos[0] += self.tempSpeed * dT
                self.changeDrawDirection(1)
        elif self.direction == 2:   # If moving north: go up.
            if (w.isSpotWalkable((self.pos[0]), (self.pos[1]) - 16 + self.tempSpeed * dT, "enemy") or (self.spriteName == "ghost" and self.pos[1] > 0)):
                self.pos[1] -= self.tempSpeed * dT
                self.changeDrawDirection(2)
        elif self.direction == 3:   # If moving south: go down.
            if (w.isSpotWalkable((self.pos[0]), (self.pos[1]) + 32 + self.tempSpeed * dT, "enemy") or (self.spriteName == "ghost" and self.pos[1] < w.worldHeightT)):
                self.pos[1] += self.tempSpeed * dT
                self.changeDrawDirection(3)

        if self.duration <= 0:      # Changes direction randomly, then randomly chooses new direction and rate.
            self.changeDrawDirection(self.direction)
            self.duration = random.randint(1,5)
            self.direction = random.randint(0,4)

            if self.AI == "range":  # For ranged enemies
                self.rangeFire(dT, w)

    def chaserMove(self, dT, w):
        """ AI pattern for enemies that chase you """
        chaseDist = 800
        for obj in self.visibles:
            if isinstance(obj, Player):
                # Calculating the distance between the Player and the Enemy
                dist = math2d.Vector2(obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1])
                distLength = dist.length()     # Finding the length of that distance
                # Start chasing the player if the Player is within the chase distance
                if distLength <= chaseDist:
                    direct = dist.normalized()    # Normalizing the distance so that it is a direction only

                    if abs(direct[0]) > abs(direct[1]) and direct[0] < 0:    # Moving more in the x direction; also moving left
                        self.changeDrawDirection(0)
                    elif abs(direct[0]) > abs(direct[1]) and direct[0] > 0:  # Moving more in the x direction; also moving right
                        self.changeDrawDirection(1)
                    elif abs(direct[0]) < abs(direct[1]) and direct[0] < 0:  # Moving more in the y direction; also moving up
                        self.changeDrawDirection(2)
                    elif abs(direct[0]) < abs(direct[1]) and direct[0] > 0:  # Moving more in the y direction; also moving down
                        self.changeDrawDirection(3)

                    # Making sure it doesn't walk through walls
                    #ignoring because GHOSTS ARE HOMING if (w.isSpotWalkable((self.pos[0]) + direct[0] * (self.size + self.tempSpeed * dT), (self.pos[1]))):
                    self.pos[0] += direct[0] * self.tempSpeed * dT
                    #if (w.isSpotWalkable((self.pos[0]), (self.pos[1]) + direct[1] * (self.size + self.tempSpeed * dT))):
                    self.pos[1] += direct[1] * self.tempSpeed * dT

                    break      # After chasing one object, don't chase another
                    # I realize this will cause strange chase patterns if there are multiple players near the object;
                    #    it won't always chase the nearest player with this code. We will implement this if we have time.

    def rangeFire(self, dT, w):
        """AI to fire a projectile in a random direction"""
        if self.drawDirection == 0:
            projPos = math2d.Vector2(self.pos[0] - 64, self.pos[1] - 20)
        elif self.drawDirection == 1:
            projPos = math2d.Vector2(self.pos[0] + 64, self.pos[1] - 20)
        elif self.drawDirection == 2:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] - 64)
        elif self.drawDirection == 3:
            projPos = math2d.Vector2(self.pos[0], self.pos[1] + 64)
        try:
            if projPos:   # Debugging
                newProjectile = Projectile(projPos, "arrow", self.spriteDB, self.weapon, self.drawDirection, self)
                self.projList.append(newProjectile)
        except:
            pass

    def update(self, dT, w, checkList):
        # The Mover.update will be called once enemy sprite sheets are implemented
        # If the format of enemy sprite sheets is different that those of the player,
        #       then there will be a new update for the enemy class.
        Mover.update(self, dT, checkList, w)
        if self.state == 0:
            if self.AI == "random":
                self.randMove(dT, w)
            if self.AI == "chase":
                self.chaserMove(dT, w)
            if self.AI == "range":
                self.randMove(dT, w)

class Loot(Entity):
    """ Any environmental entity that is helpful to the PLAYER.
        Note: Enemies cannot access any loot. """
    def __init__(self, pos, spritename, action, spriteDBase, value=None):
        Entity.__init__(self, pos, spritename, spriteDBase)
        self.action = action  # A string of what the loot DOES (when picked up), either "changeClass" or "heal" for now
        self.value = value    # If it's a potion for example, the amount it heals by

    def render(self, surf, cameraPos):
        """ Draw the blobby shadow (from Entity.render), then draw the current
            sprite on top of it """
        # Draws the shadow by using the render method of the Entity base class
        Entity.render(self, surf, cameraPos)
        # Draws the sprite of this Loot item on top of the shadow
        surf.blit(self.sprite, (self.pos[0] - self.sprite.get_width()/2 - cameraPos[0], self.pos[1] - self.sprite.get_height()/2 - cameraPos[1]))

class Easy(Enemy):
    def __init__(self, pos, spriteName, health, attack, speed, AI, spriteDBase):
        Enemy.__init__(self, pos, spriteName, spriteDBase)
        self.speed = speed      # Each enemy that has a different speed than 100 px/s is specified based upon the enemy
        self.tempSpeed = self.speed
        self.health = health
        self.maxHealth = health # The maximum health - THIS VALUE SHOULD NOT CHANGE ONCE THE ENEMY IS CREATED.
        self.damage = attack    # Is this attack DAMAGE..? - JBrant: I am implementing it as the damage enemies cause when walked on.
        self.AI = AI
        if self.AI == "range":
            self.weapon = BigDict.BigDict["Pickups"]["Weapons"]["Ranged"][0]
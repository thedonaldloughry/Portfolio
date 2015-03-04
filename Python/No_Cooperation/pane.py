import math2d
import entity
import pygame
import idevice
import gui_manager

class Pane(object):

	deadZone = 0.1

	def __init__(self, inputObject, worldPos, moverSpriteDBase, dimensions, world, appPtr, paneScreenPos, paneNum):
		self.appPtr = appPtr
		self.world = world
		self.paneNum = paneNum
		self.idevice = inputObject # Something derived from
								   # idevice.IDevice
		self.surface = pygame.Surface(dimensions)
		self.cameraPos = worldPos - math2d.Vector2(dimensions[0]/2, dimensions[1]/2)
		self.player = entity.Player(worldPos, "Human", moverSpriteDBase, appPtr.soundeffects)
		self.visibleObjects = []
		self.traps = []
		self.trapCheckList = [self.player]
		#self.GManager = gui_manager.GUI_Manager()
		for enemy in world.enemies:
			self.trapCheckList.append(enemy)
		self.paneScreenPos = paneScreenPos

	def render(self, allPanes):
		self.surface.fill((0,0,0))
		# FOR NOW, until a Game Over screen is created, the screen will be BLACK for any player that is dead to another player
		if self.player.state != 2:	# The player is ALIVE
			self.world.renderFloor(self.surface, self.cameraPos)

			for i in range(self.surface.get_height() // self.world.tileWidth + 4):
				yOffset = 0 - (self.cameraPos[1] % self.world.tileHeight)

				alphaTiles = []
				for obj in self.visibleObjects:
					if yOffset + (32 * i) <= (obj.pos[1]+32) - self.cameraPos[1] < yOffset + (32 * (i + 1)):
						alphaTiles.append(obj.pos[0]//32)
						obj.render(self.surface, self.cameraPos)

				for tamborine in allPanes:
					if yOffset + (32 * i) <= (tamborine.player.pos[1]+32) - tamborine.cameraPos[1] < yOffset + (32 * (i + 1)):
						alphaTiles.append(tamborine.player.pos[0]//32)
						tamborine.player.render(self.surface, self.cameraPos)

					#This section (calculating and drawing the red line) somehow uses up 14-18% of the entire game's resources.
	##				if tamborine == self:
	##					p = math2d.VectorN((tamborine.player.pos[0], tamborine.player.pos[1] - 20))
	##					m = p
	##					if isinstance(self.idevice, idevice.Keyboard):
	##						mx, my = pygame.mouse.get_pos()																												#This code draws a line from player towards the mouse or ANALog position,
	##						m = math2d.VectorN((mx + tamborine.cameraPos[0], my + tamborine.cameraPos[1]))																#making it easier to see where you are facing
	##						a = m - p
	##						if a.length() > 100:																														#If direction from player to mouse is too long, the line is shortened
	##							a = a.normalized()
	##							q = p + (a * 100)
	##						else:
	##							q = m
	##					else:
	##						q = p + 100 * math2d.VectorN((self.idevice.gamepad.get_axis(4), \
	##											self.idevice.gamepad.get_axis(3)))
	##
	##					pygame.draw.line(self.surface, (255,0,0), (p[0] - tamborine.cameraPos[0], p[1] - tamborine.cameraPos[1]), (q[0] - tamborine.cameraPos[0], q[1] - tamborine.cameraPos[1]) , 1)

				self.world.renderWallsOneLine(self.surface, yOffset + (32 * i) + self.cameraPos[1], self.cameraPos, alphaTiles)

	def update(self, dT, eList, world, app):
		if self.player.state == 2:
			self.player.health = 0  # If the player is dead, keep the player's health at 0
			self.player.curFrame = 4
		if self.player.state != 2:	# The player is ALIVE.
			# This is already being called in Application -- we DON'T want to do it here...
			#self.idevice.update(eList, app)

			if isinstance(self.idevice, idevice.Keyboard):
				mx, my = pygame.mouse.get_pos()
				mx -= self.paneScreenPos[0]
				my -= self.paneScreenPos[1]
				#gui_manager.GUI_Manager.getMousePos(self, mx, my)
				dx = (mx + self.cameraPos[0]) - self.player.pos[0]
				dy = (my + self.cameraPos[1]) - self.player.pos[1]
			else:
				dx = self.idevice.gamepad.get_axis(4)
				dy = self.idevice.gamepad.get_axis(3)

			if dx > 0 and abs(dx) > abs(dy):										#Direction Key:
				self.player.changeDrawDirection(1)									#0 = West
																					#1 = East
			if dx <= 0 and abs(dx) > abs(dy):										#2 = North
				self.player.changeDrawDirection(0)									#3 = South
			if dy < 0 and abs(dy) >= abs(dx):
				self.player.changeDrawDirection(2)
				self.player.changeAction(0)
			if dy > 0 and abs(dy) >= abs(dx):
				self.player.changeDrawDirection(3)
				self.player.changeAction(0)

			if abs(self.idevice.horiz) <= Pane.deadZone and abs(self.idevice.vert) <= Pane.deadZone:
				self.player.changeAction(3)
			if not abs(self.idevice.horiz) <= Pane.deadZone and abs(self.idevice.vert) <= Pane.deadZone:
				self.player.changeAction(0)

			if self.idevice.actions["attack"] == True:
				self.player.attack(self.visibleObjects)
			#May cause an error later. "attack" passes ^world, "pattack" does not
			if self.idevice.actions["pattack"] == True:
				self.player.p_attack(self.visibleObjects)

			# Notify the player that they should move. Do isSpotWalkable here???
			self.player.onMove(dT, self.idevice.horiz, self.idevice.vert, self.world)
			self.player.update(dT, self.visibleObjects, self.world)

			surfCenter = math2d.Vector2(self.surface.get_width()/2, self.surface.get_height()/2)
			self.player.pos = math2d.Vector2(self.player.pos[0], self.player.pos[1])
			self.cameraPos = self.player.pos - surfCenter
			if self.cameraPos[0] < 0:
				self.cameraPos[0] = 0
			elif self.cameraPos[0] > self.world.worldWidthT * 32 - self.surface.get_width():
				self.cameraPos[0] = self.world.worldWidthT * 32 - self.surface.get_width()
			if self.cameraPos[1] < 0:
				self.cameraPos[1] = 0
			elif self.cameraPos[1] > (self.world.worldHeightT * 32 - self.surface.get_height()):
				self.cameraPos[1] = (self.world.worldHeightT * 32 - self.surface.get_height())

			# Add enemies to the list of visible objects if they are within/near the camera boundaries
			#	  Note: This will NOT add another player to the list yet
			# This needs to be reworked, if possible - it is extremely inefficient

			#self.world.update(dT)

			self.visibleObjects = []
			for enemy in self.world.enemies:
				if self.cameraPos[0] - 100 <= enemy.pos[0] <= self.cameraPos[0] + self.surface.get_width() + 100:
					self.visibleObjects.append(enemy)
			for item in self.world.items:
				if self.cameraPos[0] - 100 <= item.pos[0] <= self.cameraPos[0] + self.surface.get_width() + 100:
					self.visibleObjects.append(item)

			# You can access the list of panes by self.appPtr.panes
			# You can access the player within a pane like self.appPtr.panes[0].player
			for pane in self.appPtr.panes:
				players = pane.player
				if self != players and self.cameraPos[0] - 100 <= players.pos[0] <= self.cameraPos[0] + self.surface.get_width() + 100:
					self.visibleObjects.append(players)

			# See if the player is touching the enemy.
			self.player.walkEnemyDmg(self.visibleObjects)
			self.player.walkLootCheck(self.visibleObjects)

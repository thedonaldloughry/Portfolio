import math2d
import pygame
import pane
import idevice
import world
import spriteDataBase
import soundDataBase
import gui_manager
import BigDict
import random
class Application(object):
	""" Controls:
		   1. all pygame objects
		   2. the list of panes
		   3. world
		   4. sprite database
		   5. sound database
		Calls all methods of every other object in the game"""

	def __init__(self):
		""" Initializes all data """
		self.quit = False
		self.pygameStartup()

		self.soundeffects = soundDataBase.SoundDBase("sounds\\sound effects")

		self.GManager = gui_manager.GUI_Manager(self)

		# Temporarily create a single player (keyboard) & pane
		self.IDeviceMasterList = [idevice.Keyboard()]
		numSticks = pygame.joystick.get_count()
		count = 0
		while numSticks > 0:
			self.IDeviceMasterList.append(idevice.Gamepad(count))
			numSticks -= 1
			count += 1

		self.spriteSheets = spriteDataBase.ImageDBase("imgs\\player")
		self.spriteSheets.addAdditionalDirectory("imgs\\enemy")
		self.spriteSheets.addAdditionalDirectory("imgs\\pickup items")
		#self.spriteSheets = spriteDataBase.ImageDBase("..\\Art")  # Designate a path to your spritesheets folder.
		#self.spriteSheets.addAdditionalDirectory("..\\Art\\Enemies")
		#self.spriteSheets.addAdditionalDirectory("..\\Art\\Pick up items")
		self.tileDBase = spriteDataBase.ImageDBase("imgs\\floor")
		self.tileDBase.addAdditionalDirectory("imgs\\wall")

		self.guiDBase = spriteDataBase.ImageDBase("imgs\\gui")

		#SOUND CODE...
		self.soundeffects = soundDataBase.SoundDBase("sounds\\sound effects")
		self.music = soundDataBase.SoundDBase("sounds\\music")
		self.songs = 6 #How many fight themes are in the music folder...
		self.musicOrder = [random.randint(1,self.songs),] #self.musicOrder will have randomized numbers from one to however many songs there are.
												#Songs are looped in this order, in-game. The following code randomly appends the next numbers...
		newval = None
		numberUnused = False
		counter = 1
		while counter < self.songs: #There are six songs so far.
			val = random.randint(1, self.songs)
			for i in self.musicOrder:
				if val == i:
					numberUnused = False
					break
				else:
					numberUnused = True
			if numberUnused:
				self.musicOrder.append(val)
				counter += 1

		self.musicIndex = 0 #This index is incremented in self.update()
		#self.world = world.World((6,4), self.tileDBase, self.spriteSheets)
		self.panes = []
		# TEMPORARY -- just to test idevice code.
		self.testPos = math2d.Vector2(400,300)

	def onAction(self, action, devNum):
		""" Called once when an 'action' is made (e.g. 'attack',
			'pattack', 'interact', 'use') """
		# TO-DO: Call Player functions
		#print("on action num",devNum)
		dic = self.GManager.handleAction(action,devNum)
		#if(self.GManager.mode=="create" or self.GManager.mode=="menu" or self.GManager.mode=="options" or self.GManager.mode=="title"):
		if dic != None:
			#print(dic)
			dim = dic["dim"]
			#print(dim)
			player = dic["player"]
			#maps = dic["mapping"]
			# Temporarily create a single player (keyboard) & pane
			self.createGame(dic)

##	def setPaneInput(self, dic):
##		maps = dic["mapping"]
##		for i in range(len(maps)):
##			self.panes.idevice = self.IDeviceMasterList[maps[i][1]]


	def createGame(self, dic):
		""" Called after the countdown in the input-chooser screen.  Creates the world and moves all players to
			a random spawn point. """
		dim = dic["dim"]
		player = dic["player"]
		maps = dic["mapping"]
		self.panes = []
		self.world = world.World(dim, self.tileDBase, self.spriteSheets)
		if(player == 1):
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[0][1]], WorldPos, self.spriteSheets, (1024,768),self.world,self, (0,0), 0))				#-------------Resolution Changed From (800,600) to (1024,768)
		if(player == 2):
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[0][1]], WorldPos, self.spriteSheets, (512,768),self.world, self, (0,0), 0))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[1][1]], WorldPos, self.spriteSheets, (512,768),self.world, self, (512,0), 1))		   #NEED TO CHANGE
		if(player == 3):
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[0][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(0,0), 0))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[1][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(512,0), 1))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[2][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(0,384), 2))  	 # 3 player split screen
		if(player == 4):
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[0][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(0,0), 0))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[1][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(512,0), 1))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[2][1]], WorldPos, self.spriteSheets, (512,384),self.world,self,(0,384), 2))
			WorldPos = random.choice(BigDict.BigDict["WorldObjects"]["Spawnpoints"])
			self.panes.append(pane.Pane(self.IDeviceMasterList[maps[3][1]], WorldPos, self.spriteSheets, (512,384),self.world, self,(512,384), 3))	   #4 player split screen

	def refresh(self):
		pygame.joystick.quit()
		pygame.joystick.init()
		self.IDeviceMasterList = [idevice.Keyboard()]
		numSticks = pygame.joystick.get_count()
		count = 0
		while numSticks > 0:
			self.IDeviceMasterList.append(idevice.Gamepad(count))
			numSticks -= 1
			count += 1
		#self.panes = [pane.Pane(self.IDeviceMasterList[count], math2d.Vector2(400,300), self.spriteSheets, (1024,768),self.world)]

	def run(self):
		""" Starts the game. """
		while not self.quit:
			dT = self.clock.tick() / 1000.0
			if pygame.key.get_pressed()[pygame.K_ESCAPE]:
				self.quit = True
			self.update(dT)
			self.render()
		self.pygameShutdown()

	def render(self):
		# Note: We'll probably need to pass the players to this
		# function eventually
        #if self.GManager.mode != "game":
		#if self.GManager.mode in ("game", "title", "main", "menu", "create"):
		if self.GManager.mode != "game" and self.GManager.mode != "input":
			self.GManager.render(self.screen)
		else:
			for pane in self.panes:
				pane.render(self.panes)
				self.GManager.render(pane.surface, pane, self.panes)
			if len(self.panes) == 1:
				self.screen.blit(self.panes[0].surface, (0,0))
			if len(self.panes) == 2:
				self.screen.blit(self.panes[0].surface, (0,0))
				self.screen.blit(self.panes[1].surface, (self.screen.get_width()/2,0))
			if len(self.panes) == 3:
				self.screen.blit(self.panes[0].surface, (0,0))
				self.screen.blit(self.panes[1].surface, (self.screen.get_width()/2,0))
				self.screen.blit(self.panes[2].surface, (0,self.screen.get_height()/2))
			if len(self.panes) == 4:
				self.screen.blit(self.panes[0].surface, (0,0))
				self.screen.blit(self.panes[1].surface, (self.screen.get_width()/2,0))
				self.screen.blit(self.panes[2].surface, (0,self.screen.get_height()/2))
				self.screen.blit(self.panes[3].surface, (self.screen.get_width()/2,self.screen.get_height()/2))
			if len(self.panes) == 2:
				self.screen.blit(self.guiDBase.get("twoPlayer_Split"), (0,0))
			elif len(self.panes) >= 3:
				self.screen.blit(self.guiDBase.get("fourPlayer_Split"), (0,0))
		# Draw the fps on the upper-left
		self.screen.blit(self.debugFont.render("FPS: " + str(round(self.clock.get_fps(),1)), False, (255,0,0), (0,0,0)), (5,5))
		pygame.display.flip()

	def pygameStartup(self):
		""" Load all pygame objects """
		pygame.display.init()
		pygame.joystick.init()
		pygame.font.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
		self.debugFont = pygame.font.SysFont("Courier New", 14)   # Temporary for testing
		self.clock = pygame.time.Clock()

	def update(self, dT):
		eList = pygame.event.get()
		volume = self.GManager.Update(dT) / 10
		if self.GManager.mode == "game":
			if pygame.mixer.music.get_busy() == False:
				MusicSelection = "FightTheme"+str(self.musicOrder[self.musicIndex])+".mp3"
				print(MusicSelection)
				pygame.mixer.music.load("sounds\\music\\"+ MusicSelection)
				pygame.mixer.music.set_volume(volume)
				pygame.mixer.music.play(0, 0.0)
				self.musicIndex += 1
				if self.musicIndex > self.songs - 1:
					self.musicIndex = 0

			self.world.update(dT)
		for dev in self.IDeviceMasterList:
			dev.update(eList, self)
		if self.GManager.mode == "game" or self.GManager.mode == "input":
			for p in self.panes:
				p.update(dT, eList, self.world, self)

		else:
			if pygame.mixer.music.get_busy() == False:
				MusicSelection = "Intro.mp3"
				print(MusicSelection)
				pygame.mixer.music.load("sounds\\music\\"+ MusicSelection)
				pygame.mixer.music.set_volume(volume)
				pygame.mixer.music.play(0, 0.0)


	def onMovement(self, horiz, vert):
		""" Called when a direction change is made (
			i.e. gamepad: dpad / analog, keyboard: u/d/l/r).
			IMPORTANT: This function should only be called
			once for a movement """
		# TO-DO: Call Player functions
		self.GManager.handleMovement(horiz, vert)

	def pygameShutdown(self):
		""" Shuts pygame down """
		pygame.font.quit()
		pygame.joystick.quit()
		pygame.mixer.quit()
		pygame.display.quit()

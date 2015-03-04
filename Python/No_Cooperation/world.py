import entity
import random
import pygame
import math2d
import BigDict

# TEMPORARY
##floor = pygame.image.load("img\\floor.bmp").convert()
##wall = pygame.image.load("img\\wall.bmp").convert()
##item = pygame.image.load("img\\item.png").convert_alpha()
##player = pygame.image.load("img\\player.png").convert_alpha()

class World(object):
	def __init__(self, dim, tileDBase, spriteDBase):
		""" Load the necessary files in the given dimensions """
		self.tileDBase = tileDBase
		self.spriteDBase = spriteDBase
		self.dim = dim
		# self.tileDBase["floor"] is the floor image

		# TEMPORARY
		self.tileWidth = 32
		self.tileHeight = 32
		self.roomWidthT = 32
		self.roomHeightT = 32
		self.EnemyCount = 0
		self.Map = []
		self.worldWR = dim[0]
		self.worldHR = dim[1]

		# For debugging purposes, checking which rooms work
		tempList = []
		for i in range(self.worldHR):
			tempList.append([])
			for j in range(self.worldWR):
				tempList[i].append(-1)

		# (temporary) Seed the random generator so we get the same map every time
		#random.seed(42)

		self.worldWidthT = self.worldWR * self.roomWidthT
		self.worldHeightT = self.worldHR * self.roomHeightT
		for i in range(self.worldWR):
			for j in range(self.worldHR):
				choose = str(random.randint(0,49))
				if len(str(choose))==1:
					tempList[j][i] = "0"+choose
				else:
					tempList[j][i] = choose
				#to create a map full of randomly selected rooms:
				room = open("maps\\room"+choose+".txt", "r")
				orientation = random.choice((0,1)) #if zero, room is appended normally. if one, a mirror image of the room is appended
				l = 0
				for line in room:
					line = list(line.strip("\n"))
					if orientation == 1:
						#Thing that reverses...
						temp = []
						#This counts down to -1, but not including -1. So 0 is the final value of k...
						for k in range(len(line)-1, -1, -1):
							temp += line[k]
						line = temp
					if len(line)!=32:
						print("ERROR IN "+choose)
					if i==0:
						self.Map.append(line)
					else:
						self.Map[(j*self.roomHeightT)+l] += line
						l += 1
				room.close()
		print(len(self.Map))
		print(len(self.Map[0]))
		print(len(self.Map[0][0]))

		# Debugging:
		print("Rooms:")
		c = 0
		for i in range(self.worldHR):
			print(tempList[i])

		self.fix()
		self.polish()
		self.populate()

		self.worldHeightT = len(self.Map)
		self.worldWidthT = self.worldWR * self.roomWidthT


	def fix(self):
		""" Correct the map borders and room exits """
		# FINISH ME (Ian).  Also do the random floor / wall textures
		for i in range(self.dim[0]*32):
			self.Map[0][i]='x'
			self.Map[self.worldHeightT-1][i]='x'
		for j in range(self.dim[1]*32):
			self.Map[j][0]='x'
			self.Map[j][self.worldWidthT-1]='x'

	def polish(self):
		""" Adds in random tile changes and sector styles """
		borderH = (self.worldHR+1)//4
		borderW = (self.worldWR+1)//4
		self.terList = []
		for i in range(self.worldHR):
			self.terList.append([])
			for j in range(self.worldWR):
				if (j<borderW or j>(self.worldWR-borderW)-1) or (i<borderH or i>(self.worldHR-borderH)-1):
					if i<(self.worldHR//2):
						if j<(self.worldWR//2):
							self.terList[i].append("for")
						else:
							self.terList[i].append("des")
					else:
						if j<(self.worldWR//2):
							self.terList[i].append("ice")
						else:
							self.terList[i].append("lav")
				else:
					self.terList[i].append("cas")

		for i in range(len(self.Map)):
			for j in range(len(self.Map[i])):
				ter = self.terList[i//32][j//32]
				tile = self.Map[i][j]
				self.Map[i][j] += ter



	def populate(self):
		""" Scans the map and creates Enemy, Trap, Loot objects """
		# Do Traps to start with, then eventually add the other type of "things"
		BigDict.BigDict["WorldObjects"]["Spawnpoints"] =[]
		self.enemies = []
		self.chests = []
		self.items = []
		tempdict = BigDict.BigDict
		# Scans through entire map code and documents the entities position in pixels
		for line in range(len(self.Map)):
			for var in range(len(self.Map[line])):
				tmp = self.Map[line][var][0]
				tmp2 = self.Map[line][var][1:]

				pos = []
				entityX = var * 32
				entityY = line * 32
				pos = math2d.Vector2(entityX, entityY)
				self.spawnEnemies
				if tmp == "c":
					 pass #self.chests.append(entity.chests(pos, "chest", self.spriteDBase))
				elif tmp == "s":
					if line < 32:
						#Top bar of map
						BigDict.BigDict["WorldObjects"]["Spawnpoints"].append(pos)
					elif line > ((self.dim[1] - 1) * 32):
						#Bottom bar of map
						BigDict.BigDict["WorldObjects"]["Spawnpoints"].append(pos)
					elif var < 32:
						#Left bar of map
						BigDict.BigDict["WorldObjects"]["Spawnpoints"].append(pos)
					elif  var > ((self.dim[0] - 1) * 32):
						#Right bar of map
						BigDict.BigDict["WorldObjects"]["Spawnpoints"].append(pos)

					 #self.chests.append(entity.chests(pos, self.spriteDBase))
	def spawnEnemies(self):
		"""respawns enemies"""
		tempdict = BigDict.BigDict
		for line in range(len(self.Map)):
			for var in range(len(self.Map[line])):
				tmp = self.Map[line][var][0]
				tmp2 = self.Map[line][var][1:]

				pos = []
				entityX = var * 32
				entityY = line * 32
				pos = math2d.Vector2(entityX, entityY)
				tmpChoice = random.randint(0,3)
				#create an instance of an enemy
				if tmp == "e":
				   #make a random enemy
					#id = random.randint(1,1) #b is the total amount of different enemies in the game, currently set at 1 because there is only the slime
					#if id == 1:
					#choice = random.choice("Easy")
					if tmp2 == "cas":
						if tmpChoice == 0:
							choice = "Medium"
						else:
							choice = "Hard"

					elif tmp2 == "des":
						tmpChoice = random.randint(0,3)
						if tmpChoice == 0 or tmpChoice == 1:
							choice = "Easy"
						elif tmpChoice == 2 or tmpChoice == 3:
							choice = "Medium"

					elif tmp2 == "lav":
						tmpChoice = random.randint(0,3)
						if tmpChoice == 0:
							choice = "Easy"
						elif tmpChoice == 1 or tmpChoice == 2:
							choice = "Medium"
						else:
							choice = "Hard"

					elif tmp2 == "ice":
						tmpChoice = random.randint(0,3)
						if tmpChoice == 0:
							choice = "Easy"
						elif tmpChoice == 1 or tmpChoice == 2:
							choice = "Medium"
						else:
							choice = "Hard"

					elif tmp2 == "for":
						if 0 <= tmpChoice <= 2:
							choice = "Easy"
						else:
							choice = "Medium"

					choice2 = random.choice(tuple(tempdict["Enemies"][choice].keys()))
					imgname = tempdict["Enemies"][choice][choice2][0]
					health = tempdict["Enemies"][choice][choice2][1]
					attack = tempdict["Enemies"][choice][choice2][2]
					speed = tempdict["Enemies"][choice][choice2][3]
					AI= tempdict["Enemies"][choice][choice2][4]
					self.enemies.append(entity.Easy(pos, imgname, health, attack, speed, AI, self.spriteDBase))
					self.EnemyCount = len(self.enemies)


	def isSpotWalkable(self, x, y, entity = "normal"):
		""" Returns True if a player / enemy can walk on this position, False or not """
		#Called in entity.py, Player class, onMove method
		#First, convert pixel pos to tile pos...
		worldTilePos = (int(x // self.tileWidth), int(y // self.tileHeight))
		#look at what letter or character is in the Map that tile position by
		#first indexing the row, and then indexing the column.
		try:
			if self.Map[worldTilePos[1]][worldTilePos[0]][0] == 'x':
				return False
		except:
			pass
		if entity == "enemy":
			try:
				if self.Map[worldTilePos[1]][worldTilePos[0]][0] == 'p' or self.Map[worldTilePos[1]][worldTilePos[0]][0] == 'P' or\
				self.Map[worldTilePos[1]][worldTilePos[0]][0] == '1' or self.Map[worldTilePos[1]][worldTilePos[0]][0] == '2':
					return False
			except:
				pass
		return True

	def isSpotTrap(self, x, y):
		"""Returns True if player walks on trap"""
		#Simillar code as isSpotwalkable
		#Returns True if tile is a trap and false for any other cases
		#should be used to detect if player is on a pit or lava tile
		trapTile = (int(x // self.tileWidth), int(y // self.tileWidth))
		if self.Map[trapTile[1]][trapTile[0]][0] == "p":
			return 0
		if self.Map[trapTile[1]][trapTile[0]][0] == "P":
			return 0
		elif self.Map[trapTile[1]][trapTile[0]][0] == "1":
			return 1
		elif self.Map[trapTile[1]][trapTile[0]][0] == "2":
			return 2
		else:
			return -1

	def isSpotPit(self, x, y):
		"""Returns True if player walks on trap"""
		#Simillar code as isSpotwalkable
		#Returns True if tile is a trap and false for any other cases
		#should be used to detect if player is on a pit or lava tile
		trapTile = (int(x // self.tileWidth), int(y // self.tileWidth))
		if self.Map[trapTile[1]][trapTile[0]][0] == "p":
			return True
		elif self.Map[trapTile[1]][trapTile[0]][0] == "P":
			return True
		else:
			return False

	def dropLoot(self, enemy):
	   """drops random item when enemy dies"""
	   tempDict = BigDict.BigDict
	   choice = random.choice(tuple(tempDict["Items"].keys()))
	   print(choice)
	   spritename = tempDict["Items"][choice][0]
	   action = tempDict["Items"][choice][1]
	   data = tempDict["Items"][choice][2]
	   self.items.append(entity.Loot(enemy.pos, spritename, action, self.spriteDBase, data))

	def renderWallsOneLine(self, surf, screenPixelY, cameraPos, transList):
		""" Renders a line of walls, doors, etc. """
		# FINISH ME (Dakota)
		#line get the title pos Y
		liney = int(screenPixelY // 32)
		liney2 = int(cameraPos[1] // 32)
		#print(screenPixelY)
		#loop through to render one line at cameraPos
		if liney >= self.worldHeightT:
			return
		start = int(cameraPos[0]//32)-1
		for i in range(start,start+2+(surf.get_width()//32)):
				try:
					if i >= len(self.Map[liney]):
						break
					trans=""
					for t in transList:
						if (t-2)<i<(t+2) and (self.Map[liney][int(t)][0]=="x"):
							trans="t"
				except:
					pass
				wallCode = self.Map[liney][i]
				if wallCode[0] == "x":
					surf.blit(self.tileDBase.get(wallCode[1:]+"_wall"+trans),(i*32 - int(cameraPos[0]),(liney*32)-64 - int(cameraPos[1])))

	def renderFloor(self, surf, cameraPos):
		""" Called once for each pane.  Draws the tile map
			to that pane relative to the given camera pos. """
		# FINISH ME (Maurice)
		startX = int(cameraPos[0] // self.tileWidth)
		startY = int(cameraPos[1] // self.tileHeight)
		curScreenYP = int(-(cameraPos[1] % self.tileHeight))
		sw = surf.get_width()
		sh = surf.get_height()
		tw = sw // self.tileWidth + 2
		th = sh // self.tileHeight + 2
		for i in range(th):
			curScreenXP = int(-(cameraPos[0] % self.tileWidth))
			for j in range(tw):
				if i + startY < self.worldHeightT and j + startX < self.worldWidthT:
					tileCode = self.Map[i + startY][j + startX]
					if tileCode[0] == "p":
						surf.blit(self.tileDBase.get(tileCode[1:]+"_pit") , (curScreenXP, curScreenYP))
					elif tileCode[0] == "P":
						surf.blit(self.tileDBase.get(tileCode[1:]+"_pitt") , (curScreenXP, curScreenYP))
					elif tileCode[0] == "1":
						surf.blit(self.tileDBase.get(tileCode[1:]+"_spikes") , (curScreenXP, curScreenYP-4))
					elif tileCode[0] == "2":
						surf.blit(self.tileDBase.get(tileCode[1:]+"_lava") , (curScreenXP+4, curScreenYP+4))
					elif tileCode[0] != "x":
						#print("blit")
						#print(curScreenXP, curScreenYP)
						surf.blit(self.tileDBase.get(tileCode[1:]+"_floor") , (curScreenXP, curScreenYP))

				curScreenXP += self.tileWidth
			curScreenYP += self.tileHeight
	#read text file
	#make dictionary
	BigDict = {}


##  Method will be created that creates a dictionary which will hold a dictionary for each different weapon
##  This dictionary will be passed to pane. From there this dictionary to player when a new weaopon is picked up.

	def update(self, dT):
		checklist =[]
		""" Resposible for moving all enemies, dropping loot, removing "dead" loot, etc. """
		for enemy in self.enemies:
			enemy.update(dT,self,checklist)
			if enemy.state==2:
				print("DEAD")
				self.dropLoot(enemy)
				self.enemies.remove(enemy)
		for item in self.items:
			if item.state == 2:
				self.items.remove(item)
		#added in a check to see how many enemies are in the game, if it is x% below, it respawn ALL of them. So the more they respawn, the more will be on the map
		#it keeps things interesting and non boring and can add a challenge mode for single player later down the road.
		if len(self.enemies) <= .50*(self.EnemyCount):
			self.spawnEnemies()



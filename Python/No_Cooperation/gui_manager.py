import pygame
import math2d
import math
import pane
import soundDataBase
import BigDict # 16, 716

class GUI_Manager(object):
	def __init__(self, app):
		self.appPtr = app
		self.mode = "title"		 # 'menu', 'credits', 'options',
		self.selectionV = 1	  # 'create', 'game','input', 'title'
		self.selectionH = 2
		self.width=4
		self.height=5
		self.playernum=1
		self.music=10
		self.soundfx=1
		self.played = False
		self.compassAngle = 50.0
		self.pAttackColor = (0,0,255)
		self.amongTheLiving = []
		self.mapping = []
		# Font objects/ images.
		button_dic={"creditsButB":pygame.image.load("imgs\\gui\\Main Menu\\Credits_Black.png"),"creditsButR":pygame.image.load("imgs\\gui\\Main Menu\\Credits_Red.png"),\
					"optionsButB":pygame.image.load("imgs\\gui\\Main Menu\\Options_Black.png"),"optionsButR":pygame.image.load("imgs\\gui\\Main Menu\\Options_Red.png"),\
					"ngamebutB":pygame.image.load("imgs\\gui\\Main Menu\\NewGame_Black.png"),"ngamebutR":pygame.image.load("imgs\\gui\\Main Menu\\NewGame_Red.png"),\
					"LArrowB":pygame.image.load("imgs\\gui\\Main Menu\\leftArrow_Black.png"),"LArrowR":pygame.image.load("imgs\\gui\\Main Menu\\leftArrow_Red.png"),\
					"RArrowR":pygame.image.load("imgs\\gui\\Main Menu\\rightArrow_Red.png"),"RArrowB":pygame.image.load("imgs\\gui\\Main Menu\\rightArrow_Black.png"),\
					"startButB":pygame.image.load("imgs\\gui\\Main Menu\\Start_Black.png"),"startButR": pygame.image.load("imgs\\gui\\Main Menu\\Start_Red.png"),\
					"backButB":pygame.image.load("imgs\\gui\\Main Menu\\Back_Black.png"),"backButR":pygame.image.load("imgs\\gui\\Main Menu\\Back_Red.png")}
		menu_dic={"main":pygame.image.load("imgs\\gui\\Main Menu\\MainMenu.png"),"create":pygame.image.load("imgs\\gui\\Main Menu\\newgame.png"),"options":pygame.image.load("imgs\\gui\\Main Menu\\options.png"),"title":pygame.image.load("imgs\\gui\\titlescreen.png")}
		screen_dic={"player 2":pygame.image.load("imgs\\gui\\twoPlayer_Split.png"),"player 4":pygame.image.load("imgs\\gui\\fourPlayer_Split.png")}
		compass_dic={"compassNeedle":pygame.image.load("imgs\\pickup items\\CompassNeedlePU.png"),"compassBackground":pygame.image.load("imgs\\pickup items\\CompassPU.png")}
		icon_dic={"Sword":pygame.image.load("imgs\\pickup items\\ClaymorePU.png"),"StrongSword":pygame.image.load("imgs\\pickup items\\ClaymorePU.png"),"MagicStaff":pygame.image.load("imgs\\pickup items\\staffPU.png"),"Bow":pygame.image.load("imgs\\pickup items\\BowPU.png"),"Scythe":pygame.image.load("imgs\\pickup items\\ScythePU.png")}
		#main dictorany
		self.gui_dic={"button":button_dic,"menu":menu_dic,"screen":screen_dic,"compass":compass_dic, "icon":icon_dic}

		#Health Bar dictionary
		self.playericon2_dic={"Human":pygame.image.load("imgs\\healthbar\\Unarmed.png"),"Knight":pygame.image.load("imgs\\healthbar\\knight.png"),"Mage":pygame.image.load("imgs\\healthbar\\mage.png"),"Archer":pygame.image.load("imgs\\healthbar\\archer.png")}
		self.playericon4_dic={"Human":pygame.image.load("imgs\\healthbar\\Unarmed4.png"),"Knight":pygame.image.load("imgs\\healthbar\\knight4.png"),"Mage":pygame.image.load("imgs\\healthbar\\mage4.png"),"Archer":pygame.image.load("imgs\\healthbar\\archer4.png")}

		self.testFont = pygame.font.SysFont("Times New Roman", 12)
		self.MainMenu = pygame.image.load("imgs\\gui\\Main Menu\\MainMenu.png")
		self.CreateMenu = pygame.image.load("imgs\\gui\\Main Menu\\newgame.png")
		self.OptionsMenu = pygame.image.load("imgs\\gui\\Main Menu\\options.png")
		#self.noCoOpFont = pygame.font.Font("imgs\\gui\\HDirtyWhore-Regular", 12)
		self.title_img = pygame.image.load("imgs\\gui\\titlescreen.png")

		#---Input images---#
		self.iconKeyboard = pygame.image.load("imgs\\gui\\Mouse and Keyboard.png")
		self.iconGamepad  = pygame.image.load("imgs\\gui\\Xbox_Controller.png")
		#------------------#
		self.Font50 = pygame.font.Font("game font\\HDirtyWhore-Regular.ttf", 50)


		# Number of Windows
		#self.numWindows = None
		#Adjust volume
		#self.appPtr.soundeffects.sounds["click1"].set_volume(1 * self.soundfx)
		#self.appPtr.soundeffects.sounds["click2"].set_volume(0.3 * self.soundfx)
		self.played = False

	def Update(self, dT):
		""" Updates the value for self.initPowerCharge
			and the mouse position on the GUI. """
		self.gMouse = pygame.mouse.get_pos()
		self.dT = dT
		return self.music

	def CompassDirection(self, curPane, paneList):  #Handles the direction of the compass to point to the nearest opponent.
		""" Takes the positions of every player on the screen
		(needs to handle the case where there is only one player),
		creates vector objects between the current player and every other
		player, finds the distance between every player and the current player
		(call the length function of math2D), and then calls math.atan2(vectorY,
		vectorX) to find the angle that we need to rotate the compass needle."""
		frenemyList = []											# List of other players that you may/may not want to kill (their positions).
		distanceList = []									   # List of distances between yourself and every other player.
		curPlayerPos = curPane.player.pos						   # Where you are.
		if len(paneList) != 1:								  # If there's more than one player on screen...
			for p in paneList:								  # For every pane...
				if p != curPane and p.player.state != 2:									# If it's not the pane that you are on...
					frenemyList.append(p.player.pos)				# Add the position of the player in that pane to frenemyList.
			for frenemy in frenemyList:						 # For every player position in frenemyList...
				curVector = frenemy - curPlayerPos				  # Create a vector by subtracting your position from the "frenemy"'s position.
				curDistance = curVector.length()					# Find the length of that vector.
				distanceList.append(curDistance)					# Append that length to distanceList.
			i = frenemyList[distanceList.index(min(distanceList))]  # Working backwards, we find the index number of the minimum value of distanceList, and we make i equal to the item in frenemyList at that same index.
			closestVector = i - curPlayerPos						# The closest vector is that item in frenemyList's value minus your positon.
			self.compassAngle = -(math.degrees(math.atan2(closestVector[1],closestVector[0])) % 360)
		else:
			self.compassAngle = 90

	def render(self, surf, pane = None, paneList = None):
		""" surf will be the entire screen.  Draw the
			GUI for the current game mode. Include a check
			to see if the player is currently dead. If so,
			display a game over screen.  """
		self.mx, self.my = pygame.mouse.get_pos()
		#the font size
		Font20 = pygame.font.SysFont("Times New Roman", 20)
		#Font21 = pygame.font.SysFont("HDirtyWhore-Regular.ttf", 20)
		Font32 = pygame.font.SysFont("Times New Roman", 38)
		#surf
		tempS = Font20.render("Menu", False, (250,0,0))
		#color
		fontcolor=(255,255,255)
		self.fontcolor2=fontcolor
		buttoncolorhit=(255,0,255)
		buttoncolor=(120,120,120)

		#title page
		if(self.mode == "title"):
			surf.fill((128,128,128))
			surf.blit(self.gui_dic["menu"]["title"], (0,0))

		#menu page
		elif(self.mode == "menu"):
			#menu surf
			MenuSurf = self.gui_dic["menu"]["main"]
			tempS1 = Font20.render("create", False, fontcolor)
			tempS2 = Font20.render("option", False, fontcolor)
			tempS3 = Font20.render("credit", False, fontcolor)
			bcolor = (128,0,0)
			surf.fill(bcolor)

			Y=395
			X=435
			#menu
			surf.blit(MenuSurf, (0,0))

			#create button
			pygame.draw.rect(surf, (bcolor), ((X),Y+55-tempS1.get_height()/2,140, 40), 0)
			surf.blit(self.gui_dic["button"]["ngamebutB"], (512-self.gui_dic["button"]["ngamebutB"].get_width()/2,Y+60-self.gui_dic["button"]["ngamebutB"].get_height()/2))
			#option button
			pygame.draw.rect(surf, (bcolor), ((X),Y+120-tempS2.get_height()/2,140, 40), 0)
			surf.blit(self.gui_dic["button"]["optionsButB"], (512-self.gui_dic["button"]["optionsButB"].get_width()/2,Y+130-self.gui_dic["button"]["optionsButB"].get_height()/2))
			#credit button
			pygame.draw.rect(surf, (bcolor), ((X),Y+200-tempS3.get_height()/2,140, 40), 0)
			surf.blit(self.gui_dic["button"]["creditsButB"], (512-self.gui_dic["button"]["creditsButB"].get_width()/2,Y+210-self.gui_dic["button"]["creditsButB"].get_height()/2))

			#collision hit
			r = pygame.Rect(((X),Y+40-tempS1.get_height()/2,155, 60))
			r1 = pygame.Rect(((X),Y+110-tempS2.get_height()/2,155, 60))
			r2 = pygame.Rect(((X),Y+200-self.gui_dic["button"]["creditsButB"].get_height()/2,155, 80))

			#draw rectangles to screen (debug, will blit objects later)
			#move with gamepad and  keyboard
			if(r.collidepoint(self.mx,self.my) or self.selectionV == 1 ):
				self.selectionV = 1
				pygame.draw.rect(surf, (bcolor),  ((X),Y+40-tempS1.get_height()/2,155, 60), 0)
				surf.blit(self.gui_dic["button"]["ngamebutR"], (512-self.gui_dic["button"]["ngamebutR"].get_width()/2,Y+60-self.gui_dic["button"]["ngamebutR"].get_height()/2))
			if(r1.collidepoint(self.mx,self.my) or self.selectionV == 2):
				self.selectionV = 2
				pygame.draw.rect(surf, (bcolor), ((X),Y+110-tempS2.get_height()/2,155, 60), 0)
				surf.blit(self.gui_dic["button"]["optionsButR"], (512-self.gui_dic["button"]["optionsButR"].get_width()/2,Y+130-self.gui_dic["button"]["optionsButR"].get_height()/2))
			if(r2.collidepoint(self.mx,self.my) or self.selectionV == 3):
				self.selectionV = 3
				pygame.draw.rect(surf, (bcolor), ((X),Y+200-self.gui_dic["button"]["creditsButR"].get_height()/2,155, 80), 0)
				surf.blit(self.gui_dic["button"]["creditsButR"], (512-self.gui_dic["button"]["creditsButR"].get_width()/2,Y+210-self.gui_dic["button"]["creditsButR"].get_height()/2))
			#sound click
			if(r.collidepoint(self.mx,self.my) or (self.selectionV == 1)):
				if not self.played:
					#print("hi")
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
			elif(r1.collidepoint(self.mx,self.my) or (self.selectionV == 2)):
				if not self.played:
					#print("hi2")
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
			elif(r2.collidepoint(self.mx,self.my) or (self.selectionV == 3)):
				if not self.played:
					#print("hi3")
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
			else:
				#print("hi4")
				self.played = False

		#credits
		elif(self.mode == "credits"):
			#------------------------------------------------------------------------------#
			surf.fill((0,0,0))
			# Initial variables
			win_width=1024
			win_height=768
			List = ["NO COOPERATION","SPRING 2013","Thomas Edwards", "Richard Janita", "Parker Kahle",\
					"Tom Paxton", "Dan Perkins", "Idris Said", "Cody Wheeler",\
					"Maurice McPherson", "John Bickel", "Rhashaun Hurt",\
					"Jimmy Albracht", "Ian Whitt", "Dakota Terry","Will Harmon",\
					"Caleb Brown", "Matt Benson","Kris Grimsley", "Don Loughry", \
					"Matt Robinson", "Cory Davis", "Joseph Brant"]
			R = 255
			G = 255
			B = 255
			Black = 0
			Speed = 40 * self.dT
			X = win_width // 2
			Y = win_height // 2
			NumSize = 30
			TimesFont = pygame.font.SysFont("Times New Roman", NumSize)
			self.StartY -= Speed
			# Earse
			surf.fill((0,0,0))
			# Draw
			self.DrawY = self.StartY
			for i in range(len(List)):
				if self.DrawY > 576 and self.DrawY < 768:
					R = (768 - self.DrawY) * 1.3
					G = 0
					B = 0
					color = (R,G,B)
				elif self.DrawY > 384 and self.DrawY < 576:
					R = (self.DrawY - 384) * 1.3
					G = (576 - self.DrawY) * 1.3
					B = 0
					color = (R,G,B)
				elif self.DrawY > 192 and self.DrawY < 384:
					R = 0
					G = (self.DrawY - 192) * 1.3
					B = (384 - self.DrawY) * 1.3
					color = (R, G, B)
				elif self.DrawY > 0 and self.DrawY < 192:		 #------------------------------#
					R = 0										 # I had to take the inverse of
					G = 0										 # the inverse because otherwise
					B = (self.DrawY * 1.3)						 # there was an odd junp between
					color = (Black, Black, B)					 # the light blue and dark blue
				else:											 #------------------------------#
					color = (Black,Black,Black)

				tempS = TimesFont.render(List[i], 1, color)
				half_width = tempS.get_width() / 2
				surf.blit(tempS, (X - half_width, self.DrawY))
				self.DrawY += NumSize
			#------------------------------------------------------------------------------#
			# Flip
			pygame.display.flip()
			if(self.DrawY<=0):
				self.mode = "menu"


		#options
		elif(self.mode == "options"):
			#option surf
			OptionSurf = self.gui_dic["menu"]["options"]
			tempS6 = Font20.render(str(self.soundfx), False, fontcolor)
			tempS7 = Font20.render(str(self.music), False, fontcolor)
			tempS8 = Font20.render("back to menu", False, fontcolor)
			bcolor = (128,0,0)
			surf.fill(bcolor)
			Y=450
			X=440
			buttoncolor = (bcolor)
			surf.blit(OptionSurf, (0,0))
			#audio background button
			# -
			pygame.draw.rect(surf, buttoncolor, ((X+2),Y+55-tempS6.get_height()/2,33, 35), 0)
			#surf.blit(self.gui_dic["button"]["LArrowB"], (X+2,Y+60-self.gui_dic["button"]["LArrowB"].get_height()/2))
			#num
			pygame.draw.rect(surf, (0,0,0), ((X+40),Y+55-tempS6.get_height()/2,46, 35), 0)
			#surf.blit(tempS6, (503-tempS6.get_width()/2,Y+61-tempS6.get_height()/2))
			# +
			pygame.draw.rect(surf, buttoncolor, ((X+90),Y+55-tempS6.get_height()/2,33, 35), 0)
			#surf.blit(self.gui_dic["button"]["RArrowB"], (X+90,Y+60-self.gui_dic["button"]["RArrowB"].get_height()/2))
			#audio music button
			# +
			pygame.draw.rect(surf, buttoncolor, ((X),Y+135-tempS7.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["LArrowB"], (X,Y+60-self.gui_dic["button"]["LArrowB"].get_height()/2))
			#num
			#pygame.draw.rect(surf, (0,0,0), ((X+38),Y+135-tempS6.get_height()/2,46, 35), 0)
			surf.blit(tempS7, (503-tempS7.get_width()/2,Y+60-tempS7.get_height()/2))
			# -
			pygame.draw.rect(surf, buttoncolor, ((X+88),Y+135-tempS7.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["RArrowB"], (X+88,Y+60-self.gui_dic["button"]["RArrowB"].get_height()/2))
			#back button
			pygame.draw.rect(surf, buttoncolor, ((X+30),Y+184-tempS8.get_height()/2,64, 35), 0)
			surf.blit(self.gui_dic["button"]["backButB"], (X,Y+190-self.gui_dic["button"]["backButB"].get_height()/2))
			pygame.draw.rect(surf,buttoncolor, ((X),Y,150,40))

			#collision hit
			r3 = pygame.Rect((X+2),Y+55-tempS6.get_height()/2,33, 35)
			r4 = pygame.Rect((X+90),Y+55-tempS6.get_height()/2,33, 35)
			r5 = pygame.Rect((X),Y+135-tempS7.get_height()/2,33, 35)
			r14 = pygame.Rect((X+88),Y+135-tempS7.get_height()/2,33, 35)
			r15 = pygame.Rect((X),Y+195-self.gui_dic["button"]["backButB"].get_height()/2,125, 50)

			#right
##			if(r3.collidepoint(self.mx,self.my) or (self.selectionV == 1  and self.selectionH == 1)):
##				self.selectionV = 1
##				self.selectionH = 1
##				if not self.played:
##					self.appPtr.soundeffects.sounds["click1"].play()
##					self.played = True
##				surf.blit(self.gui_dic["button"]["LArrowR"], (X+2,Y+60-self.gui_dic["button"]["LArrowR"].get_height()/2))
			#left
##			if(r4.collidepoint(self.mx,self.my) or (self.selectionV == 1  and self.selectionH == 2)):
##				self.selectionV = 1
##				self.selectionH = 2
##				if not self.played:
##					self.appPtr.soundeffects.sounds["click1"].play()
##					self.played = True
##				surf.blit(self.gui_dic["button"]["RArrowR"], (X+90,Y+60-self.gui_dic["button"]["RArrowR"].get_height()/2))
			#right
			if(r3.collidepoint(self.mx,self.my) or (self.selectionV == 2  and self.selectionH == 1)):
				self.selectionV = 2
				self.selectionH = 1
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				surf.blit(self.gui_dic["button"]["LArrowR"], (X+2,Y+60-self.gui_dic["button"]["LArrowR"].get_height()/2))
			#left
			if(r4.collidepoint(self.mx,self.my) or (self.selectionV == 2  and self.selectionH == 2)):
				self.selectionV = 2
				self.selectionH = 2
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				surf.blit(self.gui_dic["button"]["RArrowR"], (X+90,Y+60-self.gui_dic["button"]["RArrowR"].get_height()/2))
			#back
			if(r15.collidepoint(self.mx,self.my) or (self.selectionV == 3)):
				self.selectionV = 3
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				surf.blit(self.gui_dic["button"]["backButR"], (X,Y+190-self.gui_dic["button"]["backButR"].get_height()/2))

		elif(self.mode == "create"):
			CreateSurf = self.gui_dic["menu"]["create"]
			tempS4 = Font20.render("-", False, fontcolor)
			tempS5 = Font20.render(str(self.playernum), False, fontcolor)
			tempS9 = Font20.render("+", False, fontcolor)
			tempS12 = Font20.render(str(self.width), False, fontcolor)
			tempS13 = Font20.render(str(self.height), False, fontcolor)
			tempS14 = Font20.render("start game ", False, fontcolor)
			tempS15 = Font20.render("menu", False, fontcolor)
			Y=365
			X=455
			bcolor = (128,0,0)
			surf.fill(bcolor)
			surf.blit(CreateSurf, (0,0))
			#player
			#----------------------------------------------------------------------------------#
			#left
			surf.blit(self.gui_dic["button"]["LArrowB"], ((X-21),Y+139-tempS4.get_height()/2,33, 35))
			#num
			pygame.draw.rect(surf, (0,0,0), ((X+18),Y+135-tempS5.get_height()/2,43,35), 0)
			surf.blit(tempS5, (493-tempS5.get_width()/2,Y+140-tempS5.get_height()/2))
			#right
			surf.blit(self.gui_dic["button"]["RArrowB"], ((X+67),Y+139-tempS5.get_height()/2,33,35))
			#----------------------------------------------------------------------------------#
			#size
			#----------------------------------------------------------------------------------#
			#left
			pygame.draw.rect(surf, (bcolor), ((X+28),Y+215-tempS4.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["LArrowB"], ((X+28),Y+220-tempS4.get_height()/2,33, 35))
			#num
			pygame.draw.rect(surf, (0,0,0), ((X+68),Y+215-tempS4.get_height()/2,39, 35), 0)
			surf.blit(tempS12, (540-tempS4.get_width()/2,Y+220-tempS4.get_height()/2))
			#Right
			pygame.draw.rect(surf, (bcolor), ((X+116),Y+215-tempS4.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["RArrowB"], ((X+116),Y+220-tempS4.get_height()/2,33, 35))
			#left
			pygame.draw.rect(surf, (bcolor), ((X+29),Y+269-tempS4.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["LArrowB"], ((X+29),Y+273-tempS4.get_height()/2,33, 35))
			#num
			pygame.draw.rect(surf, (0,0,0), ((X+69),Y+270-tempS4.get_height()/2,39, 35), 0)
			surf.blit(tempS13, (541-tempS4.get_width()/2,Y+275-tempS4.get_height()/2))
			#right
			pygame.draw.rect(surf, (bcolor), ((X+117),Y+268-tempS4.get_height()/2,33, 35), 0)
			surf.blit(self.gui_dic["button"]["RArrowB"], ((X+117),Y+273-tempS4.get_height()/2,33, 35))

			#----------------------------------------------------------------------------------#

			#start
			pygame.draw.rect(surf, (bcolor), ((X - 65),Y+325-self.gui_dic["button"]["startButB"].get_height()/2,125, 65), 0)
			surf.blit(self.gui_dic["button"]["startButB"], (450-self.gui_dic["button"]["startButB"].get_width()/2,Y+330-self.gui_dic["button"]["startButB"].get_height()/2))
			#back
			pygame.draw.rect(surf, (bcolor), ((X+65),Y+315-tempS5.get_height()/2,125,55), 0)
			surf.blit(self.gui_dic["button"]["backButB"], (582-self.gui_dic["button"]["backButB"].get_width()/2,Y+330-self.gui_dic["button"]["backButB"].get_height()/2))
			#collision hit
			#player
			r6 = pygame.Rect((X-21),Y+135-tempS4.get_height()/2,33, 35)
			r7 = pygame.Rect((X+67),Y+135-tempS5.get_height()/2,33,35)
			#size
			r8 = pygame.Rect((X+28),Y+215-tempS4.get_height()/2,33, 35)
			r9 = pygame.Rect((X+116),Y+215-tempS4.get_height()/2,33, 35)
			r10 = pygame.Rect((X+117),Y+268-tempS4.get_height()/2,33, 35)
			r11 = pygame.Rect((X+29),Y+269-tempS4.get_height()/2,33, 35)
			#start
			r12 = pygame.Rect((X - 65),Y+325-self.gui_dic["button"]["startButB"].get_height()/2,125, 65)
			#end
			r13 = pygame.Rect((X+65),Y+315-tempS5.get_height()/2,125,55)

			#player number
			if(r6.collidepoint(self.mx,self.my) or (self.selectionV == 1 and self.selectionH == 1)):
				#print("R6")
				self.selectionV = 1
				self.selectionH = 1
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#right
				surf.blit(self.gui_dic["button"]["LArrowR"], ((X-21),Y+139-tempS4.get_height()/2,33, 35))

			if(r7.collidepoint(self.mx,self.my) or (self.selectionV == 1 and self.selectionH == 2)):
				#print("R7")
				self.selectionV = 1
				self.selectionH = 2
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#left
				surf.blit(self.gui_dic["button"]["RArrowR"], ((X+67),Y+139-tempS5.get_height()/2,33,35))

			#width
			if(r8.collidepoint(self.mx,self.my) or (self.selectionV == 2 and self.selectionH == 1)):
				#print("R8")
				self.selectionV = 2
				self.selectionH = 1
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#left
				surf.blit(self.gui_dic["button"]["LArrowR"], ((X+28),Y+220-tempS4.get_height()/2,33, 35))

			if(r9.collidepoint(self.mx,self.my) or (self.selectionV == 2 and self.selectionH == 2)):
				#print("R9")
				self.selectionV = 2
				self.selectionH = 2
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#right
				surf.blit(self.gui_dic["button"]["RArrowR"], ((X+116),Y+220-tempS4.get_height()/2,33, 35))

			#height
			if(r11.collidepoint(self.mx,self.my) or (self.selectionV == 3 and self.selectionH == 1)):
				#print("R10")
				self.selectionV = 3
				self.selectionH = 1
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#right
				surf.blit(self.gui_dic["button"]["LArrowR"], ((X+29),Y+273-tempS4.get_height()/2,33, 35))

			if(r10.collidepoint(self.mx,self.my) or (self.selectionV == 3 and self.selectionH == 2)):
				#print("R11")
				self.selectionV = 3
				self.selectionH = 2
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#left
				surf.blit(self.gui_dic["button"]["RArrowR"], ((X+117),Y+273-tempS4.get_height()/2,33, 35))

			#start game and back
			if(r12.collidepoint(self.mx,self.my) or (self.selectionV == 4 and self.selectionH == 1)):
				#print("R12")
				self.selectionV = 4
				self.selectionH = 1
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#start
				surf.blit(self.gui_dic["button"]["startButR"], (450-self.gui_dic["button"]["startButR"].get_width()/2,Y+330-self.gui_dic["button"]["startButR"].get_height()/2))

			if(r13.collidepoint(self.mx,self.my) or (self.selectionV == 4 and self.selectionH == 2)):
				#print("R13")
				self.selectionV = 4
				self.selectionH = 2
				if not self.played:
					self.appPtr.soundeffects.sounds["click1"].play()
					self.played = True
				#back
				surf.blit(self.gui_dic["button"]["backButR"], (582-self.gui_dic["button"]["backButR"].get_width()/2,Y+330-self.gui_dic["button"]["backButR"].get_height()/2))


		elif(self.mode == "input"):
			for i in range(self.playernum):
				if i == pane.paneNum:
					if i < len(self.mapping):
						surf.fill((128,0,0))
						#if(i == len(self.mapping) - 1):
						#	print("Self.Mapping: ", len(self.mapping) - 1)
						if(self.mapping[i][1] == 0):
								surf.blit(self.iconKeyboard, (50, 50))
						else:
							#print("Gamepad Draw", len(self.mapping))
							surf.blit(self.iconGamepad, (50, 50))
					else:
					   surf.fill((255,255,255))

				#--MESSAGE--#
				tempS20 = self.Font50.render("Press Attack After", False, self.fontcolor2)
				tempS21 = self.Font50.render("Everyone Enters", False, self.fontcolor2)
				surf.blit(tempS20, (50, 150))
				surf.blit(tempS21, (50, 210))
				#-----------#

		elif(self.mode =="game"):
			if len(paneList) == 1:
				# Circle Alpha Cutout!

				tempSurf = pygame.Surface((64,64))
				circleCutout = pygame.Surface((64,64))
				circleCutout.fill((0,0,0))
				pygame.draw.circle(circleCutout, (254,254,254), (32,32), 32)   # Border (optional)
				pygame.draw.circle(circleCutout, (255,255,255), (32,32), 31)   # Must be white for the color key
				circleCutout.set_colorkey((255,255,255))
				tempSurf.fill((0,0,0))
				# POWER ATTACK BAR (BLIT WEAPON ICON IN FRONT OF THIS!!!)
				pygame.draw.rect(tempSurf, (self.pAttackColor), (0, 64, 64,64 * -(pane.player.paCharge)))
				# Blits the Cutout!

				tempSurf.blit(circleCutout, (0,0))
				tempSurf.set_colorkey((0,0,0))	  # Make border areas outside the circle transparent
				surf.blit(tempSurf, (2, 702))	# Copy the completed overlay to the screen
				surf.blit(self.gui_dic["icon"][pane.player.weapon[0]], (18,718))

				# ATTACK AND POWERATTACK BUTTON INDICATORS
				pygame.draw.rect(surf, (0,255,0), (surf.get_width() - (surf.get_width() - 66), surf.get_height() - 67, surf.get_width() // 30, surf.get_height() // 20))
				pygame.draw.rect(surf, (255,0,0), (surf.get_width() - (surf.get_width() - 66), surf.get_height() - 35, surf.get_width() // 30, surf.get_height() // 20))
				surf.blit(self.testFont.render("ATK", False, (0,0,0)), (surf.get_width() - (surf.get_width() - 72), surf.get_height() - 60))
				surf.blit(self.testFont.render("PWR", False, (0,0,0)), (surf.get_width() - (surf.get_width() - 70), surf.get_height() - 23))

				# HEALTH BAR
				p2x = 111 + (pane.player.health*2)
				bPL = ((111, 63), (309, 63), (283, 89), (81, 89))
				rPL = ((111, 65), (304, 65), (282, 87), (87, 87))
				gPL =  ((111, 65), (p2x, 65), ((p2x-22), 87), (87, 87))
				pPL = ((36, 57), (116, 57), (80, 93), (46, 93), (16, 68))

				pygame.draw.polygon(surf,(0,0,0), bPL, 0)
				pygame.draw.polygon(surf,(255,0,0),rPL , 0)
				pygame.draw.polygon(surf,(111,111,111), pPL, 0)
				pygame.draw.polygon(surf,(0,0,0), pPL, 3)
				pygame.draw.polygon(surf,(0,255,0), gPL, 0)
				surf.blit(self.playericon2_dic[pane.player.name], (0,0))

				# COMPASS
				self.CompassDirection(pane, paneList)
				surf.blit(self.gui_dic["compass"]["compassBackground"], (surf.get_width() - 64, surf.get_height() - 64))
				tempS = pygame.transform.rotate(self.gui_dic["compass"]["compassNeedle"], self.compassAngle)
				surf.blit(tempS, (surf.get_width() - 32 - tempS.get_width() / 2, surf.get_height() - 32 - tempS.get_height()/2))

			elif len(paneList) == 2:
				# Check to see if the game has ended.
				if len(self.amongTheLiving) <= 1:
					self.mode == "GameOver"
				# Circle Alpha Cutout!

				tempSurf = pygame.Surface((64,64))
				circleCutout = pygame.Surface((64,64))
				circleCutout.fill((0,0,0))
				pygame.draw.circle(circleCutout, (254,254,254), (32,32), 32)   # Border (optional)
				pygame.draw.circle(circleCutout, (255,255,255), (32,32), 31)   # Must be white for the color key
				circleCutout.set_colorkey((255,255,255))
				tempSurf.fill((0,0,0))
				# POWER ATTACK BAR (BLIT WEAPON ICON IN FRONT OF THIS!!!)
				pygame.draw.rect(tempSurf, (self.pAttackColor), (0, 64, 64,64 * -(pane.player.paCharge)))
				# Blits the Cutout!

				tempSurf.blit(circleCutout, (0,0)) # REMEMBER: 18, 358 AND 2, 326
				tempSurf.set_colorkey((0,0,0))	  # Make border areas outside the circle transparent
				surf.blit(tempSurf, (2, 702))	# Copy the completed overlay to the screen
				surf.blit(self.gui_dic["icon"][pane.player.weapon[0]], (18,718))
				# ATTACK AND POWERATTACK BUTTON INDICATORS
				pygame.draw.rect(surf, (0,255,0), (62, surf.get_height() - 33, 30, 30))
				pygame.draw.rect(surf, (255,0,0), (62, surf.get_height() - 63, 30, 30))
				surf.blit(self.testFont.render("ATK", False, (0,0,0)), (66, surf.get_height() - 55))
				surf.blit(self.testFont.render("PWR", False, (0,0,0)), (64, surf.get_height() - 25))

				# HEALTH BAR
				p2x = 111 + (pane.player.health*2)
				bPL = ((111, 63), (309, 63), (283, 89), (81, 89))
				rPL = ((111, 65), (304, 65), (282, 87), (87, 87))
				gPL =  ((111, 65), (p2x, 65), ((p2x-22), 87), (87, 87))
				pPL = ((36, 57), (116, 57), (80, 93), (46, 93), (16, 68))

				pygame.draw.polygon(surf,(0,0,0), bPL, 0)
				pygame.draw.polygon(surf,(255,0,0),rPL , 0)
				pygame.draw.polygon(surf,(111,111,111), pPL, 0)
				pygame.draw.polygon(surf,(0,0,0), pPL, 3)
				pygame.draw.polygon(surf,(0,255,0), gPL, 0)
				surf.blit(self.playericon2_dic[pane.player.name], (0,0))

				# COMPASS
				self.CompassDirection(pane, paneList)
				surf.blit(self.gui_dic["compass"]["compassBackground"], (surf.get_width() - 64, surf.get_height() - 64))
				tempS = pygame.transform.rotate(self.gui_dic["compass"]["compassNeedle"], self.compassAngle)
				surf.blit(tempS, (surf.get_width() - 32 - tempS.get_width() / 2, surf.get_height() - 32 - tempS.get_height()/2))

			else:
				# Circle Alpha Cutout!

				tempSurf = pygame.Surface((64,64))
				circleCutout = pygame.Surface((64,64))
				circleCutout.fill((0,0,0))
				pygame.draw.circle(circleCutout, (254,254,254), (32,32), 32)   # Border (optional)
				pygame.draw.circle(circleCutout, (255,255,255), (32,32), 31)   # Must be white for the color key
				circleCutout.set_colorkey((255,255,255))
				tempSurf.fill((0,0,0))
				# POWER ATTACK BAR (BLIT WEAPON ICON IN FRONT OF THIS!!!)
				pygame.draw.rect(tempSurf, (self.pAttackColor), (0, 64, 64,64 * -(pane.player.paCharge)))
				# Blits the Cutout!

				tempSurf.blit(circleCutout, (0,0)) # REMEMBER: 18, 358 AND 2, 326
				tempSurf.set_colorkey((0,0,0))	  # Make border areas outside the circle transparent
				surf.blit(tempSurf, (2, 316))	# Copy the completed overlay to the screen
				surf.blit(self.gui_dic["icon"][pane.player.weapon[0]], (18,334))


				#surf.blit(self.gui_dic["icon"][pane.player.weapon[0]], (10, 340))
				# ATTACK AND POWERATTACK BUTTON INDICATORS
				pygame.draw.rect(surf, (0,255,0), (surf.get_width() - (surf.get_width() - 64), surf.get_height() - 61, 25, 25))
				pygame.draw.rect(surf, (255,0,0), (surf.get_width() - (surf.get_width() - 64), surf.get_height() - 36, 25, 25))
				surf.blit(self.testFont.render("ATK", False, (0,0,0)), (surf.get_width() - (surf.get_width() - 64), surf.get_height() - 58))
				surf.blit(self.testFont.render("PWR", False, (0,0,0)), (surf.get_width() - (surf.get_width() - 64), surf.get_height() - 31))

				# HEALTH BAR
				p2x = 94 + (pane.player.health*1.8)
				bPL =  ((92, 48), (279, 48), (259, 68), (72, 68))
				rPL =  ((94, 50), (274, 50), (258, 66), (78, 66))
				gPL =  ((94, 50), (p2x, 50), ((p2x-16), 66), (78, 66))
				pPL =  ((33, 42), (99, 42), (69, 72), (41, 72), (16, 52))

				pygame.draw.polygon(surf,(0,0,0), bPL, 0)
				pygame.draw.polygon(surf,(255,0,0),rPL , 0)
				pygame.draw.polygon(surf,(111,111,111), pPL, 0)
				pygame.draw.polygon(surf,(0,0,0), pPL, 3)
				pygame.draw.polygon(surf,(0,255,0), gPL, 0)
				surf.blit(self.playericon4_dic[pane.player.name], (0,0))

				# COMPASS
				self.CompassDirection(pane, paneList)
				surf.blit(self.gui_dic["compass"]["compassBackground"], (surf.get_width() - 64, surf.get_height() - 64))
				tempS = pygame.transform.rotate(self.gui_dic["compass"]["compassNeedle"], self.compassAngle)
				surf.blit(tempS, (surf.get_width() - 32 - tempS.get_width() / 2, surf.get_height() - 32 - tempS.get_height()/2))

		elif self.mode == "GameOver":
			gameOverSurf = pygame.image.load("")
			surf.fill(255,0,0)

	def handleMovement(self, horiz, vert):
		""" horiz and vert are in the range -1...+1.
			This method only changes the state of self.selection, which
			should be used in the render method to determine which box is
			currently being highlighted. """
		#input for title
		if( self.mode == "title"):
			self.selectionV = 1	 # If the player goes back to the main screen, the selection variable resets to 1.

		#input for input
		elif( self.mode == "input"):
			self.selectionV = 1

		#input for menu
		elif( self.mode == "menu"):
			if( vert == 1):
				self.selectionV += 1
			elif( vert == -1):
				self.selectionV -= 1
			if( self.selectionV > 3):
				self.selectionV = 1
			elif( self.selectionV < 1):
				self.selectionV = 3

		#input for options
		elif( self.mode == "options"):
			if( vert == 1 ):
				self.selectionV += 1
			elif( vert == -1):
				self.selectionV -= 1
			if( horiz == 1 ):
				self.selectionH += 1
			elif( horiz == -1):
				self.selectionH -= 1
			if( self.selectionH > 2): # This assumes that the "create game" screen has three options and a "back" button, lined up vertically.							1  3
				self.selectionH = 1  # Additional conditional statements may be needed: i.e. if self.selection == 2 and horiz == 1: self.selection = 4, assuming a grid of 2  4.
			elif( self.selectionH < 1):
				self.selectionH = 2
			if( self.selectionV > 3): # This assumes that the "create game" screen has three options and a "back" button, lined up vertically.							1  3
				self.selectionV = 1  # Additional conditional statements may be needed: i.e. if self.selection == 2 and horiz == 1: self.selection = 4, assuming a grid of 2  4.
			elif( self.selectionV < 1):
				self.selectionV = 3

		#input for create
		elif(self.mode == "create"):
			if( vert == 1 ):
				self.selectionV += 1
			elif( vert == -1):
				self.selectionV -= 1
			if( horiz == 1 ):
				self.selectionH += 1
			elif( horiz == -1):
				self.selectionH -= 1
			if( self.selectionH > 2): # This assumes that the "create game" screen has three options and a "back" button, lined up vertically.							1  3
				self.selectionH = 1  # Additional conditional statements may be needed: i.e. if self.selection == 2 and horiz == 1: self.selection = 4, assuming a grid of 2  4.
			elif( self.selectionH < 1):
				self.selectionH = 2
			if( self.selectionV > 4): # This assumes that the "create game" screen has three options and a "back" button, lined up vertically.							1  3
				self.selectionV = 1  # Additional conditional statements may be needed: i.e. if self.selection == 2 and horiz == 1: self.selection = 4, assuming a grid of 2  4.
			elif( self.selectionV < 1):
				self.selectionV = 4

	def handleAction(self, action, gamepad):
		""" action will be one of 'attack',
			'pattack', 'interact', 'use', '?'.  Possibly
			change the GUI mode, etc.  The return
			value should be 1, 2, 3, or 4 iff we're
			in 'create' screen and we've hit the
			'start' button.  In all other cases, it should
			be None """
		rv={}
		#title
		#print(action)
		if(self.mode == "title"):
			if(self.selectionV == 1 and action == "attack"):
				self.appPtr.soundeffects.sounds["click2"].play()
				self.mode = "menu"
			if(self.selectionV == 1 and action == "pattack"):
				rv["player"] = 1
				rv["dim"] = (4,4)
				#soundDataBase.SoundDBase.sounds["click2"].play()
				self.appPtr.soundeffects.sounds["click2"].play()
				self.mode = "game"
				pygame.mixer.music.fadeout(1000) #Stops the title song
				#return rv

		#menu
		elif(self.mode == "menu"):
			if(self.selectionV == 1 and action == "attack"):
				self.appPtr.soundeffects.sounds["click2"].play()
				self.mode = "create"
			elif(self.selectionV == 2 and action == "attack"):
				self.appPtr.soundeffects.sounds["click2"].play()
				self.mode = "options"
			elif(self.selectionV == 3 and action == "attack"):
				self.appPtr.soundeffects.sounds["click2"].play()
				self.mode = "credits"
				self.StartY = 768

		#input
		elif(self.mode == "input"):

			if action == "attack":
				if len(self.mapping) == self.playernum:
					rv["player"] = self.playernum
					rv["dim"] = (self.width,self.height)
					rv["mapping"] = self.mapping
					self.mode = "game"
					pygame.mixer.music.fadeout(1000) #Stops the title song
					return rv

				in_list = False
				for m in self.mapping:
					if m[1] == gamepad:
						in_list = True
						break
				if not in_list:
					#print("Adding ", gamepad, "to mapping number")
					mappingNum = len(self.mapping)
					self.mapping.append([mappingNum, gamepad])





		#create menu
		elif(self.mode == "create"):
			if(self.selectionV == 1):
				if(self.selectionH == 1 and action == "attack"):
					self.playernum -= 1
					if(self.playernum < 1):
						self.playernum = pygame.joystick.get_count() + 1

				if(self.selectionH == 2 and action == "attack"):
					self.playernum += 1
					if(self.playernum > pygame.joystick.get_count() + 1):
					   self.playernum = 1

			elif(self.selectionV == 2):
				if(self.selectionH == 1 and action == "attack"):
					self.width -= 1
					if(self.width < 4):
						self.width = 10

				if(self.selectionH == 2 and action == "attack"):
					self.width += 1
					if(self.width > 10):
						self.width = 4

			elif(self.selectionV == 3):
				if(self.selectionH == 1 and action == "attack"):
					self.height -= 1
					if(self.height < 4):
						self.height = 10

				if(self.selectionH == 2 and action == "attack"):
					self.height += 1
					if(self.height > 10):
						self.height = 4

			elif(self.selectionV == 4):
				if(self.selectionH == 1 and action == "attack"):
					self.mode = "input"
					self.selectionV = 1
					rv["player"] = self.playernum
					rv["dim"] = (self.width,self.height)
					rv["mapping"] = [[0,0], [1,0], [2,0], [3,0]]
					return rv
				if(self.selectionH == 2 and action == "attack"):
					self.mode = "menu"

		#options menu
		elif(self.mode == "options"):
			#BACKGORUND
			if(self.selectionV == 1):
				#+
				if(self.selectionH == 2 and action == "attack"):
					self.soundfx += 1
					if(self.soundfx > 10):
						self.soundfx = 0
				#-
				if(self.selectionH == 1 and action == "attack"):
					self.soundfx -= 1
					if(self.soundfx < 0):
						self.soundfx=0

			elif(self.selectionV == 2):
				if(self.selectionH == 1 and action == "attack"):
					self.music -= 1
					if(self.music < 0):
						self.music = 10

				if(self.selectionH == 2 and action == "attack"):
					self.music += 1
					if(self.music > 10):
						self.music = 10
				pygame.mixer.music.set_volume(self.music / 10)

			elif(self.selectionV == 3 and action == "attack"):
				self.mode = "menu"

		#credit scene
		elif(self.mode == "credits"):
			if(action == "attack"):
				self.mode = "menu"
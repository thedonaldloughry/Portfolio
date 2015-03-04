import pygame
import application

class IDevice(object):
	""" A Generic input device.  We will define classes that
		inherit from this. """
	deadZone = 0.1

	def __init__(self):
		self.horiz = 0.0   # Movement in the x-direction [-1.0 ... 1.0]
		self.vert = 0.0	# ................y-........................
		self.actions = {"attack" : False,
						"pattack" : False,
						"weapon swap" : False,
						"use powerup" : False
                        }

	def update(self, eList, app):
		""" Check for change of state """
		pass

class Gamepad(IDevice):
	""" Controls input from 360 controller. Derived from IDevice class."""
	def __init__(self, controllerNumber):
		IDevice.__init__(self)
		self.gamepad = pygame.joystick.Joystick(controllerNumber)
		self.gamepad.init()
		self.buttonIDs = [0,1,2,3,(0,1),(1,0),(-1,0),(0,-1)]
		self.value = 0 # temp

		self.id = controllerNumber + 1
		print(self.id)
	def update(self, eList, app):
		self.horiz = self.gamepad.get_axis(0)
		self.vert = self.gamepad.get_axis(1)
		#app.onMovement(self.horiz, self.vert)
		if abs(self.horiz) <= IDevice.deadZone and abs(self.vert) <= IDevice.deadZone:
			self.horiz, self.vert = self.gamepad.get_hat(0)
			self.vert = -(self.vert)
		if abs(self.horiz) <= IDevice.deadZone and abs(self.vert) <= IDevice.deadZone:
			 self.horiz = 0
			 self.vert = 0

		for e in eList:
			if e.type == pygame.JOYAXISMOTION:
				#print(e.joy, e.axis, e.value)
				pass
				#if e.value >= 0.6 or e.value <= -0.6:
				#if self.horiz >= 0.6 or self.horiz <= -0.6 or \
				#   self.vert >= 0.6 or self.vert <= -0.6:
				#	app.onMovement(self.horiz, self.vert)
			#Trigger Attack Buttons
			if self.gamepad.get_axis(2) <= -0.5:
				self.actions["attack"] = True
			if self.gamepad.get_axis(2) >= 0.5:
				self.actions["pattack"] = True
			if not self.gamepad.get_button(0):
				self.actions["attack"] = False
			if not self.gamepad.get_button(1):
				self.actions["pattack"] = False

			if e.type == pygame.JOYBUTTONDOWN:
				if self.gamepad.get_button(5):
					self.actions["attack"] = True
					#print("attack")
					app.onAction("attack", self.id)
					#print("0, Attack")
				if self.gamepad.get_button(4):
					self.actions["pattack"] = True
					app.onAction("pattack", self.id)
					#print("1, P-Attack")
				if self.gamepad.get_button(2):
					self.actions["weapon swap"] = True
					#print("2, weapon swap")
				if self.gamepad.get_button(3):
					self.actions["use powerup"] = True
					#print("3, Use Powerup")

			elif e.type == pygame.JOYBUTTONUP:
				#if not self.gamepad.get_button(0):
				if e.button == 5:
					self.actions["attack"] = False
				if e.button == 4:
					self.actions["pattack"] = False
				if e.button == 2:
					self.actions["weapon swap"] = False
				if e.button == 3:
					self.actions["use powerup"] = False

			elif e.type == pygame.JOYHATMOTION:
				app.onMovement(e.value[0], -e.value[1])

class Keyboard(IDevice):
	""" Controls input from keyboard and mouse. Derived from IDevice class."""
	def __init__(self):
		IDevice.__init__(self)

	def update(self, eList, app):
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]:
			self.horiz = -1

		elif keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]:
			self.horiz = 1
		else:
			self.horiz = 0

		if keysPressed[pygame.K_UP] or keysPressed[pygame.K_w]:
			self.vert = -1

		elif keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_s]:
			self.vert = 1
		else:
			self.vert = 0

		for e in eList:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LEFT or e.key == pygame.K_a:
					app.onMovement(self.horiz, self.vert)

				if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
					app.onMovement(self.horiz, self.vert)

				if e.key == pygame.K_UP or e.key == pygame.K_w:
					app.onMovement(self.horiz, self.vert)

				if e.key == pygame.K_DOWN or e.key == pygame.K_s:
					app.onMovement(self.horiz, self.vert)

				if e.key == pygame.K_f:
					self.actions["weapon swap"] = True

				if e.key == pygame.K_e:
					self.actions["use powerup"] = True
					app.onAction("use powerup", 0)

				if e.key == pygame.K_SPACE:
					app.onAction("attack", 0)
				if e.key == pygame.K_RETURN:
					app.onAction("pattack", 0)

				if e.key == pygame.K_r:
					app.refresh()

			if e.type == pygame.MOUSEBUTTONDOWN:

				if e.button == 1:
					self.actions["attack"] = True
					app.onAction("attack", 0)

				if e.button == 3:
					self.actions["pattack"] = True
					app.onAction("pattack", 0)

			if e.type == pygame.KEYUP:

				if e.key == pygame.K_f:
					self.actions["weapon swap"] = False

			if e.type == pygame.MOUSEBUTTONUP:

				if e.button == 1:
					self.actions["attack"] = False

				if e.button == 3:
					self.actions["pattack"] = False


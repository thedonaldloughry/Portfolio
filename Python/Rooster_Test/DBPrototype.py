import pygame, glob

class spriteDB(object):
	""" Loads every sprite for the game 'No Cooperation', then stores them in a database. """
	def __init__(self, surf):
		#self.entity = entity
		self.surf = surf
		self.dict = {"runEast" : glob.glob("player/runninge*")}

	def loadImages(self):
		""" Load every image file from the images folder. """
		print(glob.glob("player/runninge*"))

pygame.display.init()
screen = pygame.display.set_mode((300,300))
done = False
test = spriteDB(screen)
test.loadImages()
while not done:
	screen.fill((0,0,0))
	pygame.event.pump()
	keyPressed = pygame.key.get_pressed()
	if keyPressed[pygame.K_ESCAPE]:
		done = True

	pygame.display.flip()
pygame.display.quit()








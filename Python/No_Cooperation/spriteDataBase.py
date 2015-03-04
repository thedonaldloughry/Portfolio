import pygame, glob

class ImageDBase(object):
	def __init__(self, path):
		""" Use glob.glob to find all files within the given directory.
			Make the keys the last part of the file name.  e.g. if the
			path is art\tiles, and we find art\tiles\brick.png, the key
			should be "brick".  The values should be the
			pygame surface.  Make sure to do convert_alpha on all images """
		# Loads the images in path
		self.images = {}
		self.addAdditionalDirectory(path)

	def get(self, name):
		""" Returns the pygame surface from the dictionary. """
		return self.images[name]
		
	def addAdditionalDirectory(self, path):
		for img in glob.glob(path + "\\" + "*"):

			try:		# Try to load the image. If it fails, move on to the next one.
				key = img[len(path) + 1: img.rfind(".")] # Slices the string name of every image in the
													   # "Art" folder to leave only a short key name.
				image = pygame.image.load(img).convert_alpha() #Loads every image, converting alpha channels.

				self.images[str(key)] = image # Adds the loaded image, set with its key, into the images dictionary.

			except:
				pass
		
import pygame, glob

# Everything here collects the groups of these filenames found in the attached
# "player" folder, loads them, then places them into their respective lists within
# the sprite database. It works for any number of images of any type.

spriteDict = {"walkNorth": [],
			  "walkSouth": [],
			  "walkEast": [],
			  "walkWest": [],
			  "walkNortheast": [],
			  "walkNorthwest": [],
			  "walkSoutheast": [],
			  "walkSouthwest": [],
			  "talkNorth": [],
			  "talkSouth": [],
			  "talkEast": [],
			  "talkWest": [],
			  "talkNortheast": [],
			  "talkNorthwest": [],
			  "talkSoutheast": [],
			  "talkSouthwest": [],
			  "runNorth": [],
			  "runSouth": [],
			  "runEast": [],
			  "runWest": [],
			  "runNortheast": [],
			  "runNorthwest": [],
			  "runSoutheast": [],
			  "runSouthwest": [],}

names = ["n0*","s0*","e*","w*","ne*", "nw*", "se*", "sw*"]
actions = ["walking", "running", "talking"]

for name in names:
	for act in actions:
		for img in glob.glob("player/" + act + " " + name):
			image = pygame.image.load(img)
			if act == "walking":
				if name == "n0*":
					spriteDict["walkNorth"].append(image)
				if name == "s0*":
					spriteDict["walkSouth"].append(image)
				if name == "e*":
					spriteDict["walkEast"].append(image)
				if name == "w*":
					spriteDict["walkWest"].append(image)
				if name == "ne*":
					spriteDict["walkNortheast"].append(image)
				if name == "nw*":
					spriteDict["walkNorthwest"].append(image)
				if name == "se*":
					spriteDict["walkSoutheast"].append(image)
				if name == "sw*":
					spriteDict["walkSouthwest"].append(image)
			if act == "talking":
				if name == "n0*":
					spriteDict["talkNorth"].append(image)
				if name == "s0*":
					spriteDict["talkSouth"].append(image)
				if name == "e*":
					spriteDict["talkEast"].append(image)
				if name == "w*":
					spriteDict["talkWest"].append(image)
				if name == "ne*":
					spriteDict["talkNortheast"].append(image)
				if name == "nw*":
					spriteDict["talkNorthwest"].append(image)
				if name == "se*":
					spriteDict["talkSoutheast"].append(image)
				if name == "sw*":
					spriteDict["talkSouthwest"].append(image)
			if act == "running":
				if name == "n0*":
					spriteDict["runNorth"].append(image)
				if name == "s0*":
					spriteDict["runSouth"].append(image)
				if name == "e*":
					spriteDict["runEast"].append(image)
				if name == "w*":
					spriteDict["runWest"].append(image)
				if name == "ne*":
					spriteDict["runNortheast"].append(image)
				if name == "nw*":
					spriteDict["runNorthwest"].append(image)
				if name == "se*":
					spriteDict["runSoutheast"].append(image)
				if name == "sw*":
					spriteDict["runSouthwest"].append(image)

print(spriteDict["walkNorth"])




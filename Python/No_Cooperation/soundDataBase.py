import pygame, glob

class SoundDBase(object):
    def __init__(self, path):
        # Loads sounds
        self.sounds = {}
        self.addAdditionalDirectory(path)

    def get(self, name):
        return self.sounds[name]

    def addAdditionalDirectory(self, path):
        for sound in glob.glob(path + "\\" + "*"):
            try:        # Try to load the .ogg file. If it fails, move on to the next one.
                key = sound[len(path) + 1: sound.rfind(".")] # Slices the string name of every sound

                sound = pygame.mixer.Sound(sound) #Loads every sound

                self.sounds[str(key)] = sound

            except:
                pass

import pygame
import configuration

def playsound(name):
    if (configuration.config['sound'] == 'True'):
        pygame.mixer.music.load(name)
        pygame.mixer.music.play()
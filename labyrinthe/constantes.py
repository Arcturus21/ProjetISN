#Le fichier constante contient des instructions et des constantes globales
#necessaires a la plus part des fichiers du programme comme la taille d'un sprite
#ou la largeur de la fenetre

#Les stockez de cette facon permet de modifier ces constantes sans menacer l'integriter du programme
#ainsi que de modifier leur valeur partout ou elles sont utilises en une seule fois

import os 					#importe les fonctions specifiques a l'OS (chemin d'acces)
import pygame
from pygame.locals import * #importe pygame et ses constantes pour tous les fichiers

TAILLE_SPRITE = 65			#defini la taille d'un sprite (decor/personnage)
NB_SPRITE_LARGEUR = 15		#defini la taille du niveau
NB_SPRITE_HAUTEUR = 10

TAILLE_PERSO = TAILLE_SPRITE-(TAILLE_SPRITE//5)

FPS = 60 #nombre d'image par seconde

LARGEUR_FENETRE = NB_SPRITE_LARGEUR * TAILLE_SPRITE #Taille de la fenetre
HAUTEUR_FENETRE = NB_SPRITE_HAUTEUR * TAILLE_SPRITE

OBJECTIF = 2
SOLIDE = 1 #caracteristique d'un tile
VIDE = 0

#direction
HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3
NONE = -1 #old

NB_SPRITE_ANIM = 4

true = 1
false = 0

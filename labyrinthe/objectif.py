from constantes import *
from map import Map
from perso import Perso
import random

		
def point_dans_carre(point, carre):
	if point[0] > carre[0] and point[0] < carre[1] and point[1] > carre[2] and point[1] < carre[3]:
		return true
	else:
		return false
			
class Objectif:
	
	def position_objectif(self, map, perso):
		i = random.randint(0, map.nbSpriteX-1)
		j = random.randint(0, map.nbSpriteY-1)
			
		if (map.schema[j][i] == VIDE or map.liste_tile[map.schema[j][i]-1].get_solide() == VIDE) and (perso.posPerso[0] != i*TAILLE_SPRITE or perso.posPerso[1] != j*TAILLE_SPRITE):
			return [i*TAILLE_SPRITE, j*TAILLE_SPRITE]
		else:
			return self.position_objectif(map, perso)
	
	def __init__(self, map, perso):
		self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "objectif.png")), (TAILLE_SPRITE, TAILLE_SPRITE))
		
		self.taille_sprite = TAILLE_SPRITE
		self.pos = self.position_objectif(map, perso)
		
	def collision_perso(self, perso):
		if point_dans_carre(perso.posPerso, [self.pos[0], self.pos[0]+self.taille_sprite, self.pos[1], self.pos[1]+self.taille_sprite]):
			return true 
		elif point_dans_carre([perso.posPerso[0]+perso.taille_sprite, perso.posPerso[1]], [self.pos[0], self.pos[0]+self.taille_sprite, self.pos[1], self.pos[1]+self.taille_sprite]):
			return true
		elif point_dans_carre([perso.posPerso[0]+perso.taille_sprite, perso.posPerso[1]+perso.taille_sprite], [self.pos[0], self.pos[0]+self.taille_sprite, self.pos[1], self.pos[1]+self.taille_sprite]):
			return true
		elif point_dans_carre([perso.posPerso[0], perso.posPerso[1]+perso.taille_sprite], [self.pos[0], self.pos[0]+self.taille_sprite, self.pos[1], self.pos[1]+self.taille_sprite]):
			return true
		else:
			return false
			
class Texte:

		
	def __init__(self, indice, valeur, couleur=(0,0,0)): #initialisation pour un texte
		if indice > -2:
			self.police = pygame.font.Font(pygame.font.get_default_font(), TAILLE_SPRITE//2)
		else:
			self.police = pygame.font.Font(pygame.font.get_default_font(), TAILLE_SPRITE)
		self.valeur = valeur #score
		self.couleur = couleur
		
		if indice == -1:
			self.creer_surface_texte()
		elif indice == -2:
			self.creer_surface()
		else:
			self.indice = indice #classement
			self.creer_surface_score()
		
	def creer_surface(self): #permet d'afficher un simple nombre (compteur)
		self.surface = self.police.render(str(self.valeur), 0, self.couleur) #créer une surface noir en fonction de la valeur
		self.taille_surface = self.police.size(str(self.valeur)) #indique la taille de la surface
		
	def creer_surface_score(self): #affiche une chaine formaté (indice.score)
		texte = "Score {0} : {1}".format(self.indice+1, self.valeur) #texte temporaire
		self.surface = self.police.render(texte, 0, self.couleur)
		self.taille_surface = self.police.size(texte)
		
	def creer_surface_texte(self): #affiche un texte
		texte = "{0}".format(self.valeur) #texte temporaire
		self.surface = self.police.render(texte, 0, self.couleur)
		self.taille_surface = self.police.size(texte)
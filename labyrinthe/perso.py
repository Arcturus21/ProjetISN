from constantes import *
from map import *

class Perso:
	
	def __init__(self, posPerso): #modifier le chargement de sprite
		self.posPerso = [posPerso[0]*TAILLE_SPRITE, posPerso[1]*TAILLE_SPRITE]
		self.sprite = list()
		self.son = pygame.mixer.Sound(os.path.join("ressources", "meh.wav"))
		
		dossier_origine = os.path.join("ressources", "sprites_perso")
		
		NB_SPRITE_ANIM = 4
		i=0
		#chargement de chaque liste
		
		dossier_actuel = "haut"
		while i<4:
			self.sprite.append(list())
			liste_fichier = os.listdir(os.path.join(dossier_origine, dossier_actuel))
			for fichier in liste_fichier:
				self.sprite[i].append(pygame.transform.scale(pygame.image.load(os.path.join(dossier_origine, dossier_actuel, fichier)).convert(), (TAILLE_PERSO, TAILLE_PERSO)))
				self.sprite[i][0].set_colorkey((255,255,255))
				
			if dossier_actuel == "haut":
				dossier_actuel = "bas"
			elif dossier_actuel == "bas":
				dossier_actuel = "gauche"
			elif dossier_actuel == "gauche":
				dossier_actuel = "droite"
			i+=1
		
		self.sprite_actuel = 0
		self.direction = BAS
		self.en_mouvement = false
		self.taille_sprite = TAILLE_PERSO
		
	def collision_decor(self, posPerso, map):
		i = posPerso[0]
		j = posPerso[1]
		if j >= 0 and i >= 0 and (j+TAILLE_PERSO) < HAUTEUR_FENETRE and (i+TAILLE_PERSO) < LARGEUR_FENETRE:
			if ((map.schema[j//TAILLE_SPRITE][i//TAILLE_SPRITE] == VIDE or map.liste_tile[map.schema[j//TAILLE_SPRITE][i//TAILLE_SPRITE]-1].get_solide() != SOLIDE) and (map.schema[j//TAILLE_SPRITE][(i+TAILLE_PERSO)//TAILLE_SPRITE] == VIDE or map.liste_tile[map.schema[j//TAILLE_SPRITE][(i+TAILLE_PERSO)//TAILLE_SPRITE]-1].get_solide() != SOLIDE) and (map.schema[(j+TAILLE_PERSO)//TAILLE_SPRITE][i//TAILLE_SPRITE] == VIDE or map.liste_tile[map.schema[(j+TAILLE_PERSO)//TAILLE_SPRITE][i//TAILLE_SPRITE]-1].get_solide() != SOLIDE) and (map.schema[(j+TAILLE_PERSO)//TAILLE_SPRITE][(i+TAILLE_PERSO)//TAILLE_SPRITE] == VIDE or map.liste_tile[map.schema[(j+TAILLE_PERSO)//TAILLE_SPRITE][(i+TAILLE_PERSO)//TAILLE_SPRITE]-1].get_solide() != SOLIDE)):
				return 1
			else:
				return 0
		else:
			return 0
	
	def essais_deplacement(self, map, direction):
		i = TAILLE_SPRITE//NB_SPRITE_ANIM
		
		while i > 0:
			if direction == HAUT:
				posPersoEssais = (self.posPerso[0], self.posPerso[1]-i)
			if direction == BAS:
				posPersoEssais = (self.posPerso[0], self.posPerso[1]+i)
			if direction == GAUCHE:
				posPersoEssais = (self.posPerso[0]-i, self.posPerso[1])
			if direction == DROITE:
				posPersoEssais = (self.posPerso[0]+i, self.posPerso[1])
				
			if self.collision_decor(posPersoEssais, map) == 1:
				return posPersoEssais
			i-=1
			posPersoEssais = self.posPerso
		return self.posPerso
		
	def deplacer_perso(self, map, direction):
		if self.en_mouvement == true:
			if direction == HAUT and (self.posPerso[1])//TAILLE_SPRITE >= 0:
				self.posPerso = self.essais_deplacement(map, direction)
			if direction == BAS and (self.posPerso[1]+TAILLE_SPRITE-1)//TAILLE_SPRITE < map.nbSpriteY:
				self.posPerso = self.essais_deplacement(map, direction)
			if direction == GAUCHE and self.posPerso[0]//TAILLE_SPRITE >= 0:
				self.posPerso = self.essais_deplacement(map, direction)
			if direction == DROITE and (self.posPerso[0]+TAILLE_SPRITE-1)//TAILLE_SPRITE < map.nbSpriteX:
				self.posPerso = self.essais_deplacement(map, direction)
			self.anim_perso(direction)
			
	def anim_perso(self, direction):
		self.sprite_actuel+=1
		if self.sprite_actuel == len(self.sprite[direction]):
			self.sprite_actuel = 0

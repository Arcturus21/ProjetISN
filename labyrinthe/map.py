from constantes import *
from perso import *
import fichier

class Tile: #Le tile (ou tuile) est un objet representant une case dans un niveau

	def __init__(self, titre_sprite, sprite, solide): #initialise un nouveau "Tile"
		self.fichier = titre_sprite #nom du fichier contenant l'image du Tile
		self.sprite = sprite 		#image du Tile
		self.solide = solide		#defini si le tile est solide (mur) ou transparent (sol)
	
	def set_solide(self, solide):	#defini l'etat solide ou non d'un Tile 
		self.solide = solide
		
	def get_solide(self):	#donne l'etat solide d'un tile
		return self.solide
	
	def get_sprite(self):	#renvois le sprite du tile
		return self.sprite
		
class Map:
	
	def __init__(self, titre_fond, liste_sprite, map, posPerso, titre_musique):
		self.titre_fond = titre_fond	#contient le nom du fichier fond
		#la surface ne peut etre enregistrer dans le fichier niveau, il faudra l'ouvrir ulterieurement 
		self.liste_tile = liste_sprite #contient la liste des tiles (sprites et solidite) utilises
		
		self.taille_sprite = TAILLE_SPRITE #propriete des tiles
		
		self.nbSpriteX = NB_SPRITE_LARGEUR #taille de la map
		self.nbSpriteY = NB_SPRITE_HAUTEUR 
		
		self.schema = map		#liste a deux dimensions representant la map
		self.posPerso = posPerso #position initiale du personnage
		self.titre_musique = titre_musique #contient le nom du fichier musique de la map
		
		self.score = list();
		i=0
		while i<10:
			self.score.append(0)
			i+=1
		
	def initialisation(self): #charge les images en memoire vive (impossible de les enregistrer)
		self.fond = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "fond", self.titre_fond)).convert(), (LARGEUR_FENETRE, HAUTEUR_FENETRE))#(self.largeur_sprite*self.nbSpriteX, self.hauteur_sprite*self.nbSpriteY))
		#charge le fond et le redimensionne en fonction de la fenetre
		
		i=0
		while i < len(self.liste_tile): #charge les images des tiles (mur, brique...)
			self.liste_tile[i].sprite = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "sprites_decor", self.liste_tile[i].fichier)).convert_alpha(), (TAILLE_SPRITE, TAILLE_SPRITE))#(self.largeur_sprite, self.hauteur_sprite))
			i+=1
	
	def afficher_map(self, fenetre):
		i=j=0
		fenetre.blit(self.fond, (0,0)) #affiche le fond
		i=j=0
		while i < len(self.schema): #parcours la map
			while j < len(self.schema[i]):
				if self.schema[i][j] != 0: #affiche le sprite correspondant a chaque case
					fenetre.blit(self.liste_tile[self.schema[i][j]-1].get_sprite(), (j*TAILLE_SPRITE, i*TAILLE_SPRITE))
				j = j+1
			j=0
			i = i+1
	
	def sauvegarder(self, points, fichier_niveau):
		i=0
		while i<10:
			if self.score[i] < points:
				temp = self.score[i]
				self.score[i] = points
				points = temp
			i+=1
			
		fichier.sauvegarder_niveau(self, fichier_niveau)
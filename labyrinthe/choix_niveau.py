import pygame
from pygame.locals import *
import fichier
from constantes import *
import objectif
from objectif import *
import test_jeu


def main():
	pygame.init() #initialisation de pygame et ouverture d'une fenetre
	fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
	fond = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "fond", "montagne.jpg")),(LARGEUR_FENETRE, HAUTEUR_FENETRE))
	
	continuer = 1
	liste_niveau = os.listdir(os.path.join("ressources", "niveaux"))
	niveaux_actuel = 0
	NB_NIVEAUX = 9

	pos_niveaux = list()
	surface_niveaux = list()
	i=0
	pos = 25
	while i<NB_NIVEAUX and i < len(liste_niveau)-niveaux_actuel:
	
		surface_niveaux.append(Texte(-1, "niveau{0}".format(i)))
		
		pos_niveaux.append(((LARGEUR_FENETRE - surface_niveaux[i].taille_surface[0])//2, (LARGEUR_FENETRE - surface_niveaux[i].taille_surface[0])//2 + surface_niveaux[i].taille_surface[0], pos, pos+surface_niveaux[i].taille_surface[1]))
		pos+= 50
		i+=1
		
	if len(liste_niveau) >= NB_NIVEAUX:
		couleur = (0,0,0)
	else:
		couleur=(128,128,128)
	boutons = (Texte(-1, "Précédent", [128,128,128]), Texte(-1, "Suivant", couleur)) #deux boutons, l'un gris l'autre noir
	posBoutons = (25, (LARGEUR_FENETRE-25-boutons[1].taille_surface[0]), HAUTEUR_FENETRE-75)

	while continuer == 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
			if event.type == MOUSEBUTTONDOWN:
				i=0
				while i < len(pos_niveaux):
					if point_dans_carre(event.pos, pos_niveaux[i]):
						test_jeu.main("niveau{0}".format(i+niveaux_actuel))
					i+=1
				
				if point_dans_carre(event.pos, (posBoutons[0], posBoutons[0]+boutons[0].taille_surface[0], posBoutons[2], posBoutons[2]+boutons[0].taille_surface[1])):
					if niveaux_actuel != 0:
						niveaux_actuel -= NB_NIVEAUX
						
						i=0
						del surface_niveaux #supprime la liste
						surface_niveaux=list()
						while i<NB_NIVEAUX and i < len(liste_niveau)-niveaux_actuel:
							surface_niveaux.append(Texte(-1, "niveau{0}".format(i+niveaux_actuel)))
							i+=1
				
				elif point_dans_carre(event.pos, (posBoutons[1], posBoutons[1]+boutons[1].taille_surface[0], posBoutons[2], posBoutons[2]+boutons[1].taille_surface[1])):
					if niveaux_actuel + NB_NIVEAUX <= len(liste_niveau):
						niveaux_actuel += NB_NIVEAUX
						
						i=0
						del surface_niveaux #supprime la liste
						surface_niveaux=list()
						while i<NB_NIVEAUX and i < len(liste_niveau)-niveaux_actuel:
							surface_niveaux.append(Texte(-1, "niveau{0}".format(i+niveaux_actuel)))
							i+=1
				
				if niveaux_actuel == 0:
					boutons[0].couleur = (128,128,128)
					boutons[0].creer_surface_texte();
				else:
					boutons[0].couleur = (0,0,0)
					boutons[0].creer_surface_texte();
					
				if niveaux_actuel + NB_NIVEAUX > len(liste_niveau):
					boutons[1].couleur = (128,128,128)
					boutons[1].creer_surface_texte();
				else:
					boutons[1].couleur = (0,0,0)
					boutons[1].creer_surface_texte();

		fenetre.blit(fond, (0, 0))
		i=0
		while i < NB_NIVEAUX and i < len(liste_niveau)-niveaux_actuel:
			fenetre.blit(surface_niveaux[i].surface, (pos_niveaux[i][0], pos_niveaux[i][2]))
			i+=1
			
		fenetre.blit(boutons[0].surface, (posBoutons[0], posBoutons[2]))
		fenetre.blit(boutons[1].surface, (posBoutons[1], posBoutons[2]))
		
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	pygame.quit()
import pygame
from pygame.locals import *
from constantes import *
import execution_editeur
import choix_niveau
import objectif
from objectif import point_dans_carre

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
fond = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "fond_ac.bmp")).convert(), (LARGEUR_FENETRE, HAUTEUR_FENETRE))

continuer = 1

TAILLE_BOUTON = (400*LARGEUR_FENETRE/1372,100*HAUTEUR_FENETRE/1146)


bouton_jouer = (485*LARGEUR_FENETRE/1372, 240*HAUTEUR_FENETRE/1146) #produit en croix
bouton_editeur = (485*LARGEUR_FENETRE/1372, 446*HAUTEUR_FENETRE/1146)
bouton_quitter = (485*LARGEUR_FENETRE/1372, 652*HAUTEUR_FENETRE/1146)

while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 0
		if event.type == MOUSEBUTTONDOWN:
			print(event.pos)
			print(bouton_jouer[0], bouton_jouer[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1])
			if objectif.point_dans_carre(event.pos, (bouton_jouer[0], bouton_jouer[0]+TAILLE_BOUTON[0], bouton_jouer[1], bouton_jouer[1]+TAILLE_BOUTON[1])):
				choix_niveau.main()
			elif objectif.point_dans_carre(event.pos, (bouton_editeur[0], bouton_editeur[0]+TAILLE_BOUTON[0], bouton_editeur[1], bouton_editeur[1]+TAILLE_BOUTON[1])):
				execution_editeur.main()
			elif objectif.point_dans_carre(event.pos, (bouton_quitter[0], bouton_quitter[0]+TAILLE_BOUTON[0], bouton_quitter[1], bouton_quitter[1]+TAILLE_BOUTON[1])):
				continuer = 0
		
	fenetre.blit(fond, (0,0))
	pygame.display.flip()
	
pygame.quit()

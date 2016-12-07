from constantes import *
from fichier import *
from map import *
from perso import *
from objectif import *

def main(niveau):
	pygame.init()
	fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
	#pygame.mixer.init()

	continuer = 1

	map = charger_niveau(niveau)
	perso = Perso(map.posPerso)
	objectif = Objectif(map, perso)
	
	texte_timer = Texte(-2, 20)
	texte_points = Texte(-2, 0)

	pygame.mixer.music.load(os.path.join("ressources", "musique", map.titre_musique))
	pygame.mixer.music.play()

	pygame.time.set_timer(USEREVENT+1, 100) #initialise un timer (USERVENT -> constante pygame)
	pygame.time.set_timer(USEREVENT+2, 1000)
	while continuer != 0 and texte_timer.valeur > 0:

		for event in pygame.event.get():
			if event.type == USEREVENT+1: #Si la durée est respectée
				perso.deplacer_perso(map, perso.direction) #fonction de déplacement
				if objectif.collision_perso(perso):
					perso.son.play()
					objectif.pos = objectif.position_objectif(map, perso)
					texte_points.valeur += 1
					texte_points.creer_surface()
					
			if event.type == USEREVENT+2:
				texte_timer.valeur-=1
				texte_timer.creer_surface()
				

			if event.type == QUIT:
				continuer = 0

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 0

				if event.key == K_UP:
					perso.direction = HAUT #assigne la direction en fonction de la touche entrée
					perso.en_mouvement = true
				if event.key == K_DOWN:
					perso.direction = BAS
					perso.en_mouvement = true
				if event.key == K_LEFT:
					perso.direction = GAUCHE
					perso.en_mouvement = true
				if event.key == K_RIGHT:
					perso.direction = DROITE
					perso.en_mouvement = true

			if event.type == KEYUP: #si on relache une touche et que la direction correspond (flèche haut/direction vers le haut), on annule la direction
				if (event.key == K_UP and perso.direction == HAUT) or (event.key == K_DOWN and perso.direction == BAS) or (event.key == K_RIGHT and perso.direction == DROITE) or (event.key == K_LEFT and perso.direction == GAUCHE):
					perso.en_mouvement = false


		map.afficher_map(fenetre) #fonction qui affiche la map
		fenetre.blit(objectif.sprite, objectif.pos)

		if perso.en_mouvement == true: #si le personnage est en déplacement, on affiche le sprite actuel
			fenetre.blit(perso.sprite[perso.direction][perso.sprite_actuel], (perso.posPerso[0], perso.posPerso[1]))
		else: #sinon on affiche un sprite par défaut
			fenetre.blit(perso.sprite[perso.direction][0], (perso.posPerso[0], perso.posPerso[1]))

		fenetre.blit(texte_timer.surface, (LARGEUR_FENETRE - texte_timer.taille_surface[0]-2, 2))
		fenetre.blit(texte_points.surface, (2, 2))
		
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	pygame.mixer.music.stop()

	if continuer != 0:
		map.sauvegarder(texte_points.valeur, niveau)
		affiche_score(fenetre, map, niveau)
		
	else:
		pygame.quit()
	
		
def affiche_score(fenetre, niveau, nom_niveau):
	scores = list()
	i=0
	while i<10:
		scores.append(Texte(i, niveau.score[i]))
		i+=1
	
	RECOMMENCER = 0
	QUITTER = 1
	boutons = [Texte(-1, "RECOMMENCER"), Texte(-1, "QUITTER")]
	
	pos = [0, 0]
	posBoutons = ((LARGEUR_FENETRE//2 - 20 - boutons[RECOMMENCER].taille_surface[0]), (LARGEUR_FENETRE//2 + 20), (HAUTEUR_FENETRE - 5 - boutons[RECOMMENCER].taille_surface[1]))
	
	continuer = 1
	while continuer == 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			elif event.type == MOUSEBUTTONDOWN: #clic de la souris
				if point_dans_carre(event.pos, (posBoutons[0], posBoutons[0]+boutons[RECOMMENCER].taille_surface[0], posBoutons[2], posBoutons[2]+boutons[RECOMMENCER].taille_surface[1])): #clic dans bouton recommencer
					continuer = 2
				elif point_dans_carre(event.pos, (posBoutons[1], (posBoutons[1]+boutons[QUITTER].taille_surface[0]), posBoutons[2], (posBoutons[2]+boutons[QUITTER].taille_surface[1]))): #clic dans bouton recommencer
					continuer = 0

		i=0
		pos[0] = LARGEUR_FENETRE//2 - scores[0].taille_surface[0]//2
		while i < 10:
			pos[1] = (10 + i*(scores[i].valeur+scores[i].taille_surface[1]+5))
			fenetre.blit(scores[i].surface, pos)
			i+=1
			
		fenetre.blit(boutons[RECOMMENCER].surface, (posBoutons[0], posBoutons[2]))
		fenetre.blit(boutons[QUITTER].surface, (posBoutons[1], posBoutons[2]))
		
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
	
	if continuer == 2:
		main(nom_niveau)
		
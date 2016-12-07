from constantes import *
from fichier import *


def choix_fond(fenetre):
	continuer = 1 #variable qui gere le deroulement et l'arret du script
	liste_fond = charger_fond(os.path.join("ressources", "fond")) #charge tous les fond contenus dans le dossier fond
																	#os.path.join() est utilise pour une question de portabilite
	
	fond_actuel = 0 												#contient l'indice (de la liste "liste_fond) du fond actuellement a l'ecran
	
	print("\nChoisissez votre fond de carte\nScrollez pour faire defiler\nCliquez ou pressez 'Entrer' pour valider")
	#instruction
	
	while continuer==1:
		for event in pygame.event.get(): #on recupere les evenements pour les analyser
			if event.type == QUIT: #clic sur la croix
				continuer = 0 #arret du programme
				
			if event.type == KEYDOWN: #appuie sur une touche
				if event.key == K_ESCAPE:
					continuer = 0
				if event.key == K_RETURN: #valide le fond aa l'ecran, fini le script pour passer a l'etape suivante
					continuer = 2
					
			if event.type == MOUSEBUTTONDOWN: #clic de la souris
				if event.button == 1: #clic gauche similaire a entree
					continuer = 2
					
				if event.button == 4: #molette haut pour visionner le fond precedent
					fond_actuel -= 1 
					if fond_actuel < 0: #si l'on depasse l'indice minimum...
						fond_actuel = len(liste_fond)-1 #... on retourne dernier element liste
						
				if event.button == 5: #molette bas pour visionner le fond suivant
					fond_actuel += 1
					if fond_actuel > len(liste_fond) -1:
						fond_actuel = 0
	
		fenetre.blit(liste_fond[fond_actuel][1], (0, 0)) #affiche un fond de la liste en fonction de l'indice
		pygame.display.flip() #met l'ecran aa jour
		pygame.time.Clock().tick(FPS) #limite l'affichage a 60FPS

	return continuer, liste_fond[fond_actuel][0], liste_fond[fond_actuel][1] #renvoit la valeur de continuer (= fin ou suite du programme), 
	#l'image du fond et le nom du fichier correspondant
	
def verif_unicite_liste(nom_fichier, liste): #verifie si l'element a dejaa ete selectionne
	j=0
	for i in liste: 						#parcours tous les elements selectionnes
		if i.fichier == nom_fichier[0]: 	#si le fichier correspond a un element de la liste
			return j						#on renvoit son indice
		j+=1
	return -1 								#sinon c'est qu'il n'existe pas encore
	
def selection_tiles(fond, fenetre):
	i = j = 0
	continuer = 2
	verif = 0 #permet 
	
	print("\nSelectionnez les elements de decors que vous souhaitez integrer:\nCliquez pour selectionner/deselectionner\n'Entrer' pour valider")
	
	surface_selectionne = pygame.Surface((TAILLE_SPRITE, TAILLE_SPRITE), SRCALPHA) #creer surface transparente
	surface_selectionne.fill((128, 128, 128, 128)) #gris transparent
	#surface_selectionne est un masque qui permettra d'indiquer quels elements ont ete selectionne
	
	liste_sprite = charger_sprite(os.path.join("ressources", "sprites_decor")) #charge tous les sprites
	liste_tiles = list() 														#initialise la liste des tiles selectionnes
	
	while continuer==2:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: #reviens a l'etape precedente
					continuer = 1
				if event.key == K_RETURN:
					continuer = 3
					
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: 					#clic gauche
					i = event.pos[0]//(TAILLE_SPRITE) #on repere la position de la souris 
					j = event.pos[1]//(TAILLE_SPRITE) #et leur indice correspondant potentiel dans la liste de sprite
					
					if (i+j*NB_SPRITE_LARGEUR) < len(liste_sprite): 																	#si l'indice est compris dans la liste
						verif = verif_unicite_liste(liste_sprite[i+j*NB_SPRITE_LARGEUR], liste_tiles) 									#on verifie si l'element a deja ete selectionne
						if verif == -1: 																								#si non, on l'ajoute a la liste finale
							liste_tiles.append(Tile(liste_sprite[i+j*NB_SPRITE_LARGEUR][0], liste_sprite[i+j*NB_SPRITE_LARGEUR][1], 0))
						else: 																											#si oui, on supprime l'element dans la liste, a l'indice renvoye
							del liste_tiles[verif]
	
		fenetre.blit(fond, (0, 0)) #affiche le fond
		i=0
		while i < len(liste_sprite): #affiche les elements de decors un par un les uns a cote des autres
			fenetre.blit(liste_sprite[i][1], (i*TAILLE_SPRITE%LARGEUR_FENETRE, i*TAILLE_SPRITE//LARGEUR_FENETRE))
			if verif_unicite_liste(liste_sprite[i], liste_tiles) != -1: # si le sprite est selectionne, on lui applique un masque gris
				fenetre.blit(surface_selectionne, (i*TAILLE_SPRITE%LARGEUR_FENETRE, i*TAILLE_SPRITE//LARGEUR_FENETRE))
			i+=1
			
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	return continuer, liste_tiles
	
def selection_solides(fond, fenetre, liste_tiles): #determine si un tile est solide ou non
	i = j = 0
	continuer = 3
	
	print("\nSelectionnez les elements de decors solides:\nCliquez pour selectionner/deselectionner\n'Entrer' pour valider")

	surface_selectionne = pygame.Surface((TAILLE_SPRITE, TAILLE_SPRITE), SRCALPHA) #creer surface transparente
	surface_selectionne.fill((128, 128, 128, 128)) #gris
	
	while continuer==3:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 2
				if event.key == K_RETURN:
					continuer = 4
					
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: #clic gauche
					i = event.pos[0]//(TAILLE_SPRITE) #posX souris
					j = event.pos[1]//(TAILLE_SPRITE) #posY souris
					
					if (i+j*NB_SPRITE_LARGEUR) < len(liste_tiles):
						if liste_tiles[i+j*NB_SPRITE_LARGEUR].get_solide() == VIDE: #si le tile est transparent
							liste_tiles[i+j*NB_SPRITE_LARGEUR].set_solide(SOLIDE) 	#on le rend solide
						else:
							liste_tiles[i+j*NB_SPRITE_LARGEUR].set_solide(VIDE) 	#sinon, on le rend transparent

		fenetre.blit(fond, (0, 0))
		i = 0
		while i < len(liste_tiles):
			fenetre.blit(liste_tiles[i].get_sprite(), (i*TAILLE_SPRITE%LARGEUR_FENETRE, i*TAILLE_SPRITE//LARGEUR_FENETRE))
			if liste_tiles[i].solide == 1:
				fenetre.blit(surface_selectionne, (i*TAILLE_SPRITE%LARGEUR_FENETRE, i*TAILLE_SPRITE//LARGEUR_FENETRE))
			i+=1
			
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	return continuer, liste_tiles

def choix_tiles(fond, fenetre): #etape divisee en deux
	continuer = 2
	
	continuer, liste_tiles = selection_tiles(fond, fenetre) #on selectionne ceux que l'on veux
	if continuer == 3:
		continuer, liste_tiles = selection_solides(fond, fenetre, liste_tiles) #puis ceux qui sont solide
	if continuer == 4: #a changer, inutile !
		continuer = 3
	
	return continuer, liste_tiles
	
def construction_map(fenetre, fond, liste_sprite):
	clic_gauche = 0 #determine si le clic gauche est enfonce
	clic_droit = 0
	posX = 0
	posY = 0
	i = j = 0
	sprite_actuel = 0
	continuer = 3
	map = list()

	print("\nConstruisez votre map:\nClic gauche pour poser un element\nClic droit pour enlever un element\nScrollez pour changer d'element\n'Entrer' pour valider\n")

	while i < NB_SPRITE_HAUTEUR:
		map.append(list())
		while j < NB_SPRITE_LARGEUR: #construit une map, toute les cases sont VIDE
			map[i].append(0)
			j = j+1
		j=0
		i += 1
	
	while continuer == 3:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 2
				if event.key == K_RETURN:
					continuer = 4
					
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: #clic gauche
					clic_gauche = 1
					clic_droit = 0
				if event.button == 3: #clic droit
					clic_droit = 1
					clic_gauche = 0
				if event.button == 4: 						#molette haut
					sprite_actuel -= 1 						#meme principe que les fonds, le sprite precedent est affiche
					if sprite_actuel < 0:
						sprite_actuel = len(liste_sprite)-1 #dernier element liste
				if event.button == 5: #molette bas
					sprite_actuel += 1 #le sprite suivant est affiche
					if sprite_actuel > len(liste_sprite) -1:
						sprite_actuel = 0
					
				posX = event.pos[0] #posX souris
				posY = event.pos[1] #posY souris
				
			if event.type == MOUSEBUTTONUP:
				if event.button == 1: #clic gauche
					clic_gauche = 0
				if event.button == 3: #clic droit
					clic_droit = 0
				posX = event.pos[0] #posX souris
				posY = event.pos[1] #posY souris
					
			if event.type == MOUSEMOTION:
				posX = event.pos[0] #posX souris
				posY = event.pos[1] #posY souris
				
		if clic_gauche:
			map[posY//TAILLE_SPRITE][posX//TAILLE_SPRITE] = sprite_actuel+1 #on rentre la valeur representant le sprite correspondant
		if clic_droit:														#+1 car 0 correspond a un sprite dans la liste, mais au vide dans la map
			map[posY//TAILLE_SPRITE][posX//TAILLE_SPRITE] = 0 				#0 equivaut au vide
		
		fenetre.blit(fond, (0, 0))
		i=j=0
		while i < len(map):
			while j < len(map[i]): 	#affiche l'element de la map si elle n'est pas vide
				if map[i][j] != 0:
					fenetre.blit(liste_sprite[map[i][j]-1].get_sprite(), (j*TAILLE_SPRITE, i*TAILLE_SPRITE))
				j = j+1
			j=0
			i = i+1
		fenetre.blit(liste_sprite[sprite_actuel].get_sprite(), (posX, posY)) #affiche le sprite actuel a la position de la souris
		
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	return continuer, map

def choix_pos_perso(fenetre, fond, map, liste_sprite):
	continuer = 4
	sprite_actuel = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "sprites_perso", "bas", "Sprite_mouton_face1.png")).convert_alpha(), (TAILLE_PERSO, TAILLE_PERSO))
	sprite_actuel.set_colorkey((255,255,255))
	posX = posY=0
	posPerso = (0, 0)
	
	print("Positionnez votre personnage au depart")
	
	while continuer == 4:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 3
					
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: #clic gauche
					posPerso = (event.pos[0]//TAILLE_SPRITE, event.pos[1]//TAILLE_SPRITE) #determine la position du personnage (en indice de map)
					continuer = 5 #passe a l'etape suivante
					
			if event.type == MOUSEMOTION:
				posX = event.pos[0] #posX souris
				posY = event.pos[1] #posY souris
				
				
		fenetre.blit(fond, (0, 0)) #affiche le fond et la map
		i=j=0
		while i < len(map):
			while j < len(map[i]):
				if map[i][j] != 0:
					fenetre.blit(liste_sprite[map[i][j]-1].get_sprite(), (j*TAILLE_SPRITE, i*TAILLE_SPRITE))
				j = j+1
			j=0
			i = i+1
		fenetre.blit(sprite_actuel, (posX, posY)) #affiche un personnage a l'endroit de la souris
			
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)
		
	#re-affichage
	fenetre.blit(fond, (0, 0))
	i=j=0
	while i < len(map):
		while j < len(map[i]):
			if map[i][j] != 0:
				fenetre.blit(liste_sprite[map[i][j]-1].get_sprite(), (j*TAILLE_SPRITE, i*TAILLE_SPRITE))
			j = j+1
		j=0
		i = i+1
	fenetre.blit(sprite_actuel, (posPerso[0]*TAILLE_SPRITE, posPerso[1]*TAILLE_SPRITE)) #affiche le personnage dans la case correspondante
			
	pygame.display.flip()
	pygame.time.Clock().tick(FPS)
		
	return continuer, posPerso
	
def choix_musique():
	pygame.mixer.init()
	
	print("Selectionner votre musique:\nScrollez pour changer\nClic gauche ou 'Entrer' pour selectionner\n")

	continuer = 5
	
	liste_musique = list()
	dossier_origine = os.path.join("ressources", "musique") 
	
	liste_fichier = os.listdir(dossier_origine) #ouvre le repertoire et liste son contenue
	for fichier in liste_fichier:
		liste_musique.append(fichier)
	musique_actuel = 0
	#charger musique
	
	pygame.mixer.music.load(os.path.join(dossier_origine, liste_musique[musique_actuel])) #charge la premiere musique
	pygame.mixer.music.play() #joue la musique
	while continuer==5:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 4
				if event.key == K_RETURN:
					continuer = 6
					titre_musique = liste_musique[musique_actuel] #selectionne la musique choisie
					
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: #clic gauche
					continuer = 6 #+fond
					titre_musique = liste_musique[musique_actuel] #selectionne la musique choisie
					
				if event.button == 4: #molette haut
					musique_actuel -= 1
					if musique_actuel < 0:
						musique_actuel = len(liste_musique)-1 #dernier element liste
					pygame.mixer.music.load(os.path.join(dossier_origine, liste_musique[musique_actuel])) 
					pygame.mixer.music.play() #meme idee que le fond, on selectionne et joue la musique precedente
				if event.button == 5: #molette bas
					musique_actuel += 1
					if musique_actuel > len(liste_musique) -1:
						musique_actuel = 0
					pygame.mixer.music.load(os.path.join(dossier_origine, liste_musique[musique_actuel]))
					pygame.mixer.music.play() #on selectionne et joue la musique suivante


	return continuer, titre_musique #renvois le titre de la musique
	
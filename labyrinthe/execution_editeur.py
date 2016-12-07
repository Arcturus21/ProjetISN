#script principale du programme
#defini le deroulement des differentes etapes de la confections du niveau

from constantes import *
from fonctions_editeur import *
from fichier import *

def main():
	continuer = 1 #controle le deroulement du script (etape/arret)

	pygame.init() #initialisation de pygame et ouverture d'une fenetre
	fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

	while continuer != 0: #tant que la variable ne vaut pas 0, on execute
		if continuer == 1:
			continuer, titre_fond, fond = choix_fond(fenetre) #permet de choisir le fond de son niveau
			
		if continuer == 2:
			continuer, liste_sprite = choix_tiles(fond, fenetre) 
			#on selectionne les elements de decors a utiliser et ceux qui seront solides (murs)
			
		if continuer == 3:
			continuer, map = construction_map(fenetre, fond, liste_sprite)
			print("construit!") #on construit le schema du niveau
			
		if continuer == 4:
			continuer, posPerso = choix_pos_perso(fenetre, fond, map, liste_sprite)
			#on choisit la position initiale du personnage
			
		if continuer == 5:
			continuer, titre_musique = choix_musique()
			#on selectionne la musique qui sera jouee pendant la partie
			
		if continuer == 6:
			niveau = Map(titre_fond, liste_sprite, map, posPerso, titre_musique) #creer un objet de type Map
			continuer = sauvegarder_niveau(niveau)
			#sauvegarde les choix selectionne dans un nouveau fichier niveau
	print("NIVEAU SAUVEGARDE\n")

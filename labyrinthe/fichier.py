from constantes import * #importe les variables du fichier constante (taille des sprites, ...)

from map import * #importe les variables du fichier map (class)

import pickle #module permettant d'enregistrer un objet dans un fichier

def charger_fond(dossier_origine):
	liste_fond = list()	#creer la liste contenant les fonds et leur nom ("fond.bmp")
	liste_fichier = os.listdir(dossier_origine) #charge tous les nom des fonds contenu dans le dossier "fond"
	
	for fichier in liste_fichier: #parcours la liste contenant les sprites du dossier grace a l'iteration
		liste_fond.append([fichier, pygame.transform.scale(pygame.image.load(os.path.join(dossier_origine, fichier)).convert_alpha(), (LARGEUR_FENETRE, HAUTEUR_FENETRE))])
		#assigne a chaque element de la liste une variable contenant le nom du sprite et une variable contenant son image
		#la commange "os.path.join()" permet de creer un chemin pour le fihcier qui s'adapte a l'OS (\\ pour windows, // pour linux...)

	return liste_fond

def charger_sprite(dossier_origine):
	liste_sprite = list()	#creer la liste contenant les sprites et leur nom ("mur.bmp")
	liste_fichier = os.listdir(dossier_origine) #charge tous les nom des sprites contenu dans le dossier "sprites_decor"
	
	for fichier in liste_fichier: #parcours la liste contenant les sprites du dossier grace a l'iteration
		liste_sprite.append([fichier, pygame.transform.scale(pygame.image.load(os.path.join(dossier_origine, fichier)).convert_alpha(), (TAILLE_SPRITE, TAILLE_SPRITE))])
		#assigne a chaque element de la liste une variable contenant le nom du sprite et une variable contenant son image
		#la commange "os.path.join()" permet de creer un chemin pour le fihcier qui s'adapte a l'OS (\\ pour windows, // pour linux...)

	return liste_sprite

def sauvegarder_niveau(niveau, indice = "null"):
	
	dossier_origine = os.path.join("ressources", "niveaux") #defini ou sauvegarder le niveau, toujours selon la meme logique de portabilite
	nombre_niveaux = os.listdir(dossier_origine)
	
	if indice == "null":
		i=0
		for fichier in nombre_niveaux: #enumerate
			i+=1 #compte le nombre de niveaux enregistres dans le dossier de reception
			nom_fichier = "niveau{0}".format(i) #creer le nom du niveau en fonction du nombre de niveau deja cree
	
	else:
		nom_fichier = indice

	with open(os.path.join(dossier_origine, nom_fichier), 'wb') as fichier: #creer le nouveau niveau et l'ouvre en ecriture
		pickler = pickle.Pickler(fichier) #initialise un objet pour sauvegarder le niveau
		pickler.dump(niveau) #copie le niveau creer dans le fichier correspondant pour le sauvegarder
		
	print("Niveau sauvegarde !")
	return 0
		
def charger_niveau(fichier_niveau):
	with open(os.path.join("ressources", "niveaux", fichier_niveau), 'rb') as fichier: #ouvre le niveau choisis en ouverture
		unpickler = pickle.Unpickler(fichier) #initialise un objet pour charger le niveau
		niveau = unpickler.load() #charge le niveau en memoire vive
		niveau.initialisation() #initialise l'objet representant le niveau (importation des images)
		return niveau #renvois l'objet niveau
		
	
#class Meilleure_score: #tableau 2D (niveau/score)
	
	#def __init__(self):
		

	#def sauvegarder_points(self, points, niveau):
		
		
	#def charger_score(self):
	
	#def afficher_score(self):
		
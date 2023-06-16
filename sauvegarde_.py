

#function to save the values in a file text
def sauvegarde(nom_fichier, grid):

    fichier = open(nom_fichier, "w")
    contenu = fichier.write(str(grid))
    fichier.close()

    return contenu

#function to return what's in the file text
def read(nom_fichier):

    fichier = open(nom_fichier, "r")
    contenu = fichier.read()
    fichier.close()

    return contenu

#methode pour remplacer les espaces par des virgules
def replace(nom_fichier):
    pass
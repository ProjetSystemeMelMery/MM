#!/usr/bin/env python3

# génération de la liste de fichiers

import os
import options

#On récupère les arguments de la ligne de commande dans args
args = options.arguments()

#La liste de fichiers Source contient soit : 
# - plusieurs fichiers et répertoires (*)
# - un nom de fichier
# - un nom de répertoire avec ou sans /
# - un chemain absolu
# - un chemin relatif (.) 

#Définition d'une liste de fichiers associé à leurs chemins d'un répertoire de façon non récurise, en prenant en compte le /
def listeFichiersSansRec(src,string): #intervention de string uniquement pour faciliter les comparaisons dans le générateur
    liste = []
    for e in src:
        #Si / présent, on visite aussi les fichiers que contient le répertoire
        if e[-1]=='/':
            if os.path.isdir(e):
                for elt in os.listdir(e):
                    liste = liste + [(elt,elt)]
        #Sinon, on ne transfère que le répertoire seul
        else:
            liste = liste + [(string+e,os.path.basename(e))]
    return liste 
    #retoure une liste de type [(chemin, noms du fichier), ...]

#Définition d'une liste de manière récursive, on visite les sous-répertoires...
listerec = []
def listeFichiersRec(src):
    global listerec
    #Si il y a un slash alors on prend comme source les fichiers du répertoire sans le répertoire parent
    if src[0][-1]=='/':
        deb = src[0]
        src = os.listdir(src[0])
    else:
        deb = ""
    #deb nous permet de conserver le nom du répertoire parent pour effectuer les tests sur la nature des fichiers.
    for e in src:
        #Si c'est un fichier, on le rajoute à la liste
        if os.path.isfile(deb+e):
            listerec = listerec + [(e,os.path.basename(e))]
        #Si c'est un répertoire, on visite son contenu de manière récursive en rappelant la fonction
        if os.path.isdir(deb+e):
            listerec = listerec + [(e,os.path.basename(e))]
            l = []
            if os.listdir(deb+e)!=[]:
                for elt in os.listdir(deb+e):
                    l.append(os.path.join(e,elt))
                listerec.append(listeFichiersRec(l))
    return listerec
    #retoure une liste de type [(chemin, noms du fichier), ...]

#On pense à préciser les chemins respectifs de chaque fichier pour ne faire aucune erreur sur la localité de chaque fichier (transfert, copie, création...)

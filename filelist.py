#!/usr/bin/env python3

# génération de la liste de fichiers

import os
import options

args = options.arguments()

#La liste de fichiers Source contient soit : 
# - plusieurs fichiers et répertoires (*)
# - un nom de fichier
# - un nom de répertoire avec ou sans /
# - un chemain absolu
# - un chemin relatif (.) 
# Pour la suite, il faut être certain de bien connaître le chemin absolu de chaque fichier :

def misajour(src):
    newsrc = []
    for e in src:
        if e == '.':
            newe = os.getcwd()
        else :
            newe = os.path.join(os.getcwd(),e)
        newsrc.append(newe)
    return newsrc


def listeFichiersSansRec(src):
    liste = []
    for e in src:
        if e[-1]=='/':
            liste = liste + [(os.path.join(os.getcwd(),e[:-1]),os.path.basename(e[:-1]))]
            if os.path.isdir(e):
                for elt in os.listdir(e):
                    liste = liste + [(os.path.join(e,elt),elt)]
        else:
            liste = liste + [(e,os.path.basename(e))]
    return liste

listerec = []
def listeFichiersRec(src):
    global listerec
    for e in src:
        if e[-1]=='/':
            e = e[:-1]
        if os.path.isfile(e):
            listerec = listerec + [(e,os.path.basename(e))]
        if os.path.isdir(e):
            listerec = listerec + [(e,os.path.basename(e))]
            l = []
            for elt in os.listdir(e):
                l.append(os.path.join(e,elt))
            listerec.append(listeFichiersRec(l))
    return listerec

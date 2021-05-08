#!/usr/bin/env python3 

import os, options, message, sys

args = options.arguments()

def generateur(fichierssrc,fichiersdst):
    #Trier la liste

    #liste des noms dans destinations
    nomsdest = []
    for e in fichiersdst:
        nomsdest.append(e[1])
    print(nomsdest)
    #liste des chemins dans destinations
    cheminsdest = []
    for e in fichiersdst:
        cheminsdest.append(e[0])

    for e in fichierssrc:
        if e[1] in nomsdest:
            i = index(nomsdest,e[1])
            print(i)
            if os.path.isfile(e[0]):
                message.send(1,"écraser ou créer fichier",e)
            if os.path.isdir(e[0]) and os.path.isfile(nomsdest[i][0]):
                message.send(1,'créer répertoire',e)
        if e[1] not in nomsdest:
            if os.path.isfile(e[0]):
                message.send(1,"créer fichier",e)
            if os.path.isdir(e[0]):
                message.send(1,'créer répertoire',e)
    message.send(1,"fin requête",'')
    sys.exit(0)

def index(liste,e):
    for i in range(len(liste)):
        if liste[i]== e:
            return i

def fichiers_tries(src ='.'):
    i = [s for s in os.listdir(src)
        if os.path.isfile(os.path.join(src, s))]
    i.sort(key=lambda s: os.path.getsize(os.path.join(src, s)))
    return i

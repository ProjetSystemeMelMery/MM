#!/usr/bin/env python3 

import os, options, message, sys
from sender import *

args = options.arguments()

def generateur(fichierssrc,fichiersdst): #les deux arguments sont respectivement la liste de fichiers à la source, et celle se trouvant à la destination
    #On se place dans la répertoire courant initial de lancement de commande, pour pouvoir contrôler la nature des fichiers.
    print(fichierssrc, file=sys.stderr)
    print(fichiersdst, file=sys.stderr)

    #On se place dans le bon répertoire courant pour tester le type des fichiers (en fonction de /)
    if src[0][-1]=='/':
        os.chdir(position_courante+'/'+src[0])
    else:
        os.chdir(position_courante)
    #Nous n'avons pas trié les listes, car la manière dont nous contruisons nos listes de fichiers était déjà assez pratique.

    #liste des noms de fichiers dans le répertoire destinataire 
    nomsdest = []
    for e in fichiersdst:
        nomsdest.append(e[1])
    #liste des chemins de fichiers dans le répertoire destinateire
    cheminsdest = []
    for e in fichiersdst:
        cheminsdest.append(e[0])
    nomssrc = []
    for e in fichierssrc:
        nomssrc.append(e[1])

    #Commencement de l'envoi des requêtes
    message.send(1,"debut requete",'')
    #si l'option delete est activée alors on compare les fichiers sources et destinataires, et on efface les fichiers qui sont présents dans destinataire mais pas dans source
    if args.delete:
        for e in fichiersdst:
            if e[1] not in nomssrc:
                message.send(1,"supprimer fichier", e)


    #On parcourt les fichiers de la source
    for e in fichierssrc: 
        #Si le nom de fichier est aussi présent dans la liste destinataire
        if e[1] in nomsdest: 
            #On cherche l'indice du tuple destinateire correspondant à ce nom de fichier
            i = index(nomsdest,e[1])
            #Si c'est un fichier ordinaire, on envoie une requête de création/remplacement ici de fichier au client, en liant le tuple du fichier
            if os.path.isfile(e[0]):
                message.send(1,"creer fichier",e)
            if os.path.isfile(e[0]) and os.path.isdir(cheminsdest[i]):
                if args.force:
                        message.send(1,"supprimer repertoire",e)
            #Si c'est un répertoire, mais qu'il n'a pas la même place dans l'arborescence côté destinataire (il ets dans un sous répertoire), on crée le répertoire à sa place.
            if os.path.isdir(e[0]) and (e[0]!=cheminsdest[i]):
                message.send(1,'creer repertoire',e)
            #Si ce sont deux répertoites identiques, on ne fait rien.
        #Si le fichier ou répertoire n'existe pas chez le destinataire, alors on le crée !
        if e[1] not in nomsdest:
            if os.path.isfile(e[0]):
                message.send(1,"creer fichier",e)
            if os.path.isdir(e[0]):
                message.send(1,'creer repertoire',e)
    #Quand on a passé en revue toute la liste source, on envoie un message de fin de requête au client.
    message.send(1,"fin requete",'')
    #fin
    sys.exit(0)

#fonction de comparaison et return l'index
def index(liste,e):
    for i in range(len(liste)):
        if liste[i]== e:
            return i

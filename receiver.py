#!/usr/bin/env python3 

import options, filelist, generator
import message, os, sys
from sender import *

#On récupère les arguments
args = options.arguments()

def receiver():
    #On se place dans le répertoire destinataire
    os.chdir(dst)
    #Petit aménagement pour faciliter les comparaison des chemins dans le générateur.
    if dst[-1]!="/":
        prefixe = dst+"/"
    else:
        prefixe = dst
    #On génère la liste de fichiers contenues dans le rep destinataire.
    fichiersdansdest = filelist.listeFichiersSansRec(os.listdir(os.getcwd()),"")
    #Récupération des fichiers sources dans une liste
    fichierssource = []
    (tag,v) = message.receive(0)
    while tag == "fichier":
        fichierssource = fichierssource + [v]
        (tag,v) = message.receive(0)
    
    pid = os.fork()
    if pid == 0 :
        #On crée un nouveau processus fils pour lancer le générateur !
        generator.generateur(fichierssource,fichiersdansdest)
    else:
        #Dans le père, on recoit les fichiers que nous transmet le client suite aux requêtes du générateur, et on les crée !
        (tag,v)=message.receive(0)
        #Tant que le client ne nous indique pas que c'ets la fin du transfert des fichier, on attend des messages !
        while tag != "fin transfert":
            #Demande de création/remplacement de fichier
            if tag == "debut creer":
                #On indique à mrsync d'ignorer la création de fichiers et répertoire qui n'existent pas encore sur la destination.
                if args.existing:
                    pass
                else:
                    if args.force:
                        for e in fichiersdansdest:
                            if os.listdir(e) == []:
                                os.rmdir(v[0])
                #On ouvre le fichier en écriture, s'il n'existe pas déjà, on le crée, puis on écrit ce que le client nous envoie à l'intérieur tant qu'il ne nous tag pas que c'est la fin des données.
                f = os.open(v[0],os.O_WRONLY|os.O_CREAT)
                (tag,v) = message.receive(0)
                while tag == "donnees":
                    os.write(f,v)
                    (tag,v) = message.receive(0)
            #Demande de création de répertoire
            if tag == "creer repertoire":
                #S'il y a une erreur, c'est que le répertoire existe déjà, normalement ça ne drevait pas se produire, mais au cas où ^^'
                try:
                    os.mkdir(v[0])
                except:
                    os.mkdir(v[1])
             #demande de supprimer un fichier
            if tag == "supprimer fichier":
                try:
                    os.unlink(v[0])
                except:
                    os.unlink(v[1])
            #Puis on attend une nouvelle requête de la part du client.
            (tag,v) = message.receive(0)

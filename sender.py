#!/usr/bin/env python3 

import options, sys, os
import message
import filelist

#On récupère les arguments de la ligne de commande dans args
args = options.arguments()

#On sauvegarde la position courante de lancement de commande
position_courante = os.getcwd()

#On définit dans liste reçue en commande qui est Source, qui est Destinataire.
#Nous avons personnellement défini que quand la liste contient plusieurs sources, alors il y a forcément un destinataire derrière.
if len(args.SD)>1:
    src = args.SD[:-1]
    dst = args.SD[-1]
else:
    src = args.SD
    dst = []

#On gère le cas où on utilise . pour désigner le répertoire courant
if src == ['.']:
    src = [os.getcwd()]

#Message pour résumer source et destinataire si verbose activé.
if args.verbose:
    print("La source est",src,". La destination est",dst,".")

#Si il n'y pas de destinataire, on affiche seulement les fichiers du répertoires, ainsi on active l'option de listonly.
if dst == []:
    args.listonly = True

#Test pour vérifier si la/les source(s) existe(nt) ou non dans le répertoire courant.
if len(src)>1:
    contenu = filelist.listeFichiersSansRec([os.getcwd()+"/"],"")
    cont = []
    for e in contenu:
        cont.append(e[1])
    sourceliste = filelist.listeFichiersSansRec(src,"")
    source = []
    for e in sourceliste:
        source.append(e[1])
    for e in source:
        if e not in cont :
            print("Source ", src, " non reconnue")
            sys.exit(0)
else:
    try:
        os.chdir(src[0])
    except:
        print("Source ", src, " non reconnue")
        sys.exit(0)
    os.chdir(position_courante)

#Créer le répertoire destination s'il n'existe pas déjà. 
try :
    os.mkdir(dst)
except :
    pass

#Partie du client
def client(fin,fout):
    #Choix d'une liste de fichiers récursive ou non suivant l'option de récursivité.
    if args.recursive:
        liste = filelist.listeFichiersRec(src)
    else:
        liste = filelist.listeFichiersSansRec(src,"")
    #Indications en plus si verbose activé
    if args.verbose:
        print("La liste des fichiers est : ", liste)
    #Si on est seulement dans le cas d'un ls, on affiche les fichiers de la liste un par un, puis on ferme le client.
    if args.listonly:
        for e in liste:
            print(e[1])
        sys.exit(0)
    #Sinon, on met en place le transfer.
    else:
        #On parcourt les élements de la liste source et on les envoie un par un au receiver, il les communiquera plus tard au générateur.
        for e in liste :
            message.send(fout,"fichier",e)
        #On indique au receiver que l'on a finit d'envoyer la liste des fichiers.
        message.send(fout,"fin envoie fichiers",'')

        #Le client se met un attention de requête de la part du générateur
        (tag,v)=message.receive(fin)
        #Ca commence !
        if tag == "debut requete":
            #On attend quelle requête sera demandée.
            (tag,v)=message.receive(fin)
            #On fait ça tant que le générateur ne nous a pas indiqué que c'était la fin des requêtes.
            while tag != "fin requete":
                #Demande de création/remplacement de fichier
                if tag == "creer fichier":
                    #On ouvre le fichier en question, on le lie et on envoie son contenu au serveur (devenu client)
                    #Avant ça, on pense à se placer dans le bon répertoire pour ouvrir le fichier (en fonction du slash)
                    if src[0][-1]=='/':
                        os.chdir(position_courante+'/'+src[0])
                    else:
                        os.chdir(position_courante) 
                    f = os.open(v[0],os.O_RDONLY)
                    message.send(fout,"debut creer",v)
                    text = os.read(f,1000)
                    while len(text) > 0:
                        message.send(fout,"donnees",text)
                        text = os.read(f,1000)
                    #On a fini d'envoyer le contenu du fichier, on le précise au serveur.
                    message.send(fout,'fin',"")
                    #On attend un nouvelle requête
                    (tag,v)=message.receive(fin)
                #Demande de création de répertoire
                if tag == "creer repertoire":
                    #On envoie cette demande au serveur qui créera un répertoire.
                    message.send(fout,"creer repertoire",v)
                    #On attend une nouvelle demande
                    (tag,v)=message.receive(fin)
                if tag == "supprimer fichier":
                    message.send(fout,"supprimer fichier",v)
                    (tag,v)=message.receive(fin)
                if tag == "supprimer repertoire":
                    message.send(fout,"supprimer repertoire",v)
                    (tag,v)=message.receive(fin)
            #On précise au serveur qu'on a terminé !
            message.send(fout,"fin transfert",'')
    

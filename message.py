#fonctions utilitaires pour envoyer et recevoir des informations de processus à processus via un descripteur 
# de fichier (qui pointera en pratique sur un tube ou une socket) en mettant ces informations dans des “messages”

#!/usr/bin/env python3

import pickle, os
import options
import filelist

#On récupère les arguments de la ligne de commande
args = options.arguments()
 
#Fonction d'envoi
def send(fd,tag,v):
    a_envoyer = (tag,v) #on enverra le tag et le v simultanément sous la forme d'un tuple
    buff = pickle.dumps(a_envoyer) #on convertit le message
    size = len(buff)
    os.write(fd,size.to_bytes(3,'little')) #On récupère d'abord la taille du message pour en informer le receveur
    #Pour être certaines de bien tout envoyer, on boucle.
    nboctets = os.write(fd,buff)
    while 0 < nboctets < size :
        buff = buff[nboctets:]
        nboctets = os.write(fd,buff)

#Fonction de réception
def receive(fd):
    size = int.from_bytes(os.read(fd,3),'little') #On récupère la taille du message
    buff = os.read(fd,size) #On lit dans le tube
    msg = buff
    #On boucle pour être certaines de bien récupérer l'entièreté du message
    while len(msg)<size :
        buff = os.read(fd,size)
        msg = msg + buff
    (tag,v) = pickle.loads(msg) #On reconvertit le message
    return (tag,v) #On renvoie le couple (tag,v) où tag représente une info sur le message et v les données à transporter (liste de fichiers, fichiers... etc)

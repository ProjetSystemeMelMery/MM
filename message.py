#fonctions utilitaires pour envoyer et recevoir des informations de processus à processus via un descripteur 
# de fichier (qui pointera en pratique sur un tube ou une socket) en mettant ces informations dans des “messages”

#!/usr/bin/env python3

import pickle, os
import options
import filelist

args = options.arguments()
 
def send(fd,tag,v):
    a_envoyer = (tag,v)
    buff = pickle.dumps(a_envoyer)
    size = len(buff)
    os.write(fd,size.to_bytes(3,'little'))
    nboctets = os.write(fd,buff)
    while 0 < nboctets < size :
        buff = buff[nboctets:]
        nboctets = os.write(fd,buff)

def receive(fd):
    size = int.from_bytes(os.read(fd,3),'little')
    buff = os.read(fd,size)
    msg = buff
    while len(msg)<size :
        buff = os.read(fd,size)
        msg = msg + buff
    (tag,v) = pickle.loads(msg)
    return (tag,v)

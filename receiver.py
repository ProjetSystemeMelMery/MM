#!/usr/bin/env python3 

import options, filelist, generator
import message, os, sys
from sender import *


args = options.arguments()

def receiver():
    os.chdir(dst)
    fichiersdansdest = filelist.listeFichiersSansRec(filelist.misajour(os.listdir(os.getcwd())))
    print(fichiersdansdest,file=sys.stderr )
    fichierssource = []
    (tag,v) = message.receive(0)
    while tag == "fichier":
        fichierssource = fichierssource + [v]
        (tag,v) = message.receive(0)
    pid = os.fork()
    if pid == 0 :
        generator.generateur(fichierssource,fichiersdansdest)
    else:
        (tag,v)=message.receive(0)
        while tag != "fin requête":
            if tag == "debut/créer/écraser":
                f = os.open(v,O_WRONLY|O_CREAT)
                (tag,v) = message.receive(0)
                while tag != "fin":
                    os.write(f,v)
                    (tag,v) = message.receive(0)
            if tag == "créer répertoire":
                os.mkdir(v)

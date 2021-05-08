#!/usr/bin/env python3 

import options, filelist
import message, os, sys
from sender import *


args = options.arguments()

def receiver():
    os.chdir(dst)
    fichiersdansdest = filelist.listeFichiersRec(filelist.misajour(os.listdir(os.getcwd())))
    print(fichiersdansdest,file=sys.stderr )
    fichierssource = []
    (tag,v) = message.receive(0)
    while tag == "fichier":
        fichierssource = fichierssource + [v]
        (tag,v) = message.receive(0)

    pid = os.fork()
    if pid == 0 :
        generator.generateur(fichierssource,fichiersdansdest)

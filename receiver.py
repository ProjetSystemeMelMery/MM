#!/usr/bin/env python3 

import message
import filelist
import os, sys
import generator
import options

args = options.aruguments()

def serveur(fin,fout):
    if args.listonly:
        sys.exit(0)
    condition = True
    while condition:
        (tag,v) = message.receive(fin)
        if tag == "destinataire":
            dest = v
            os.chdir(dest)
            listedest = filelist.listeFichiersSourceSansOp(dest)
            message.send(fout,"réponse dest",0)
        if tag == "fichiers":
            listesource = v
        condition = False
    sys.exit(0)


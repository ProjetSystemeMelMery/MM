#!/usr/bin/env python3 

from filelist import *
import options
import message
import sys

args = options.aruguments()

if len(args.SD) > 1 :
    destinataire = args.SD[-1]
    source = args.SD[:-1]
else : 
    source = args.SD
    args.listonly = True

print(source,destinataire)

def client(fin,fout):
    if args.listonly:
        for e in listeF(source):
            print(e)
        sys.exit(0)
    else:
        message.send(fout,"destinataire",destinataire)
        (tag,v) = message.receive(fin)
        if tag == "réponse dest" and v==0 :
            message.send(fout,"fichiers",listeF(source))
        sys.exit(0)


    
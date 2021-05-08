#!/usr/bin/env python3 

import options, sys, os
import message
import filelist

args = options.arguments()

if len(args.SD)>1:
    src = args.SD[:-1]
    dst = args.SD[-1]
else:
    src = args.SD
    dst = []

if dst == []:
    args.listonly = True

print(src,dst)

def client(fin,fout):
    if args.recursive:
        liste = filelist.listeFichiersRec(filelist.misajour(src))
    else:
        liste = filelist.listeFichiersSansRec(filelist.misajour(src))
    print(liste)
    if args.listonly:
        for e in liste:
            print(e[1])
        sys.exit(0)
    else:
        for e in liste :
            message.send(fout,"fichier",e)
        message.send(fout,"fin envoie fichiers",'')
        (tag,v)=message.receive(fd)


    

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
        (tag,v)=message.receive(fin)
        while tag != "fin requête":
            if tag == "écraser ou créer fichier":
                f = os.open(v[1],os.O_RDONLY)
                message.send(fout,"debut/créer/écraser","")
                text = os.read(f,1000)
                while len(text) > 0:
                    message.send(fout,"",text)
                    text = os.read(f,1000)
                message.send(fout,'fin',"")
            if tag == "créer répertoire":
                message.send(fout,tag,v[1])
        message(fout,tag,'')


    

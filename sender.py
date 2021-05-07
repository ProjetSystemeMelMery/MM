#!/usr/bin/env python3 

#!/usr/bin/env python3 

import options, sys
import message
import filelist

args = options.arguments()

src = args.SRC
dst = args.DST

print(src,dst)

def sender(fin,fout):
    if args.recursive:
        liste = filelist.listeFichiersRec(src)
    else:
        liste = filelist.listeFichiersSansRec(src)
    print(liste)
    if args.listonly:
        for e in liste:
            print(e)
    message.send(fout,"début envoi fichiers",0)
    for e in liste:
        message.send(fout,"fichier",e)
    message.send(fout,"fin envoi fichiers",0)
    sys.exit(0)


    

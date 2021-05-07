#!/usr/bin/env python3 

import options
import message

args = options.arguments()

def receiver(fin,fout):
    
    stop = False
    fichiers = []
    (tag,v) = message.receive(fin)
    print(tag,v)
    if tag=='début envoi fichiers':
        stop = True
    while stop:
        (tag,v) = message.receive(fin)
        if tag=="fichier":
            fichiers += v
        if tag=="fin envoi fichiers":
            stop = False
    print(fichiers, file=sys.stderr)

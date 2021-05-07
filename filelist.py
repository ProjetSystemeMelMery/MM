#!/usr/bin/env python3

# génération de la liste de fichiers

import os
import options

args = options.aruguments()

def listeFichiersSourceSansOp(src):
    if isinstance(src,list):
        return src
    else:
        if src=='.':
            src=os.getcwd()
        if os.path.isfile(src) or os.path.islink(src):
            return [os.path.basename(src)]
        if os.path.isdir(src):
            return os.listdir(src)

liste = []
def listeFichiersRec(src):
    global liste
    if src=='.':
        src=os.getcwd()
    if os.path.isfile(src) or os.path.islink(src):
        liste = liste + [os.path.basename(src)]
        return liste
    if os.path.isdir(src):
        liste = liste + [os.path.basename(src)]
        fichiers = os.listdir(src)
        for e in fichiers:
            new = os.path.join(src,e)
            liste.append(listeFichiersRec(new))
    return liste

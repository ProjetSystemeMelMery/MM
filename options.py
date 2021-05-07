#!/usr/bin/env python3

# gestion des options et des paramètres, fonctions utilitaires d’affichage dépendant des options, 
# gestion des messages d’erreurs, etc

import argparse, os

parser = argparse.ArgumentParser()
#Une liste dont le dernier élement est la destination
parser.add_argument("SD",nargs='+', default=os.getcwd())
#Option -v --verbose
parser.add_argument("-v","--verbose",help="augmente la verbosité",action="store_true")
#Option -q --quiet
parser.add_argument("-q","--quiet",help="supprime les messages sans erreur",action="store_true")
#Option -r --recursive
parser.add_argument("-r","--recursive",help="récursion dans les répertoires",action="store_true")
#Option --blocking-io
parser.add_argument("--blocking-io",help="utilise des E / S bloquantes pour le shell distant",action="store_true")
#Option --list-only
parser.add_argument("--listonly",help="lister les fichiers au lieu de les copiert",action="store_true")
args=parser.parse_args()

def aruguments():
    return args

    
    
    
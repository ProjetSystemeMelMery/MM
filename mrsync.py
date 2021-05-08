#!/usr/bin/env python3

#le programme principal, qui contient notamment le code du rôle “client”

import options, os, sys, sender, server

#importation des arguments de la ligne de commande dans args
args = options.arguments()

#création des tubes
fd1,fw1 = os.pipe()
fd2,fw2 = os.pipe()

pid = os.fork()
if pid == 0 : #fils (client)
    #fermeture des entrées/sorties non utilisés par le fils
    os.close(fd1)
    os.close(fw2)
    #lancement du client
    sender.client(fd2,fw1)
    #fin du client
    sys.exit(0)
else : #père (serveur)
    #fermeture des entrées/sorties non utilisés par le fils
    os.close(fw1)
    os.close(fd2)
    #redirection des entrées et sorties
    os.dup2(fd1,0)
    os.dup2(fw2,1)
    #lancement du serveur
    server.serveur()
    #attente de la fin du fils
    os.waitpid(pid,0)
#fin du programme
sys.exit(0)

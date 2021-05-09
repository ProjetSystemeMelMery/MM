#!/usr/bin/env python3

#le programme principal, qui contient notamment le code du rôle “client”

import options, os, sys, sender, server

#importation des arguments de la ligne de commande dans args
args = options.arguments()

def transfert_local():
    #création des tubes
    fd1,fw1 = os.pipe()
    fd2,fw2 = os.pipe()

    pid = os.fork()
    if pid == 0 : #fils (serveur)
        #fermeture des entrées/sorties non utilisés par le fils
        os.close(fd1)
        os.close(fw2)
        #redirection des entrées et sorties
        os.dup2(fw1,1)
        os.dup2(fd2,0)
        #lancement du serveur seulement si on doit faire un transfert de fichiers. Sinon seul le client fonctionne.
        if not args.listonly:
            server.serveur()
            sys.exit(0)
    else : #père (client)
        #fermeture des entrées/sorties non utilisés par le père
        os.close(fw1)
        os.close(fd2)
        #lancement du client
        sender.client(fd1,fw2)
        #attente de la fin du fils
        os.waitpid(pid,0)
    #fin du programme
    sys.exit(0)

#Nous sommes restées bloquées lors du transfert vers l'utilisateur distant... Cette fonction est une idée/tentative.
def transfert_distant(dst):
    #création des tubes
    fd1,fw1 = os.pipe()
    fd2,fw2 = os.pipe()

    pid = os.fork()
    if pid == 0 : #fils (client)
        #fermeture des entrées/sorties non utilisés par le fils
        os.close(fw1)
        os.close(fd2)
        #lancement du client
        sender.client(fd1,fw2)
        sys.exit(0)
    else : #père (serveur)
        #fermeture des entrées/sorties non utilisés par le père
        os.close(fd1)
        os.close(fw2)
        #redirection des entrées et sorties
        os.dup2(fw1,1)
        os.dup2(fd2,0)
        #lancement du serveur distant
        distant(dst)
        #attente de la fin du fils
        os.waitpid(pid,0)
    #fin du programme
    sys.exit(0)

def distant(dst):
    iarobase = sender.dst.index("@")
    ipoints = sender.dst.index(":")
    #On récupère le non de l'autre utilisateur et du host.
    distant = sender.dst[:iarobase]
    localhost = sender.dst[(iarobase+1):ipoints]
    #On construit la liste d'arguments.
    arg = ["ssh", "-e", "none", "-l", distant, localhost, "--", "./mrsync.py", "--server"]+sys.argv[1:] 
    os.execvp("ssh", arg)
    sys.exit(0)

if __name__ =="__main__":
    #Si le destinataire est distant (contient : dans son nom) alors on exécute le transfert distant.
    if ":" in sender.dst:
        transfert_distant(sender.dst)
    #Sinon on fait un transfert local normal.
    else:
        transfert_local()

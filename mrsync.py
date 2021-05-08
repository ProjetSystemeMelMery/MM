#!/usr/bin/env python3

#le programme principal, qui contient notamment le code du rôle “client”

import options, os, sys, sender, server

args = options.arguments()

fd1,fw1 = os.pipe()
fd2,fw2 = os.pipe()
pid = os.fork()
if pid == 0 : #fils
    os.close(fd1)
    os.close(fw2)
    sender.client(fd2,fw1)
    sys.exit(0)
else : #père
    os.close(fw1)
    os.close(fd2)
    os.dup2(fd1,0)
    os.dup2(fw2,1)
    server.serveur()
    os.waitpid(pid,0)
sys.exit(0)

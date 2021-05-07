#!/usr/bin/env python3

#le programme principal, qui contient notamment le code du rôle “client”

from options import *
import sender
import receiver
import os, sys    

fd1,fw1 = os.pipe()
fd2,fw2 = os.pipe()
pid = os.fork()
if pid == 0 : #fils
    os.close(fd1)
    os.close(fw2)
    sender.client(fd2,fw1)
else : #père
    os.close(fw1)
    os.close(fd2)
    receiver.serveur(fd1,fw2)
    os.waitpid(pid,0)
sys.exit(0)
#!/usr/bin/env python3  
#!/usr/bin/env python3  

import receiver, sys

def serveur(fin,fout):
    receiver.receiver(fin, fout)
    sys.exit(0)




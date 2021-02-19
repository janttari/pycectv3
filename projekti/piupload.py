#!/usr/bin/env python3

import os, sys

komento=sys.argv[1]
hakemisto=sys.argv[2]+'/raspberry'
raspipolku=sys.argv[3]
pi_ip=sys.argv[4]
#os.system("xmessage "+hakemisto)
os.system("ssh "+pi_ip+" mkdir -p "+raspipolku)
os.system("scp -rp "+hakemisto+"/* "+pi_ip+":"+raspipolku)
os.system('ssh '+pi_ip+' "cd '+raspipolku+' && chmod a+x run && ./run"')

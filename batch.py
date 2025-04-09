# Hi :) if just starting out - probably should start with the duplex.py this main.py references models that aren't shared on this repo

import HTMLBuild as hb

i=1
while i < 13:
    hb.modelLoader("24_{}_MEP".format(str(i).rjust(2, '0')))
    i+=1

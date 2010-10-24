from sys import path
path.append("/usr/lib/python2.6/site-packages")

from dinoisland import Dinosaur
from dinoisland.ttypes import EntityType, Direction

from thrift.transport.TSocket import TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

# AVAILABLES_EGGS = list()
# 
# class Dino(Dinosaur.client):
#     def __init__(self, egg_id):
#         self.egg__id = egg_i
# 
#     def run()
#         self.state = self.hatch(self.egg_id)

if __name__ == "__main__":
    transport = TSocket("thriftpuzzle.facebook.com", 9033)
    protocol = TBinaryProtocol(transport)
    
    client = Dinosaur.Client(protocol)

    transport.open()

    for i in range(10):
        rcr = client.registerClient("xzoiid@gmail.com", "xzoiid", EntityType.HERBIVORE)
        print rcr
#    AVAILABLE_EGGS.append(rcr.eggID)
  
    
#    ds = client.hatch(rcr.eggID)
#    print ds

#    while ds.growCost < 0.3 * ds.calories:
#        print "Growing!"
#        gs = client.grow()
#        if gs.succeeded:
#            ds = gs.myState
#        else:
#            break
#        print "GROW: %s" % gs.message
#
#    for dv in (0,):
#        print "Looking %s" % Direction._VALUES_TO_NAMES[dv]
#        lr = client.look(dv)
#        #print lr
#        if lr.succeeded and len(lr.thingsSeen) != 0:
#            for i in sorted([t for t in lr.thingsSeen if t.type == EntityType.PLANT and t.size <= ds.size+2]):
#                print i
    

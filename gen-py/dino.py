from sys import path
path.append("/usr/lib/python2.6/site-packages")

import threading

from dinoisland import Dinosaur
from dinoisland.ttypes import EntityType, Direction, Coordinate

from thrift.transport.TSocket import TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

import logging

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


EMAIL = "xzoiid@gmail.com"
SCORE_NAME = "xzoiid"
ENTITY = EntityType.HERBIVORE

EGG_POOL = set()
DINO_POOL = list()

class MapManager:
    def __init__(self):
        self.sightings = list()

    def addSighting(self, sighting, position):
        sighting.coordinate = sighting.coordinate.toAbsolute(position)
        self.sightings.append(sighting)

    def findClosest(self, position, type):
        l = sorted([i.alterCoordsToRelative(position) for i in self.sightings if i.type == type])
        if len(l) > 0:
            return l[0]
        return None

    def getDirections(self, position, coords):
        msg = "From %s to %s. " % (position, coords)
        cc = coords - position
        ret = list()
        while cc.distance() != 0:
            while cc.row > 0 and cc.column == 0:
                ret.append(Direction.S)
                cc.row -= 1
            while cc.row < 0 and cc.column == 0:
                ret.append(Direction.N)
                cc.row += 1
            while cc.column > 0 and cc.row == 0:
                ret.append(Direction.E)
                cc.column -= 1
            while cc.column < 0 and cc.row == 0:
                ret.append(Direction.W)
                cc.column += 1
            while cc.column > 0 and cc.row > 0:
                ret.append(Direction.SE)
                cc.row -= 1
                cc.column -= 1
            while cc.column < 0 and cc.row > 0:
                ret.append(Direction.SW)
                cc.row -= 1
                cc.column += 1
            while cc.column < 0 and cc.row < 0:
                ret.append(Direction.NW)
                cc.row += 1
                cc.column += 1
            while cc.column > 0 and cc.row < 0:
                ret.append(Direction.NE)
                cc.row += 1
                cc.column -= 1
 
        logger.info(msg + "Directions: %s" % [Direction._VALUES_TO_NAMES[i] for i in ret])
        return ret
        
MAP_MANAGER = MapManager()

class Dino(Dinosaur.Client, threading.Thread):
    def __init__(self, protocol, eggID=None, coords = Coordinate(0, 0)):
        self.eggID = eggID
        name = eggID is None and "Mama" or eggID
        self.position = coords
        logger.info("New Dino. eggID=%s, name=%s, position=%s" % (self.eggID, name, str(self.position)))
        Dinosaur.Client.__init__(self, protocol)
        threading.Thread.__init__(self, name=name)

    def move(self, dir):
        logger.info("Try move to: %s" % dir)
        mr = Dinosaur.Client.move(self, dir)
        logger.info(mr.message)
        if mr.succeeded:
            logger.info("position was %s" % self.position)
            logger.info("state was %s" % self.state)
            t = Direction._RELATIVE_COORDINATES[dir]
            self.position += Coordinate(t[0], t[1])
            self.state = mr.myState
            logger.info("position is %s" % self.position)
            logger.info("state is %s" % self.state)

    def moveTo(self, coords):
        logger.info("Will move to %s" % coords)
        for d in MAP_MANAGER.getDirections(self.position, coords):
            self.move(d)
            
    def run(self):
        logger.info("Dino %s starting..." % self.name)
        # init
        if self.eggID is None:
            logger.info("I am the first egg. Registering.")
            rcr = self.registerClient(EMAIL, SCORE_NAME, ENTITY)
            logger.info(rcr.message)
            self.species = rcr.species
            self.eggID = rcr.eggID
            logger.info("Got an eggID: %s" % self.eggID)
        self.state = self.hatch(self.eggID)
        logger.info("Got a state: %s" % self.state)

        # Real algo here...

        while True:
            # Should I grow?
            while self.state.growCost < 0.3 * self.state.calories:
                logger.info("Growing!")
                gs = self.grow()
                if gs.succeeded:
                    self.state = gs.myState
                    logger.info("New state agter GROW: %s" % self.state)
                else:
                    break
                logger.info("GROW: %s" % gs.message)
            # Looking around
            for direction in (0, 2, 4, 6):
                logger.info("Looking %s" % Direction._VALUES_TO_NAMES[direction])
                lr = self.look(direction)
                if lr.succeeded and len(lr.thingsSeen) != 0:
                    for s in lr.thingsSeen:
                        MAP_MANAGER.addSighting(s, self.position)
                logger.debug(MAP_MANAGER.sightings)
                a = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                logger.info("Found closest %s" % a)
                if a is not None:
                    self.moveTo(a.coordinate)
                    


if __name__ == "__main__":
    transport = TSocket("thriftpuzzle.facebook.com", 9033)
    protocol = TBinaryProtocol(transport)
    
    DINO_POOL.append(Dino(protocol))

    transport.open()
    logger.info("Transport open")

    for d in DINO_POOL:
        d.start()

    for d in DINO_POOL:
        d.join()

#     for i in range(10):
#         rcr = client.registerClient("xzoiid@gmail.com", "xzoiid", EntityType.HERBIVORE)
#         print rcr
#    AVAILABLE_EGGS.append(rcr.eggID)
  
    
#    ds = client.hatch(rcr.eggID)
#    print ds


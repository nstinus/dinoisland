from sys import path
path.append("/usr/lib/python2.6/site-packages")

import threading
from copy import deepcopy

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
        """ Returns the list of closest elements reachable from my current position. Returned positions are absolute. """
        # logger.debug("Sightings: %s" % self.sightings)
        self.sightings = [i for i in self.sightings if i.coordinate != position]
        logger.debug("Sightings:")
        for s in self.sightings:
            logger.debug(s)
        l = sorted([deepcopy(i).alterCoordsToRelative(position) for i in self.sightings if i.type == type])
        l = [deepcopy(i).alterCoordsToAbsolute(position) for i in l]
        if len(l) > 0:
            return l
        return None

    def getDirections(self, c):
        ret = list()
        while c.distance() != 0:
            while c.row > 0 and c.column == 0:
                ret.append(Direction.S)
                c.row -= 1
            while c.row < 0 and c.column == 0:
                ret.append(Direction.N)
                c.row += 1
            while c.column > 0 and c.row == 0:
                ret.append(Direction.E)
                c.column -= 1
            while c.column < 0 and c.row == 0:
                ret.append(Direction.W)
                c.column += 1
            while c.column > 0 and c.row > 0:
                ret.append(Direction.SE)
                c.row -= 1
                c.column -= 1
            while c.column < 0 and c.row > 0:
                ret.append(Direction.SW)
                c.row -= 1
                c.column += 1
            while c.column < 0 and c.row < 0:
                ret.append(Direction.NW)
                c.row += 1
                c.column += 1
            while c.column > 0 and c.row < 0:
                ret.append(Direction.NE)
                c.row += 1
                c.column -= 1
 
        logger.info("Directions: %s" % [Direction._VALUES_TO_NAMES[i] for i in ret])
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
        logger.info("Try move to: %s" % Direction._VALUES_TO_NAMES[dir])
        mr = Dinosaur.Client.move(self, dir)
        logger.info(mr.message)
        if mr.succeeded:
            logger.info("I moved! Updating infos")
            t = Direction._RELATIVE_COORDINATES[dir]
            self.position += Coordinate(t[0], t[1])
            self.state = mr.myState
        else:
            logger.warning("Move failed!")
            

    def moveTo(self, coords):
        logger.info("Will move to %s" % coords)
        old_pos = deepcopy(self.position)
        old_cal = self.state.calories
        for d in MAP_MANAGER.getDirections(coords - self.position):
            self.move(d)
        logger.info("Moved from %s to %s. Calories gained %d (%d)" % (old_pos, self.position, self.state.calories - old_cal, self.state.calories))
            
    def growIfWise(self):
        while self.state.growCost < 0.3 * self.state.calories:
            logger.info("Growing!")
            gs = self.grow()
            if gs.succeeded:
                self.state = gs.myState
                logger.info("New state agter GROW: %s" % self.state)
            else:
                break
            logger.info("GROW: %s" % gs.message)
            

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
            self.growIfWise()
            # Looking around
            for direction in (0, 2, 4, 6):
                logger.info("Looking %s" % Direction._VALUES_TO_NAMES[direction])
                lr = self.look(direction)
                if lr.succeeded and len(lr.thingsSeen) != 0:
                    self.state = lr.myState
                    for s in lr.thingsSeen:
                        MAP_MANAGER.addSighting(s, self.position)
                for s in MAP_MANAGER.sightings:
                    logger.debug(s)
                candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                if candidates is not None and len(candidates) > 0:
                    candidates.reverse()
                else:
                    logger.warning("No candidates found. Moving on...")
                    continue
                while candidates is not None and len(candidates) > 0:
                    logger.debug("Closest elements found:")
                    for c in sorted(candidates[-4:], reverse=True):
                        logger.debug(c)
                    a = candidates.pop()
                    logger.info("Found closest %s" % a)
                    if a.size > self.state.size + 2:
                        logger.info("Seems big! Discarding")
                        continue
                    self.moveTo(a.coordinate)
                    self.growIfWise()
                    # lay if wise...
                    candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                    if candidates is not None and len(candidates) > 0:
                        candidates.reverse()
                    else:
                        logger.warning("No candidates found. Moving on...")
                        break
                    


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


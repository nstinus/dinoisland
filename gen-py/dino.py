from sys import path
path.append("/usr/lib/python2.6/site-packages")

import threading
from copy import deepcopy

from dinoisland import Dinosaur
from dinoisland.ttypes import EntityType, Direction, Coordinate

from thrift.transport.TSocket import TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

import logging

LOG_FORMAT = "%(asctime)s - %(name)7s - %(levelname)7s - %(message)s"

THRIFT_SERVER = "thriftpuzzle.facebook.com"
THRIFT_PORT = 9033

EMAIL = "xzoiid@gmail.com"
SCORE_NAME = "xzoiid"
ENTITY = EntityType.HERBIVORE

EGG_POOL = set()
DINO_POOL = list()

def counter(init):
    i = init
    while True:
        i += 1
        yield i

DINO_COUNTER = counter(0)

class MapManager:
    def __init__(self):
        self.sightings = list()
        self.logger = logging.getLogger("Map")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def addSighting(self, sighting, position):
        sighting.coordinate = sighting.coordinate.toAbsolute(position)
        self.sightings.append(sighting)

    def findClosest(self, position, type):
        """ Returns the list of closest elements reachable from my current position. Returned positions are absolute. """
        self.sightings = [i for i in self.sightings if i.coordinate != position]
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
 
        self.logger.info("Directions: %s" % [Direction._VALUES_TO_NAMES[i] for i in ret])
        return ret
        
MAP_MANAGER = MapManager()

class Dino(Dinosaur.Client, threading.Thread):
    def __init__(self, eggID=None, coords = Coordinate(0, 0)):
        self.eggID = eggID
        name = eggID is None and str(0) or str(DINO_COUNTER.next())
        self.position = coords
        self.transport = TSocket(THRIFT_SERVER, THRIFT_PORT)
        self.protocol = TBinaryProtocol(self.transport)
        self.logger = logging.getLogger("Dino %s" % name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.info("New Dino. eggID=%s, name=%s, position=%s" % (self.eggID, name, str(self.position)))
        Dinosaur.Client.__init__(self, self.protocol)
        threading.Thread.__init__(self, name=name)

    def move(self, dir):
        self.logger.info("Try move to: %s" % Direction._VALUES_TO_NAMES[dir])
        mr = Dinosaur.Client.move(self, dir)
        self.logger.info(mr.message)
        if mr.succeeded:
            self.logger.info("I moved! Updating infos")
            t = Direction._RELATIVE_COORDINATES[dir]
            self.position += Coordinate(t[0], t[1])
            self.state = mr.myState
        else:
            self.logger.warning("Move failed!")
            

    def moveTo(self, coords):
        self.logger.info("Will move to %s" % coords)
        old_pos = deepcopy(self.position)
        old_cal = self.state.calories
        for d in MAP_MANAGER.getDirections(coords - self.position):
            self.move(d)
        self.logger.info("Moved from %s to %s. Calories gained %d (%d)" % (old_pos, self.position, self.state.calories - old_cal, self.state.calories))
            
    def growIfWise(self):
        while self.state.growCost < 0.3 * self.state.calories:
            self.logger.info("Growing!")
            gs = self.grow()
            if gs.succeeded:
                self.state = gs.myState
                self.logger.info("New state: %s" % self.state)
            else:
                break
            self.logger.info("GROW: %s" % gs.message)

    def run(self):
        self.logger.info("Dino %s starting..." % self.name)
        self.transport.open()
        self.logger.info("Transport open.")
        if self.eggID is None:
            self.logger.info("I am the first egg. Registering.")
            rcr = self.registerClient(EMAIL, SCORE_NAME, ENTITY)
            self.logger.info(rcr.message)
            self.species = rcr.species
            self.eggID = rcr.eggID
            self.logger.info("Got an eggID: %s" % self.eggID)
        self.state = self.hatch(self.eggID)
        self.logger.info("Got a state: %s" % self.state)

        # Real algo here...

        while True:
            self.growIfWise()
            # Looking around
            for direction in (0, 2, 4, 6):
                self.logger.info("Looking %s" % Direction._VALUES_TO_NAMES[direction])
                lr = self.look(direction)
                if lr.succeeded and len(lr.thingsSeen) != 0:
                    self.state = lr.myState
                    for s in lr.thingsSeen:
                        MAP_MANAGER.addSighting(s, self.position)
                for s in MAP_MANAGER.sightings:
                    self.logger.debug(s)
                candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                if candidates is not None and len(candidates) > 0:
                    candidates.reverse()
                else:
                    self.logger.warning("No candidates found. Moving on...")
                    continue
                while candidates is not None and len(candidates) > 0:
                    self.logger.debug("Closest elements found:")
                    for c in sorted(candidates[-4:], reverse=True):
                        self.logger.debug(c)
                    a = candidates.pop()
                    self.logger.info("Found closest %s" % a)
                    if a.size > self.state.size + 2:
                        self.logger.info("Seems big! Discarding")
                        continue
                    self.moveTo(a.coordinate)
                    self.growIfWise()
                    # lay if wise...
                    candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                    if candidates is not None and len(candidates) > 0:
                        candidates.reverse()
                    else:
                        self.logger.warning("No candidates found. Moving on...")
                        break
                    


if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    DINO_POOL.append(Dino())

    for d in DINO_POOL:
        d.start()

    for d in DINO_POOL:
        d.join()

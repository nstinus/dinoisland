from sys import path
path.append("/usr/lib/python2.6/site-packages")

import threading
from copy import deepcopy
from time import sleep
from random import choice

from dinoisland import Dinosaur
from dinoisland.ttypes import EntityType, Direction, Coordinate
from dinoisland.ttypes import GameOverException, YouAreDeadException, BadEggException

from thrift.transport.TSocket import TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

import logging

LOG_FORMAT = "%(asctime)s - %(name)7s - %(levelname)7s - %(message)s"

THRIFT_SERVER = "thriftpuzzle.facebook.com"
THRIFT_PORT = 9033

EMAIL = "xzoiid@gmail.com"
SCORE_NAME = "xzoiid"
ENTITY = EntityType.HERBIVORE
OFFSPRING_DONATION = 1000

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
        self.lock = threading.Lock()
        self.logger = logging.getLogger("Map")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def addSighting(self, sighting, position):
        sighting.coordinate = sighting.coordinate.toAbsolute(position)
        self.lock.acquire()
        self.sightings.append(sighting)
        self.lock.release()

    def findClosest(self, position, type):
        """ Returns the list of closest elements reachable from my current position. Returned positions are absolute. """
        self.lock.acquire()
        self.sightings = [i for i in self.sightings if i.coordinate != position]
        l = sorted([deepcopy(i).alterCoordsToRelative(position) for i in self.sightings if i.type == type])
        self.lock.release()
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
            return True
        else:
            self.logger.warning("Move failed!")
            direction = choice(list(set(Direction._VALUES_TO_NAMES.keys()) - set([dir,])))
            self.move(direction)
            self.look(direction)
            return False
            

    def moveTo(self, coords):
        self.logger.info("Will move to %s" % coords)
        old_pos = deepcopy(self.position)
        old_cal = self.state.calories
        directions = MAP_MANAGER.getDirections(coords - self.position)
        self.logger.info("Directions: %s" % [Direction._VALUES_TO_NAMES[i] for i in directions])
        for d in directions:
            if not self.move(d):
                break
        success = self.state.calories - old_cal > 0
        self.logger.info("Moved from %s to %s. Calories gained %d (%d)" % (old_pos, self.position, self.state.calories - old_cal, self.state.calories))
        return success
            
    def growIfWise(self):
        if self.state.growCost < 0.3 * self.state.calories:
            self.logger.info("Growing!")
            gs = self.grow()
            if gs.succeeded:
                self.state = gs.myState
                self.logger.info("New state: %s" % self.state)
            self.logger.info("GROW: %s" % gs.message)

    def layIfWise(self):
        if self.state.size > 10 \
               and (self.state.eggCost + 1.2*OFFSPRING_DONATION) < 0.3 * self.state.calories:
            self.logger.info("Laying offspring!")
            direction = choice([0, 2, 4, 6])
            er = self.egg(direction, OFFSPRING_DONATION)
            if er.succeeded:
                self.logger.info("Successfully layed an egg!")
                self.state = er.parentDinoState
                self.logger.info("New State: %s" % self.state)
                rc = Direction._RELATIVE_COORDINATES[direction]
                p = self.position + Coordinate(rc[1], rc[0])
                EGG_POOL.add((er.eggID, p.column, p.row))
            self.logger.info("LAY: %s" % er.message)

    def showReport(self):
        self.logger.info("size=%d, calories=%d" % (self.state.size, self.state.calories))

    def run(self):
        self.logger.info("Dino %s starting..." % self.name)
        self.transport.open()
        self.logger.info("Transport open.")
        if self.eggID is None:
            self.logger.info("I am the first egg. Registering.")
            rcr = self.registerClient(EMAIL, SCORE_NAME, ENTITY)
            for l in rcr.message.split("*"):
                self.logger.info("MESSAGE: %s" % l)
            self.species = rcr.species
            self.eggID = rcr.eggID
            self.logger.info("Got an eggID: %s" % self.eggID)
        self.state = self.hatch(self.eggID)
        self.logger.info("Got a state: %s" % self.state)

        # Real algo here...

        try:
            while True:
                self.growIfWise()
                # Looking around
                direction = choice([0, 2, 4, 6])
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
                    self.layIfWise()
                    self.growIfWise()
                    candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                    if candidates is not None and len(candidates) > 0:
                        candidates.reverse()
                    else:
                        self.logger.warning("No candidates found. Moving on...")
                        break
        except GameOverException, e:
            self.logger.error("GameOver! won=%s, score=%d" % (e.wonGame, e.score))
            self.logger.info("HighScoreTable:")
            for l in e.highScoreTable.splitlines():
                self.logger.info(l)
        except YouAreDeadException, e:
            self.logger.warning("I'm dead! %s" % e.description)
        except Exception, e:
            self.logger.error("An unheld exception occured!")
            raise(e)
        finally:
            self.showReport()


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

    while threading.active_count() > 1:
        while len(EGG_POOL) != 0:
            logger.info("Found egg to wake up!")
            e = EGG_POOL.pop()
            d = Dino(e[0], Coordinate(e[2], e[1]))
            DINO_POOL.append(d)
            d.start()
        sleep(1)

    for d in DINO_POOL:
        d.join()

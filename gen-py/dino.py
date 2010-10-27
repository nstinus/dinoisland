from sys import path
path.append("/usr/lib/python2.6/site-packages")

import threading
from copy import deepcopy
from time import sleep
from random import choice
from commands import getstatusoutput
from datetime import datetime

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
OFFSPRING_DONATION = 1500
END_SCORE, BEST_SCORE = -1, -1

EGG_POOL = set()
DINO_POOL = list()
NOW = datetime.today()

def counter(init):
    i = init
    while True:
        i += 1
        yield i

DINO_COUNTER = counter(0)

def gitDescribe():
    r = getstatusoutput("git describe --tags --abbrev --dirty")
    return r[0] == 0 and r[1] or None

def vectorToOrientation(c):
    """ Returns the general direction of a vector."""
    if c.row > 0 and c.column == 0: return Direction.S
    if c.row < 0 and c.column == 0: return Direction.N
    if c.column > 0 and c.row == 0: return Direction.E
    if c.column < 0 and c.row == 0: return Direction.W
    if c.column > 0 and c.row > 0: return Direction.SE
    if c.column < 0 and c.row > 0: return Direction.SW
    if c.column < 0 and c.row < 0: return Direction.NW
    if c.column > 0 and c.row < 0: return Direction.NE

def vectorToDirections(c):
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

def getCone(direction):
    return set([range(8)[direction-1], direction, range(8)[(direction+1)%8]])

def minmax(l):
    return min(l), max(l)


def getCone(direction):
    return set([range(8)[direction-1], direction, range(8)[(direction+1)%8]])

class MapManager:
    def __init__(self):
        self.sightings = list()
        self.lock = threading.Lock()
        self.logger = logging.getLogger("Map")
        self.logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def __addSighting(self, sighting, position):
        sighting.coordinate = sighting.coordinate.toAbsolute(position)
        self.sightings.append(sighting)

    def __deleteSightings(self, position, direction, distance):
        old_n = len(self.sightings)
        if len(self.sightings) != 0:
            self.sightings = [i for i in self.sightings if i.coordinate.distance(position) > distance \
                                  or vectorToOrientation(i.coordinate - position) not in getCone(direction)]
        new_n = len(self.sightings)
        msg = "DELETE pos=%s, dir=%s, d=%d: deleted %d/%d (is %d now) sightings"
        self.logger.info(msg % (position,
                                Direction._VALUES_TO_NAMES[direction],
                                distance,
                                old_n - new_n,
                                old_n,
                                new_n))

    def addSightings(self, position, direction, distance, sightings):
        self.lock.acquire()
        self.__deleteSightings(position, direction, distance)
        old_n = len(self.sightings)
        for s in sightings:
            self.__addSighting(s, position)
        new_n = len(self.sightings)
        self.lock.release()
        msg = "ADD pos=%s: added %d/%d (is %d now) sightings"
        self.logger.info(msg % (position,
                                new_n - old_n,
                                old_n,
                                new_n))

    def findClosest(self, position, type):
        """ Returns the list of closest elements reachable from my current position. Returned positions are absolute. """
        self.lock.acquire()
        self.sightings = [i for i in self.sightings if i.coordinate != position]
        l = sorted([deepcopy(i).alterCoordsToRelative(position) for i in self.sightings if i.type == type])
        self.lock.release()
        l = [deepcopy(i).alterCoordsToAbsolute(position) for i in l]
        if len(l) > 0:
            for i in l:
                self.logger.debug("Closest elements: %s" % i)
            return l
        return None
        

class Dino(Dinosaur.Client, threading.Thread):
    def __init__(self, eggID=None, coords = Coordinate(0, 0)):
        self.eggID = eggID
        name = eggID is None and str(0) or str(DINO_COUNTER.next())
        self.position = coords
        self.transport = TSocket(THRIFT_SERVER, THRIFT_PORT)
        self.protocol = TBinaryProtocol(self.transport)
        self.logger = logging.getLogger("Dino %s" % name)
        self.logger.setLevel(LOG_LEVEL)
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.counters = {'actions': 0, 'moves': 0, 'calories_found': 0, 'calories_burnt': 0, 'eggs': 0, 'looks': 0}
        self.logger.info("New Dino. eggID=%s, name=%s, position=%s" % (self.eggID, name, str(self.position)))
        Dinosaur.Client.__init__(self, self.protocol)
        threading.Thread.__init__(self, name=name)

    def look(self, direction):
        self.counters['actions'] += 1
        self.counters['looks'] += 1
        self.counters['calories_burnt'] += self.state.lookCost
        lr = Dinosaur.Client.look(self, direction)
        self.logger.debug(lr)
        if lr.succeeded:
            self.state = lr.myState
        if lr.succeeded and len(lr.thingsSeen) != 0:
            distances = [i.coordinate.distance(self.position) for i in lr.thingsSeen]
            closest, farest = minmax(distances)
            MAP_MANAGER.addSightings(self.position, direction, farest, lr.thingsSeen)
            self.logger.info("LOOK OK (%s): %d things seen. Closest/Farest %d/%d," % (Direction._VALUES_TO_NAMES[direction],
                                                                                      len(lr.thingsSeen),
                                                                                      closest,
                                                                                      farest))
        else:
            self.logger.warning("LOOK KO (%s): seen nothing." % Direction._VALUES_TO_NAMES[direction])
        return lr.succeeded

    def move(self, dir):
        mr = Dinosaur.Client.move(self, dir)
        self.logger.debug(mr)
        if mr.succeeded:
            self.logger.info("MOVE OK: %s. %s" % (Direction._VALUES_TO_NAMES[dir],
                                                  mr.message))
            t = Direction._RELATIVE_COORDINATES[dir]
            self.position += Coordinate(t[0], t[1])
            self.state = mr.myState
            self.counters['actions'] += 1
            self.counters['moves'] += 1
            self.counters['calories_burnt'] += self.state.moveCost
            return True
        else:
            self.logger.warning("MOVE KO: %s. %s" % (Direction._VALUES_TO_NAMES[dir],
                                                     mr.message))
            direction = choice(list(set(Direction._VALUES_TO_NAMES.keys()) - set([dir,])))
            self.move(direction)
            self.look(direction)
            return False
            
    def moveTo(self, coords):
        old_pos = deepcopy(self.position)
        old_cal = self.state.calories
        directions = vectorToDirections(deepcopy(coords) - self.position)
        self.logger.info("Will move to %s. Directions: %s" % (coords,
                                                              [Direction._VALUES_TO_NAMES[i] for i in directions]))
        moves = list()
        for d in directions:
            moves.append(self.move(d))
            moveto_successful = reduce(lambda x, y: x and y, moves)
            if not moveto_successful: break
        cal_found = (self.state.calories - old_cal) - (len(directions) * self.state.moveCost) # Bilan - Known losses
        msg = "MOVETO %%s. %s -> %s. Calories gained %d." % (old_pos,
                                                             self.position,
                                                             self.state.calories - old_cal)
        if cal_found > 0:
            self.counters['calories_found'] += cal_found
        if cal_found > 0 and moveto_successful:
            self.logger.info(msg % "OK")
        else:
            self.logger.warning(msg % ("%s (m=%s, f=%s)" % ("KO",
                                                           moveto_successful and "OK" or "KO",
                                                           cal_found > 0 and "OK" or "KO"),))
        return cal_found > 0 and moveto_successful
            
    def growIfWise(self):
        if self.state.growCost < 0.3 * self.state.calories:
            gs = self.grow()
            self.logger.debug(gs)
            msg = "GROW %%s: %s" % gs.message
            if gs.succeeded:
                self.state = gs.myState
                self.counters['actions'] += 1
                self.counters['calories_burnt'] += self.state.growCost
                self.logger.info(msg % "OK")
            else:
                self.logger.warning(msg % "KO")
        self.logger.info("STATE: %s" % self.state)

    def layIfWise(self):
        expected_calories_cost  = self.state.eggCost + 1.2*OFFSPRING_DONATION + 5*self.state.moveCost + self.state.lookCost
        if self.state.size > 5 and expected_calories_cost < 0.5 * self.state.calories:
            self.logger.info("Laying offspring!")
            direction = choice([0, 2, 4, 6])
            er = self.egg(direction, OFFSPRING_DONATION)
            if er.succeeded:
                self.logger.info("Successfully layed an egg!")
                self.state = er.parentDinoState
                self.logger.info("STATE: %s" % self.state)
                rc = Direction._RELATIVE_COORDINATES[direction]
                p = self.position + Coordinate(rc[1], rc[0])
                EGG_POOL.add((er.eggID, p.column, p.row))
                new_dir = choice(list(set([0, 2, 4, 6]) - set([direction,])))
                # Stupidly go away...
                for i in range(5):
                    self.move(new_dir)
                self.look(new_dir)
                self.counters['actions'] += 1
                self.counters['eggs'] += 1
                self.counters['calories_burnt'] += expected_calories_cost
            self.logger.info("LAY: %s" % er.message)

    def showPMReport(self):
        self.logger.info("POST MORTEM REPORT")
        self.logger.info("              PMR: size=%d" % self.state.size)
        self.logger.info("              PMR: calories=%d, burnt=%d, found=%d, ratio=%f" % (self.state.calories,
                                                                                           self.counters['calories_burnt'],
                                                                                           self.counters['calories_found'],
                                                                                           self.counters['calories_found'] != 0 and self.counters['calories_burnt']/self.counters['calories_found'] or -1))
        self.logger.info("              PMR: moves=%d, looks=%d, eggs=%d, actions=%d" % (self.counters['moves'],
                                                                                         self.counters['looks'],
                                                                                         self.counters['eggs'],
                                                                                         self.counters['actions']))

    def run(self):
        self.logger.info("Dino %s starting..." % self.name)
        self.transport.open()
        self.logger.info("Transport open.")
        if self.eggID is None:
            self.logger.info("I am the first egg. Registering.")
            rcr = self.registerClient(EMAIL, SCORE_NAME, ENTITY)
            self.logger.debug(rcr)
            for l in rcr.message.split("*"):
                self.logger.info("MESSAGE: %s" % l)
            self.species = rcr.species
            self.eggID = rcr.eggID
            self.logger.info("Got an eggID: %s" % self.eggID)
        self.state = self.hatch(self.eggID)
        self.logger.info("STATE: %s" % self.state)

        # Real algo here...

        try:
            while True:
                self.growIfWise()
                # Looking around
                direction = choice(range(8))
                self.logger.info("Looking %s" % Direction._VALUES_TO_NAMES[direction])
                self.look(direction)
                candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                if candidates is not None and len(candidates) > 0:
                    if candidates[0].coordinate.distance(self.position)*self.state.eggCost > 0.5*self.state.calories:
                        self.look(choice(list(set(range(8)) - getCone(direction))))
                        candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                else:
                    self.logger.warning("No candidates found. Moving on...")
                    continue
                while candidates is not None and len(candidates) > 0:
                    a = candidates.pop(0)
                    self.logger.info("FOUND closest at %d, species='%s', size=%d" % (a.coordinate.distance(self.position),
                                                                                     a.species,
                                                                                     a.size))
                    if a.size > self.state.size + 2:
                        self.logger.info("Seems big! Discarding")
                        continue
                    if not self.moveTo(a.coordinate):
                        self.look(choice(range(8)))
                    elif self.counters['moves'] % 10 == 0:
                        self.logger.info("Random look")
                        self.look(choice(range(8)))
                    self.layIfWise()
                    self.growIfWise()
                    candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                    if candidates is not None and len(candidates) > 0:
                        if candidates[0].coordinate.distance(self.position)*self.state.eggCost > 0.5*self.state.calories:
                            self.look(choice(list(set(range(8)) - getCone(direction))))
                            candidates = MAP_MANAGER.findClosest(self.position, EntityType.PLANT)
                    else:
                        self.logger.warning("No candidates found. Moving on...")
                        break
        except GameOverException, e:
            global END_SCORE, BEST_SCORE
            self.logger.debug(e)
            self.logger.error("GameOver! won=%s, score=%d" % (e.wonGame, e.score))
            self.logger.info("HighScoreTable:")
            for l in e.highScoreTable.splitlines():
                self.logger.info(l)
            END_SCORE = e.score
            BEST_SCORE = [int(l.split()[-1]) for l in e.highScoreTable.splitlines() if SCORE_NAME in l][0]
        except YouAreDeadException, e:
            self.logger.debug(e)
            self.logger.warning("DEAD: %s" % e.description)
        except Exception, e:
            self.logger.debug(e)
            self.logger.error("An unheld exception occured!")
            raise(e)
        finally:
            self.showPMReport()


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(version=gitDescribe())
    parser.add_option("--server", default=None, dest="server")
    parser.add_option("--offspring_donation", type="int", dest="offspring_donation", default=-1)
    parser.add_option("--debug", action="store_true", default=False, dest="debug")
    (options, args) = parser.parse_args()

    LOG_LEVEL = options.debug and logging.DEBUG or logging.INFO

    logger = logging.getLogger("main")
    logger.setLevel(LOG_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("dino %s starting at %s" % (gitDescribe(), NOW))

    if options.server is not None:
        THRIFT_SERVER, THRIFT_PORT = options.server.split(':')
        THRIFT_PORT = int(THRIFT_PORT)
    if options.offspring_donation != -1:
        OFFSPRING_DONATION = options.offspring_donation

    MAP_MANAGER = MapManager()

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

    logger.info("All dinos appear to be dead.")
    msg = "END: score=%d, best=%d" % (END_SCORE, BEST_SCORE)
    logger.info(msg)
    print msg

    sleep(1)
    exit(0)

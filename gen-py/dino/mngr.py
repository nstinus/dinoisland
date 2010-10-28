#!/usr/bin/env python

import logging
from threading import Lock
from copy import deepcopy

from dinoisland.ttypes import Direction

from core import vectorToOrientation, getCone


class MapManager:
    def __init__(self):
        self.sightings = list()
        self.lock = Lock()
        self.logger = logging.getLogger("Map")

    def __addSighting(self, sighting, position):
        sighting.coordinate = sighting.coordinate.toAbsolute(position)
        self.sightings.append(sighting)

    def __deleteSightings(self, position, direction, distance):
        old_n = len(self.sightings)
        if len(self.sightings) != 0:
            self.sightings = [i for i in self.sightings \
                              if i.coordinate.distance(position) > distance \
                                  or vectorToOrientation(i.coordinate - position) \
                                      not in getCone(direction)]
        new_n = len(self.sightings)
        msg = "DELETE pos=%s, dir=%s, d=%d: deleted %d/%d (is %d now) sightings"
        self.logger.info(msg \
            % (position,
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
        self.logger.info(msg \
            % (position, new_n - old_n, old_n, new_n))

    def findClosest(self, position, type):
        """ Returns the list of closest elements reachable from my current position.
            Returned positions are absolute. """
        self.lock.acquire()
        self.sightings = [i for i in self.sightings if i.coordinate != position]
        l = sorted([deepcopy(i).alterCoordsToRelative(position) \
                    for i in self.sightings if i.type == type])
        self.lock.release()
        l = [deepcopy(i).alterCoordsToAbsolute(position) for i in l]
        if len(l) > 0:
            for i in l:
                self.logger.debug("Closest elements: %s" % i)
            return l
        return None
#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#

from math import sqrt

from thrift.Thrift import *

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class EntityType:
  """
  Entity types

  Entities are things that your dinosaur can see and possibly interact with.
  Your dinosaur is able to interact with Plants, Herbivore dinosaurs, and
  Carnivore dinosaurs. Your dinosaur can see impassable terrain, but cannot
  interact with it.
  """
  PLANT = 0
  HERBIVORE = 1
  CARNIVORE = 2
  IMPASSABLE = 3

  _VALUES_TO_NAMES = {
    0: "PLANT",
    1: "HERBIVORE",
    2: "CARNIVORE",
    3: "IMPASSABLE",
  }

  _NAMES_TO_VALUES = {
    "PLANT": 0,
    "HERBIVORE": 1,
    "CARNIVORE": 2,
    "IMPASSABLE": 3,
  }

class Direction:
  """
  Directions

  These enums define directions used on the grid based map of Dinosaur Island.
  In order for your dinosaur to lay an egg, look, or move, it must supply one
  of these enums.
  """
  N = 0
  NE = 1
  E = 2
  SE = 3
  S = 4
  SW = 5
  W = 6
  NW = 7

  _VALUES_TO_NAMES = {
    0: "N",
    1: "NE",
    2: "E",
    3: "SE",
    4: "S",
    5: "SW",
    6: "W",
    7: "NW",
  }

  _NAMES_TO_VALUES = {
    "N": 0,
    "NE": 1,
    "E": 2,
    "SE": 3,
    "S": 4,
    "SW": 5,
    "W": 6,
    "NW": 7,
  }

  _RELATIVE_COORDINATES = {N:  (-1,  0),
                           NE: (-1,  1),
                           E:  ( 0,  1),
                           SE: ( 1,  1),
                           S:  ( 1,  0),
                           SW: ( 1, -1),
                           W:  ( 0, -1),
                           NW: (-1, -1)}


class Coordinate:
  """
  Coordinate struct

  This structure is intended to explicitly define how the coordinate system of
  Dinosaur Island is set up.

  Attributes:
   - row
   - column
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'row', None, None, ), # 1
    (2, TType.I32, 'column', None, None, ), # 2
  )

  def __init__(self, row=None, column=None,):
    self.row = row
    self.column = column

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.row = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.column = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Coordinate')
    if self.row != None:
      oprot.writeFieldBegin('row', TType.I32, 1)
      oprot.writeI32(self.row)
      oprot.writeFieldEnd()
    if self.column != None:
      oprot.writeFieldBegin('column', TType.I32, 2)
      oprot.writeI32(self.column)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

  def __add__(self, other):
    self.row += other.row
    self.column += other.column
    return self

  def __sub__(self, other):
    self.row -= other.row
    self.column -= other.column
    return self

  def toRelative(self, position):
    return self - position

  def toAbsolute(self, position):
    return self + position
  
  def distance(self, other = None):
    r = self.row - (other is not None and other.row or 0)
    c = self.column - (other is not None and other.column or 0)
    return max(abs(r), abs(c))

class DinosaurState:
  """
  Dinosaur State

  This structure contains all pertinent data regarding your dinosaur instance,
  including its available calories to spend, its current size, and how many
  calories it will cost to lay an egg, grow one size, look in a direction,
  and move in a direction.

  Attributes:
   - calories
   - size
   - eggCost
   - growCost
   - lookCost
   - moveCost
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'calories', None, None, ), # 1
    (2, TType.I32, 'size', None, None, ), # 2
    (3, TType.I32, 'eggCost', None, None, ), # 3
    (4, TType.I32, 'growCost', None, None, ), # 4
    (5, TType.I32, 'lookCost', None, None, ), # 5
    (6, TType.I32, 'moveCost', None, None, ), # 6
  )

  def __init__(self, calories=None, size=None, eggCost=None, growCost=None, lookCost=None, moveCost=None,):
    self.calories = calories
    self.size = size
    self.eggCost = eggCost
    self.growCost = growCost
    self.lookCost = lookCost
    self.moveCost = moveCost

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.calories = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.size = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.eggCost = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I32:
          self.growCost = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.I32:
          self.lookCost = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.I32:
          self.moveCost = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DinosaurState')
    if self.calories != None:
      oprot.writeFieldBegin('calories', TType.I32, 1)
      oprot.writeI32(self.calories)
      oprot.writeFieldEnd()
    if self.size != None:
      oprot.writeFieldBegin('size', TType.I32, 2)
      oprot.writeI32(self.size)
      oprot.writeFieldEnd()
    if self.eggCost != None:
      oprot.writeFieldBegin('eggCost', TType.I32, 3)
      oprot.writeI32(self.eggCost)
      oprot.writeFieldEnd()
    if self.growCost != None:
      oprot.writeFieldBegin('growCost', TType.I32, 4)
      oprot.writeI32(self.growCost)
      oprot.writeFieldEnd()
    if self.lookCost != None:
      oprot.writeFieldBegin('lookCost', TType.I32, 5)
      oprot.writeI32(self.lookCost)
      oprot.writeFieldEnd()
    if self.moveCost != None:
      oprot.writeFieldBegin('moveCost', TType.I32, 6)
      oprot.writeI32(self.moveCost)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Sighting:
  """
  Sighting struct

  This structure represents your dinosaur sighting something interesting, be
  it plants to eat, dinosaurs to eat, or fearsome carnivores to avoid. Lastly,
  this struct is also used to tell your dinosaur when it sees impassable
  terrain.

  Each sighting includes coordinates of the sighting (coordinates are always
  relative to your own dinosaur's position), what kind of entity was spotted,
  as well as the species string and what size the entity is. In the case of
  impassable terrain, species will be blank and size will be 0.

  Attributes:
   - coordinate
   - type
   - species
   - size
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'coordinate', (Coordinate, Coordinate.thrift_spec), None, ), # 1
    (2, TType.I32, 'type', None, None, ), # 2
    (3, TType.STRING, 'species', None, None, ), # 3
    (4, TType.I32, 'size', None, None, ), # 4
  )

  def __init__(self, coordinate=None, type=None, species=None, size=None,):
    self.coordinate = coordinate
    self.type = type
    self.species = species
    self.size = size

  def alterCoordsToAbsolute(self, position):
    self.coordinate.toAbsolute(position)
    return self

  def alterCoordsToRelative(self, position):
    self.coordinate.toRelative(position)
    return self

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.coordinate = Coordinate()
          self.coordinate.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.species = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I32:
          self.size = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Sighting')
    if self.coordinate != None:
      oprot.writeFieldBegin('coordinate', TType.STRUCT, 1)
      self.coordinate.write(oprot)
      oprot.writeFieldEnd()
    if self.type != None:
      oprot.writeFieldBegin('type', TType.I32, 2)
      oprot.writeI32(self.type)
      oprot.writeFieldEnd()
    if self.species != None:
      oprot.writeFieldBegin('species', TType.STRING, 3)
      oprot.writeString(self.species)
      oprot.writeFieldEnd()
    if self.size != None:
      oprot.writeFieldBegin('size', TType.I32, 4)
      oprot.writeI32(self.size)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

  def __cmp__(self, other):
    t = cmp(self.type, other.type)
    if t != 0:
      return t
    else:
      return cmp(self.coordinate.distance(), other.coordinate.distance())

class RegisterClientResults:
  """
  Register Client results

  This structure is returned to your client after it calls the registerClient
  function. It includes a string message welcoming you to Dinosaur Island,
  as well as your randomly generated species name. It is important to note
  that this randomly generated species name is how other clients will see your
  dinosaur, and this is different from the highScoreName you chose originally
  if your dinosaur makes it into the evolutionary hall of fame. Lastly, it
  includes an integer egg ID which your client can then use to take over
  control of the very first instance of your dinosaur species.

  Attributes:
   - message
   - species
   - eggID
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'message', None, None, ), # 1
    (2, TType.STRING, 'species', None, None, ), # 2
    (3, TType.I64, 'eggID', None, None, ), # 3
  )

  def __init__(self, message=None, species=None, eggID=None,):
    self.message = message
    self.species = species
    self.eggID = eggID

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.species = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.eggID = iprot.readI64();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('RegisterClientResults')
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 1)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.species != None:
      oprot.writeFieldBegin('species', TType.STRING, 2)
      oprot.writeString(self.species)
      oprot.writeFieldEnd()
    if self.eggID != None:
      oprot.writeFieldBegin('eggID', TType.I64, 3)
      oprot.writeI64(self.eggID)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class LookResults:
  """
  Look action results

  This structure is returned to your client after it calls the look function.
  It includes a string message (useful for debugging), a boolean indicating
  action success, as well as the new state for your dinosaur, and a list of
  Sighting structs (see above).

  Attributes:
   - message
   - succeeded
   - myState
   - thingsSeen
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'message', None, None, ), # 1
    (2, TType.BOOL, 'succeeded', None, None, ), # 2
    (3, TType.STRUCT, 'myState', (DinosaurState, DinosaurState.thrift_spec), None, ), # 3
    (4, TType.LIST, 'thingsSeen', (TType.STRUCT,(Sighting, Sighting.thrift_spec)), None, ), # 4
  )

  def __init__(self, message=None, succeeded=None, myState=None, thingsSeen=None,):
    self.message = message
    self.succeeded = succeeded
    self.myState = myState
    self.thingsSeen = thingsSeen

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.BOOL:
          self.succeeded = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.myState = DinosaurState()
          self.myState.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.LIST:
          self.thingsSeen = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = Sighting()
            _elem5.read(iprot)
            self.thingsSeen.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('LookResults')
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 1)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.succeeded != None:
      oprot.writeFieldBegin('succeeded', TType.BOOL, 2)
      oprot.writeBool(self.succeeded)
      oprot.writeFieldEnd()
    if self.myState != None:
      oprot.writeFieldBegin('myState', TType.STRUCT, 3)
      self.myState.write(oprot)
      oprot.writeFieldEnd()
    if self.thingsSeen != None:
      oprot.writeFieldBegin('thingsSeen', TType.LIST, 4)
      oprot.writeListBegin(TType.STRUCT, len(self.thingsSeen))
      for iter6 in self.thingsSeen:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class GrowResults:
  """
  Grow action results

  This structure is returned to your client after it calls the grow function.
  It includes a string message (useful for debugging), a boolean indicating
  action success, as well as the new state for your dinosaur.

  Attributes:
   - message
   - succeeded
   - myState
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'message', None, None, ), # 1
    (2, TType.BOOL, 'succeeded', None, None, ), # 2
    (3, TType.STRUCT, 'myState', (DinosaurState, DinosaurState.thrift_spec), None, ), # 3
  )

  def __init__(self, message=None, succeeded=None, myState=None,):
    self.message = message
    self.succeeded = succeeded
    self.myState = myState

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.BOOL:
          self.succeeded = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.myState = DinosaurState()
          self.myState.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('GrowResults')
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 1)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.succeeded != None:
      oprot.writeFieldBegin('succeeded', TType.BOOL, 2)
      oprot.writeBool(self.succeeded)
      oprot.writeFieldEnd()
    if self.myState != None:
      oprot.writeFieldBegin('myState', TType.STRUCT, 3)
      self.myState.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class MoveResults:
  """
  Move action results

  This structure is returned to your client after it calls the move function.
  It includes a string message (useful for debugging), a boolean indicating
  action success, as well as the new state for your dinosaur. The most common
  reason for the boolean succeeded returning False is your dinosaur attempted
  to move into impassable terrain.

  Attributes:
   - message
   - succeeded
   - myState
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'message', None, None, ), # 1
    (2, TType.BOOL, 'succeeded', None, None, ), # 2
    (3, TType.STRUCT, 'myState', (DinosaurState, DinosaurState.thrift_spec), None, ), # 3
  )

  def __init__(self, message=None, succeeded=None, myState=None,):
    self.message = message
    self.succeeded = succeeded
    self.myState = myState

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.BOOL:
          self.succeeded = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.myState = DinosaurState()
          self.myState.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('MoveResults')
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 1)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.succeeded != None:
      oprot.writeFieldBegin('succeeded', TType.BOOL, 2)
      oprot.writeBool(self.succeeded)
      oprot.writeFieldEnd()
    if self.myState != None:
      oprot.writeFieldBegin('myState', TType.STRUCT, 3)
      self.myState.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class EggResults:
  """
  Lay an Egg action results

  This structure is returned to your client after it calls the egg function.
  It includes a string message (useful for debugging), a boolean indicating
  action success, the new state of your dinosaur, and the integer egg ID of
  your newly created egg if the action was successful. If the egg function
  fails, the egg ID will be 0.

  Attributes:
   - message
   - succeeded
   - parentDinoState
   - eggID
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'message', None, None, ), # 1
    (2, TType.BOOL, 'succeeded', None, None, ), # 2
    (3, TType.STRUCT, 'parentDinoState', (DinosaurState, DinosaurState.thrift_spec), None, ), # 3
    (4, TType.I64, 'eggID', None, None, ), # 4
  )

  def __init__(self, message=None, succeeded=None, parentDinoState=None, eggID=None,):
    self.message = message
    self.succeeded = succeeded
    self.parentDinoState = parentDinoState
    self.eggID = eggID

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.BOOL:
          self.succeeded = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.parentDinoState = DinosaurState()
          self.parentDinoState.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.eggID = iprot.readI64();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('EggResults')
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 1)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.succeeded != None:
      oprot.writeFieldBegin('succeeded', TType.BOOL, 2)
      oprot.writeBool(self.succeeded)
      oprot.writeFieldEnd()
    if self.parentDinoState != None:
      oprot.writeFieldBegin('parentDinoState', TType.STRUCT, 3)
      self.parentDinoState.write(oprot)
      oprot.writeFieldEnd()
    if self.eggID != None:
      oprot.writeFieldBegin('eggID', TType.I64, 4)
      oprot.writeI64(self.eggID)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class BadEggException(Exception):
  """
  Bad egg exception

  This exception is thrown if a client attempts to take control of a newly
  hatched dinosaur egg but fails. The string contains a description of the
  failure, which may include incorrect egg ID or trying to take over an egg
  of a different species (i.e. a dinosaur that does not belong to your email
  address).

  Attributes:
   - description
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'description', None, None, ), # 1
  )

  def __init__(self, description=None,):
    self.description = description

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.description = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('BadEggException')
    if self.description != None:
      oprot.writeFieldBegin('description', TType.STRING, 1)
      oprot.writeString(self.description)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class YouAreDeadException(Exception):
  """
  You are dead exception

  This exception is thrown if a client attempts to call an action function,
  but the dinosaur controlled turns out to be already dead. This can happen if
  the dinosaur your client controls is eaten by a predator, or has exceeded
  its real time lifespan. The string will contain useful information about the
  cause of death for your dinosaur.

  Attributes:
   - description
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'description', None, None, ), # 1
  )

  def __init__(self, description=None,):
    self.description = description

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.description = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('YouAreDeadException')
    if self.description != None:
      oprot.writeFieldBegin('description', TType.STRING, 1)
      oprot.writeString(self.description)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class AlreadyRegisteredException(Exception):
  """
  Already registered exception

  This exception is thrown if a client that is already controlling a dinosaur
  attempts to call registerClient().

  Attributes:
   - description
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'description', None, None, ), # 1
  )

  def __init__(self, description=None,):
    self.description = description

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.description = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('AlreadyRegisteredException')
    if self.description != None:
      oprot.writeFieldBegin('description', TType.STRING, 1)
      oprot.writeString(self.description)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class GameOverException(Exception):
  """
  Game over exception

  This exception is thrown if a client attempts to call an action function,
  but the species has already died out, either due to having all of the
  dinosaurs die of natural causes or due to the species time limit being
  reached. The wonGame field will be true if your species scored high enough
  to win the game. The score field will provide your total score. The message
  field will contain instructions for how to get credit for winning the game
  if your species scored high enough to win, and will also contain the reason
  your species went extinct. The highScoreTable field will contain the top 10
  high scores since the server was started. Note that the highScoreTable
  does not list dinosaur species names, instead it users the chosen
  highScoreNames provided by each puzzler's registerClient() call to register
  their species.

  Attributes:
   - wonGame
   - score
   - message
   - highScoreTable
  """

  thrift_spec = (
    None, # 0
    (1, TType.BOOL, 'wonGame', None, None, ), # 1
    (2, TType.I32, 'score', None, None, ), # 2
    (3, TType.STRING, 'message', None, None, ), # 3
    (4, TType.STRING, 'highScoreTable', None, None, ), # 4
  )

  def __init__(self, wonGame=None, score=None, message=None, highScoreTable=None,):
    self.wonGame = wonGame
    self.score = score
    self.message = message
    self.highScoreTable = highScoreTable

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.BOOL:
          self.wonGame = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.score = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.message = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.highScoreTable = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('GameOverException')
    if self.wonGame != None:
      oprot.writeFieldBegin('wonGame', TType.BOOL, 1)
      oprot.writeBool(self.wonGame)
      oprot.writeFieldEnd()
    if self.score != None:
      oprot.writeFieldBegin('score', TType.I32, 2)
      oprot.writeI32(self.score)
      oprot.writeFieldEnd()
    if self.message != None:
      oprot.writeFieldBegin('message', TType.STRING, 3)
      oprot.writeString(self.message)
      oprot.writeFieldEnd()
    if self.highScoreTable != None:
      oprot.writeFieldBegin('highScoreTable', TType.STRING, 4)
      oprot.writeString(self.highScoreTable)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

/**
 * Autogenerated by Thrift
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 */
#ifndef dinoisland_TYPES_H
#define dinoisland_TYPES_H

#include <Thrift.h>
#include <TApplicationException.h>
#include <protocol/TProtocol.h>
#include <transport/TTransport.h>





struct EntityType {
  enum type {
    PLANT = 0,
    HERBIVORE = 1,
    CARNIVORE = 2,
    IMPASSABLE = 3
  };
};

extern const std::map<int, const char*> _EntityType_VALUES_TO_NAMES;

struct Direction {
  enum type {
    N = 0,
    NE = 1,
    E = 2,
    SE = 3,
    S = 4,
    SW = 5,
    W = 6,
    NW = 7
  };
};

extern const std::map<int, const char*> _Direction_VALUES_TO_NAMES;

typedef struct _Coordinate__isset {
  _Coordinate__isset() : row(false), column(false) {}
  bool row;
  bool column;
} _Coordinate__isset;

class Coordinate {
 public:

  static const char* ascii_fingerprint; // = "989D1F1AE8D148D5E2119FFEC4BBBEE3";
  static const uint8_t binary_fingerprint[16]; // = {0x98,0x9D,0x1F,0x1A,0xE8,0xD1,0x48,0xD5,0xE2,0x11,0x9F,0xFE,0xC4,0xBB,0xBE,0xE3};

  Coordinate() : row(0), column(0) {
  }

  virtual ~Coordinate() throw() {}

  int32_t row;
  int32_t column;

  _Coordinate__isset __isset;

  bool operator == (const Coordinate & rhs) const
  {
    if (!(row == rhs.row))
      return false;
    if (!(column == rhs.column))
      return false;
    return true;
  }
  bool operator != (const Coordinate &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const Coordinate & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _DinosaurState__isset {
  _DinosaurState__isset() : calories(false), size(false), eggCost(false), growCost(false), lookCost(false), moveCost(false) {}
  bool calories;
  bool size;
  bool eggCost;
  bool growCost;
  bool lookCost;
  bool moveCost;
} _DinosaurState__isset;

class DinosaurState {
 public:

  static const char* ascii_fingerprint; // = "62CBF95059CB084430B0BABE2E5A68C7";
  static const uint8_t binary_fingerprint[16]; // = {0x62,0xCB,0xF9,0x50,0x59,0xCB,0x08,0x44,0x30,0xB0,0xBA,0xBE,0x2E,0x5A,0x68,0xC7};

  DinosaurState() : calories(0), size(0), eggCost(0), growCost(0), lookCost(0), moveCost(0) {
  }

  virtual ~DinosaurState() throw() {}

  int32_t calories;
  int32_t size;
  int32_t eggCost;
  int32_t growCost;
  int32_t lookCost;
  int32_t moveCost;

  _DinosaurState__isset __isset;

  bool operator == (const DinosaurState & rhs) const
  {
    if (!(calories == rhs.calories))
      return false;
    if (!(size == rhs.size))
      return false;
    if (!(eggCost == rhs.eggCost))
      return false;
    if (!(growCost == rhs.growCost))
      return false;
    if (!(lookCost == rhs.lookCost))
      return false;
    if (!(moveCost == rhs.moveCost))
      return false;
    return true;
  }
  bool operator != (const DinosaurState &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const DinosaurState & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _Sighting__isset {
  _Sighting__isset() : coordinate(false), type(false), species(false), size(false) {}
  bool coordinate;
  bool type;
  bool species;
  bool size;
} _Sighting__isset;

class Sighting {
 public:

  static const char* ascii_fingerprint; // = "7059FE933F4B0CDEB5FE6A7DE0007E92";
  static const uint8_t binary_fingerprint[16]; // = {0x70,0x59,0xFE,0x93,0x3F,0x4B,0x0C,0xDE,0xB5,0xFE,0x6A,0x7D,0xE0,0x00,0x7E,0x92};

  Sighting() : species(""), size(0) {
  }

  virtual ~Sighting() throw() {}

  Coordinate coordinate;
  EntityType::type type;
  std::string species;
  int32_t size;

  _Sighting__isset __isset;

  bool operator == (const Sighting & rhs) const
  {
    if (!(coordinate == rhs.coordinate))
      return false;
    if (!(type == rhs.type))
      return false;
    if (!(species == rhs.species))
      return false;
    if (!(size == rhs.size))
      return false;
    return true;
  }
  bool operator != (const Sighting &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const Sighting & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _RegisterClientResults__isset {
  _RegisterClientResults__isset() : message(false), species(false), eggID(false) {}
  bool message;
  bool species;
  bool eggID;
} _RegisterClientResults__isset;

class RegisterClientResults {
 public:

  static const char* ascii_fingerprint; // = "A0ED90CE9B69D7A0FCE24E26CAECD2AF";
  static const uint8_t binary_fingerprint[16]; // = {0xA0,0xED,0x90,0xCE,0x9B,0x69,0xD7,0xA0,0xFC,0xE2,0x4E,0x26,0xCA,0xEC,0xD2,0xAF};

  RegisterClientResults() : message(""), species(""), eggID(0) {
  }

  virtual ~RegisterClientResults() throw() {}

  std::string message;
  std::string species;
  int64_t eggID;

  _RegisterClientResults__isset __isset;

  bool operator == (const RegisterClientResults & rhs) const
  {
    if (!(message == rhs.message))
      return false;
    if (!(species == rhs.species))
      return false;
    if (!(eggID == rhs.eggID))
      return false;
    return true;
  }
  bool operator != (const RegisterClientResults &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const RegisterClientResults & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _LookResults__isset {
  _LookResults__isset() : message(false), succeeded(false), myState(false), thingsSeen(false) {}
  bool message;
  bool succeeded;
  bool myState;
  bool thingsSeen;
} _LookResults__isset;

class LookResults {
 public:

  static const char* ascii_fingerprint; // = "11270F2FE570B21C9FDF9E2A8C39CC30";
  static const uint8_t binary_fingerprint[16]; // = {0x11,0x27,0x0F,0x2F,0xE5,0x70,0xB2,0x1C,0x9F,0xDF,0x9E,0x2A,0x8C,0x39,0xCC,0x30};

  LookResults() : message(""), succeeded(0) {
  }

  virtual ~LookResults() throw() {}

  std::string message;
  bool succeeded;
  DinosaurState myState;
  std::vector<Sighting>  thingsSeen;

  _LookResults__isset __isset;

  bool operator == (const LookResults & rhs) const
  {
    if (!(message == rhs.message))
      return false;
    if (!(succeeded == rhs.succeeded))
      return false;
    if (!(myState == rhs.myState))
      return false;
    if (!(thingsSeen == rhs.thingsSeen))
      return false;
    return true;
  }
  bool operator != (const LookResults &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const LookResults & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _GrowResults__isset {
  _GrowResults__isset() : message(false), succeeded(false), myState(false) {}
  bool message;
  bool succeeded;
  bool myState;
} _GrowResults__isset;

class GrowResults {
 public:

  static const char* ascii_fingerprint; // = "796648A7E7B433BA37D5A275574F56C7";
  static const uint8_t binary_fingerprint[16]; // = {0x79,0x66,0x48,0xA7,0xE7,0xB4,0x33,0xBA,0x37,0xD5,0xA2,0x75,0x57,0x4F,0x56,0xC7};

  GrowResults() : message(""), succeeded(0) {
  }

  virtual ~GrowResults() throw() {}

  std::string message;
  bool succeeded;
  DinosaurState myState;

  _GrowResults__isset __isset;

  bool operator == (const GrowResults & rhs) const
  {
    if (!(message == rhs.message))
      return false;
    if (!(succeeded == rhs.succeeded))
      return false;
    if (!(myState == rhs.myState))
      return false;
    return true;
  }
  bool operator != (const GrowResults &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const GrowResults & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _MoveResults__isset {
  _MoveResults__isset() : message(false), succeeded(false), myState(false) {}
  bool message;
  bool succeeded;
  bool myState;
} _MoveResults__isset;

class MoveResults {
 public:

  static const char* ascii_fingerprint; // = "796648A7E7B433BA37D5A275574F56C7";
  static const uint8_t binary_fingerprint[16]; // = {0x79,0x66,0x48,0xA7,0xE7,0xB4,0x33,0xBA,0x37,0xD5,0xA2,0x75,0x57,0x4F,0x56,0xC7};

  MoveResults() : message(""), succeeded(0) {
  }

  virtual ~MoveResults() throw() {}

  std::string message;
  bool succeeded;
  DinosaurState myState;

  _MoveResults__isset __isset;

  bool operator == (const MoveResults & rhs) const
  {
    if (!(message == rhs.message))
      return false;
    if (!(succeeded == rhs.succeeded))
      return false;
    if (!(myState == rhs.myState))
      return false;
    return true;
  }
  bool operator != (const MoveResults &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const MoveResults & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _EggResults__isset {
  _EggResults__isset() : message(false), succeeded(false), parentDinoState(false), eggID(false) {}
  bool message;
  bool succeeded;
  bool parentDinoState;
  bool eggID;
} _EggResults__isset;

class EggResults {
 public:

  static const char* ascii_fingerprint; // = "C9B464BA8B9DE84FBC129C7ADE870271";
  static const uint8_t binary_fingerprint[16]; // = {0xC9,0xB4,0x64,0xBA,0x8B,0x9D,0xE8,0x4F,0xBC,0x12,0x9C,0x7A,0xDE,0x87,0x02,0x71};

  EggResults() : message(""), succeeded(0), eggID(0) {
  }

  virtual ~EggResults() throw() {}

  std::string message;
  bool succeeded;
  DinosaurState parentDinoState;
  int64_t eggID;

  _EggResults__isset __isset;

  bool operator == (const EggResults & rhs) const
  {
    if (!(message == rhs.message))
      return false;
    if (!(succeeded == rhs.succeeded))
      return false;
    if (!(parentDinoState == rhs.parentDinoState))
      return false;
    if (!(eggID == rhs.eggID))
      return false;
    return true;
  }
  bool operator != (const EggResults &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const EggResults & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _BadEggException__isset {
  _BadEggException__isset() : description(false) {}
  bool description;
} _BadEggException__isset;

class BadEggException : public ::apache::thrift::TException {
 public:

  static const char* ascii_fingerprint; // = "EFB929595D312AC8F305D5A794CFEDA1";
  static const uint8_t binary_fingerprint[16]; // = {0xEF,0xB9,0x29,0x59,0x5D,0x31,0x2A,0xC8,0xF3,0x05,0xD5,0xA7,0x94,0xCF,0xED,0xA1};

  BadEggException() : description("") {
  }

  virtual ~BadEggException() throw() {}

  std::string description;

  _BadEggException__isset __isset;

  bool operator == (const BadEggException & rhs) const
  {
    if (!(description == rhs.description))
      return false;
    return true;
  }
  bool operator != (const BadEggException &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const BadEggException & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _YouAreDeadException__isset {
  _YouAreDeadException__isset() : description(false) {}
  bool description;
} _YouAreDeadException__isset;

class YouAreDeadException : public ::apache::thrift::TException {
 public:

  static const char* ascii_fingerprint; // = "EFB929595D312AC8F305D5A794CFEDA1";
  static const uint8_t binary_fingerprint[16]; // = {0xEF,0xB9,0x29,0x59,0x5D,0x31,0x2A,0xC8,0xF3,0x05,0xD5,0xA7,0x94,0xCF,0xED,0xA1};

  YouAreDeadException() : description("") {
  }

  virtual ~YouAreDeadException() throw() {}

  std::string description;

  _YouAreDeadException__isset __isset;

  bool operator == (const YouAreDeadException & rhs) const
  {
    if (!(description == rhs.description))
      return false;
    return true;
  }
  bool operator != (const YouAreDeadException &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const YouAreDeadException & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _AlreadyRegisteredException__isset {
  _AlreadyRegisteredException__isset() : description(false) {}
  bool description;
} _AlreadyRegisteredException__isset;

class AlreadyRegisteredException : public ::apache::thrift::TException {
 public:

  static const char* ascii_fingerprint; // = "EFB929595D312AC8F305D5A794CFEDA1";
  static const uint8_t binary_fingerprint[16]; // = {0xEF,0xB9,0x29,0x59,0x5D,0x31,0x2A,0xC8,0xF3,0x05,0xD5,0xA7,0x94,0xCF,0xED,0xA1};

  AlreadyRegisteredException() : description("") {
  }

  virtual ~AlreadyRegisteredException() throw() {}

  std::string description;

  _AlreadyRegisteredException__isset __isset;

  bool operator == (const AlreadyRegisteredException & rhs) const
  {
    if (!(description == rhs.description))
      return false;
    return true;
  }
  bool operator != (const AlreadyRegisteredException &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const AlreadyRegisteredException & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};

typedef struct _GameOverException__isset {
  _GameOverException__isset() : wonGame(false), score(false), message(false), highScoreTable(false) {}
  bool wonGame;
  bool score;
  bool message;
  bool highScoreTable;
} _GameOverException__isset;

class GameOverException : public ::apache::thrift::TException {
 public:

  static const char* ascii_fingerprint; // = "CF2341ED4AD72C0BB19C06AA571743A1";
  static const uint8_t binary_fingerprint[16]; // = {0xCF,0x23,0x41,0xED,0x4A,0xD7,0x2C,0x0B,0xB1,0x9C,0x06,0xAA,0x57,0x17,0x43,0xA1};

  GameOverException() : wonGame(0), score(0), message(""), highScoreTable("") {
  }

  virtual ~GameOverException() throw() {}

  bool wonGame;
  int32_t score;
  std::string message;
  std::string highScoreTable;

  _GameOverException__isset __isset;

  bool operator == (const GameOverException & rhs) const
  {
    if (!(wonGame == rhs.wonGame))
      return false;
    if (!(score == rhs.score))
      return false;
    if (!(message == rhs.message))
      return false;
    if (!(highScoreTable == rhs.highScoreTable))
      return false;
    return true;
  }
  bool operator != (const GameOverException &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const GameOverException & ) const;

  uint32_t read(::apache::thrift::protocol::TProtocol* iprot);
  uint32_t write(::apache::thrift::protocol::TProtocol* oprot) const;

};



#endif

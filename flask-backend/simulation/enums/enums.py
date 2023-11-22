import enum

class SessionType(enum.Enum):
  Practice = enum.auto()
  Pre_Qualifying = enum.auto()
  Qualifying = enum.auto()
  Race = enum.auto()

  def __getstate__(self):
    return self._name_

class LogDetailLevel(enum.Enum):
  low = enum.auto()
  medium = enum.auto()
  high = enum.auto()

  def __getstate__(self):
    return self._name_

class LogEventType(enum.Enum):
  default = enum.auto()
  crash = enum.auto()
  retirement = enum.auto()
  newLeader = enum.auto()
  yellowFlag = enum.auto()
  redFlag = enum.auto()
  purpleSector = enum.auto()
  fastestLap = enum.auto()
  personalBest = enum.auto()
  mistake = enum.auto()

  def __getstate__(self):
    return self._name_

class SectorTimeState(enum.Enum):
  yellow = enum.auto()
  green = enum.auto()
  purple = enum.auto()
  white = enum.auto()

  def __getstate__(self):
    return self._name_

class EntryState(enum.Enum):
    Garage = enum.auto()
    OutLap = enum.auto()
    Running = enum.auto()
    InLap = enum.auto()
    PitStop = enum.auto()
    Retired = enum.auto()

    def __getstate__(self):
        return self._name_

class SimulationState(enum.Enum):
  Running = enum.auto()
  Finished = enum.auto()
  Paused = enum.auto()
  Cancelled = enum.auto()

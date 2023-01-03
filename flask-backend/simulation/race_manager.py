from .race_engine import RaceEngine
from .sheet_engine import SheetEngine
import simulation.session as session
import simulation.track as track

from threading import Lock

class RaceManagerMeta(type):
  _instances = {}
  _lock: Lock = Lock()

  def __call__(cls, *args, **kwds):
    with cls._lock:
      if cls not in cls._instances:
        instance = super().__call__(*args, **kwds)
        cls._instances[cls] = instance
    return cls._instances[cls]


class RaceManager(metaclass=RaceManagerMeta):
  engine_ :RaceEngine = None

  def __init__(self):
    self.engine_ = SheetEngine(track.Track("Test Track", "AUT", 1, 1, [track.Sector(90, True, [track.MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 1"), track.MicroSector(5, 5, 5, 5, 5, 15)]), track.Sector(30, False, [track.MicroSector(5, 5, 5, 5, 5, 30, "Micro_Sector 3"), track.MicroSector(5, 5, 5, 5, 5, 30)]), track.Sector(90, True, [track.MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 5"), track.MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 6")])]), [])

  def setTrack(self, track :track.Track):
    self.engine_.setTrack(track)

  def setEntryList(self, entry_list :list):
    self.engine_.setEntryList(entry_list)

  def startSession(self, session :session.SessionType, socket):
    return self.engine_.startSession(session, socket)

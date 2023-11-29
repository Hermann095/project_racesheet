from copy import copy, deepcopy
from time import time

from ..models.race_entry import RaceEntry
from ..models.entry_track_state import EntryTrackState
from ..models.lap import Lap
from ..models.sector_time import SectorTime
from ..enums.enums import EntryState
import simulation.models.track as track
import simulation.session as session
import simulation.utils as utils

from flask_socketio import SocketIO
from typing import Callable



class RaceEngine():
  def __init__(self, track :track.Track, entry_list :list[RaceEntry], options = session.SessionOptions()) -> None:
    self.track_ = track
    self.entry_list_ = entry_list
    self.options_ = options
    self.lap_dict_ : dict[str, list[session.Lap]] = {}
    self.position_dict_ : dict[str, int] = {}
    self.overall_time_ : dict[str, float] = {}
    self.log = []
    self.fastest_lap : dict[str, session.Lap] = {}
    self.personal_best : dict[str, session.Lap] = {}
    self.currentTime: float
    self.sessionLengthTime: int
    self.sessionLengthLaps: int
    self.entry_track_state_dict: dict[str, EntryTrackState]

  def setTrack(self, track :track.Track):
    self.track_ = track

  def setEntryList(self, entry_list :list[RaceEntry]):
    self.entry_list_ = entry_list

  def startSession(self, session :session.SessionType, socket: SocketIO, stateCallback: Callable, simSpeedCallback: Callable) -> session.SessionResult:
    pass

  def initSession(self, sessionLengthTime: int = 3600, sessionLengthLaps: int = 50):
    self.initLapDict()
    self.initPositionDict()
    self.initOverallTime()
    self.initFastestLapDict()
    self.initPersonalBestDict()
    self.initEntryTrackStateDict()
    self.log = []
    self.currentTime = 0
    self.sessionLengthTime = sessionLengthTime
    self.sessionLengthLaps = sessionLengthLaps

  def initLapDict(self):
    lap_dict = dict()
    for entry in self.entry_list_:
      lap_dict[entry.number] = []

    self.lap_dict_ = lap_dict

  def initPositionDict(self):
    position_dict = dict()
    for index, entry in enumerate(self.entry_list_):
      position_dict[entry.number] = index

    self.position_dict_ = position_dict

  def initOverallTime(self):
    overall = dict()
    for entry in self.entry_list_:
      overall[entry.number] = 0.0

    self.overall_time = overall

  def initFastestLapDict(self):
    fastest_lap = dict()
    for entry in self.entry_list_:
      sector_list = [session.SectorTime()]*(len(self.track_.sectors))
      fastest_lap[entry.number] = session.Lap(entry, utils.FLOAT_MAX, sector_list)

    self.fastest_lap = fastest_lap

  def initPersonalBestDict(self):
    personal_best = dict()
    for entry in self.entry_list_:
      sector_list = [session.SectorTime()]*(len(self.track_.sectors))
      personal_best[entry.number] = session.Lap(entry, utils.FLOAT_MAX, sector_list)

    self.personal_best = personal_best

  def initEntryTrackStateDict(self):
    entry_track_state_dict = dict()
    for entry in self.entry_list_:
      entry_track_state_dict[entry.number] = EntryTrackState(entry, Lap(entry))

    self.entry_track_state_dict = entry_track_state_dict

  def recordLap(self, entry :RaceEntry, lap :session.Lap):

    self.lap_dict_[entry.number].append(lap)
    #TODO: remove debug
    self.DEBUG_print_lap(lap)

    #FIXME
    """
    if len(self.lap_dict_.get(entry.number)) == 1:
      self.fastest_lap[entry.number] = lap
      self.addLogEntry(entry.drivers[entry.current_driver].name + " set a first lap of " + utils.secToTimeStr(lap.time))
    elif lap.time < self.fastest_lap.get(entry.number).time: 
      self.fastest_lap[entry.number] = lap
      self.addLogEntry(entry.drivers[entry.current_driver].name + " set a new personal best of " + utils.secToTimeStr(lap.time), type=session.LogEventType.personalBest)
    else:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " set a laptime of " + utils.secToTimeStr(lap.time), session.LogDetailLevel.medium)

    for index, sector in enumerate(self.personal_best.get(entry.number).sector_times):
      if lap.sector_times[index].time < sector.time:
        self.personal_best.get(entry.number).sector_times[index] = lap.sector_times[index]
      else:
        lap.sector_times[index].state = session.SectorTimeState.yellow
    """
  def recordSector(self, entry: RaceEntry, sector_time: float):
      #TODO: add sector recording
      self.entry_track_state_dict[entry.number].current_lap.sector_times.append(SectorTime(sector_time))

  #
  # TODO: rewrite or delete, not working currently
  #
  def swapPosition(self, entry_1 : RaceEntry, entry_2 : RaceEntry):
    position_1 = self.position_dict_.get(entry_1.number)
    position_2 = self.position_dict_.get(entry_2.number)

    laps_1 = self.lap_list_[position_1]
    laps_2 = self.lap_list_[position_2]

    self.lap_list_[position_1] = laps_2
    self.lap_list_[position_2] = laps_1

    self.position_dict_[entry_1.number] = position_2
    self.position_dict_[entry_2.number] = position_1

  def sortEntryList(self):
    old_entry_list = self.entry_list_
    new_entry_list = []
    for entry in old_entry_list:
      new_entry_list.append([])

    for entry in old_entry_list:
      new_entry_list[self.position_dict_.get(entry.number)] = entry

    self.entry_list_ = new_entry_list


  def addLogEntry(self, message: str, detail_level: session.LogDetailLevel = session.LogDetailLevel.low, type: session.LogEventType = session.LogEventType.default):
    new_entry = session.LogEntry(message, detail_level, type)
    self.log.append(new_entry)
    #TODO: remove DUBUG
    print(message)


  def startNewLap(self, entry: RaceEntry, state: EntryState):
    entry.setState(state)
    self.entry_track_state_dict[entry.number].startNewLap(Lap(entry), state)

  def finishLap(self, entry: RaceEntry, state: EntryState):
    self.entry_track_state_dict[entry.number].finishLap()
    self.recordLap(entry, self.entry_track_state_dict[entry.number].current_lap)
    entry.setState(state)

  def DEBUG_print_lap(self, lap :session.Lap):
    driver_name = lap.entry.drivers[lap.entry.current_driver].name
    sector_string = ""

    for sector_time in lap.sector_times:
      sector_string += ("  " + utils.secToTimeStr(sector_time.time))

    print("Lap: " + driver_name + " | " + sector_string + " | " + utils.secToTimeStr(lap.time))
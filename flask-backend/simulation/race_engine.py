from time import time

import simulation.track as track
import simulation.race_entry as race_entry
import simulation.session as session
import simulation.utils as utils

from flask_socketio import SocketIO
from typing import Callable



class RaceEngine():
  def __init__(self, track :track.Track, entry_list :list[race_entry.RaceEntry], options = session.SessionOptions()) -> None:
    self.track_ = track
    self.entry_list_ = entry_list
    self.options_ = options
    self.lap_dict_ : dict[str, list[session.Lap]] = {}
    self.position_dict_ : dict[str, int] = {}
    self.overall_time_ : dict[str, float] = {}
    self.retired = []
    self.log = []
    self.fastest_lap : dict[str, session.Lap] = {}
    self.personal_best : dict[str, session.Lap] = {}

  def setTrack(self, track :track.Track):
    self.track_ = track

  def setEntryList(self, entry_list :list[race_entry.RaceEntry]):
    self.entry_list_ = entry_list

  def startSession(self, session :session.SessionType, socket: SocketIO, stateCallback: Callable) -> session.SessionResult:
    pass

  def initSession(self):
    self.initLapDict()
    self.initPositionDict()
    self.initOverallTime()
    self.retired = []
    self.log = []
    self.fastest_lap = {}
    self.personal_best = {}

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

  def recordLap(self, entry :race_entry.RaceEntry, lap :session.Lap):
    
    #
    # TODO: Fix bug where sectory are flagged wrong
    #
    try:
      for index, sector in enumerate(self.personal_best.get(entry.number).sector_times):
        if sector.time < lap.sector_times[index].time:
          lap.sector_times[index].time = sector.time
          lap.sector_times[index].state = session.SectorTimeState.green
        else:
          lap.sector_times[index].state = session.SectorTimeState.yellow

      self.personal_best.get(entry.number).time = sum(x.time for x in self.personal_best.get(entry.number).sector_times)
    except:
      for index, sector in enumerate(lap.sector_times):
        sector.state = session.SectorTimeState.green
      self.personal_best[entry.number] = lap

    self.lap_dict_[entry.number].append(lap)

    try:
      if lap.time < self.fastest_lap.get(entry.number).time:
        self.fastest_lap[entry.number] = lap
        self.addLogEntry(entry.drivers[entry.current_driver].name + " set a new personal best of " + utils.secToTimeStr(lap.time), type=session.LogEventType.personalBest)
        #self.DEBUG_print_lap(lap)
      else:
        self.addLogEntry(entry.drivers[entry.current_driver].name + " set a laptime of " + utils.secToTimeStr(lap.time), session.LogDetailLevel.medium)
    except:
      self.fastest_lap[entry.number] = lap
      self.addLogEntry(entry.drivers[entry.current_driver].name + " set a first lap of " + utils.secToTimeStr(lap.time))
      #self.DEBUG_print_lap(lap)
      

  def swapPosition(self, entry_1 : race_entry.RaceEntry, entry_2 : race_entry.RaceEntry):
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


  def isRetired(self, car_number :int):
    try:
      self.retired.index(car_number)
      return True
    except:
      return False

  def addLogEntry(self, message: str, detail_level: session.LogDetailLevel = session.LogDetailLevel.low, type: session.LogEventType = session.LogEventType.default):
    new_entry = session.LogEntry(message, detail_level, type)
    self.log.append(new_entry)

  def DEBUG_print_lap(self, lap :session.Lap):
    driver_name = lap.entry.drivers[lap.entry.current_driver].name
    sector_string = ""

    for sector_time in lap.sector_times:
      sector_string += ("  " + utils.secToTimeStr(sector_time))

    print("Lap: " + driver_name + " | " + sector_string + " | " + utils.secToTimeStr(lap.time))

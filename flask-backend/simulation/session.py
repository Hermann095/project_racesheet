from dataclasses import dataclass
from dataclasses import field
from json import JSONEncoder
import json
import simulation.utils as utils
from .enums.enums import *
from .models.race_entry import RaceEntry
from .models.track import Track
from .models.log_entry import LogEntry
from .models.sector_time import SectorTime
from .models.lap import Lap


class SessionOptions():
  def __init__(self, skill_range = 1000, min_weight = 505, drag_multiplier = 1, low_speed_mult = 0.25, high_speed_mult = 0.25, acceleration_mult = 0.25, top_speed_mult = 0.25, weight_factor = 0.3, tyre_factor = 0.5, driver_mult = 2, random_range = 200, allowed_quali_laps = 4, time_step = 1.0, out_lap_mult = 2.0) -> None:
    self.skill_range_ = skill_range
    self.min_weight_ = min_weight
    self.drag_multiplier_ = drag_multiplier
    self.low_speed_mult_ = low_speed_mult
    self.high_speed_mult_ = high_speed_mult
    self.acceleration_mult_ = acceleration_mult
    self.top_speed_mult_ = top_speed_mult
    self.weight_factor_ = weight_factor
    self.tyre_factor_ = tyre_factor
    self.driver_mult_ = driver_mult
    self.random_range_ = random_range
    self.allowed_quali_laps = allowed_quali_laps
    self.time_step = time_step
    self.out_lap_mult = out_lap_mult


class SessionResult():
  def __init__(self, session :SessionType, track: Track, entries :list[RaceEntry], time :list, notes :list, lap_times :dict[list[Lap]], fastest_lap :dict[Lap], 
                personal_best:dict[Lap], position_chart = [], log :list[LogEntry] = [], current_tick :int = 0, total_ticks :int = 0) -> None:
    self.session_ = session
    self.track_ = track
    self.entries_ = entries
    self.time_ = time
    self.notes_ = notes
    self.lap_times_ = lap_times
    self.fastest_lap_ = fastest_lap
    self.position_chart_ = position_chart
    self.log_ = log
    self.personal_best_ = personal_best
    self.sortResults()
    self.leader_time_ = self.time_[0] if len(self.time_) != 0 else 0
    self.best_sectors :dict[Lap] = self.setBestSectors()
    self.gap_ = self.setGap()
    self.current_tick_ = current_tick
    self.total_ticks_ = total_ticks
    

  def printLog(self):
    for log_entry in self.log_:
      print(log_entry.text)

  def printResults(self):
    print("Results from " + str(self.session_))

    self.sortResults()

    for index,entry in enumerate(self.entries_):
      driver_name = entry.drivers[entry.current_driver].name
      gap = self.time_[index] - self.leader_time_
      print(str(index+1) + ": " + driver_name + "\t| " + utils.secToTimeStr(self.fastest_lap_.get(entry.number).sector_times[0].time) + "\t| " + utils.secToTimeStr(self.fastest_lap_.get(entry.number).sector_times[1].time) + "\t| " + utils.secToTimeStr(self.fastest_lap_.get(entry.number).sector_times[2].time) + "\t| " + utils.secToTimeStr(self.time_[index]) + "\t| + " + utils.secToTimeStr(gap))

  def sortResults(self):

    if len(self.time_) == 0:
      return

    zipped_lists = zip(self.time_, self.entries_)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    self.time_, self.entries_ = [list(tuple) for tuple in tuples]
    self.leader_time_ = self.time_[0]
    self.setBestSectors()

  def setBestSectors(self) -> Lap:
    sector_list = []
    #for index in range(len(self.fastest_lap_.get(self.entries_[0].number).sector_times)):
    #  sector_list.append(SectorTime(utils.FLOAT_MAX))

    """
    for entry in self.entries_:
      if (len(self.lap_times_) > 0):
        for index in range(len(self.fastest_lap_.get(entry.number).sector_times)):
          sector_list.append(SectorTime(utils.FLOAT_MAX))
    """

    for i in range(len(self.track_.sectors)):
      sector_list.append(SectorTime(utils.FLOAT_MAX))

    best_lap = Lap(self.entries_[0], 0, sector_list.copy())

    for entry in self.entries_:
      #self.personal_best_[entry.number] = Lap(entry, utils.FLOAT_MAX, sector_list.copy())
      for lap in self.lap_times_.get(entry.number):
        #if lap.time < self.personal_best_[entry.number].time:
          #self.personal_best_[entry.number].time = lap.time
        for sector_index, time in enumerate(best_lap.sector_times):
          #if lap.sector_times[sector_index].time < self.personal_best_[entry.number].sector_times[sector_index].time:
            #self.personal_best_[entry.number].sector_times[sector_index].time = lap.sector_times[sector_index].time
          if lap.sector_times[sector_index].time < best_lap.sector_times[sector_index].time:
            best_lap.sector_times[sector_index].time = lap.sector_times[sector_index].time
          
    #best_lap.time = sum(best_lap.sector_times)
    best_lap.time = sum(x.time for x in best_lap.sector_times)

    return best_lap

  def setGap(self) -> list:
    gap_list = []
    for index,entry in enumerate(self.entries_):
      gap = self.time_[index] - self.leader_time_
      gap_list.append(gap)
    return gap_list


  def __getstate__(self):
    return {
      "session": self.session_,
      "track_name": self.track_.name,
      "entries": self.entries_,
      "time": list(map(utils.secToTimeStr,self.time_)),
      "gap": list(map(utils.secToTimeStr,self.gap_)),
      "notes": self.notes_,
      "lap_times": self.lap_times_,
      "fastest_lap": self.fastest_lap_,
      "position_chart": self.position_chart_,
      "log": self.log_,
      "leader_time": utils.secToTimeStr(self.leader_time_),
      "best_sectors": self.best_sectors,
      "personal_best": self.personal_best_,
      "current_tick": self.current_tick_,
      "total_ticks": self.total_ticks_
    }


        
        



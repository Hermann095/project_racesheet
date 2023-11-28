from random import randint
from .race_engine import RaceEngine
from .session import Lap, SessionResult, SessionType, LogDetailLevel, LogEventType, SectorTime
from .models.track import MicroSector
from .models.race_entry import RaceEntry
from .enums.enums import SimulationState
from .enums.enums import EntryState
import simulation.utils as utils
from flask_socketio import SocketIO, emit
import jsonpickle
from typing import Callable


FLOAT_MAX = utils.FLOAT_MAX


class SheetEngine(RaceEngine):

  def startSession(self, session :SessionType, socket: SocketIO, stateCallback: Callable, simSpeedCallback: Callable) -> SessionResult:
    self.socket = socket
    self.stateCallback : Callable = stateCallback
    self.simSpeedCallback : Callable = simSpeedCallback
    if session == SessionType.Practice:
      self.initSession(sessionLengthTime=5400)
      result = self.practice()
    elif session == SessionType.Pre_Qualifying:
      self.initSession(sessionLengthTime=1800)
      result = self.pre_qualifying()
    elif session == SessionType.Qualifying:
      self.initSession(sessionLengthTime=3600)
      result = self.qualifying()
    elif session == SessionType.Race:
      self.initSession()
      result = self.race()

    return result

  def hello_message(self, session :SessionType):
    self.addLogEntry("Hello from a " + str(session._name_) + " session at " + str(self.track_.name) + ", " + str(self.track_.nation), LogDetailLevel.high)

  def practice(self):
    self.hello_message(SessionType.Practice)
    self.calcLap(SessionType.Practice)

  def pre_qualifying(self):
    self.hello_message(SessionType.Pre_Qualifying)
    self.calcLap(SessionType.Pre_Qualifying)

  def qualifying(self) -> SessionResult:

    self.hello_message(SessionType.Qualifying)
    #sessionLenght = 3600 #seconds
    #numQualiLaps = 4
    #numPossibleLaps = math.ceil(self.sessionLengthTime / self.track_.lap_time())
    """for i in range(numPossibleLaps):
      while self.stateCallback() == utils.SimulationState.Paused:
        print("paused simulation...")
        self.socket.emit("paused_qualifying")
        self.socket.sleep(2)
      
      if self.stateCallback() == utils.SimulationState.Cancelled:
        self.socket.emit("cancelled_qualifying")
        results = self.constructSessionResults(SessionType.Qualifying, i, numPossibleLaps)
        return results
      
      self.calcLap(SessionType.Qualifying, i, numPossibleLaps)
      self.record_fastest_lap() 
      results = self.constructSessionResults(SessionType.Qualifying, i, numPossibleLaps)
      #self.record_fastest_lap()
      self.socket.emit("update_qualifying_results", jsonpickle.encode(results, unpicklable=False))
      self.socket.sleep(self.simSpeedCallback())

    self.record_fastest_lap() 
    results = self.constructSessionResults(SessionType.Qualifying, numPossibleLaps, numPossibleLaps)
    
    #for entry in self.entry_list_:
    #  self.DEBUG_print_lap(self.lap_list_[self.position_dict_.get(entry.number)][0])
    """

    while self.currentTime < self.sessionLengthTime:
      
      if self.stateCallback() == SimulationState.Cancelled:
        self.socket.emit("cancelled_qualifying")
        results = self.constructSessionResults(SessionType.Qualifying, self.currentTime, self.sessionLengthTime)
        return results

      if self.stateCallback() == SimulationState.Paused:
        print("paused simulation...")
        self.socket.emit("paused_qualifying")
        self.socket.sleep(1)
        continue
      

      self.calcTimeStep(SessionType.Qualifying, self.currentTime, self.sessionLengthTime)
      #self.calcLap(SessionType.Qualifying, self.currentTime, self.sessionLengthTime)
      self.record_fastest_lap() 
      results = self.constructSessionResults(SessionType.Qualifying, self.currentTime, self.sessionLengthTime)
      self.socket.emit("update_qualifying_results", jsonpickle.encode(results, unpicklable=False))
      self.socket.sleep(self.simSpeedCallback())
      self.currentTime += self.options_.time_step

    self.record_fastest_lap() 
    results = self.constructSessionResults(SessionType.Qualifying, self.currentTime, self.sessionLengthTime)
    return results


  def race(self):
    self.hello_message(SessionType.Race)
    self.calcLap(SessionType.Race)

  def calcLap(self, session :SessionType, current_tick: int, total_ticks: int):
    self.addLogEntry("calculate lap time...", LogDetailLevel.high)

    #print("new lap")

    sector_dict: dict[str, SectorTime] = {}
    micro_sector_dict = dict()

    for entry in self.entry_list_:
      sector_dict[entry.number] = []

    for entry in self.entry_list_:
      match entry.getState():
        case EntryState.InLap:
          self.addLogEntry(entry.drivers[entry.current_driver].name + " comes back to the garage." , LogDetailLevel.high)
          entry.setState(EntryState.Garage)
          continue
        case EntryState.OutLap:
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts fast lap." , LogDetailLevel.high)
          entry.setState(EntryState.Running)
          continue
        case EntryState.Running:
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts in lap." , LogDetailLevel.high)
          entry.setState(EntryState.InLap)
          continue
        case EntryState.Garage:
          pass
        case _:
          continue
      
      laps_done = len(self.lap_dict_.get(entry.number))
      
      if laps_done < self.options_.allowed_quali_laps:
        if (total_ticks - current_tick) <= (self.options_.allowed_quali_laps - laps_done):
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts out lap." , LogDetailLevel.high)
          entry.setState(EntryState.OutLap)
        elif randint(0, 100) < 10:
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts out lap." , LogDetailLevel.high)
          entry.setState(EntryState.OutLap)
    
    for sector in self.track_.sectors:
      if not sector.microsector_timing:
        micro_sector_time = sector.time / len(sector.micro_sectors)

      for entry in self.entry_list_:
          micro_sector_dict[entry.number] = []

      for micro_sector in sector.micro_sectors:
        if not sector.microsector_timing:
          micro_sector.time = micro_sector_time
        self.calcMicroSector(session, micro_sector, micro_sector_dict)
      
      for entry in self.entry_list_:
        if entry.getState() != EntryState.Running:
          continue
        sector_time = sum(micro_sector_dict.get(entry.number))
        #print("#" + entry.number + " " + utils.secToTimeStr(sector_time))
        old_sector_list = sector_dict.get(entry.number)
        old_sector_list.append(SectorTime(sector_time))
        sector_dict[entry.number] = old_sector_list

    
    for entry in self.entry_list_:
      if entry.getState() == EntryState.Running:
        sector_list = sector_dict.get(entry.number)
        lap_time = sum(x.time for x in sector_list)
        self.recordLap(entry, Lap(entry, lap_time, sector_list))
    
        

  def calcMicroSector(self, session :SessionType, micro_sector :MicroSector, micro_sector_dict: dict):
    for entry in self.entry_list_:
      
      if entry.getState() != EntryState.Running:
        continue

      driver_pace = 0
      tyre_grip = 0
      engine_power = 0
      spread_factor = 0

      if session == SessionType.Qualifying:
        driver_pace = entry.drivers[entry.current_driver].qualy_speed
        tyre_grip = entry.tyres.qualy_grip
        engine_power = entry.engine.qualy_power
        engine_acceleration = entry.engine.qualy_acceleration
        spread_factor = self.track_.qualy_spread
      else:
        driver_pace = entry.drivers[entry.current_driver].race_speed
        tyre_grip = entry.tyres.race_grip
        spread_factor = self.track_.race_spread
        engine_power = entry.engine.race_power
        engine_acceleration = entry.engine.race_acceleration

      spread_factor *= 0.2

      car_acceleration = (engine_acceleration + entry.engine.driveablity) / 2
      car_top_speed = (engine_power - (entry.chassis.drag_ * self.options_.drag_multiplier_)) / (2 + self.options_.drag_multiplier_ - 1)

      low_speed_corner_factor = 1 + (((self.options_.skill_range_ / 2) - entry.chassis.grip_low_speed_) * self.options_.low_speed_mult_ * spread_factor / (self.options_.skill_range_  * 2.25))
      high_speed_corner_factor = 1 + (((self.options_.skill_range_ / 2) - entry.chassis.grip_high_speed_) * self.options_.high_speed_mult_ * spread_factor  / (self.options_.skill_range_  * 2.25))
      acceleration_factor = 1 + (((self.options_.skill_range_ / 2) - car_acceleration) * self.options_.acceleration_mult_* spread_factor * 2 / (self.options_.skill_range_  * 2.25))
      top_speed_factor = 1 + (((self.options_.skill_range_ / 2) - car_top_speed) * self.options_.top_speed_mult_ * spread_factor * 2 / (self.options_.skill_range_  * 2.25))

      car_weight_factor = 1 + ((entry.chassis.weight_ + entry.engine.weight - self.options_.min_weight_) * self.options_.weight_factor_ * spread_factor) * 3.1 / (self.options_.skill_range_  * 2)
      tyre_factor = 1 + (((self.options_.skill_range_ / 2) - tyre_grip) * self.options_.tyre_factor_ * spread_factor / (self.options_.skill_range_  * 2.25 * 3))
      driver_factor = 1 + (((self.options_.skill_range_ / 2) - driver_pace) * self.options_.driver_mult_ * spread_factor / (self.options_.skill_range_  * 2.25 * 3))

      micro_sector_time_unit = micro_sector.time / (micro_sector.low_speed_corners + micro_sector.high_speed_corners + micro_sector.acceleration + micro_sector.top_speed)

      low_speed_corner_time = micro_sector_time_unit * micro_sector.low_speed_corners * low_speed_corner_factor * car_weight_factor * tyre_factor * driver_factor
      high_speed_corner_time =  micro_sector_time_unit * micro_sector.high_speed_corners * high_speed_corner_factor * car_weight_factor * tyre_factor * driver_factor
      acceleration_time =  micro_sector_time_unit * micro_sector.acceleration * acceleration_factor * car_weight_factor * tyre_factor * driver_factor
      top_speed_time =  micro_sector_time_unit * micro_sector.top_speed * top_speed_factor

      driver_consistency = 1 + ((self.options_.skill_range_ - entry.drivers[entry.current_driver].consistency) / self.options_.skill_range_)

      time = (low_speed_corner_time + high_speed_corner_time + acceleration_time + top_speed_time)
      time += randint(-self.options_.random_range_ * driver_consistency, self.options_.random_range_ * driver_consistency) / 1000
      mistake_time = self.checkMistakes(session, entry, micro_sector)
      if mistake_time == FLOAT_MAX:
        self.addLogEntry(entry.drivers[entry.current_driver].name + " retired ", LogEventType.retirement)
        entry.setRetired()

      
      time += mistake_time

      old_micro_sector_list = micro_sector_dict.get(entry.number)
      old_micro_sector_list.append(time)
      micro_sector_dict[entry.number] = old_micro_sector_list


  def checkMistakes(self, session_type :SessionType, entry :RaceEntry, micro_sector :MicroSector) -> float:
    random_value = randint(0, self.options_.skill_range_ * 10)

    if random_value > entry.drivers[entry.current_driver].error_prone:
      return 0.0


    if micro_sector.name:
      track_part_name = "in " + micro_sector.name
    else:
      track_part_name = "on his Lap"

    mistake_severity = randint(0, 100)

    if mistake_severity <= 50:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " made a minor mistake " + track_part_name, LogDetailLevel.high, LogEventType.mistake)
      return randint(100, 300) / 1000
    elif mistake_severity <= 75:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " made a small mistake " + track_part_name, LogDetailLevel.high, LogEventType.mistake)
      return randint(200, 500) / 1000
    elif mistake_severity <= 90:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " made an error " + track_part_name, LogDetailLevel.high, LogEventType.mistake)
      return randint(400, 1000) / 1000
    elif mistake_severity <= 97:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " made a big mistake " + track_part_name, LogDetailLevel.high, LogEventType.mistake)
      return randint(900, 3000) / 1000
    elif mistake_severity <= 99:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " spun " + track_part_name, LogDetailLevel.medium, LogEventType.mistake)
      return randint(4000, 10000) / 1000
    else:
      self.addLogEntry(entry.drivers[entry.current_driver].name + " crashed " + track_part_name, LogEventType.crash)
      return FLOAT_MAX

  def constructSessionResults(self, session_type :SessionType, current_tick: int, total_ticks: int) -> SessionResult:
    self.sortEntryList()
    overall_list = []
    for entry in self.entry_list_:
      overall_list.append(self.overall_time.get(entry.number))

    results = SessionResult(session_type, self.track_, self.entry_list_, overall_list, [], self.lap_dict_, self.fastest_lap, self.personal_best, [], self.log, current_tick, total_ticks)
    return results

  def record_fastest_lap(self):
    for entry in self.entry_list_:
      try:
        fastest_time = FLOAT_MAX

        """
        if len(self.lap_dict_.get(entry.number)) == 0:
          sector_list = [SectorTime()]*(self.track_.sectors)
          print(sector_list)
          self.fastest_lap[entry.number] = Lap(entry, FLOAT_MAX, sector_list)
          continue
        """
        for lap in self.lap_dict_.get(entry.number):
          if lap.time < fastest_time:
            fastest_time = lap.time
            self.fastest_lap[entry.number] = lap

        self.overall_time[entry.number] = fastest_time
      except:
        self.overall_time[entry.number] = FLOAT_MAX
        

  def decideEntryOutLap(self):
    for entry in self.entry_list_:
      if entry.getState() != EntryState.Garage:
        continue

      laps_done = len(self.lap_dict_.get(entry.number))
      remaining_time = self.currentTime - self.sessionLengthTime
      predicted_time = self.track_.lap_time * self.options_.out_lap_mult
      
      if laps_done < self.options_.allowed_quali_laps:
        if (remaining_time) <= (predicted_time * (self.options_.allowed_quali_laps - laps_done) + 30):
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts out lap." , LogDetailLevel.high)
          self.startNewLap(entry, EntryState.OutLap)
        elif randint(0, 100) < 5:
          self.addLogEntry(entry.drivers[entry.current_driver].name + " starts out lap." , LogDetailLevel.high)
          self.startNewLap(entry, EntryState.OutLap)

  def calcTimeStep(self, session :SessionType, step_size: int = 1):
    self.decideEntryOutLap()

    for entry in self.entry_list_:
      if entry.getState() == EntryState.Garage:
        continue
      if entry.getState() == EntryState.InLap or entry.getState() == EntryState.OutLap:
        current_sector_index = self.entry_track_state_dict[entry.number].current_sector
        current_microsector_index = self.entry_track_state_dict[entry.number].current_microsector
        current_microsector = self.track_.sectors[current_sector_index].micro_sectors[current_microsector_index]
        
        if not self.track_.sectors[current_sector_index].microsector_distance:
          added_distance = self.track_.sectors[current_sector_index].distance
        else:
          added_distance = current_microsector.distance

        added_distance = added_distance / self.options_.out_lap_mult * step_size

        target_distance = self.entry_track_state_dict[entry.number].lap_distance + added_distance
        new_sector_indices = self.track_.allSectorIndexFromDistance(target_distance)

        if new_sector_indices.sector != current_sector_index or new_sector_indices.micro_sector != current_microsector_index:
          pass # TODO: add sector jump behaviour



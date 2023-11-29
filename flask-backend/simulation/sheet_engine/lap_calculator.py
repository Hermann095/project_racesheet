from random import randint
from ..enums.enums import EntryState, LogDetailLevel
from ..session import SessionType
from ..models.race_entry import RaceEntry
from ..race_engine.race_engine import RaceEngine

def decideEntryOutLap(self: RaceEngine) -> None:
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

def calcTimeStep(self: RaceEngine, session: SessionType, step_size: int = 1) -> None:
    if session != SessionType.Race:
        decideEntryOutLap(self)

    for entry in self.entry_list_:
        match entry.getState():
            case EntryState.OutLap | EntryState.InLap:
                calcOutLapTimeStep(self, session, entry, step_size)
            case EntryState.Running:
                calcLapTimeStep(self, session, entry, step_size)
            case _:
                continue


def calcOutLapTimeStep(self: RaceEngine, session: SessionType, entry: RaceEntry, step_size: int = 1) -> None:
    #print(self.entry_track_state_dict[entry.number])
    current_sector_index = self.entry_track_state_dict[entry.number].current_sector
    #print(entry.number + " " + str(current_sector_index))
    current_sector = self.track_.sectors[current_sector_index]
    current_microsector_index = self.entry_track_state_dict[entry.number].current_microsector
    current_microsector = current_sector.micro_sectors[current_microsector_index]

    if not current_sector.microsector_distance:
        added_distance = current_sector.distance
    else:
        added_distance = current_microsector.distance
    
    if not current_sector.microsector_timing:
        reference_time = current_sector.time
    else:
        reference_time = current_microsector.time

    new_added_distance = added_distance / self.options_.out_lap_mult * (step_size / reference_time)

    simulated_distance = self.entry_track_state_dict[entry.number].lap_distance
    target_distance = simulated_distance + new_added_distance
    new_sector_indices = self.track_.allSectorIndexFromDistance(target_distance)

    if new_sector_indices.sector != current_sector_index or new_sector_indices.micro_sector != current_microsector_index:
        total_speed = new_added_distance / step_size
        handleSectorJump(self, session, entry, current_sector_index, current_microsector_index, simulated_distance, total_speed, step_size)
        return
    
    print("calling recordTimeStep from calcOutLapTimeStep")
    assert new_added_distance >= 0, "NEGATIVE DISTANCE: " + str({"number": entry.number, "current_sector_index": current_sector_index, "current_microsector_index": current_microsector_index, "reference_time": reference_time, "added_distance": added_distance, "new_added_distance": new_added_distance, "step_size": step_size})
    self.entry_track_state_dict[entry.number].recordTimeStep(new_added_distance, step_size, current_sector_index, current_microsector_index)


def calcLapTimeStep(self: RaceEngine, session: SessionType, entry: RaceEntry, step_size: int = 1) -> None:
    pass # TODO: add flying lap calculations

def handleSectorJump(self: RaceEngine, session: SessionType, entry: RaceEntry, current_sector_index: int, current_microsector_index: int, simulated_distance: float, total_speed: float, step_size: int = 1) -> None:
    if current_sector_index == len(self.track_.sectors) - 1 and current_microsector_index == len(self.track_.sectors[current_sector_index].micro_sectors) - 1:
        handleLapJump(self, session, entry, current_sector_index, current_microsector_index, simulated_distance, total_speed, step_size)
        return

    print("handleSectorJump " + entry.number + " " + str(current_sector_index))
    sector_distance = self.track_.calcDistanceToSectorEnd(current_sector_index, current_microsector_index)
    
    distance_left = sector_distance - simulated_distance
    print({"distance_left": distance_left, "sector_distance": sector_distance, "simulated_distance": simulated_distance})
    achieved_time = calcSectorFinish(distance_left, total_speed)
    
    if current_microsector_index == len(self.track_.sectors[current_sector_index].micro_sectors) - 1:
        sector_time = self.entry_track_state_dict[entry.number].current_time + achieved_time - self.entry_track_state_dict[entry.number].combinedSectorTimes(current_sector_index)
        self.recordSector(entry, sector_time)
        new_current_sector_index = current_sector_index + 1
        new_current_microsector_index = 0
    else:
        new_current_sector_index = current_sector_index
        new_current_microsector_index = current_microsector_index + 1

    print("calling recordTimeStep from handleSectorJump")
    self.entry_track_state_dict[entry.number].recordTimeStep(distance_left, achieved_time, new_current_sector_index, new_current_microsector_index)

    time_left = step_size - achieved_time
    calcTimeStep(self, session, time_left)


def handleLapJump(self: RaceEngine, session: SessionType, entry: RaceEntry, current_sector_index: int, current_microsector_index: int, simulated_distance: float, total_speed: float, step_size: int = 1) -> None:
    print("handleLapJump " + entry.number + " " + str(current_sector_index))
    lap_distance = self.track_.lap_distance
    distance_left = lap_distance - simulated_distance
    achieved_time = calcSectorFinish(distance_left, total_speed)
    
    print("calling recordTimeStep from handleLapJump")
    self.entry_track_state_dict[entry.number].recordTimeStep(distance_left, achieved_time, current_sector_index, current_microsector_index)
    sector_time = self.entry_track_state_dict[entry.number].current_time + achieved_time - self.entry_track_state_dict[entry.number].combinedSectorTimes(current_sector_index)
    self.recordSector(entry, sector_time)
    #self.recordLap(entry, self.entry_track_state_dict[entry.number].current_lap)

    self.finishLap(entry, entry.getState())

    if entry.getState() == EntryState.InLap:
        self.addLogEntry(entry.drivers[entry.current_driver].name + " comes back to garage." , LogDetailLevel.high)
        entry.setState(EntryState.Garage)
        return
    if entry.getState() == EntryState.OutLap:
        #self.startNewLap(entry, EntryState.Running)
        self.startNewLap(entry, EntryState.InLap) # just for DEBUG
        self.addLogEntry(entry.drivers[entry.current_driver].name + " starts in lap." , LogDetailLevel.high)
        time_left = step_size - achieved_time
        calcTimeStep(self, session, time_left)

def calcSectorFinish(distance_left: float, total_speed: float) -> float:
    print("calcSectorFinish: " + str({"distance_left": distance_left, "total_speed": total_speed}))
    achieved_time = distance_left / total_speed
    return achieved_time
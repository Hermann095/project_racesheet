from random import randint
from ..enums.enums import EntryState, LogDetailLevel
from ..session import SessionType
from ..models.race_entry import RaceEntry
from ..race_engine import RaceEngine

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

def calcLapTimeStep(self: RaceEngine, session: SessionType, entry: RaceEntry, step_size: int = 1) -> None:
    pass
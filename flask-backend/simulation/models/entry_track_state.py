from dataclasses import dataclass
from dataclasses import field

from .lap import Lap
from .race_entry import RaceEntry
from ..enums.enums import EntryState
from .sector_time import SectorTime, SectorTimeState

@dataclass
class EntryTrackState():
    entry: RaceEntry
    current_lap : Lap
    state :EntryState = field(default=EntryState.Garage)
    lap_distance : float = field(default=0.0)
    current_time : float = field(default=0.0)
    current_sector : int = field(default=0)
    current_microsector : int = field(default=0)

    def combinedSectorTimes(self, sector_index: int) -> float:
        return sum(x.time for x in self.current_lap.sector_times[:sector_index + 1])
    
    def recordTimeStep(self, addedDistance: float, addedTime: float, newSector: int, newMicroSector: int):
        #print("recordTimeStep")
        self.current_time += addedTime
        
        """
        if newSector != self.current_sector:
            if newSector == 1:
                self.current_lap.sector_times.append(SectorTime(self.current_time))
            else: 
                old_sector_time = self.combinedSectorTimes(newSector - 1)
                new_sector_time = self.current_time - old_sector_time
                self.current_lap.sector_times.append(SectorTime(new_sector_time))
        """

        self.lap_distance = round(self.lap_distance + addedDistance, ndigits=3)
        #print({"number": self.entry.number,"addedDistance": addedDistance, "addedTime": addedTime, "newSector": newSector, "newMicroSector": newMicroSector, "current_time": self.current_time, "lap_distance": self.lap_distance }) #DEBUG
        self.current_sector = newSector
        self.current_microsector = newMicroSector
        
        
    def startNewLap(self, new_lap: Lap, state: EntryState):
        self.state = state
        self.current_lap = new_lap
        self.lap_distance = 0.0
        self.current_time = 0.0
        self.current_sector = 0
        self.current_microsector = 0

    def finishLap(self):
        self.current_lap.time = self.current_time
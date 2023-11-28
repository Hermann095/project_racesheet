from dataclasses import dataclass
from dataclasses import field

from .lap import Lap
from .race_entry import RaceEntry
from ..enums.enums import EntryState

@dataclass
class EntryTrackState():
    entry: RaceEntry
    current_lap : Lap
    state :EntryState = field(default=EntryState.Garage)
    lap_distance : float = field(default=0.0)
    current_time : float = field(default=0.0)
    current_sector : int = field(default=0)
    current_microsector : int = field(default=0)

    def recordTimeStep(self, addedDistance: float, addedTime: float, newSector: int, newMicroSector: int, currentLap: Lap):
        self.lap_distance += addedDistance
        self.current_time += addedTime
        self.current_sector = newSector
        self.current_microsector = newMicroSector
        self.current_lap = currentLap

    def startNewLap(self, new_lap: Lap, state: EntryState):
        self.state = state
        self.current_lap = new_lap
        self.lap_distance = 0.0
        self.current_time = 0.0
        self.current_sector = 0.0
        self.current_microsector = 0.0
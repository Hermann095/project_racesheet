from dataclasses import dataclass
from dataclasses import field
import simulation.driver as driver
import simulation.chassis as chassis
import simulation.engine as engine
import simulation.tyres as tyres
from .session import Lap, SectorTime
import enum

class EntryState(enum.Enum):
    Garage = enum.auto()
    OutLap = enum.auto()
    Running = enum.auto()
    InLap = enum.auto()
    PitStop = enum.auto()
    Retired = enum.auto()

    def __getstate__(self):
        return self._name_

@dataclass
class EntryTrackState():
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
        currentLap = currentLap



@dataclass(order=True)
class RaceEntry():
    sort_index: float = field(init=False)
    number :str
    team :str
    color :list[str]
    chassis :chassis.Chassis
    engine :engine.Engine
    tyres :tyres.Tyres
    state :EntryTrackState
    drivers :list[driver.Driver] = field(default_factory=list)
    current_driver: int = 0
    

    def __post_init__(self):
        self.sort_index = self.number

    def isRetired(self):
        return self.state == EntryState.Retired
    
    def setRetired(self):
        self.state = EntryState.Retired

    def recordTimeStep(self, addedDistance: float, addedTime: float, newSector: int, newMicroSector: int):
        self.state.recordTimeStep(addedDistance, addedTime, newSector, newMicroSector)

    def getState(self) -> EntryState:
        return self.state.state

    def setState(self, newState: EntryState):
        self.state.state = newState


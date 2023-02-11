from dataclasses import dataclass
from dataclasses import field
import simulation.driver as driver
import simulation.chassis as chassis
import simulation.engine as engine
import simulation.tyres as tyres
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

@dataclass(order=True)
class RaceEntry():
    sort_index: float = field(init=False)
    number :str
    team :str
    color :list[str]
    chassis :chassis.Chassis
    engine :engine.Engine
    tyres :tyres.Tyres
    drivers :list[driver.Driver] = field(default_factory=list)
    current_driver: int = 0
    state :EntryState = field(default=EntryState.Garage)

    def __post_init__(self):
        self.sort_index = self.number

    def isRetired(self):
        return self.state == EntryState.Retired
    
    def setRetired(self):
        self.state = EntryState.Retired
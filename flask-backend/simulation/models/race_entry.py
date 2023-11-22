from dataclasses import dataclass
from dataclasses import field
from .driver import Driver
from .chassis import Chassis
from .engine import Engine
from .tyres import Tyres
from ..enums.enums import EntryState


@dataclass(order=True)
class RaceEntry():
    sort_index: float = field(init=False)
    number :str
    team :str
    color :list[str]
    chassis :Chassis
    engine :Engine
    tyres :Tyres
    state :EntryState
    drivers :list[Driver] = field(default_factory=list)
    current_driver: int = 0
    

    def __post_init__(self):
        self.sort_index = self.number

    def isRetired(self):
        return self.state == EntryState.Retired
    
    def setRetired(self):
        self.state = EntryState.Retired

    """
    def recordTimeStep(self, addedDistance: float, addedTime: float, newSector: int, newMicroSector: int):
        self.state.recordTimeStep(addedDistance, addedTime, newSector, newMicroSector)
    """

    def getState(self) -> EntryState:
        return self.state

    def setState(self, newState: EntryState):
        self.state = newState


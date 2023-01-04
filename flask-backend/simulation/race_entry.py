from dataclasses import dataclass
from dataclasses import field
import simulation.driver as driver
import simulation.chassis as chassis
import simulation.engine as engine
import simulation.tyres as tyres

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

    def __post_init__(self):
        self.sort_index = self.number
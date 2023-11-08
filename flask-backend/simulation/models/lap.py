from dataclasses import dataclass, field
#from .race_entry import RaceEntry
from ..utils import FLOAT_MAX, secToTimeStr
from .sector_time import SectorTime

@dataclass(order=True)
class Lap():
  sort_index: float = field(init=False)
  #entry :RaceEntry
  time :float = field(default=FLOAT_MAX)
  sector_times :list[SectorTime] = field(default_factory=list)

  def __post_init__(self):
    self.sort_index = self.time

  def __getstate__(self):
    return {
      "time": secToTimeStr(self.time),
      "sector_times": self.sector_times
    }
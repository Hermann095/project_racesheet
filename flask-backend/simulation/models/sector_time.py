from dataclasses import dataclass, field
from ..utils import FLOAT_MAX, secToTimeStr
from ..enums.enums import SectorTimeState

@dataclass
class SectorTime():
  time: float = field(default=FLOAT_MAX)
  state: SectorTimeState = field(default=SectorTimeState.green)

  def __getstate__(self):
    return {
      "time": secToTimeStr(self.time),
      "state": self.state
    }
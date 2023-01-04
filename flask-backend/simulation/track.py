from dataclasses import dataclass
from dataclasses import field


@dataclass
class MicroSector():
  low_speed_corners: int
  high_speed_corners: int
  acceleration: int
  top_speed: int
  overtake_difficulty :int
  time :float = 0.0
  name :str = ""


@dataclass
class Sector():
  time :float
  microsector_timing: bool = False
  micro_sectors :list[MicroSector] = field(default_factory=list)


@dataclass
class Track():
  name :str
  nation :str
  qualy_spread :int
  race_spread :int
  sectors :list[Sector] = field(default_factory=list)

  def lap_time(self) -> float:
    lap_total = 0
    for sector in self.sectors:
      if not sector.microsector_timing:
        lap_total += sector.time
      else:
        for micro_sector in sector.micro_sectors:
          lap_total += micro_sector.time
    return lap_total
from dataclasses import dataclass
from dataclasses import field
from collections import namedtuple


@dataclass
class MicroSector():
  low_speed_corners: int
  high_speed_corners: int
  acceleration: int
  top_speed: int
  overtake_difficulty :int
  time :float = 0.0 # in s
  distance: float = 0.0 # in m
  name :str = ""


@dataclass
class Sector():
  time :float # in s
  distance: float # in m
  microsector_timing: bool = False
  microsector_distance: bool = False
  micro_sectors :list[MicroSector] = field(default_factory=list)


@dataclass
class Track():
  name :str
  nation :str
  qualy_spread :int
  race_spread :int
  sectors :list[Sector] = field(default_factory=list)
  lap_time : float = field(init=False)
  lap_distance : float = field(init=False)
  

  def __post_init__(self):
    self.lap_time = self.calcLapTime()
    self.lap_distance = self.calcLapDistance()

  def calcLapTime(self) -> float:
    lap_total = 0
    for sector in self.sectors:
      if not sector.microsector_timing:
        lap_total += sector.time
      else:
        for micro_sector in sector.micro_sectors:
          lap_total += micro_sector.time
    return lap_total

  def calcLapDistance(self) -> float:
    return self.calcDistanceToSectorStart(self, len(self.sectors) - 1)

  def calcDistanceToSectorStart(self, sector_index: int) -> float:
    distance_total = 0.0
    for sector in self.sectors[:(sector_index + 1)]:
      if not sector.microsector_distance:
        distance_total += sector.distance
      else:
        for micro_sector in sector.micro_sectors:
          distance_total += micro_sector.distance
    return distance_total

  def sectorIndexFromDistance(self, distance: float) -> int:
    index = 0
    checked_distance = 0

    if distance == 0.0:
      return index
    
    if distance >= self.lap_distance:
      distance -= self.lap_distance
    
    while checked_distance <= distance:
      checked_distance += self.sectors[index].distance
      if distance <= checked_distance:
        return index
      else: 
        index += 1

    return index


  def allSectorIndexFromDistance(self, distance: float):
    sector_index = self.sectorIndexFromDistance(distance)

    micro_sector_index = 0
    start_distance = distance - self.calcDistanceToSectorStart(sector_index)

    micro_sector_distance = 0
    if not self.sectors[sector_index].microsector_distance:
      micro_sector_distance = self.sectors[sector_index].distance / len(self.sectors[sector_index].micro_sectors)

    checked_distance = start_distance

    for micro_sector in self.sectors[sector_index].micro_sectors:
      if self.sectors[sector_index].microsector_distance:
        micro_sector_distance = micro_sector.distance
      checked_distance += micro_sector_distance

      if distance < checked_distance:
        break
      else:
        micro_sector_index += 1
      

    Sector_indices = namedtuple("sector_indices", ["sector", "micro_sector"])
    return Sector_indices(sector_index, micro_sector_index)


    
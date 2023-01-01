from dataclasses import dataclass
import simulation.utils as utils

@dataclass
class Driver():
    name :str
    nation :str
    team :str
    race_speed :int
    qualy_speed :int
    wet_skill :int
    consistency :int
    error_prone :int

    def __getstate__(self):
        return {
        "name": self.name,
        "nation": utils.nationCodeToFlag(self.nation),
        "team": self.team,
        "race_speed": self.race_speed,
        "qualy_speed": self.qualy_speed,
        "wet_skill": self.wet_skill,
        "consistency": self.consistency,
        "error_prone": self.error_prone
        }

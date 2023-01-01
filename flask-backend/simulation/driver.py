from dataclasses import dataclass

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

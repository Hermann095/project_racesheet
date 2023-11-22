from dataclasses import dataclass

@dataclass
class Engine():
    name :str
    race_power :int
    qualy_power :int
    race_acceleration :int
    qualy_acceleration :int
    reliability :int
    weight :int
    driveablity :int

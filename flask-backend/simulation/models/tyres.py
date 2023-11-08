from dataclasses import dataclass

@dataclass
class Tyres():
    name :str
    race_grip :int
    qualy_grip :int
    wet_grip :int
    intermediate_grip :int
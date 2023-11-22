from dataclasses import dataclass

@dataclass
class Chassis():
    name :str
    team :str
    grip_low_speed_ :int
    grip_high_speed_ :int
    drag_ :int
    reliability_ :int
    weight_ :float
    driveablity_ :int

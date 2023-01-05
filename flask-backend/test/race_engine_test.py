import pytest

from simulation.tyres import Tyres
from simulation.driver import Driver
from simulation.engine import Engine
from simulation.chassis import Chassis
from simulation.race_entry import RaceEntry

from simulation.race_engine import RaceEngine
from simulation.session import LogEntry, LogEventType, LogDetailLevel
from simulation.track import Track, Sector, MicroSector

@pytest.fixture
def log_entry():
    return LogEntry("Test Entry", LogDetailLevel.high, LogEventType.mistake)

@pytest.fixture
def log_entry2():
    return LogEntry("Test Entry", LogDetailLevel.low, LogEventType.default)

@pytest.fixture
def get_track():
    return Track("Test Track", "AUT", 1, 1, [Sector(90, True, 
        [MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 1"), MicroSector(5, 5, 5, 5, 5, 15)]), 
        Sector(30, False, [MicroSector(5, 5, 5, 5, 5, 30, "Micro_Sector 3"), MicroSector(5, 5, 5, 5, 5, 30)]), 
        Sector(90, True, [MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 5"), MicroSector(5, 5, 5, 5, 5, 15, "Micro_Sector 6")])])

@pytest.fixture
def get_entry_list():
    entry_a = RaceEntry("13", "Team A", ["#000000"], Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("Heinz-Harald Frentzen", "GER", "Team A", 500, 500, 500, 500, 500)])
    entry_a2 = RaceEntry("46", "Team A", ["#f50537", "#666666"], Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("a2", "FIN", "Team A", 500, 500, 500, 500, 500)])
    entry_b = RaceEntry("95", "Team B", ["#F5A114"], Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B", "BRA", "Team B", 1000, 1000, 1000, 1000, 1000)])
    return [entry_a, entry_a2, entry_b]


def test_add_log(log_entry, get_track, get_entry_list):
    engine =  RaceEngine(get_track, get_entry_list)
    engine.addLogEntry("Test Entry", LogDetailLevel.high, LogEventType.mistake)
    assert engine.log == [log_entry]

def test_add_log2(log_entry, get_track, get_entry_list, log_entry2):
    engine =  RaceEngine(get_track, get_entry_list)
    engine.addLogEntry("Test Entry", LogDetailLevel.high, LogEventType.mistake)
    engine.addLogEntry("Test Entry")
    assert engine.log == [log_entry, log_entry2]

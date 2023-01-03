from .chassis import Chassis
from .driver import Driver
from .engine import Engine
import simulation.race_manager as race_manager
from .session import SessionType, SessionResult
from .track import Track
from .race_entry import RaceEntry
from .tyres import Tyres
import simulation.utils as utils
import jsonpickle


def runTestQualifying(printResults: bool, socket):
    rm = race_manager.RaceManager()
    entry_a = RaceEntry("13", "Team A", "#000000", Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("Heinz-Harald Frentzen", "GER", "Team A", 500, 500, 500, 500, 500)])
    entry_a2 = RaceEntry("46", "Team A", "#5313EB", Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("a2", "FIN", "Team A", 500, 500, 500, 500, 500)])
    entry_b = RaceEntry("95", "Team B", "#F5A114", Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B", "BRA", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_b2 = RaceEntry("96", "Team B", "#1DDEA4", Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B2", "AUT", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_c = RaceEntry("1", "Team C", "#EBDD13", Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("c", "USSR", "Team A", 100, 100, 100, 100, 100)])
    entry_c2 = RaceEntry("2", "Team C", "#8b0000", Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("c2", "USA", "Team A", 100, 100, 100, 100, 100)])
    entry_list = [entry_a, entry_a2, entry_b, entry_b2, entry_c, entry_c2]
    rm.setEntryList(entry_list)
    result = rm.startSession(SessionType.Qualifying, socket)
    if printResults:
        result.printLog()
        result.printResults()
    return buildResults(result)

def startTestQualifying(printResults: bool):
    rm = race_manager.RaceManager()
    entry_a = RaceEntry("13", "Team A", "#000000", Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("Heinz-Harald Frentzen", "GER", "Team A", 500, 500, 500, 500, 500)])
    entry_a2 = RaceEntry("46", "Team A", "#5313EB", Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("a2", "FIN", "Team A", 500, 500, 500, 500, 500)])
    entry_b = RaceEntry("95", "Team B", "#F5A114", Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B", "BRA", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_b2 = RaceEntry("96", "Team B", "#1DDEA4", Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B2", "AUT", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_c = RaceEntry("1", "Team C", "#EBDD13", Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("c", "USSR", "Team A", 100, 100, 100, 100, 100)])
    entry_c2 = RaceEntry("2", "Team C", "#8b0000", Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("c2", "USA", "Team A", 100, 100, 100, 100, 100)])
    entry_list = [entry_a, entry_a2, entry_b, entry_b2, entry_c, entry_c2]
    rm.setEntryList(entry_list)
    result = rm.startSession(SessionType.Qualifying)
    if printResults:
        result.printLog()
        result.printResults()
    return buildResults(result)

def pauseTestQualifying():
    return
    

def buildResults(result: SessionResult):
    return jsonpickle.encode(result, unpicklable=False)



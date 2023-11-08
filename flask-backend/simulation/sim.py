from .models.chassis import Chassis
from .models.driver import Driver
from .models.engine import Engine
import simulation.race_manager as race_manager
from .session import SessionType, SessionResult
from .models.race_entry import RaceEntry
from .models.tyres import Tyres
from .enums.enums import SimulationState
import jsonpickle
import numbers

from flask_socketio import SocketIO


state = SimulationState.Running
simSpeed = 1

def startTestQualifying(printResults: bool, socket: SocketIO, baseSimSpeed: float = 1.0):
    
    global simSpeed
    global state
    simSpeed = baseSimSpeed
    state = SimulationState.Running
    
    @socket.on("pause_qualifying")
    def pause_qualifying():
        print("recieved pause_qualifying")
        global state
        state = SimulationState.Paused

    @socket.on("resume_qualifying")
    def resume_qualifying(json):
        print("recieved resume_qualifying with " + str(json))

        global state
        if state == SimulationState.Cancelled:
            print("session was already cancelled")
            return

        global simSpeed
        if "simSpeed" in json:
            newSimSpeed = json["simSpeed"]
            if isinstance(newSimSpeed, numbers.Number):
                simSpeed = newSimSpeed

        state = SimulationState.Running

    @socket.on("cancel_qualifying")
    def cancel_qualifying():
        print("recieved cancel_qualifying")
        global state
        state = SimulationState.Cancelled
    
    def getState() -> SimulationState:
        global state
        return state

    def getSimSpeed() -> float:
        global simSpeed
        return simSpeed


    rm = race_manager.RaceManager()
    entry_a = RaceEntry("13", "Team A", ["#000000"], Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("Heinz-Harald Frentzen", "GER", "Team A", 500, 500, 500, 500, 500)])
    entry_a2 = RaceEntry("46", "Team A", ["#f50537", "#666666"], Chassis("Chassis A", "Team A", 500, 500, 500, 500, 350, 500), Engine("Engine A", 500, 500, 500, 500, 500, 155, 500), Tyres("Tyre A", 500, 500, 500, 500), [Driver("a2", "FIN", "Team A", 500, 500, 500, 500, 500)])
    entry_b = RaceEntry("95", "Team B", ["#F5A114"], Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B", "BRA", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_b2 = RaceEntry("96", "Team B", ["#1DDEA4", "#000000"], Chassis("Chassis B", "Team B", 1000, 1000, 100, 1000, 350, 1000), Engine("Engine B", 1000, 1000, 1000, 1000, 1000, 155, 1000), Tyres("Tyre B", 1000, 1000, 1000, 1000), [Driver("B2", "AUT", "Team B", 1000, 1000, 1000, 1000, 1000)])
    entry_c = RaceEntry("1", "Team C", ["#81C4FF", "#16588E", "#E7222E"], Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("Thomas Pitt Cholmondeley-Tapper", "NZL", "Team A", 100, 100, 100, 100, 100)])
    entry_c2 = RaceEntry("2", "Team C", ["#8b0000"], Chassis("Chassis C", "Team C", 100, 100, 1000, 100, 350, 100), Engine("Engine A", 100, 100, 100, 100, 100, 155, 100), Tyres("Tyre A", 100, 100, 100, 100), [Driver("c2", "USA", "Team A", 100, 100, 100, 100, 100)])
    entry_list = [entry_a, entry_a2, entry_b, entry_b2, entry_c, entry_c2]
    rm.setEntryList(entry_list)
    result = rm.startSession(SessionType.Qualifying, socket, getState, getSimSpeed)
    if printResults:
        result.printLog()
        result.printResults()
    socket.emit("finished_qualifying")
    return buildResults(result)
    

def buildResults(result: SessionResult):
    return jsonpickle.encode(result, unpicklable=False)

def disconnectionHandler():
    print("called disconnectionHandler")
    global state
    state = SimulationState.Cancelled



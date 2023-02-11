import { DriverResults, Entry, SessionResults } from "../types/types";


export function convertSessionResultsToDriverResults(data: SessionResults) {
    let results: DriverResults = {drivers: []};
    results.drivers = data?.entries.map((entry: Entry, index: number) => {
      let driver = entry.drivers[0];
      let time = data.time[index]
      let gap = data.gap[index]
      let fastest_lap_object = data.fastest_lap[entry.number]
      let fastest_lap = {time: fastest_lap_object.time, sector_times: fastest_lap_object.sector_times}
      let sectors = data.fastest_lap[entry.number].sector_times
      let laps = data.lap_times[entry.number].length.toString()
      let state = entry.state
      
      return {name: driver.name, nationality: driver.nation, number: entry.number, team: entry.team, laps: laps, color: entry.color, sectors: sectors, time: time, gap: gap, fastestLap: fastest_lap, state: state};
    })

    let best_lap = {time: data?.best_sectors.time, sector_times: data?.best_sectors.sector_times};
    results.bestLap = best_lap;
    
    return results
  }
import { DriverResults, Entry, SessionResults } from '../types/types'

export function convertSessionResultsToDriverResults(data: SessionResults) {
  const results: DriverResults = { drivers: [] }
  results.drivers = data?.entries.map((entry: Entry, index: number) => {
    const driver = entry.drivers[0]
    const time = data.time[index]
    const gap = data.gap[index]
    const fastest_lap_object = data.fastest_lap[entry.number]
    const fastest_lap = {
      time: fastest_lap_object.time,
      sector_times: fastest_lap_object.sector_times
    }
    const sectors = data.fastest_lap[entry.number].sector_times
    const laps = data.lap_times[entry.number].length.toString()
    const state = entry.state

    return {
      name: driver.name,
      nationality: driver.nation,
      number: entry.number,
      team: entry.team,
      laps: laps,
      color: entry.color,
      sectors: sectors,
      time: time,
      gap: gap,
      fastestLap: fastest_lap,
      state: state
    }
  })

  const best_lap = {
    time: data?.best_sectors.time,
    sector_times: data?.best_sectors.sector_times
  }
  results.bestLap = best_lap

  return results
}

export interface DriverResults {
  drivers: Array<{
    name: string
    nationality: string
    number: string
    team: string
    laps: string
    color: string[]
    sectors: Sector[]
    time: string
    gap: string
    fastestLap?: Lap
    state: EntryState
  }>
  bestLap?: Lap
}

export interface ResultsTableProbs extends React.HTMLProps<HTMLBaseElement> {
  Results: DriverResults
  showSectorBars: boolean
  showEntryIcons: boolean
  showTheoreticalBest: boolean
  carsetName: string
}

export interface ResultsTableSectorsProbs
  extends React.HTMLProps<HTMLBaseElement> {
  sectors?: Sector[]
  bestLap?: Lap
  showSectorBars?: boolean
}

export interface EventLogProbs extends React.HTMLProps<HTMLBaseElement> {
  events: LogItem[]
}

export interface SessionResults {
  session: string
  track_name: string
  entries: Entry[]
  time: string[]
  gap: string[]
  notes: any[]
  lap_times: { [key: string]: Lap[] }
  fastest_lap: { [key: string]: Lap }
  position_chart: any[]
  log: LogItem[]
  leader_time: string
  best_sectors: Lap
  personal_best: { [key: string]: Lap }
  current_tick: number
  total_ticks: number
}

export interface Lap {
  time: string
  sector_times: Sector[]
}

export interface Sector {
  time: string
  state: State
}

export enum State {
  Green = 'green',
  Yellow = 'yellow',
  Purple = 'purple',
  White = 'white'
}

export enum EntryState {
  Garage = 'garage',
  OutLap = 'outlap',
  Running = 'running',
  InLap = 'inlap',
  PitStop = 'pitstop',
  Retired = 'retired'
}

export interface Entry {
  number: string
  team: string
  color: string[]
  chassis: Chassis
  engine: Engine
  tyres: Tyres
  drivers: Driver[]
  current_driver: number
  sort_index: string
  state: EntryState
}

export interface Chassis {
  name: string
  team: string
  grip_low_speed_: number
  grip_high_speed_: number
  drag_: number
  reliability_: number
  weight_: number
  driveablity_: number
}

export interface Driver {
  name: string
  nation: string
  team: string
  race_speed: number
  qualy_speed: number
  wet_skill: number
  consistency: number
  error_prone: number
}

export interface Engine {
  name: string
  race_power: number
  qualy_power: number
  race_acceleration: number
  qualy_acceleration: number
  reliability: number
  weight: number
  driveablity: number
}

export interface Tyres {
  name: string
  race_grip: number
  qualy_grip: number
  wet_grip: number
  intermediate_grip: number
}

export interface LogItem {
  text: string
  detailLevel: LogDetailLevel
  type: LogType
}

export enum LogDetailLevel {
  High = 'high',
  Low = 'low',
  Medium = 'medium'
}

export enum LogType {
  Default = 'default',
  Mistake = 'mistake',
  PersonalBest = 'personalBest',
  FastestLap = 'fastestLap',
  PurpleSector = 'purpleSector',
  RedFlag = 'redFlag',
  YellowFlag = 'yellowFlag',
  NewLeader = 'newLeader',
  Retirement = 'retirement',
  Crash = 'crash'
}

export enum SimState {
  Cancelled = 'Cancelled',
  Finished = 'Finished',
  Paused = 'Paused',
  Running = 'Running',
  Ready = 'Ready'
}

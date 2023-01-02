
export interface BestLap {
    time: string,
    sector_times: Array<string>
}

export interface DriverResults {
    drivers: Array<{
        name: string,
        nationality: string,
        team: string,
        sectors: Array<string>,
        time: string,
        gap: string,
        fastestLap?: BestLap
    }>
    bestLap?: BestLap
}

export interface ResultsTableProbs extends React.HTMLProps<HTMLBaseElement> {
    Results: DriverResults
}

export interface EventLogItem {
    text: string,
    detailLevel: string,
    type: string
}

export interface EventLogProbs extends React.HTMLProps<HTMLBaseElement> {
    events: Array<EventLogItem>
}



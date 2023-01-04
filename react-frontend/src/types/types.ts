
export interface BestLap {
    time: string,
    sector_times: Array<Sector>
}

export interface Sector {
    time: string,
    state: string
}

export interface DriverResults {
    drivers: Array<{
        name: string,
        nationality: string,
        number: string,
        team: string,
        sectors: Array<Sector>,
        time: string,
        gap: string,
        fastestLap?: BestLap
    }>
    bestLap?: BestLap
}

export interface ResultsTableProbs extends React.HTMLProps<HTMLBaseElement> {
    Results: DriverResults,
    showSectorBars: boolean,
    showEntryIcons: boolean,
    showTheoreticalBest: boolean,
    carsetName: string
}

export interface EventLogItem {
    text: string,
    detailLevel: string,
    type: string
}

export interface EventLogProbs extends React.HTMLProps<HTMLBaseElement> {
    events: Array<EventLogItem>
}



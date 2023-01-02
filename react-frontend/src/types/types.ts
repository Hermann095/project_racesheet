
export interface BestLap {
    time: string,
    sector_times: Array<string>
}

export interface DriverResults {
    drivers: Array<{
        name: string,
        nationality: string,
        number: string,
        team: string,
        sectors: Array<string>,
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



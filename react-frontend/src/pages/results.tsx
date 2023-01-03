import * as React from "react"
import { useEffect, useState } from "react";

import Container from '@mui/material/Container';

import { DriverResults } from '../types/types';
import ResultsTable from "../components/ResultsTable/ResultsTable";
import EventLog from "../components/EventLog/EventLog";
import { Button, FormControlLabel, FormGroup, Grid, Switch } from "@mui/material";


export default function ResultsPage(props: any) {

    //const socket = props.socketInstance;

    const [fetchedData, setFetchedData] = useState<any>(null);
    const [resultData, setResultData] = useState<DriverResults>({drivers: []});

    const [carsetName, setCarsetName] = useState("");

    const [showSectorBars, setShowSectorBars] = useState(false);
    const [showEntryIcons, setShowEntryIcons] = useState(false);
    const [showTheoreticalBest, setShowTheoreticalBest] = useState(false);

    useEffect(() => {
      fetch("http://localhost:5000/carset").then(res => res.json()).then(data => {
        setCarsetName(data.name)
      });
    }, []);

    function runQualifying() {
      fetch("http://localhost:5000/qualifying").then(res => res.json()).then(data => {
        setFetchedData(data);
        fillDriverArray(data);
      });
      props.onRunQualifying({greeting: "hello", data: "some data from qualifying front end", printResults: false});
    }

    function fillDriverArray(data: any) {
      let results: DriverResults = {drivers: []};
      results.drivers = data?.entries.map((entry: any, index: any) => {
        let driver = entry.drivers[0];
        let time = data.time[index]
        let gap = data.gap[index]
        let personal_best_object = data.personal_best[entry.number]
        let personal_best = {time: personal_best_object.time, sector_times: personal_best_object.sector_times}
        let sectors = data.fastest_lap[entry.number].sector_times
        
        return {name: driver.name, nationality: driver.nation, number: entry.number, team: entry.team, sectors: sectors, time: time, gap: gap, fastestLap: personal_best};
      })

      let best_lap = {time: data?.best_sectors.time, sector_times: data?.best_sectors.sector_times};
      results.bestLap = best_lap;
      setResultData(results);
    }
    
    function handleSectorBarChange(event: any, checked: boolean) {
      setShowSectorBars(checked)
    }

    function handleEntryIconChange(event: any, checked: boolean) {
      setShowEntryIcons(checked)
    }

    function handleTheoreticalBest(event: any, checked: boolean) {
      setShowTheoreticalBest(checked)
    }

    return (
        <>
        <Container>
            <Grid container>
              <Grid xs={6}>
                <h1>{fetchedData?.session} Results</h1>
              </Grid>
              <Grid xs={6} display={"flex"} alignItems={"center"} justifyContent={"end"}>
                  <FormGroup>
                    <FormControlLabel control={<Switch defaultChecked={showTheoreticalBest} onChange={handleTheoreticalBest}/>} label="Theoretical Best" />
                  </FormGroup>
                  <FormGroup>
                    <FormControlLabel control={<Switch defaultChecked={showEntryIcons} onChange={handleEntryIconChange}/>} label="Entry Icons" />
                  </FormGroup>
                  <FormGroup>
                    <FormControlLabel control={<Switch defaultChecked={showSectorBars} onChange={handleSectorBarChange}/>} label="Sector Bars" />
                  </FormGroup>
                  <Button variant="contained" onClick={runQualifying}>Run Qualifying</Button>
              </Grid>
            </Grid>
            <ResultsTable carsetName={carsetName} Results={resultData} showSectorBars={showSectorBars} showEntryIcons={showEntryIcons} showTheoreticalBest={showTheoreticalBest}></ResultsTable>
            <EventLog events={fetchedData?.log}></EventLog>
        </Container>
        </>
    );
}


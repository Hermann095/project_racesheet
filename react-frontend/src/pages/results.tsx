import * as React from "react"
import { useState } from "react";

import Container from '@mui/material/Container';

import { DriverResults } from '../types/types';
import ResultsTable from "../components/ResultsTable/ResultsTable";
import EventLog from "../components/EventLog/EventLog";
import { Button, Grid } from "@mui/material";


export default function ResultsPage() {

    const [fetchedData, setFetchedData] = useState<any>(null);
    const [resultData, setResultData] = useState<DriverResults>({drivers: []});

    /*useEffect(() => {
      fetch("http://localhost:5000/drivers").then(res => res.json()).then(data => {
        setFetchedData(data.drivers);
      });
    }, []);

    useEffect(() => {
      fillDriverArray()
    }, [fetchedData])

    function fillDriverArray() {
      let results: DriverResults = {drivers: []};
      fetchedData?.map((driver: any) => {
        results.drivers.push({name: driver.name, nationality: driver.nationality, team: "", time: "", gap: ""});
      })
      console.log(results);
      setResultData(results);
    }*/

    function runQualifying() {
      fetch("http://localhost:5000/qualifying").then(res => res.json()).then(data => {
        setFetchedData(data);
        fillDriverArray(data);
      });
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
        
        return {name: driver.name, nationality: driver.nation, team: entry.team, sectors: sectors, time: time, gap: gap, fastestLap: personal_best};
      })

      let best_lap = {time: data?.best_sectors.time, sector_times: data?.best_sectors.sector_times};
      results.bestLap = best_lap;
      setResultData(results);
    }
    

    return (
        <>
        <Container>
            <Grid container>
              <Grid xs={8}>
                <h1>{fetchedData?.session} Results</h1>
              </Grid>
              <Grid xs={4} display={"flex"} alignItems={"center"} justifyContent={"end"}>
                  <Button variant="contained" onClick={runQualifying}>Run Qualifying</Button>
              </Grid>
            </Grid>
            <ResultsTable Results={resultData}></ResultsTable>
            <EventLog events={fetchedData?.log}></EventLog>
        </Container>
        </>
    );
}

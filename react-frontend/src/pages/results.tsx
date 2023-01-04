import * as React from "react"
import { useEffect, useState } from "react";
import io, { Socket } from "socket.io-client";

import Container from '@mui/material/Container';

import { DriverResults } from '../types/types';
import ResultsTable from "../components/ResultsTable/ResultsTable";
import EventLog from "../components/EventLog/EventLog";
import { Button, FormControlLabel, FormGroup, Grid, Stack, Switch } from "@mui/material";



export default function ResultsPage(props: any) {

    const [socketInstance, setSocketInstance] = useState<Socket>();

    const [fetchedData, setFetchedData] = useState<any>(null);
    const [resultData, setResultData] = useState<DriverResults>({drivers: []});

    const [carsetName, setCarsetName] = useState("");

    const [showSectorBars, setShowSectorBars] = useState(false);
    const [showEntryIcons, setShowEntryIcons] = useState(false);
    const [showTheoreticalBest, setShowTheoreticalBest] = useState(false);

    const [isPaused, setIsPaused] = useState(false);

    useEffect(() => {
  
      const socket = io("localhost:5000/", {
        transports: ["websocket"],
      });

      setSocketInstance(socket);

      socket.on("connect", () => {
        console.log("connected");
      });
  
      socket.on("disconnect", () => {
        console.log("disconnected");
      });
  
      socket?.on("update_qualifying_results", (data: any) => {
        console.log("recived data from update_qualifying_results");
        let jsonData = JSON.parse(data)
        console.log(jsonData);
        setFetchedData(jsonData);
        fillDriverArray(jsonData);
      })
  
      return function cleanup() {
        socket.offAny();
        socket.disconnect();
      }
    }, []);

    useEffect(() => {
      fetch("http://localhost:5000/carset").then(res => res.json()).then(data => {
        setCarsetName(data.name)
      });
    }, []);

    function runQualifying() {
      /*fetch("http://localhost:5000/qualifying").then(res => res.json()).then(data => {
        setFetchedData(data);
        fillDriverArray(data);
      });*/
      setIsPaused(false)
      if (isPaused) {
        socketInstance?.emit("resume_qualifying");
      } else {
        socketInstance?.emit("run_qualifying", {printResults: false});
      }
    }

    function pauseQualifying() {
      setIsPaused(true);
      socketInstance?.emit("pause_qualifying");
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
                  <Stack>
                    <Button variant="contained" onClick={runQualifying}>Start Qualifying</Button>
                    <Button variant="contained" onClick={pauseQualifying}>Pause Qualifying</Button>
                  </Stack>
              </Grid>
            </Grid>
            <ResultsTable carsetName={carsetName} Results={resultData} showSectorBars={showSectorBars} showEntryIcons={showEntryIcons} showTheoreticalBest={showTheoreticalBest}></ResultsTable>
            <EventLog events={fetchedData?.log}></EventLog>
        </Container>
        </>
    );
}


import * as React from "react"
import { useEffect, useState } from "react";
import io, { Socket } from "socket.io-client";

import Container from '@mui/material/Container';

import { DriverResults, SimState } from '../types/types';
import ResultsTable from "../components/ResultsTable/ResultsTable";
import EventLog from "../components/EventLog/EventLog";
import { Button, CircularProgress, FormControlLabel, FormGroup, Grid, Stack, Switch, FormControl, FormLabel, Slider } from "@mui/material";
import { convertSessionResultsToDriverResults } from "../utils/utils";



export default function ResultsPage(props: any) {

    const [socketInstance, setSocketInstance] = useState<Socket>();

    const [fetchedData, setFetchedData] = useState<any>(null);
    const [resultData, setResultData] = useState<DriverResults>({drivers: []});

    const [carsetName, setCarsetName] = useState("");

    const [showSectorBars, setShowSectorBars] = useState(false);
    const [showEntryIcons, setShowEntryIcons] = useState(false);
    const [showTheoreticalBest, setShowTheoreticalBest] = useState(false);

    const [isPaused, setIsPaused] = useState(false);
    const [simState, setSimState] = useState(SimState.Ready);

    const [simSpeed, setSimSpeed] = useState(1);

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

      socket.on("cancelled_qualifying", () => {
        console.log("cancelled_qualifying");
        setSimState(SimState.Cancelled);
      });

      socket.on("finished_qualifying", () => {
        console.log("finished_qualifying");
        setSimState(SimState.Finished);
      });

      socket.on("paused_qualifying", () => {
        console.log("paused_qualifying");
        setSimState(SimState.Paused);
      });
  
      socket?.on("update_qualifying_results", (data: any) => {
        console.log("recived data from update_qualifying_results");
        setSimState(SimState.Running);
        let jsonData = JSON.parse(data)
        console.log(jsonData);
        setFetchedData(jsonData);
        let results = convertSessionResultsToDriverResults(jsonData)
        setResultData(results);
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

    useEffect(() => {
      if (simState === SimState.Running) {
        socketInstance?.emit("resume_qualifying", {simSpeed: simSpeed});
      }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [simSpeed]);

    function runQualifying() {
      setIsPaused(false)
      if (isPaused) {
        socketInstance?.emit("resume_qualifying", {simSpeed: simSpeed});
      } else {
        socketInstance?.emit("run_qualifying", {printResults: false, simSpeed: simSpeed});
      }
    }

    function pauseQualifying() {
      setIsPaused(true);
      socketInstance?.emit("pause_qualifying");
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

    const simSpeedMarks = [
      {
        value: 0,
        label: 'Very Slow',
        speed: 3,
      },
      {
        value: 25,
        label: 'Slow',
        speed: 2,
      },
      {
        value: 50,
        label: 'Standard',
        speed: 1,
      },
      {
        value: 75,
        label: 'Fast',
        speed: 0.5,
      },
      {
        value: 100,
        label: 'Very Fast',
        speed: 0.1,
      },
    ];

    const handleSimSpeedChange = (event: any, value: any) => {
      let index = simSpeedMarks.findIndex((mark) => mark.value === value);
      setSimSpeed(simSpeedMarks[index].speed)
    };

    function valueSimSpeedLabelFormat(value: number) {
      let index = simSpeedMarks.findIndex((mark) => mark.value === value);
      return simSpeedMarks[index].label;
    }

    return (
        <>
        <Container>
            <Grid container>
              <Grid xs={6}>
                <Stack>
                  <h1>{fetchedData?.session} Results</h1>
                  <Grid container display={"flex"} alignItems={"center"} columnSpacing={2}>
                    <Grid item>
                    <h3>{simState}</h3>
                    </Grid>
                    <Grid item>
                    <CircularProgress variant="determinate"
                      value={simState === "Finished" ? 100 : simState === "Ready" ? 0 : fetchedData?.current_tick / fetchedData?.total_ticks * 100} />
                    </Grid>
                    <Grid item>
                      <FormControl>
                      <FormLabel sx={{display: 'inline'}}>Sim Speed</FormLabel>
                      <Slider 
                        defaultValue={50}
                        valueLabelFormat={valueSimSpeedLabelFormat}
                        valueLabelDisplay='auto'
                        marks
                        step={25}
                        min={0}
                        max={100}
                        onChange={handleSimSpeedChange}
                        />
                      </FormControl>
                    </Grid>
                  </Grid>
                </Stack>
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


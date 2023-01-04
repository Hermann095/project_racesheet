import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import { ResultsTableProbs } from '../../types/types';
import "../ResultsTable/ResultsTable.scss"
import { TableFooter } from '@mui/material';

export default function ResultsTable(props: ResultsTableProbs) {

  //const [showSectorBars, setShowSectorBars] = React.useState(true);
  
  let showSectorBars = props.showSectorBars;
  let showEntryIcons = props.showEntryIcons;
  let showTheoreticalBest = props.showTheoreticalBest;
  let Results = props.Results;
  let numSectors = 0
  if (Results !== undefined) {
    numSectors = Number(Results?.bestLap?.sector_times.length);
  }
  //console.log(Results);

  //file:///C:/Users/tomi_/Desktop/alternate_f1/project_racesheet_flask_react/project_racesheet/carsets/test123/

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell align="center">Pos</TableCell>
            {showEntryIcons ? <TableCell></TableCell> : <TableCell align="center">Number</TableCell>}
            <TableCell align="center"></TableCell>
            <TableCell>Name</TableCell>
            <TableCell align="center">Nationality</TableCell>
            <TableCell align="center">Team</TableCell>
            <TableCell align="center">Laps</TableCell>
            {showSectorBars ? 
              <TableCell align='center'>Sectors</TableCell>
            : Results.drivers[0]?.sectors.map((sector, index) => (
                <TableCell align='center'>Sector {index+1}</TableCell>
            ))}
            <TableCell align="center">Time</TableCell>
            <TableCell align="center">Gap</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Results.drivers?.map((row, index) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align='center'>{index+1}</TableCell>
              {showEntryIcons ? 
                <TableCell align="center"><img className='entry-icon' src={"/images/carsets/" + props.carsetName + "/entry_icons/" + row?.number + ".png"} alt=""></img></TableCell> 
                : <TableCell align="center">{row?.number}</TableCell>}
              <TableCell align='center'>
                <div style={{"--num-colors": row.color.length.toString()} as React.CSSProperties} className="color-cell-container">
                  {row.color.map((color, index) => (
                    <ColorCell cellColor={color}></ColorCell>
                  ))}
                </div>
              </TableCell>
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="center"><img className="flag-icon" src={process.env.PUBLIC_URL + "/flags/" + row?.nationality} alt={"flag_" + row?.nationality}></img></TableCell>
              <TableCell align="center">{row.team}</TableCell>
              <TableCell align="center">{row.laps}</TableCell>
              {showSectorBars ? 
                (<TableCell>
                  <div style={{"--num-sectors": numSectors.toString()} as React.CSSProperties} className="sector-cell-container">
                  {row.sectors.map((sector_time, index) => (
                    sector_time.time !== "No Time" ?
                    <SectorCell 
                      cellClass={sector_time.time === Results.bestLap?.sector_times[index].time ? "fastest-time-cell" : (sector_time.state === "green" ? "personal-best-cell" : "slower-time-cell")}>
                      </SectorCell> : null))}
                  </div>
                </TableCell>)
              : (row.sectors.map((sector_time, index) => (
                <TableCell align='center'>
                  <span className={sector_time.time === Results.bestLap?.sector_times[index].time ? "fastest-time" : (sector_time.state === "green" ? "personal-best" : "slower-time")}>
                      {sector_time.time === "No Time" ? "" : sector_time.time}
                      </span>
                </TableCell>)
              ))}
              <TableCell align="center">{row.time}</TableCell>
              <TableCell align="center">{row.gap === "No Time" ? "" : ("+ " + row.gap)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        { showTheoreticalBest ?
        <TableFooter>
          <TableRow>
            <TableCell></TableCell>
            {showEntryIcons ? <TableCell></TableCell> : <TableCell align="center"></TableCell>}
            <TableCell></TableCell>
            <TableCell>Theoretical best</TableCell>
            <TableCell align="center"></TableCell>
            <TableCell align="center"></TableCell>
            <TableCell align="center"></TableCell>
            {showSectorBars ? 
              <TableCell align='center'></TableCell>
            : Results.bestLap?.sector_times.map((sector, index) => (
                <TableCell align='center'>{sector.time}</TableCell>
            ))}
            <TableCell align="center">{Results.bestLap?.time}</TableCell>
            <TableCell align="center"></TableCell>
          </TableRow>
        </TableFooter> : null}
      </Table>
    </TableContainer>
  );
}

function SectorCell(props: any) {
  return (
      <span className={props.cellClass}></span>
  )
}

function ColorCell(props: any) {
  return (
      <span style={{"--cell-color": props.cellColor} as React.CSSProperties}></span>
  )
}

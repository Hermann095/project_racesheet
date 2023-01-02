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

export default function ResultsTable(props: ResultsTableProbs) {

  //const [showSectorBars, setShowSectorBars] = React.useState(true);
  
  let showSectorBars = props.showSectorBars;
  let Results = props.Results;
  let numSectors = 0
  if (Results !== undefined) {
    numSectors = Number(Results?.bestLap?.sector_times.length);
  }
  //console.log(Results);


  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="center">Nationality</TableCell>
            <TableCell align="center">Team</TableCell>
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
          {Results.drivers?.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="center"><img className="flag-icon" src={process.env.PUBLIC_URL + "/flags/" + row?.nationality} crossOrigin="anonymous" alt={"flag_" + row?.nationality}></img></TableCell>
              <TableCell align="center">{row.team}</TableCell>
              {showSectorBars ? 
                (<TableCell>
                  <div style={{"--num-sectors": numSectors.toString()} as React.CSSProperties} className="sector-cell-container">
                  {row.sectors.map((sector_time, index) => (
                    <SectorCell 
                      cellClass={(sector_time === Results.bestLap?.sector_times[index] ? "fastest-time-cell" : (sector_time === row.fastestLap?.sector_times[index] ? "personal-best-cell" : "slower-time-cell"))}>
                      </SectorCell>))}
                  </div>
                </TableCell>)
              : (row.sectors.map((sector_time, index) => (
                <TableCell align='center'>
                  <span className={sector_time === Results.bestLap?.sector_times[index] ? "fastest-time" : (sector_time === row.fastestLap?.sector_times[index] ? "personal-best" : "slower-time")}>
                      {sector_time}
                      </span>
                </TableCell>)
              ))}
              <TableCell align="center">{row.time}</TableCell>
              <TableCell align="center">+ {row.gap}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

function SectorCell(props: any) {
  return (
      <span className={props.cellClass}></span>
  )
}

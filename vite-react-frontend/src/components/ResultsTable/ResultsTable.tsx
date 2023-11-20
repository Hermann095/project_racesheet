import * as React from 'react'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

import { ResultsTableProbs } from '../../types/types'
import '../ResultsTable/ResultsTable.css'
import { TableFooter } from '@mui/material'
import {
  ResultsTableSectorsBody,
  ResultsTableSectorsFooter,
  ResultsTableSectorsHead
} from './ResultsTableSectors'

export default function ResultsTable(props: ResultsTableProbs) {
  const showSectorBars = props.showSectorBars
  const showEntryIcons = props.showEntryIcons
  const showTheoreticalBest = props.showTheoreticalBest
  const Results = props.Results

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell align="center">Pos</TableCell>
            {showEntryIcons ? (
              <TableCell></TableCell>
            ) : (
              <TableCell align="center">Number</TableCell>
            )}
            <TableCell align="center"></TableCell>
            <TableCell>Name</TableCell>
            <TableCell align="center">Nationality</TableCell>
            <TableCell align="center">Team</TableCell>
            <TableCell align="center">Laps</TableCell>
            <ResultsTableSectorsHead
              sectors={Results?.drivers[0]?.sectors}
              bestLap={Results.bestLap}
              showSectorBars={showSectorBars}
            ></ResultsTableSectorsHead>
            <TableCell align="center">Time</TableCell>
            <TableCell align="center">Gap</TableCell>
            <TableCell align="center">State</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Results.drivers?.map((row, index) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="center">{index + 1}</TableCell>
              {showEntryIcons ? (
                <TableCell align="center">
                  <img
                    className="entry-icon"
                    src={
                      '/images/carsets/' +
                      props.carsetName +
                      '/entry_icons/' +
                      row?.number +
                      '.png'
                    }
                    alt=""
                  ></img>
                </TableCell>
              ) : (
                <TableCell align="center">{row?.number}</TableCell>
              )}
              <TableCell align="center">
                <div
                  style={
                    {
                      '--num-colors': row.color.length.toString()
                    } as React.CSSProperties
                  }
                  className="color-cell-container"
                >
                  {row.color.map((color, index) => (
                    <ColorCell key={index} cellColor={color}></ColorCell>
                  ))}
                </div>
              </TableCell>
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="center">
                <img
                  className="flag-icon"
                  src={'/flags/' + row?.nationality}
                  alt={'flag_' + row?.nationality}
                ></img>
              </TableCell>
              <TableCell align="center">{row.team}</TableCell>
              <TableCell align="center">{row.laps}</TableCell>
              <ResultsTableSectorsBody
                sectors={row.fastestLap?.sector_times}
                bestLap={Results.bestLap}
                showSectorBars={showSectorBars}
              ></ResultsTableSectorsBody>
              <TableCell align="center">{row.time}</TableCell>
              <TableCell align="center">
                {row.gap === 'No Time' ? '' : '+ ' + row.gap}
              </TableCell>
              <TableCell align="center" className="results-table-state-cell">
                {row.state}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        {showTheoreticalBest ? (
          <TableFooter>
            <TableRow>
              <TableCell></TableCell>
              {showEntryIcons ? (
                <TableCell></TableCell>
              ) : (
                <TableCell align="center"></TableCell>
              )}
              <TableCell></TableCell>
              <TableCell>Theoretical best</TableCell>
              <TableCell align="center"></TableCell>
              <TableCell align="center"></TableCell>
              <TableCell align="center"></TableCell>
              <ResultsTableSectorsFooter
                bestLap={Results.bestLap}
                showSectorBars={showSectorBars}
              ></ResultsTableSectorsFooter>
              <TableCell align="center">{Results.bestLap?.time}</TableCell>
              <TableCell align="center"></TableCell>
              <TableCell align="center"></TableCell>
            </TableRow>
          </TableFooter>
        ) : null}
      </Table>
    </TableContainer>
  )
}

function ColorCell(props: any) {
  return (
    <span
      style={{ '--cell-color': props.cellColor } as React.CSSProperties}
    ></span>
  )
}

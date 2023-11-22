import * as React from 'react'

import { ResultsTableProbs } from '../../types/types'
import '../ResultsTable/ResultsTable.css'

import {
  ResultsTableSectorsBody,
  ResultsTableSectorsFooter,
  ResultsTableSectorsHead
} from './ResultsTableSectors'
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow
} from '../ui/table'

export default function ResultsTable(props: ResultsTableProbs) {
  const showSectorBars = props.showSectorBars
  const showEntryIcons = props.showEntryIcons
  const showTheoreticalBest = props.showTheoreticalBest
  const Results = props.Results

  return (
    <Table aria-label="simple table">
      <TableHeader>
        <TableRow>
          <TableHead align="center">Pos</TableHead>
          {showEntryIcons ? (
            <TableHead></TableHead>
          ) : (
            <TableHead align="center">Number</TableHead>
          )}
          <TableHead align="center"></TableHead>
          <TableHead>Name</TableHead>
          <TableHead align="center">Nationality</TableHead>
          <TableHead align="center">Team</TableHead>
          <TableHead align="center">Laps</TableHead>
          <ResultsTableSectorsHead
            sectors={Results?.drivers[0]?.sectors}
            bestLap={Results.bestLap}
            showSectorBars={showSectorBars}
          ></ResultsTableSectorsHead>
          <TableHead align="center">Time</TableHead>
          <TableHead align="center">Gap</TableHead>
          <TableHead align="center">State</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Results.drivers?.map((row, index) => (
          <TableRow key={row.name} className="last:border-0">
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
            <TableCell>{row.name}</TableCell>
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
  )
}

interface ColorCellPropbs {
  cellColor: string
}

function ColorCell({ cellColor }: ColorCellPropbs) {
  return (
    <span style={{ '--cell-color': cellColor } as React.CSSProperties}></span>
  )
}

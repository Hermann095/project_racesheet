import * as React from 'react'
import TableCell from '@mui/material/TableCell'
import { ResultsTableSectorsProbs } from '../../types/types'

import '../ResultsTable/ResultsTable.css'

interface SectorCellProbs {
  cellClass: string
}

function SectorCell({ cellClass }: SectorCellProbs) {
  return <span className={cellClass}></span>
}

export function ResultsTableSectorsHead(props: ResultsTableSectorsProbs) {
  const showSectorBars =
    props.showSectorBars === undefined ? false : props.showSectorBars
  const sectors = props.sectors

  return (
    <>
      {showSectorBars ? (
        <TableCell align="center">Sectors</TableCell>
      ) : (
        sectors?.map((sector, index) => (
          <TableCell key={index} align="center">
            Sector {index + 1}
          </TableCell>
        ))
      )}
    </>
  )
}

export function ResultsTableSectorsBody(props: ResultsTableSectorsProbs) {
  const showSectorBars =
    props.showSectorBars === undefined ? false : props.showSectorBars
  const sectors = props.sectors
  const bestLap = props.bestLap
  let numSectors = 0

  if (sectors !== undefined) {
    numSectors = Number(sectors.length)
  }

  return (
    <>
      {showSectorBars ? (
        <TableCell>
          <div
            style={
              { '--num-sectors': numSectors.toString() } as React.CSSProperties
            }
            className="sector-cell-container"
          >
            {sectors?.map((sector_time, index) =>
              sector_time.time !== 'No Time' ? (
                <SectorCell
                  key={index}
                  cellClass={
                    sector_time.time === bestLap?.sector_times[index].time
                      ? 'fastest-time-cell'
                      : sector_time.state === 'green'
                        ? 'personal-best-cell'
                        : 'slower-time-cell'
                  }
                ></SectorCell>
              ) : null
            )}
          </div>
        </TableCell>
      ) : (
        sectors?.map((sector_time, index) => (
          <TableCell key={index} align="center">
            <span
              className={
                sector_time.time === bestLap?.sector_times[index].time
                  ? 'fastest-time'
                  : sector_time.state === 'green'
                    ? 'personal-best'
                    : 'slower-time'
              }
            >
              {sector_time.time === 'No Time' ? '' : sector_time.time}
            </span>
          </TableCell>
        ))
      )}
    </>
  )
}

export function ResultsTableSectorsFooter(props: ResultsTableSectorsProbs) {
  const showSectorBars =
    props.showSectorBars === undefined ? false : props.showSectorBars
  const bestLap = props.bestLap

  return (
    <>
      {showSectorBars ? (
        <TableCell align="center"></TableCell>
      ) : (
        bestLap?.sector_times.map((sector, index) => (
          <TableCell key={index} align="center">
            {sector.time}
          </TableCell>
        ))
      )}
    </>
  )
}

import React from 'react'

//import { CircularProgress } from '@mui/material'
import { SimState } from '@/types/types'
import { Button } from '../ui/button'
import SwitchWithLabel from '../SwitchWithLabel/SwitchWithLabel'
import StepInput from '../StepInput/StepInput'
import { buildStyles, CircularProgressbar } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

interface ResultsTopControlsProps {
  fetchedData: any
  simState: SimState
  onSimSpeedChange: (value: number) => void
  showTheoreticalBest: boolean
  onTheoreticalBestChange: (value: boolean) => void
  showEntryIcons: boolean
  onShowEntryIconsState: (value: boolean) => void
  showSectorBars: boolean
  onShowSectorBarChange: (value: boolean) => void
  runQualifying: () => void
  pauseQualifying: () => void
}

export default function ResultsTopControls({
  fetchedData,
  simState,
  onSimSpeedChange,
  showTheoreticalBest,
  onTheoreticalBestChange,
  showEntryIcons,
  onShowEntryIconsState,
  showSectorBars,
  onShowSectorBarChange,
  runQualifying,
  pauseQualifying
}: ResultsTopControlsProps) {
  const simSpeeds = ['1/3', '1/2', '1', '2', '10']

  const handleSimSpeedChange = (value: number | string) => {
    if (value !== typeof String) {
      console.log(value)
      onSimSpeedChange(1 / Number(value))
    }
  }

  return (
    <div className="grid grid-cols-2">
      <div>
        <div className="flex flex-col">
          <h1>{fetchedData?.session} Results</h1>
          <div className="grid w-1/2 grid-cols-3 items-center gap-1">
            <div>
              <h3>{simState}</h3>
            </div>
            <div className="h-14 w-14">
              <CircularProgressbar
                value={
                  simState === 'Finished'
                    ? 100
                    : simState === 'Ready'
                      ? 0
                      : (fetchedData?.current_tick / fetchedData?.total_ticks) *
                        100
                }
                strokeWidth={50}
                styles={buildStyles({
                  strokeLinecap: 'butt',
                  trailColor: 'rgb(41, 37, 36)',
                  pathColor: 'rgb(234, 88, 12)'
                })}
              ></CircularProgressbar>
            </div>
            <div className="mb-2 flex items-center">
              <StepInput
                label="Sim speed"
                stepValues={simSpeeds}
                startIndex={2}
                onValueChange={handleSimSpeedChange}
              ></StepInput>
            </div>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-end gap-4">
        <SwitchWithLabel
          label="Theoretical Best"
          id="show-theoretical-best"
          labelPosition={'top'}
          checked={showTheoreticalBest}
          onCheckedChange={(checked) => onTheoreticalBestChange(checked)}
        />
        <SwitchWithLabel
          label="Entry Icons"
          id="show-entry-icons"
          labelPosition={'top'}
          checked={showEntryIcons}
          onCheckedChange={(checked) => onShowEntryIconsState(checked)}
        />
        <SwitchWithLabel
          label="Sector Bars"
          id="show-sector-bars"
          labelPosition={'top'}
          checked={showSectorBars}
          onCheckedChange={(checked) => onShowSectorBarChange(checked)}
        />
        <div className="flex flex-col">
          <Button onClick={runQualifying}>Start Qualifying</Button>
          <Button onClick={pauseQualifying}>Pause Qualifying</Button>
        </div>
      </div>
    </div>
  )
}

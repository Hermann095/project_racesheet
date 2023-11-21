import * as React from 'react'
import { useEffect, useState } from 'react'
import io, { Socket } from 'socket.io-client'

import Container from '@mui/material/Container'

import { DriverResults, SimState } from '../types/types'
import ResultsTable from '../components/ResultsTable/ResultsTable'
import EventLog from '../components/EventLog/EventLog'

import { convertSessionResultsToDriverResults } from '../utils/utils'
import ResultsTopControls from '@/components/ResultsTopControls/ResultsTopControls'

//TODO: change to shadcn

export default function ResultsPage(props: any) {
  const [socketInstance, setSocketInstance] = useState<Socket>()

  const [fetchedData, setFetchedData] = useState<any>(null)
  const [resultData, setResultData] = useState<DriverResults>({ drivers: [] })

  const [carsetName, setCarsetName] = useState('')

  const [showSectorBars, setShowSectorBars] = useState<boolean>(false)
  const [showEntryIcons, setShowEntryIcons] = useState<boolean>(false)
  const [showTheoreticalBest, setShowTheoreticalBest] = useState<boolean>(false)

  const [isPaused, setIsPaused] = useState(false)
  const [simState, setSimState] = useState<SimState>(SimState.Ready)

  const [simSpeed, setSimSpeed] = useState<number>(1)

  useEffect(() => {
    //const socket = io('ws://127.0.0.1:5000/')
    const socket = io('http://127.0.0.1:5000', {
      transports: ['websocket']
    })

    setSocketInstance(socket)

    socket.on('connect', () => {
      console.log('connected')
    })

    socket.on('disconnect', () => {
      console.log('disconnected')
    })

    socket.on('cancelled_qualifying', () => {
      console.log('cancelled_qualifying')
      setSimState(SimState.Cancelled)
    })

    socket.on('finished_qualifying', () => {
      console.log('finished_qualifying')
      setSimState(SimState.Finished)
    })

    socket.on('paused_qualifying', () => {
      console.log('paused_qualifying')
      setSimState(SimState.Paused)
    })

    socket?.on('update_qualifying_results', (data: any) => {
      console.log('recived data from update_qualifying_results')
      setSimState(SimState.Running)
      const jsonData = JSON.parse(data)
      console.log(jsonData)
      setFetchedData(jsonData)
      const results = convertSessionResultsToDriverResults(jsonData)
      setResultData(results)
    })

    return function cleanup() {
      socket.offAny()
      socket.disconnect()
    }
  }, [])

  useEffect(() => {
    fetch('/api/carset')
      .then((res) => res.json())
      .then((data) => {
        setCarsetName(data.name)
      })
  }, [])

  useEffect(() => {
    console.log(carsetName)
  }, [carsetName])

  useEffect(() => {
    if (simState === SimState.Running) {
      socketInstance?.emit('resume_qualifying', { simSpeed: simSpeed })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [simSpeed])

  function runQualifying() {
    setIsPaused(false)
    if (isPaused) {
      socketInstance?.emit('resume_qualifying', { simSpeed: simSpeed })
    } else {
      socketInstance?.emit('run_qualifying', {
        printResults: false,
        simSpeed: simSpeed
      })
    }
  }

  function pauseQualifying() {
    setIsPaused(true)
    socketInstance?.emit('pause_qualifying')
  }

  function handleSectorBarChange(checked: boolean) {
    setShowSectorBars(checked)
  }

  function handleEntryIconChange(checked: boolean) {
    setShowEntryIcons(checked)
  }

  function handleTheoreticalBest(checked: boolean) {
    setShowTheoreticalBest(checked)
  }

  return (
    <>
      <Container maxWidth="xl">
        <ResultsTopControls
          fetchedData={fetchedData}
          simState={simState}
          onSimSpeedChange={setSimSpeed}
          showTheoreticalBest={showTheoreticalBest}
          onTheoreticalBestChange={handleTheoreticalBest}
          onShowEntryIconsState={handleEntryIconChange}
          onShowSectorBarChange={handleSectorBarChange}
          showEntryIcons={showEntryIcons}
          showSectorBars={showSectorBars}
          runQualifying={runQualifying}
          pauseQualifying={pauseQualifying}
        />
        <ResultsTable
          carsetName={carsetName}
          Results={resultData}
          showSectorBars={showSectorBars}
          showEntryIcons={showEntryIcons}
          showTheoreticalBest={showTheoreticalBest}
        ></ResultsTable>
        <EventLog events={fetchedData?.log}></EventLog>
      </Container>
    </>
  )
}

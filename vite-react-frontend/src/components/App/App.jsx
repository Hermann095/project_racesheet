import React from 'react'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import CssBaseline from '@mui/material/CssBaseline'

import HomePage from '../../pages'
import ResultsPage from '../../pages/results'
import StandingsPage from '../../pages/standings'
import Navbar from '../Navbar/navbar'
import { ThemeProvider } from '../ThemeProvider/ThemeProvider'

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <CssBaseline />
      <Router>
        <Navbar></Navbar>
        <Routes>
          <Route exact path="/" element={<HomePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/standings" element={<StandingsPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App

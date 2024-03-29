import React from 'react'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'

import HomePage from '../../pages/index'
import ResultsPage from '../../pages/results'
import StandingsPage from '../../pages/standings'
import Navbar from '../Navbar/Navbar'
import { ThemeProvider } from '../ThemeProvider/ThemeProvider'

import '../../index.css'

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/standings" element={<StandingsPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App

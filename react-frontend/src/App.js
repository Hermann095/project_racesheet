import React, { useEffect, useState } from 'react';
import './App.scss';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import useMediaQuery from '@mui/material/useMediaQuery';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import {io} from "socket.io-client";

import HomePage from './pages';
import ResultsPage from './pages/results';
import StandingsPage from './pages/standings';
import Navbar from './components/Navbar/navbar';

const socket = io("localhost:5000/", {
  transports: ["websocket"],
  cors: {
    origin: "http://localhost:3000/",
  },
});

function App() {

  //const [socketInstance, setSocketInstance] = useState("");
  //const [loadedSocket, setLoadedSocket] = useState(false);

  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const [darkMode, setDarkMode] = React.useState(prefersDarkMode)
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        console.log("toggledColorMode");
        setDarkMode((prevMode) => (!prevMode));
      },
    }),
    [],
  );

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode, darkMode],
  );

  useEffect(() => {
    

    //setSocketInstance(socket);

    socket.on("connect", (data) => {
      console.log(data);
    });

    socket.on("disconnect", (data) => {
      console.log(data);
    });

    socket?.on("update_qualifying_results", (data) => {
      console.log("recived data from update_qualifying_results");
      console.log(data);
    })

    return function cleanup() {
      //socket.disconnect();
      socket.offAny();
    }
  }, []);

  function runQualifyingSocket(message) {
    console.log("sending message");
    console.log(message);
    socket.emit("run_qualifying", message);
  }


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />    
      <Router>
        <Navbar toggleColorMode={colorMode.toggleColorMode} darkMode={darkMode}></Navbar>
        <Routes>
          <Route exact path='/' element={<HomePage />} />
          <Route path="/results" element={<ResultsPage  onRunQualifying={(message) => runQualifyingSocket(message)}/>} />
          <Route path="/standings" element={<StandingsPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

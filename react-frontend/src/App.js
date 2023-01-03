import React from 'react';
import './App.scss';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import useMediaQuery from '@mui/material/useMediaQuery';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';



import HomePage from './pages';
import ResultsPage from './pages/results';
import StandingsPage from './pages/standings';
import Navbar from './components/Navbar/navbar';



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
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [prefersDarkMode, darkMode],
  );


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />    
      <Router>
        <Navbar toggleColorMode={colorMode.toggleColorMode} darkMode={darkMode}></Navbar>
        <Routes>
          <Route exact path='/' element={<HomePage />} />
          <Route path="/results" element={<ResultsPage/>} />
          <Route path="/standings" element={<StandingsPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

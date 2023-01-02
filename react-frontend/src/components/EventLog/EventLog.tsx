import * as React from 'react';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import { EventLogProbs, EventLogItem } from '../../types/types';
import { FormControl, FormLabel, Grid, Slider } from '@mui/material';
import { red, orange, green, yellow, purple } from '@mui/material/colors';


function renderRow(props: ListChildComponentProps) {
  const { data, index, style } = props;

  let styleItem = {};

  if (data[index].type === "default"){
    styleItem = {}
  } else if (data[index].type === "crash") {
    styleItem = {backgroundColor: orange[900]}
  } else if (data[index].type === "retirement") {
    styleItem = {color: red[900]}
  } else if (data[index].type === "newLeader") {
    styleItem = {color: green[900]}
  } else if (data[index].type === "yellowFlag") {
    styleItem = {backgroundColor: yellow[900]}
  } else if (data[index].type === "redFlag") {
    styleItem = {backgroundColor: red[900]}
  } else if (data[index].type === "purpleSector") {
    styleItem = {color: purple[900]}
  } else if (data[index].type === "fastestLap") {
    styleItem = {backgroundColor: purple[900]}
  } else if (data[index].type === "personalBest") {
    styleItem = {backgroundColor: green[900]}
  } else if (data[index].type === "mistake") {
    styleItem = {color: orange[900]}
  }


  return (
    <ListItem style={style} key={index} component="div" disablePadding sx={styleItem}>
      <ListItemButton>
        <ListItemText primary={data[index]?.text} />
      </ListItemButton>
    </ListItem>
  );
}

export default function EventLog(props: EventLogProbs) {

  const [detailLevel, setDetailLevel] = React.useState("high");

  let numItems = props.events?.length;
  

  function filterEvents() {
    let events = [];

    if (props.events === undefined){
      events = []
    }

    if (detailLevel === "high") {
      events = props.events;
    }
    else if (detailLevel === "medium") {
      events = props.events?.filter((event: EventLogItem) => event.detailLevel !== "high")
    } else {
      events = props.events?.filter((event: EventLogItem) => event.detailLevel === "low")
    }

    numItems = events?.length;
    return events;
  }

  const marks = [
    {
      value: 0,
      label: 'Low',
    },
    {
      value: 50,
      label: 'Medium',
    },
    {
      value: 100,
      label: 'High',
    },
  ];

  const handleDetailChange = (event: any, value: any) => {
    let index = marks.findIndex((mark) => mark.value === value);
    setDetailLevel(marks[index].label.toLocaleLowerCase());
  };

  
  function valueLabelFormat(value: number) {
    let index = marks.findIndex((mark) => mark.value === value);
    return marks[index].label;
  }

  return (
    <Box
      sx={{ width: '100%', height: 360, bgcolor: 'background.paper', marginTop: '10px'}}
    >
      <Grid display={"flex"} justifyContent={"end"} sx={{marginBottom: '10px'}}>
      <FormControl>
        <FormLabel sx={{display: 'inline'}}>Log detail Level</FormLabel>
        <Slider 
          defaultValue={100}
          valueLabelFormat={valueLabelFormat}
          valueLabelDisplay='auto'
          step={null}
          marks={marks}
          onChange={handleDetailChange}
          />
      </FormControl>
      </Grid>
      <FixedSizeList
        height={280}
        width={"100%"}
        itemSize={46}
        itemData={filterEvents()}
        itemCount={numItems}
        overscanCount={5}
      >
        {renderRow}
      </FixedSizeList>
    </Box>
  );
}




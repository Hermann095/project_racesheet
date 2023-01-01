import * as React from 'react';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import { EventLogProbs } from '../../types/types';


function renderRow(props: ListChildComponentProps) {
  const { data, index, style } = props;

  return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton>
        <ListItemText primary={data[index]} />
      </ListItemButton>
    </ListItem>
  );
}

export default function EventLog(props: EventLogProbs) {

  const numItems = props.events?.length;

  return (
    <Box
      sx={{ width: '100%', height: 360, bgcolor: 'background.paper', marginTop: "40px" }}
    >
      <FixedSizeList
        height={360}
        width={"100%"}
        itemSize={46}
        itemCount={numItems}
        overscanCount={5}
        itemData={props.events}
      >
        {renderRow}
      </FixedSizeList>
    </Box>
  );
}

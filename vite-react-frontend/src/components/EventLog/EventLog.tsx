import * as React from 'react'
import {
  EventLogProbs,
  LogItem,
  LogDetailLevel,
  LogType
} from '../../types/types'
import { ScrollArea } from '../ui/scroll-area'
import { Separator } from '../ui/separator'
import { cn } from '@/lib/utils'
import { ToggleGroup, ToggleGroupItem } from '../ui/toggle-group'
import { SignalHigh, SignalLow, SignalMedium } from 'lucide-react'

export default function EventLog(props: EventLogProbs) {
  const [detailLevel, setDetailLevel] = React.useState('high')

  function filterEvents() {
    let events = []

    if (props.events === undefined) {
      events = []
    }

    if (detailLevel === LogDetailLevel.High) {
      events = props.events
    } else if (detailLevel === LogDetailLevel.Medium) {
      events = props.events?.filter(
        (event: LogItem) => event.detailLevel !== LogDetailLevel.High
      )
    } else {
      events = props.events?.filter(
        (event: LogItem) => event.detailLevel === LogDetailLevel.Low
      )
    }

    return events
  }

  const handleDetailChange = (value: string) => {
    setDetailLevel(value)
  }

  const detailSteps: EventLogToggleItem[] = [
    {
      value: 'low',
      icon: <SignalLow></SignalLow>
    },
    {
      value: 'medium',
      icon: <SignalMedium></SignalMedium>
    },
    {
      value: 'high',
      icon: <SignalHigh></SignalHigh>
    }
  ]

  return (
    <div className="bg-background mt-2 h-[350px] w-full">
      <div className="mb-2 flex justify-end">
        <EventLogDetailSelector
          label="Log Detail"
          steps={detailSteps}
          onChange={handleDetailChange}
          defaultValue={detailLevel}
        />
      </div>
      <EventLogList items={filterEvents()}></EventLogList>
    </div>
  )
}

interface EventLogItemProps extends React.ComponentPropsWithoutRef<'div'> {
  item: LogItem
}

function EventLogItem({ item, ...props }: EventLogItemProps) {
  let itemStyle = ''

  switch (item.type) {
    case LogType.Crash:
      itemStyle = 'bg-orange-900'
      break
    case LogType.Retirement:
      itemStyle = 'text-red-900'
      break
    case LogType.NewLeader:
      itemStyle = 'text-green-900'
      break
    case LogType.YellowFlag:
      itemStyle = 'text-yellow-800'
      break
    case LogType.RedFlag:
      itemStyle = 'bg-red-900'
      break
    case LogType.PurpleSector:
      itemStyle = 'text-purple-900'
      break
    case LogType.FastestLap:
      itemStyle = 'bg-purple-500'
      break
    case LogType.PersonalBest:
      itemStyle = 'bg-green-900'
      break
    case LogType.Mistake:
      itemStyle = 'text-orange-600'
      break
    default:
      itemStyle = ''
      break
  }

  return (
    <>
      <div
        className={cn('bg-background flex h-12 items-center px-4', itemStyle)}
        key={props.key}
      >
        <p>{item.text}</p>
      </div>
      <Separator className="my-2"></Separator>
    </>
  )
}

interface EventLogListProps {
  items: LogItem[]
}

function EventLogList({ items }: EventLogListProps) {
  return (
    <ScrollArea className="h-[280px] w-full rounded-md">
      {items?.map((item, index) => (
        <EventLogItem item={item} key={index}></EventLogItem>
      ))}
    </ScrollArea>
  )
}

interface EventLogToggleItem {
  value: string
  icon: React.ReactNode
  ariaLabel?: string
}

interface EventLogDetailSelctorProps {
  label: string
  steps: EventLogToggleItem[]
  defaultValue?: string
  onChange?: (value: string) => void
}

function EventLogDetailSelector({
  label,
  steps,
  defaultValue,
  onChange
}: EventLogDetailSelctorProps) {
  return (
    <div className="flex flex-col justify-center">
      <p className="text-center">{label}</p>
      <ToggleGroup
        type="single"
        onValueChange={onChange}
        defaultValue={defaultValue}
      >
        {steps.map((item, index) => (
          <ToggleGroupItem
            key={index}
            value={item.value}
            aria-label={
              item.ariaLabel !== undefined ? item.ariaLabel : item.value
            }
          >
            {item.icon}
          </ToggleGroupItem>
        ))}
      </ToggleGroup>
    </div>
  )
}

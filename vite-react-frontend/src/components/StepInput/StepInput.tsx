import { Minus, Plus } from 'lucide-react'
import React, { useEffect, useState } from 'react'
import { Button } from '../ui/button'
import { Label } from '../ui/label'

interface StepInputProps {
  label: string
  stepValues: number[] | string[]
  startIndex: number
  onValueChange?: (value: number | string) => void
}

export default function StepInput({
  label,
  stepValues,
  startIndex,
  onValueChange
}: StepInputProps) {
  const [index, setIndex] = useState<number>(startIndex)

  function decrementIndex() {
    if (index > 0) {
      setIndex(index - 1)
    }
  }

  function incrementIndex() {
    if (index < stepValues.length - 1) {
      setIndex(index + 1)
    }
  }

  useEffect(() => {
    if (onValueChange !== undefined) {
      onValueChange(stepValues[index])
    }
  }, [index, onValueChange, stepValues])

  return (
    <div className="flex flex-col gap-2 text-center">
      <Label>{label}</Label>
      <div className="grid grid-cols-3 text-center">
        <Button variant={'outline'} size="sm" onClick={decrementIndex}>
          <Minus className="h-4 w-4"></Minus>
        </Button>
        <div className="border-input bg-background border p-1 text-center">
          {stepValues[index]}
        </div>
        <Button variant={'outline'} size="sm" onClick={incrementIndex}>
          <Plus className="h-4 w-4"></Plus>
        </Button>
      </div>
    </div>
  )
}

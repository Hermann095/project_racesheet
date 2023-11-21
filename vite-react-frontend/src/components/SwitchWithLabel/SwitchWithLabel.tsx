import { cn } from '@/lib/utils'
import { SwitchProps } from '@radix-ui/react-switch'
import { cva, VariantProps } from 'class-variance-authority'
import React from 'react'
import { Label } from '../ui/label'
import { Switch } from '../ui/switch'

const switchVariants = cva('flex items-center gap-2', {
  variants: {
    labelPosition: {
      right: '',
      left: 'flex-row-reverse',
      top: 'flex-col-reverse',
      bottom: 'flex-col'
    }
  },
  defaultVariants: {
    labelPosition: 'right'
  }
})

interface SwitchWithLabelProps
  extends SwitchProps,
    VariantProps<typeof switchVariants> {
  label: string
}

export default function SwitchWithLabel({
  label,
  id,
  labelPosition,
  onCheckedChange,
  ...props
}: SwitchWithLabelProps) {
  return (
    <div className={cn(switchVariants({ labelPosition }))}>
      <Switch id={id} onCheckedChange={onCheckedChange} {...props} />
      <Label htmlFor={id}>{label}</Label>
    </div>
  )
}

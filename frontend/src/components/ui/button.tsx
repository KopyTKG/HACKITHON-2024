import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
 'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
 {
  variants: {
   variant: {
    default:
     'bg-white text-black shadow hover:bg-white/90 dark:bg-stone-700 dark:text-stone-100 dark:hover:bg-stone-600',
    primary: 'bg-blue-700 text-white shadow hover:bg-blue-800/90',
    danger: 'bg-red-600 text-destructive-foreground shadow-sm hover:bg-red-700/90',
    neutral: 'bg-zinc-500 text-white shadow-sm hover:bg-zinc-600/80',
    outline:
     'bg-transparent text-white border border-stone-200 shadow-sm hover:bg-stone-50 hover:text-black dark:border-stone-800 dark:hover:bg-stone-800 dark:hover:text-stone-100',
    ghost:
     'bg-transparent text-white shadow-sm hover:bg-stone-50 hover:text-black dark:hover:bg-stone-800 dark:hover:text-stone-100',
   },
   size: {
    default: 'h-9 px-4 py-2',
    sm: 'h-8 rounded-md px-3 text-xs',
    lg: 'h-10 rounded-md px-8',
    icon: 'h-9 w-9',
   },
  },
  defaultVariants: {
   variant: 'default',
   size: 'default',
  },
 },
)

export interface ButtonProps
 extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
 asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
 ({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : 'button'
  return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
 },
)
Button.displayName = 'Button'

export { Button, buttonVariants }

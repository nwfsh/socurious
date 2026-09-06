import { useRef } from 'react'
import { motion, useMotionValue, useSpring, useTransform, type MotionValue } from 'framer-motion'

type DockItem = {
  icon: React.ReactNode
  label: string
  onClick: () => void
}

type DockProps = {
  items: DockItem[]
  children?: React.ReactNode
  panelHeight?: number
  baseItemSize?: number
  magnification?: number
}

function DockItem({ item, baseItemSize, magnification, mouseX }: {
  item: DockItem
  baseItemSize: number
  magnification: number
  mouseX: MotionValue<number>
}) {
  const ref = useRef<HTMLButtonElement>(null)

  const distance = useTransform(mouseX, (val) => {
    const bounds = ref.current?.getBoundingClientRect() ?? { x: 0, width: 0 }
    return val - bounds.x - bounds.width / 2
  })

  const size = useSpring(
    useTransform(distance, [-150, 0, 150], [baseItemSize, magnification, baseItemSize]),
    { mass: 0.1, stiffness: 150, damping: 12 }
  )

  return (
    <div className="relative flex flex-col items-center group">
      <span className="absolute -top-8 text-xs text-white bg-zinc-800 px-2 py-0.5 rounded-md opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
        {item.label}
      </span>
      <motion.button
        ref={ref}
        style={{ width: size, height: size }}
        onClick={item.onClick}
        className="flex items-center justify-center rounded-xl bg-white/10 hover:bg-white/20 text-zinc-300 hover:text-white transition-colors"
      >
        {item.icon}
      </motion.button>
    </div>
  )
}

export default function Dock({ items, children, panelHeight = 68, baseItemSize = 50, magnification = 70 }: DockProps) {
  const mouseX = useMotionValue(Infinity)

  return (
    <motion.div
      onMouseMove={(e) => mouseX.set(e.clientX)}
      onMouseLeave={() => mouseX.set(Infinity)}
      className="fixed bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-3 rounded-2xl border border-white/10 bg-zinc-900/90 backdrop-blur-md px-5 z-50"
      style={{ height: panelHeight }}
    >
      {children && (
        <>
          {children}
          <div className="w-px self-stretch bg-white/20 my-3" />
        </>
      )}
      <div className="flex items-end gap-3">
        {items.map((item) => (
          <DockItem
            key={item.label}
            item={item}
            baseItemSize={baseItemSize}
            magnification={magnification}
            mouseX={mouseX}
          />
        ))}
      </div>
    </motion.div>
  )
}

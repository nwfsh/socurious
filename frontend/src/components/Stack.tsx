import { useState, useRef } from 'react'
import { motion, useMotionValue, useTransform } from 'framer-motion'

type CardItem = {
  id: number
  content: React.ReactNode
  rotation: number
}

function CardComponent({ card, index, total, isTop, sensitivity, sendToBackOnClick, onSendToBack }: {
  card: CardItem
  index: number
  total: number
  isTop: boolean
  sensitivity: number
  sendToBackOnClick: boolean
  onSendToBack: () => void
}) {
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const rotate = useTransform(x, [-200, 0, 200], [-15 + card.rotation, card.rotation, 15 + card.rotation])

  const stackOffset = total - 1 - index
  const scale = 1 - stackOffset * 0.04
  const yOffset = -stackOffset * 10

  return (
    <motion.div
      style={{
        position: 'absolute',
        x: isTop ? x : 0,
        y: isTop ? y : yOffset,
        rotate: isTop ? rotate : card.rotation,
        scale,
        zIndex: index,
        width: '100%',
        height: '100%',
        cursor: isTop ? 'grab' : 'default',
        top: 0,
        left: 0,
      }}
      drag={isTop}
      dragElastic={0.15}
      whileDrag={{ cursor: 'grabbing' }}
      onDragEnd={(_, info) => {
        const distance = Math.sqrt(info.offset.x ** 2 + info.offset.y ** 2)
        if (distance > sensitivity) onSendToBack()
        else {
          x.set(0)
          y.set(0)
        }
      }}
      onClick={() => { if (isTop && sendToBackOnClick) onSendToBack() }}
      animate={{ y: isTop ? 0 : yOffset, scale, rotate: card.rotation }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    >
      {card.content}
    </motion.div>
  )
}

type StackProps = {
  cards: React.ReactNode[]
  randomRotation?: boolean
  sensitivity?: number
  sendToBackOnClick?: boolean
  onComplete?: () => void
}

export default function Stack({ cards, randomRotation = false, sensitivity = 150, sendToBackOnClick = true, onComplete }: StackProps) {
  const rotations = useRef(cards.map(() => randomRotation ? (Math.random() - 0.5) * 12 : 0))
  const cycleCount = useRef(0)

  const [items, setItems] = useState<CardItem[]>(
    cards.map((card, i) => ({ id: i, content: card, rotation: rotations.current[i] }))
  )

  function sendToBack(id: number) {
    setItems(prev => {
      const idx = prev.findIndex(i => i.id === id)
      const item = prev[idx]
      const next = [...prev]
      next.splice(idx, 1)
      next.unshift(item)
      cycleCount.current += 1
      if (cycleCount.current >= prev.length) onComplete?.()
      return next
    })
  }

  return (
    <div className="relative" style={{ width: '100%', height: '100%' }}>
      {items.map((card, index) => (
        <CardComponent
          key={card.id}
          card={card}
          index={index}
          total={items.length}
          isTop={index === items.length - 1}
          sensitivity={sensitivity}
          sendToBackOnClick={sendToBackOnClick}
          onSendToBack={() => sendToBack(card.id)}
        />
      ))}
    </div>
  )
}

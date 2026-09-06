import { useState, useRef, useEffect } from 'react'
import { RotateCw, ChevronRight, Check } from 'lucide-react'
import { Slider } from '@/components/ui/slider'

const CATEGORIES = [
  'relationships',
  'family and childhood',
  'career',
  'fears and insecurities',
  'random everyday questions',
  'hypothetical scenarios',
  'sexual',
  'controversial debate',
  'advice',
]

type NavProps = {
  intimacy: [number, number]
  loading: boolean
  onIntimacyChange: (v: [number, number]) => void
  onIntimacyCommit: (v: [number, number]) => void
  onRefresh: () => void
}

export default function Nav({ intimacy, loading, onIntimacyChange, onIntimacyCommit, onRefresh }: NavProps) {
  const [catOpen, setCatOpen] = useState(false)
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const dropdownRef = useRef<HTMLDivElement>(null)
  const ditherRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    function drawDither() {
      const canvas = ditherRef.current
      if (!canvas) return
      const ctx = canvas.getContext('2d')!
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
      const w = canvas.width, h = canvas.height
      const img = ctx.createImageData(w, h)
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const i = (y * w + x) * 4
          const threshold = ((x % 4) + (y % 4) * 4) / 16 * 255
          const noise = Math.random() * 255
          const v = noise > threshold ? 0 : 255
          img.data[i] = v; img.data[i+1] = v; img.data[i+2] = v; img.data[i+3] = 255
        }
      }
      ctx.putImageData(img, 0, 0)
    }
    drawDither()
    window.addEventListener('resize', drawDither)
    return () => window.removeEventListener('resize', drawDither)
  }, [])

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setCatOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function toggle(cat: string) {
    setSelected(prev => {
      const next = new Set(prev)
      next.has(cat) ? next.delete(cat) : next.add(cat)
      return next
    })
  }

  return (
    <nav className="fixed right-0 top-0 h-screen w-64 z-50 overflow-hidden flex flex-col border-l border-white/10 bg-zinc-900/90 backdrop-blur-md px-5 py-8">
      <canvas ref={ditherRef} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.06, mixBlendMode: 'overlay', pointerEvents: 'none' }} />

      {/* Intimacy */}
      <div className="relative flex flex-col gap-3 flex-1">
        <span className="text-xs text-zinc-400">intimacy</span>
        <div className="flex-1 flex items-center justify-center py-4">
          <Slider
            orientation="vertical"
            min={-25}
            max={60}
            step={1}
            value={intimacy}
            onValueChange={(v) => onIntimacyChange(v as [number, number])}
            onValueCommitted={(v) => onIntimacyCommit(v as [number, number])}
            className="h-full"
          />
        </div>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="p-1.5 rounded-full text-zinc-400 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-50 self-start"
        >
          <RotateCw size={13} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="relative h-px bg-white/20 my-4" />

      {/* Bottom links */}
      <div className="relative flex flex-col gap-3">
        <div ref={dropdownRef}>
          <button
            onClick={() => setCatOpen(o => !o)}
            className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-white transition-colors w-full"
          >
            Categories
            {selected.size > 0 && (
              <span className="text-xs bg-white/20 rounded-full px-1.5 py-0.5 text-white">
                {selected.size}
              </span>
            )}
            <ChevronRight size={12} className={`ml-auto transition-transform ${catOpen ? 'rotate-90' : ''}`} />
          </button>
          {catOpen && (
            <div className="absolute bottom-full left-full ml-2 bg-zinc-900 border border-white/10 rounded-xl py-1.5 min-w-52 z-50 shadow-xl">
              {CATEGORIES.map(cat => (
                <button
                  key={cat}
                  onClick={() => toggle(cat)}
                  className="flex items-center gap-2.5 w-full px-3 py-1.5 text-sm text-left text-zinc-300 hover:text-white hover:bg-white/5 transition-colors capitalize"
                >
                  <span
                    className={`w-3.5 h-3.5 rounded border flex items-center justify-center shrink-0 transition-colors ${selected.has(cat) ? 'border-[#53131E]' : 'border-white/30'}`}
                    style={selected.has(cat) ? { backgroundColor: '#53131E' } : {}}
                  >
                    {selected.has(cat) && <Check size={9} strokeWidth={3} />}
                  </span>
                  {cat}
                </button>
              ))}
            </div>
          )}
        </div>

        <button
          className="text-sm px-3.5 py-1.5 rounded-full text-white hover:opacity-90 transition-opacity text-left"
          style={{ backgroundColor: '#53131E' }}
        >
          Game Mode
        </button>
      </div>
    </nav>
  )
}

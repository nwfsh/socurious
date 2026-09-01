import { RotateCw } from 'lucide-react'
import { Slider } from '@/components/ui/slider'

type NavProps = {
  intimacy: [number, number]
  loading: boolean
  onIntimacyChange: (v: [number, number]) => void
  onIntimacyCommit: (v: [number, number]) => void
  onRefresh: () => void
}

export default function Nav({ intimacy, loading, onIntimacyChange, onIntimacyCommit, onRefresh }: NavProps) {
  return (
    <nav className="pointer-events-auto flex items-center gap-4 rounded-2xl border border-white/10 bg-zinc-900/90 backdrop-blur-md px-5 py-4">
      <div className="flex items-center gap-3">
        <span className="text-xs text-zinc-400 shrink-0 tabular-nums w-16 text-center">
          {(intimacy[0] / 100).toFixed(1)}–{(intimacy[1] / 100).toFixed(1)}
        </span>
        <div className="w-40">
          <Slider
            min={-100}
            max={100}
            step={1}
            value={intimacy}
            onValueChange={(v) => onIntimacyChange(v as [number, number])}
            onValueCommitted={(v) => onIntimacyCommit(v as [number, number])}
          />
        </div>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="p-1.5 rounded-full text-zinc-400 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-50 shrink-0"
        >
          <RotateCw size={13} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="w-px h-4 bg-white/20 shrink-0" />

      <div className="flex items-center gap-4 shrink-0">
        <a href="#" className="text-sm text-zinc-400 hover:text-white transition-colors">Browse</a>
        <a href="#" className="text-sm text-zinc-400 hover:text-white transition-colors">Categories</a>
        <a href="#" className="text-sm text-zinc-400 hover:text-white transition-colors">Saved</a>
        <a href="#" className="text-sm text-zinc-400 hover:text-white transition-colors">About</a>
        <button
          className="text-sm px-3.5 py-1 rounded-full text-white hover:opacity-90 transition-opacity"
          style={{ backgroundColor: '#53131E' }}
        >
          Get started
        </button>
      </div>
    </nav>
  )
}

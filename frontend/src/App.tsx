import { useEffect, useState } from 'react'
import { RotateCw } from 'lucide-react'
import { QuestionCard } from './components/QuestionCard'
import { Slider } from "@/components/ui/slider"

type Question = {
    id: number;
    text: string;
    intimacy_score: number;
};

async function fetchQuestions(min: number, max: number): Promise<Question[]> {
    const params = new URLSearchParams({
        limit: '9',
        min_intimacy: (min / 100).toFixed(2),
        max_intimacy: (max / 100).toFixed(2),
    })
    const res = await fetch(`/questions/random/batch?${params}`)
    return res.json()
}

function drawDither() {
  const canvas = document.getElementById('dither') as HTMLCanvasElement
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  const w = canvas.width, h = canvas.height
  const img = ctx.createImageData(w, h)
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4
      const threshold = ((x % 4) + (y % 4) * 4) / 16 * 255
      const noise = Math.random() * 255
      const v = noise > threshold ? 0 : 255
      img.data[i] = v; img.data[i + 1] = v; img.data[i + 2] = v; img.data[i + 3] = 255
    }
  }
  ctx.putImageData(img, 0, 0)
}

function App() {

const [questions, setQuestions] = useState<Question[]>([])
const [loading, setLoading] = useState(false)
const [intimacy, setIntimacy] = useState<[number, number]>([-100, 100])

async function loadQuestions(min = intimacy[0], max = intimacy[1]) {
  setLoading(true)
  const q = await fetchQuestions(min, max)
  setQuestions(q)
  setLoading(false)
}

useEffect(() => {
  drawDither()
  window.addEventListener('resize', drawDither)
  return () => window.removeEventListener('resize', drawDither)
}, [])

useEffect(() => {
  loadQuestions()
}, [])

return (
  <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-8">
    <div className="w-full max-w-5xl flex items-center gap-4">
      <span className="text-sm text-muted-foreground w-24">intimacy {(intimacy[0]/100).toFixed(1)}–{(intimacy[1]/100).toFixed(1)}</span>
      <Slider
        min={-100}
        max={100}
        step={1}
        value={intimacy}
        onValueChange={(v) => setIntimacy(v as [number, number])}
        onValueCommitted={(v) => loadQuestions((v as number[])[0], (v as number[])[1])}
        className="flex-1"
      />
      <button onClick={() => loadQuestions()} disabled={loading} className="p-2 rounded-full hover:bg-muted transition-colors disabled:opacity-50">
        <RotateCw size={18} />
      </button>
    </div>
    {loading && <p className="text-muted-foreground text-sm">loading...</p>}
    {!loading && questions.length > 0 && (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-5xl">
        {questions.map(q => <QuestionCard key={q.id} question={q} />)}
      </div>
    )}
  </div>
)

}

export default App

import { useEffect, useState } from 'react'
import { QuestionCard } from './components/QuestionCard'
import { Button } from '@base-ui/react'

type Question = {
    id: number;
    text: string;
    intimacy_score: number;
};

async function fetchRandomQuestion(): Promise<Question> {
    const res = await fetch("/questions/random");
    return res.json();
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
    
const [question, setQuestion] = useState<Question | null>(null)
const [loading, setLoading] = useState(false)

async function loadQuestion() {
  setLoading(true)
  const q = await fetchRandomQuestion()
  setQuestion(q)
  setLoading(false)
}

useEffect(() => {
  drawDither()
  window.addEventListener('resize', drawDither)
  return () => window.removeEventListener('resize', drawDither)
}, [])

useEffect(() => {
  loadQuestion()
}, [])

return (
  <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-8">
    {loading && <p className="text-muted-foreground text-sm">loading...</p>}
    {question && !loading && <QuestionCard question={question} />}
    <Button onClick={loadQuestion} disabled={loading}>
      next question
    </Button>
  </div>
)

}

export default App

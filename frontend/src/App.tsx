import { useEffect, useState } from 'react'
import { QuestionCard } from './components/QuestionCard'
import DecryptedText from './components/DecryptedText'
import Nav from './components/Nav'

type Question = {
    id: number;
    text: string;
    intimacy_score: number;
};

async function fetchQuestions(min: number, max: number): Promise<Question[]> {
    const params = new URLSearchParams({
        limit: '16',
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
    <>
        {/* Fixed header: title overlaps nav from above */}
        <div className="fixed top-16 inset-x-0 z-50 flex flex-col items-center pointer-events-none">
            <h1
                className="text-8xl tracking-tight relative z-10 pointer-events-auto"
                style={{
                    color: "#53131E",
                    marginBottom: "1.75rem",
                    fontFamily: "'Kranky', cursive",
                    marginTop: "1.00rem",
                }}
            >
                <DecryptedText
                    text="SoCurious"
                    animateOn="hover"
                    sequential
                    revealDirection="center"
                    speed={100}
                />
            </h1>
            <Nav
                intimacy={intimacy}
                loading={loading}
                onIntimacyChange={(v) => setIntimacy(v)}
                onIntimacyCommit={(v) => loadQuestions(v[0], v[1])}
                onRefresh={() => loadQuestions()}
            />
        </div>

        <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-8 pt-80">
            {loading && (
                <p className="text-muted-foreground text-sm">loading...</p>
            )}
            {!loading && questions.length > 0 && (
                <div
                    className="grid gap-4 w-full max-w-6xl"
                    style={{
                        gridTemplateColumns:
                            "repeat(auto-fill, minmax(220px, 1fr))",
                    }}
                >
                    {questions.map((q) => (
                        <QuestionCard key={q.id} question={q} />
                    ))}
                </div>
            )}
        </div>
    </>
);

}

export default App

import { useEffect, useState } from 'react'
import { QuestionCard } from './components/QuestionCard'
import DecryptedText from './components/DecryptedText'
import Dock from './components/Dock'
import Stack from './components/Stack'
import { ModeSelectModal } from './components/ModeSelectModal'
import { Slider } from './components/ui/slider'
import { RefreshCw, Layers, Gamepad2, Check } from 'lucide-react'

const CATEGORIES = [
  'relationships', 'family and childhood', 'career',
  'fears and insecurities', 'random everyday questions',
  'hypothetical scenarios', 'sexual', 'controversial debate', 'advice',
]

type Question = {
    id: number;
    text: string;
    intimacy_score: number;
};


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
const [rateLimited, setRateLimited] = useState(false)
const [showModeSelect, setShowModeSelect] = useState(true)
const [gameMode, setGameMode] = useState(false)
const [intimacy, setIntimacy] = useState<[number, number]>([-25, 60])
const [isMobile, setIsMobile] = useState(() => window.innerWidth < 640)
const [catOpen, setCatOpen] = useState(false)
const [selectedCats, setSelectedCats] = useState<Set<string>>(new Set())

function toggleCat(cat: string) {
  setSelectedCats(prev => {
    const next = new Set(prev)
    next.has(cat) ? next.delete(cat) : next.add(cat)
    loadQuestions(intimacy[0], intimacy[1], next)
    return next
  })
}

async function loadQuestions(min = intimacy[0], max = intimacy[1], cats = selectedCats) {
  setLoading(true)
  setRateLimited(false)
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/questions/random/batch?${(() => {
      const p = new URLSearchParams({ limit: '16', min_intimacy: (min / 100).toFixed(2), max_intimacy: (max / 100).toFixed(2) })
      cats.forEach(cat => p.append('topic', cat))
      return p
    })()}`
  )
  if (res.status === 429) {
    setRateLimited(true)
    setLoading(false)
    return
  }
  const q = await res.json()
  setQuestions(q)
  setLoading(false)
}

useEffect(() => {
  drawDither()
  const handleResize = () => {
    drawDither()
    setIsMobile(window.innerWidth < 640)
  }
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])

useEffect(() => {
  loadQuestions()
}, [])

return (
    <>
        {showModeSelect && (
            <ModeSelectModal
                onSelect={(mode) => {
                    setGameMode(mode === 'game')
                    setShowModeSelect(false)
                }}
            />
        )}
        {rateLimited && (
            <div className="fixed inset-0 flex items-center justify-center z-[100] pointer-events-none">
                <div className="pointer-events-auto bg-zinc-900 border border-white/10 rounded-none px-6 py-4 flex items-center gap-4 shadow-xl">
                    <span className="text-sm text-zinc-200">
                        you're going too fast {":("}, take your time to read
                    </span>
                    <button
                        onClick={() => setRateLimited(false)}
                        className="text-xs text-zinc-500 hover:text-white transition-colors"
                    >
                        close
                    </button>
                </div>
            </div>
        )}
        <svg
            style={{
                position: "absolute",
                width: 0,
                height: 0,
                overflow: "hidden",
            }}
        >
            <defs>
                <filter id="grain">
                    <feTurbulence
                        type="fractalNoise"
                        baseFrequency="0.65"
                        numOctaves="3"
                        stitchTiles="stitch"
                        result="noise"
                    />
                    <feColorMatrix
                        type="saturate"
                        values="0"
                        in="noise"
                        result="grayNoise"
                    />
                    <feComponentTransfer in="grayNoise" result="subtleNoise">
                        <feFuncR type="linear" slope="0.2" intercept="0.4" />
                        <feFuncG type="linear" slope="0.2" intercept="0.4" />
                        <feFuncB type="linear" slope="0.2" intercept="0.4" />
                    </feComponentTransfer>
                    <feBlend
                        in="SourceGraphic"
                        in2="subtleNoise"
                        mode="overlay"
                        result="blended"
                    />
                    <feComposite
                        in="blended"
                        in2="SourceGraphic"
                        operator="in"
                    />
                </filter>
            </defs>
        </svg>
        {catOpen && (
            <div className="fixed bottom-36 left-1/2 -translate-x-1/2 z-50 bg-zinc-900/95 backdrop-blur-md border border-white/10 rounded-lg p-2 sm:p-3 shadow-xl grid grid-cols-2 sm:grid-cols-3 gap-1 sm:gap-1.5 w-max max-w-[calc(100vw-32px)]">
                {CATEGORIES.map((cat) => (
                    <button
                        key={cat}
                        onClick={() => toggleCat(cat)}
                        className={`flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-md text-xs sm:text-sm capitalize transition-colors text-left ${selectedCats.has(cat) ? "bg-[#53131E] text-white" : "text-zinc-300 hover:bg-white/10"}`}
                    >
                        {selectedCats.has(cat) && (
                            <Check size={10} strokeWidth={3} className="sm:hidden" />
                        )}
                        {selectedCats.has(cat) && (
                            <Check size={12} strokeWidth={3} className="hidden sm:block" />
                        )}
                        {cat}
                    </button>
                ))}
            </div>
        )}
        <Dock
            items={[
                {
                    icon: <Layers size={18} />,
                    label: "Categories",
                    onClick: () => setCatOpen((o) => !o),
                },
                {
                    icon: (
                        <RefreshCw
                            size={18}
                            className={loading ? "animate-spin" : ""}
                        />
                    ),
                    label: "Refresh",
                    onClick: () => loadQuestions(),
                },
                {
                    icon: <Gamepad2 size={18} />,
                    label: "Game Mode",
                    onClick: () => setGameMode(o => !o),
                },
            ]}
            panelHeight={isMobile ? 60 : 80}
            baseItemSize={isMobile ? 40 : 52}
            magnification={isMobile ? 52 : 72}
        >
            <div className="flex flex-col items-center gap-1 sm:gap-1.5 px-1 sm:px-2">
                <span className="text-xs text-zinc-400">intimacy</span>
                <div className="flex items-center gap-1.5 sm:gap-2">
                    <span className="text-xs text-zinc-500">low</span>
                    <div className="w-24 sm:w-36">
                        <Slider
                            min={-25}
                            max={60}
                            step={1}
                            value={intimacy}
                            onValueChange={(v) =>
                                setIntimacy(v as [number, number])
                            }
                            onValueCommitted={(v) =>
                                loadQuestions(
                                    (v as number[])[0],
                                    (v as number[])[1]
                                )
                            }
                        />
                    </div>
                    <span className="text-xs text-zinc-500">high</span>
                </div>
            </div>
        </Dock>

        <div className="min-h-screen flex flex-col items-center gap-6 p-8 pt-16 pb-32">
            <h1
                className="text-7xl sm:text-9xl tracking-tight pointer-events-auto"
                style={{ color: "#53131E", filter: "url(#grain)" }}
            >
                <span style={{ fontFamily: "'Fraunces', serif" }}>
                    <DecryptedText
                        text="So"
                        animateOn="hover"
                        sequential
                        revealDirection="center"
                        speed={100}
                    />
                </span>
                <span style={{ fontFamily: "'Fraunces', serif" }}>
                    <DecryptedText
                        text="Curious"
                        animateOn="hover"
                        sequential
                        revealDirection="center"
                        speed={100}
                    />
                </span>
            </h1>
            <p className="text-base text-zinc-600 -mt-4">
                Curated questions to grow closer to one another.
            </p>
            <p className="text-xs text-center text-zinc-400 -mt-4">
                · not fully SFW yet · typos happen · sourced from reddit, so
                occasionally in french ·
                <br /> · question quality varies · possibly offensive & unhinged
                · report button coming soon ·
            </p>
            <hr className="w-full max-w-6xl border-1.5 border-zinc-300" />
            <hr className="w-full max-w-6xl border-1.5 border-zinc-400 -mt-4" />
            {loading && (
                <p className="text-muted-foreground text-sm">loading...</p>
            )}
            {!loading && questions.length > 0 && !gameMode && (
                <div
                    className="grid gap-4 w-full max-w-6xl mt-2"
                    style={{
                        gridTemplateColumns:
                            "repeat(auto-fill, minmax(190px, 1fr))",
                    }}
                >
                    {questions.map((q) => (
                        <QuestionCard key={q.id} question={q} />
                    ))}
                </div>
            )}
            {!loading && questions.length > 0 && gameMode && (
                <div className="flex flex-col items-center gap-3 -mt-2">
                    <p className="text-xs text-zinc-500">{isMobile ? 'tap or swipe to go through' : 'click or drag to go through'}</p>
                    <div style={{ width: isMobile ? Math.min(window.innerWidth - 48, 270) : 290, height: isMobile ? 340 : 380, position: 'relative' }}>
                        <Stack
                            randomRotation
                            sendToBackOnClick
                            sensitivity={isMobile ? 80 : 150}
                            onComplete={() => loadQuestions()}
                            cards={questions.map(q => (
                                <div
                                    key={q.id}
                                    className="relative w-full h-full rounded-md flex items-center justify-center p-6 sm:p-8 select-none"
                                    style={{ backgroundColor: '#FDFDFD', border: '1px solid #53131E', outline: '1px solid #53131E', outlineOffset: '-4px' }}
                                >
                                    <p className="text-sm sm:text-base font-medium leading-relaxed text-center text-zinc-800">
                                        {q.text}
                                    </p>
                                </div>
                        ))}
                    />
                </div>
            </div>
        )}
        </div>
        <footer className="fixed bottom-0 left-0 w-full text-center text-xs text-zinc-500 pb-3 pointer-events-none">
            questions sourced from{" "}
            <a
                href="https://reddit.com"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-zinc-300 pointer-events-auto"
            >
                reddit
            </a>
        </footer>
    </>
);

}

export default App

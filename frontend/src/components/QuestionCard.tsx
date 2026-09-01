type Question = {
  id: number
  text: string
  intimacy_score: number
}

export function QuestionCard({ question }: { question: Question }) {
  return (
    <div className="relative group max-w-lg w-full bg-card text-card-foreground rounded-xl border shadow-sm">
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl overflow-visible"
      >
        <rect
          x="1" y="1"
          width="calc(100% - 2px)"
          height="calc(100% - 2px)"
          rx="11"
          fill="none"
          stroke="black"
          strokeWidth="2"
          strokeLinecap="round"
          strokeDasharray="5 5"
          style={{ animation: 'marchingDots 2s linear infinite' }}
        />
      </svg>
      <div className="relative p-8">
        <p className="text-xl font-medium leading-relaxed">{question.text}</p>
        <p className="mt-4 text-sm text-muted-foreground">
          intimacy {Math.round(question.intimacy_score * 100)}
        </p>
      </div>
    </div>
  )
}

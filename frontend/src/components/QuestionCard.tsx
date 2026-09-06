type Question = {
  id: number
  text: string
}

export function QuestionCard({ question }: { question: Question }) {
  return (
    <div className="relative group w-full bg-card text-card-foreground rounded-md border ">
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-md overflow-visible"
      >
        <rect
          x="1" y="1"
          width="calc(100% - 2px)"
          height="calc(100% - 2px)"
          rx="11"
          fill="none"
          stroke="#53131E"
          strokeWidth="2"
          strokeLinecap="round"
          strokeDasharray="5 5"
          style={{ animation: 'marchingDots 2s linear infinite' }}
        />
      </svg>
      <div className="relative p-8">
        <p className="text-base font-medium leading-relaxed">{question.text}</p>
      </div>
    </div>
  )
}

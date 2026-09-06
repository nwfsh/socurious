type Question = {
  id: number
  text: string
}

export function QuestionCard({ question }: { question: Question }) {
  return (
      <div
          className="relative group w-full rounded-md border"
          style={{ backgroundColor: "#FDFDFD" }}
      >
          <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity duration-300 rounded-md overflow-visible">
              <rect
                  x="1"
                  y="1"
                  width="99%"
                  height="99%"
                  rx="7"
                  fill="none"
                  stroke="#53131E"
                  strokeWidth="1"
                  strokeLinecap="square"
                  strokeDasharray="5 5"
                  style={{ animation: "marchingDots 2s linear infinite" }}
              />
          </svg>
          <div className="relative p-8">
              <p className="text-base font-medium leading-relaxed">
                  {question.text}
              </p>
          </div>
      </div>
  );
}

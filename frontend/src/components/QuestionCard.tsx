import { Card, CardContent } from "@/components/ui/card"

type Question = {
  id: number
  text: string
  intimacy_score: number
}

export function QuestionCard({ question }: { question: Question }) {
  return (
    <Card className="max-w-lg w-full">
      <CardContent className="p-8">
        <p className="text-xl font-medium leading-relaxed">{question.text}</p>
        <p className="mt-4 text-sm text-muted-foreground">
          intimacy {Math.round(question.intimacy_score * 100)}
        </p>
      </CardContent>
    </Card>
  )
}

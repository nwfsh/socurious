# socurious
data pipeline transforming raw reddit posts into a feed of deduplicated interesting questions to ask friends, family and your significant other. 

## file structure

```
socurious/
├── .github/workflows/pipeline.yml   daily run: fetch -> clean/dedup -> classify
├── migrations/                      postgres schema, 001 to 007, run in order
├── src/
│   ├── adapters/reddit_rss.py       reads subreddit RSS feeds
│   ├── loaders/db_loader.py         fetch step, saves posts into raw_questions
│   ├── transform/                   clean, dedup, classify raw_questions -> questions
│   │   ├── filters.py               hard reject rules
│   │   ├── load_clean.py            clean + dedup step
│   │   ├── classify.py              topic + intimacy labels
│   │   ├── review_*.py              look over what filters/classify did
│   │   ├── dedup_diagnostic.py      tune the dedup threshold
│   │   ├── embedding_dedup_test.py  minilm embedding dedup experiment
│   │   └── reset_all_data_pipeline.py  wipe and start over
│   ├── api/                         fastapi backend for the frontend
│   │   ├── main.py                  app + rate limiter (limiter.py)
│   │   ├── routers/questions.py     endpoints
│   │   ├── services/question_service.py  logic
│   │   └── repository/question_repo.py   sql
│   └── ml/                          offline ml, run by hand, not in the pipeline
│       ├── common.py                shared helpers (jsonl, paths)
│       ├── topic/                   topic classifier: sample -> label -> split -> train -> evaluate
│       └── directed/                "is this question directed at someone" labels, see its README
├── data/                            hand labels for the ml work
│   ├── topic/sample.jsonl
│   └── directed/                    test, train, relabel + their pools
├── frontend/                        vite + react + tailwind/shadcn
│   └── src/
│       ├── App.tsx, main.tsx
│       ├── components/              QuestionCard, Stack, Dock, Nav, ModeSelectModal, ...
│       │   └── ui/                  shadcn button, card, slider
│       └── lib/utils.ts
├── docs/
│   ├── adr/                         decision records 001 to 012
│   ├── guidelines/directed-labelling.md
│   └── futurefeatures.txt
├── requirements.txt                 pipeline deps
├── requirements-api.txt             api deps
└── notes.txt                        setup notes
```

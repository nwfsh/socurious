TYPES OF CLASSIFICATION I CAN USE 

THIS FOR NOW, SINCE GOAL IS NOT THIS 
ALREADY PRETRAINED FROM SOMEONE ELSE 
MVP !! 
1. Zero-shot classification — no training data needed, you just supply labels at inference time. Fits when: you have a fixed label set (your categories) but no labeled examples to train on. This is exactly your situation — you never sat down and hand-labeled hundreds of questions by topic.

MAYBE THIS IS A LATER STAGE, NEED TO DO MANUAL LABELLING WHICH TAKES A LOT OF TIME 
2. Fine-tuned/trained classifier — you take a base model and train it on your own labeled examples (e.g. 200 questions you've manually tagged "career," "relationships," etc.), so it learns your specific categories precisely. Fits when: you have (or are willing to build) real labeled training data, and want higher accuracy than zero-shot can offer for your exact categories. You don't have labeled data, and building it means manually tagging hundreds of questions — real work you haven't done.

DONT WANT THIS BECUS : dont want one to one matching, like one-to-one/nearest-neighbor, and i want broader category assignment
3. Sentence embeddings + similarity matching — embed your categories as reference sentences, embed each question, and match by closest cosine similarity. Fits when: you want something faster/cheaper than zero-shot's full reasoning pass, and are okay with a rougher, more "vibes-based" match. Worth knowing this exists as a lighter alternative if zero-shot proves too slow.

DONT WANT THIS BECUS : need training data, Converts text into numbers first (word counts, frequencies), then learns statistical patterns from your labeled examples, i dont want to train my own ML classifier 
4. Traditional ML classifier (logistic regression, SVM, etc.) on hand-crafted features — older-school approach, needs labeled training data same as #2, generally weaker than modern transformer-based approaches for text. Not a strong contender here.



WHAT RESEARCH I FOUND 
The most directly applicable finding: < cite index="40-1">a research paper specifically on "Quantifying Intimacy in Language," which studies intimacy as a continuous variable in questions drawn from question-centered subreddits including r/AskReddit</cite> — same data source as you, same underlying goal (measuring how personal/intimate a question is). This confirms treating intimacy/closeness as a continuous score, not discrete buckets, is a legitimate, research-backed approach — potentially a better fit than your current fixed 1-3 severity scale or fixed topic categories.
The foundational psychology behind your whole app's premise: < cite index="38-1">Arthur Aron's 1997 study found that pairs who asked each other increasingly personal questions, starting superficial and escalating, felt significantly closer than pairs who only asked superficial questions</cite>. < cite index="43-1">The 36 Questions are explicitly structured in three sets, each more probing than the last, moving from rapport-building to deeper vulnerability</cite>. This is a real, validated design pattern: progression matters, not just categorization. Your app could be about ordering — surfacing lighter questions first, escalating over time or with more "likes"/engagement — not just tagging each question with a static severity level.
One caution worth flagging, since it showed up in results: one source mixed in commentary from what looks like a "couples game app" (NaughtyMatch) — a product plug, not research. Worth ignoring that specific bit and focusing on the Aron study and the intimacy-quantification paper, which are the actual substantive findings.
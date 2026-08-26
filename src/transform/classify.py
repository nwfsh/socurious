from transformers import pipeline
from question_intimacy.predict_intimacy import IntimacyEstimator


## to decide on topic, zero shot classification 
topic_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v1")

## intamacy score model ( researched backed YAY win for avery)
intimacy_scorer = IntimacyEstimator(cuda=False)

## very simple maybe not the best for now
categories = [
    "relationships",
    "family and childhood",
    "career",
    "fears and insecurities",
    "values",
    "hypotheticals",
    "funny and random"
]

def classify_topic(title: str) -> tuple[str,float]:
    result = topic_classifier(title, categories)
    return result["labels"][0], result["scores"][0]

def classify_intimacy(title: str) -> float:
    return intimacy_scorer.predict(title, type='list')


# if __name__ == "__main__":
#     result = classifier("Do you have any siblings?", candidate_labels=[...])
#     print(result["labels"][0], result["scores"][0])



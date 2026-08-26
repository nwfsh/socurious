from transformers import pipeline
from question_intimacy.predict_intimacy import IntimacyEstimator
from dotenv import load_dotenv
import os

load_dotenv()

## to decide on topic, zero shot classification 
topic_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

## intamacy score model ( researched backed YAY win for avery)
intimacy_scorer = IntimacyEstimator(cuda=False)

## very simple maybe not the best for now
categories = [
    "relationships",
    "family and childhood",
    "career",
    "fears and insecurities",
    "random everyday questions",
    "hypothetical scenarios",
    "sexual",
    "controversial debate",
    "advice",
]

def classify_topic(title: str) -> tuple[str,float]:
    result = topic_classifier(title, categories)
    return result["labels"][0], result["scores"][0]

def classify_intimacy(title: str) -> float:
    result = intimacy_scorer.predict([title], type='list')
    return float(result[0])


# if __name__ == "__main__":
#     result = classifier("Do you have any siblings?", candidate_labels=[...])
#     print(result["labels"][0], result["scores"][0])



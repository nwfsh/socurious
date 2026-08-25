import re
from langdetect import detect, LangDetectException

 # also desinging which function should run first to filter out the bad results 
 # and kick off to the next one asap 


def extract_question(text: str) -> str | None:
    """If the title contains a question followed by non-question trailing
    text, extract just the question part. Returns None if no '?' found."""
    if "?" not in text:
        return None
    
    # split at ? 
    question_part, _, trailing = text.partition("?")
    return (question_part + "?").strip()


def contains_i_pronoun(title:str) -> bool:
    return bool(re.search(r'\bI\b', title))

def contains_me_pronoun(title: str) -> bool:
    return bool(re.search(r'\bme\b', title))

# want better questions + not dumb and surface ones 
def is_too_short(title: str, min_words: int = 4) -> bool:
    return len(title.strip().split()) < min_words

def targets_specific_group(title: str) -> bool:
    return "people who" in title.lower()

def is_english(title: str) -> bool:
    try:
        return detect(title) == "en"
    except LangDetectException:
        return False # cant determine language 


## cheap to expensive
## also by
def should_reject(title: str) -> tuple[bool, str | None]:
    if is_too_short(title):
        return True, "too_short"
    title = extract_question(title)
    if title is None:
        return True, "not_a_question"
    if contains_i_pronoun(title):
        return True, "contains_i"
    if contains_me_pronoun(title):
        return True, "contains_me"
    if not is_english(title):
        return True, "not_english"
    return False, None
    

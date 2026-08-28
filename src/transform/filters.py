import re
from langdetect import detect, LangDetectException
from profanity_check import predict

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
    return bool(re.search(r'\bI\b', title, re.IGNORECASE))

def contains_me_pronoun(title: str) -> bool:
    return bool(re.search(r'\bme\b', title))

def contains_my_pronoun(title: str) -> bool:
    return bool(re.search(r'\bmy\b', title, re.IGNORECASE))

# want better questions + not dumb and surface ones 
def is_too_short(title: str, min_words: int = 4) -> bool:
    if title is None:
        return False
    return len(title.strip().split()) < min_words

def targets_specific_group(title: str) -> bool:
    t = title.lower()
    patterns = ["people who", "for those with", "to the people of", "to those who", " as a ", "what are your stories"]
    return any(p in t for p in patterns)

def targets_reddit_audience(title: str) -> bool:
    t = title.lower()
    return bool(re.search(r'\bof reddit\b', t))

# remove cus less than 0.3% of data, and cannot filter accurately 
# def is_english(title: str) -> bool:
#     if len(title.split()) < 4:
#         return True  # too short to reliably detect, assume English
#     try:
#         return detect(title) == "en"
#     except LangDetectException:
#         return False

# sub reddit auto filters anything 
#def contains_hate_speech(title: str) -> bool:
#    return predict([title])[0] == 1

## cheap to expensive
## also by
def should_reject(title: str) -> tuple[bool, str, str| None]:
    title = extract_question(title)
    if is_too_short(title):
        return True, "too_short", ""
    if title is None:
        return True, "not_a_question", ""
    if contains_i_pronoun(title):
        return True, "contains_i", ""
    if contains_me_pronoun(title):
        return True, "contains_me", ""
    if contains_my_pronoun(title):
        return True, "contains_my", ""
    if targets_specific_group(title):
        return True, "contains_certain_group", ""
    if targets_reddit_audience(title):
        return True, "contains_reddit_audience"
        
    # if not is_english(title):
    #     return True, "not_english"
    # if contains_hate_speech(title):
    #     return True, "contain_hate_speech"
    return False, None, title 


    

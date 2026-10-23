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
    cleaned = (question_part + "?").strip()
    return cleaned[0].upper() + cleaned[1:] if cleaned else cleaned


def contains_i_pronoun(title:str) -> bool:
    return bool(re.search(r'\bI\b', title, re.IGNORECASE))

def contains_me_pronoun(title: str) -> bool:
    return bool(re.search(r'\bme\b', title))

def contains_my_pronoun(title: str) -> bool:
    return bool(re.search(r'\bmy\b', title, re.IGNORECASE))

def contains_im_pronoun(title: str) -> bool:
    return bool(re.search(r'\bim\b', title, re.IGNORECASE))

def is_too_short(title: str, min_words: int = 4) -> bool:
    if title is None:
        return False
    words = [w for w in title.strip().split() if any(c.isalnum() for c in w)]
    return len(words) < min_words

def targets_specific_group(title: str) -> bool:
    t = title.lower()
    patterns = ["people who", "for those with", "to the people of", "to those who", " as a ", "what are your stories", "in reddit"]
    return any(p in t for p in patterns)

def targets_reddit_audience(title: str) -> bool:
    t = title.lower()
    return bool(re.search(r'\bof reddit\b', t))

def is_ama_format(title: str) -> bool:
    """Reddit AMA posts: 'ama' as a standalone word, often with age/gender flair."""
    return bool(re.search(r'\bama\b', title.lower()))

# might add 
# DISCOURSE_MARKERS = {"honestly", "so", "ok", "wait", "also", "genuinely"}

# def has_vocative_group_address(title: str) -> bool:
#     match = re.match(r'^([A-Za-z][a-zA-Z\s]{2,25}),\s', title)
#     if not match:
#         return False
#     leading = match.group(1).strip().lower()
#     return leading not in DISCOURSE_MARKERS

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

## two layers (ADR 012):
##   layer 1 format_reject   = is it even a usable question? these rules stay forever
##   layer 2 directed_reject = is it aimed at a group? regex for now, the directed classifier replaces this later
## cheap to expensive, layer 1 always runs first

def format_reject(title: str) -> tuple[bool, str | None, str | None]:
    title = extract_question(title)
    if title is None:
        return True, "not_a_question", None
    if is_too_short(title):
        return True, "too_short", None
    if contains_i_pronoun(title):
        return True, "contains_i", None
    if contains_me_pronoun(title):
        return True, "contains_me", None
    if contains_my_pronoun(title):
        return True, "contains_my", None
    if contains_im_pronoun(title):
        return True, "contains_im", None
    if is_ama_format(title):
        return True, "is_ask_me_anything", None

    # if not is_english(title):
    #     return True, "not_english"
    # if contains_hate_speech(title):
    #     return True, "contain_hate_speech"
    return False, None, title


## takes an already cleaned question from format_reject, not a raw title
## these two rules are the baseline the directed classifier has to beat, dont delete them until it ships
def directed_reject(question: str) -> tuple[bool, str | None]:
    if targets_specific_group(question):
        return True, "contains_certain_group"
    if targets_reddit_audience(question):
        return True, "contains_reddit_audience"
    return False, None


def should_reject(title: str) -> tuple[bool, str | None, str | None]:
    rejected, reason, question = format_reject(title)
    if rejected:
        return True, reason, None
    rejected, reason = directed_reject(question)
    if rejected:
        return True, reason, None
    return False, None, question 


    

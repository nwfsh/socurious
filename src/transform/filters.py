import re

def extract_question(text: str) -> str | None:
    ""


def is_question(title:str) -> bool:
    return title.strip().endswith("?")

def contains_i_pronoun(title:str) -> bool:
    return bool(re.search(r'\bI\b', title))

def contains_me_pronoun(title.str) -> bool:
    return bool(re.search(r'\bme\b,', title))

def starts_with_why(title: str) -> bool:
    return title.strip().lower().startswith("why ")
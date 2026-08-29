from src.api.repository.question_repo import fetch_random_question, fetch_random_questions

# business logic, calls the repository, decides what "not found" means.

def get_random_question(topic: str | None = None): 
    """Fetch a random question and return it to the router."""
    question = fetch_random_question(topic = topic)
    return question # will return DICT if found, if not return None 

def get_random_questions(topic: str |None = None):
    """ Fetch a batch of random question and return it to the router """
    question = fetch_random_questions(topic = topic)
    return question 

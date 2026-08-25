import os
import psycopg
from collections import Counter
from dotenv import load_dotenv
from src.transform.filters import should_reject

load_dotenv()

def get_conn():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def run_analysis():
    conn = get_conn()
    raw_rows = conn.execute("SELECT id, raw_title FROM raw_questions").fetchall()
    conn.close()

    reasons = Counter()
    for id, title in raw_rows:
        rejected, reason = should_reject(title)
        status = f"REJECT ({reason})" if rejected else "KEEP"
        print(f"[{status}] {title}")
        if rejected:
            reasons[reason] += 1

    print(f"\nTotal: {len(raw_rows)}")
    for reason, count in reasons.most_common():
        print(f"{reason}: {count}")


def review_rule(reason_to_check: str):
    conn = get_conn()
    rows = conn.execute("SELECT id, raw_title FROM raw_questions").fetchall()
    conn.close()

    for id, title in rows:
        rejected, reason = should_reject(title)
        if rejected and reason == reason_to_check:
            print(title)


if __name__ == "__main__":
    run_analysis()
    review_rule("contains_i") #LOOKS GOOD ## rejected 39, 1 false positives 
    #review_rule("too_short") # LOOKS good, rejected 7, no false positives 
    ## review_rule("contain_hate_speech") ill reavulate that
    ## review_rule("contains_me") # 5 inside, 1 false positive 
    ## review_rule("contains_certain_group") ## might need to be marked for manual review 
    ## review_rule("not_a_question") ## ~15/18 correct, ~2-3 borderline/false positives, ~83-90% precision
    ## review_rule("contains_my") # 5/7 correct, 2/7 false positives — ~71% precision.

# 624 total, 82 rejected, ~13% rejection rate, ~87% kept.
from src.transform.classify import get_conn

def reset_all():
    conn = get_conn()

    # Null out FK first so questions can be deleted
    conn.execute("UPDATE raw_questions SET question_id = NULL, rejection_reason = NULL")
    conn.execute("DELETE FROM question_category")
    conn.execute("DELETE FROM questions")

    conn.commit()
    conn.close()
    print("Reset complete — raw_questions cleared of processing markers, questions and question_category wiped.")


if __name__ == "__main__":
    reset_all()
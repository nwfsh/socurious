-- pushed questions, category and relationship context into a tertiary structure by accident
-- when infact it should be 2 many to many relationships
-- category & question and relationship context & question
-- called overmodelling 

CREATE TABLE question_category (
    question_id  INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    PRIMARY KEY (question_id, category_id)
);


-- will use joins later to mix both together when needed, but in context, tags are not used as often 

DROP TABLE question_tags;
DROP TABLE relationship_context;

CREATE INDEX idx_question_category ON question_category(category_id)

INSERT INTO categories (name) VALUES
    ('relationships'),
    ('family and childhood'),
    ('career'),
    ('fears and insecurities'),
    ('random everyday questions'),
    ('hypothetical scenarios'),
    ('sexual'),
    ('controversial debate'),
    ('advice')
ON CONFLICT DO NOTHING;

ALTER TABLE sources DROP COLUMN default_severity_hint;
ALTER TABLE questions ALTER COLUMN severity TYPE NUMERIC(4,3); -- means 4 total digits, 3 decimal points
ALTER TABLE questions RENAME COLUMN severity TO intimacy_score;
ALTER TABLE questions ADD CONSTRAINT intimacy_score_range CHECK (intimacy_score >= -1 AND intimacy_score <= 1);


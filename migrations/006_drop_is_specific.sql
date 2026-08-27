ALTER TABLE questions DROP COLUMN is_specific;
ALTER INDEX idx_questions_severity RENAME TO idx_questions_intimacy_score;
ALTER TABLE questions ALTER COLUMN intimacy_score DROP NOT NULL;
UPDATE questions SET intimacy_score = NULL;

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
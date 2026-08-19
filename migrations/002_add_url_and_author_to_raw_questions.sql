-- Add url and author columns to raw_questions for better traceability

ALTER TABLE raw_questions ADD COLUMN url TEXT;
ALTER TABLE raw_questions ADD COLUMN author TEXT;
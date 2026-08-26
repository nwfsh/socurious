-- pushed questions, category and relationship context into a tertiary structure by accident
-- when infact it should be 2 many to many relationships
-- category & question and relationship context & question
-- called overmodelling 

CREATE TABLE question_category (
    question_id  INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    PRIMARY KEY (question_id, category_id)
);

CREATE TABLE question_relationship_context (
    question_id     INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    relationship_id INTEGER NOT NULL REFERENCES relationship_context(id) ON DELETE RESTRICT,
    PRIMARY KEY (question_id, relationship_id)
);

-- will use joins later to mix both together when needed, but in context, tags are not used as often 

DROP TABLE question_tags;

CREATE INDEX idx_question_category ON question_category(category_id)
CREATE INDEX idx_question_relationship_context ON question_relationship_context(relationship_id)
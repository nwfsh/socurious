
-- uh sources aka each subreddit but named sources for now becus incase i wanna reach to other stuff
-- one row one specific origi 
CREATE TABLE sources (
    id                     SERIAL PRIMARY KEY,          
    name                   TEXT NOT NULL UNIQUE,        -- e.g. 'r/AskReddit', 'r/TooAfraidToAsk'
    platform               TEXT NOT NULL,                -- e.g. 'reddit', 'scraped_site'
    url                    TEXT,
    default_severity_hint  SMALLINT CHECK (default_severity_hint IN (1, 2, 3)),
    default_topic_hint     TEXT,                          -- e.g. 'fears/insecurities'
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- categories being lists of topics - career, hypotheticals, values 
-- primary key is id instead of name as its cheaper with integers
-- when its a foreign key of another table 
CREATE TABLE categories (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

-- relationship_context being asking if its for strangers, family, friends or relationship 
CREATE TABLE relationship_context (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL UNIQUE 
);

-- raw questions ( data ) JUST SCRAPPED 
-- used to track origin, this will always stay n survive cleaning 
-- ++ for debugging ++ prevent resinserts of same posts during incremental runs
CREATE TABLE raw_questions (
    id                SERIAL PRIMARY KEY,
    source_id         INTEGER NOT NULL REFERENCES sources(id),
    post_id           TEXT NOT NULL,          -- external ID (e.g. Reddit post ID)
    raw_title         TEXT NOT NULL,
    raw_body          TEXT,
    scraped_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    question_id       INTEGER,              -- stays null until cleaned question is created for it 
    UNIQUE (source_id, post_id) 
);

-- BIG ISSUE ADDRESSED 
-- question wants to reference raw question ( using raw question ID )
-- but raw question wants to reference questions ( using question ID )
-- since raw question does come first, keep question_id null until its cleaned up then insert 

-- cleaned questions that actually will be put up ( survived )
-- severity assigned per question (1 light / 2 personal / 3 heavy-excluded)
-- is_rant flags format-classifcation result (personal rant vs genuine general question) 
CREATE TABLE questions (
    id             SERIAL PRIMARY KEY,
    raw_question_id INTEGER NOT NULL REFERENCES raw_questions(id),
    text           TEXT NOT NULL,
    severity       SMALLINT NOT NULL CHECK (severity IN (1, 2, 3)),
    is_rant        BOOLEAN NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Now that both table question and raw questions full exist, link them tgt ( fill in raw_question's question_id)
ALTER TABLE raw_questions
    ADD CONSTRAINT fk_raw_questions_question
    FOREIGN KEY (question_id) REFERENCES questions(id);


-- question tag, this is a many to many relationship, could reference multiple things 
-- on delete restrict means they will blocks the delete until you've handled the affected tags yourself (??) look into later
-- might change to cascade 
CREATE TABLE question_tags (
    question_id  INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    relationship_id INTEGER NOT NULL REFERENCES relationship_context(id) ON DELETE RESTRICT,

    PRIMARY KEY (question_id, category_id, relationship_id)
);

-- tracking users and what questions they like or dislike .. 
-- weak entity relationship to question_id 
CREATE TABLE question_data (
    user_id      TEXT NOT NULL,
    question_id  INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    reaction     SMALLINT NOT NULL,   -- 1 = like, -1 = dislike
    PRIMARY KEY (user_id, question_id)
);

-- you create index for common query patterns, things you ask a lot 

CREATE INDEX idx_questions_severity ON questions(severity);
CREATE INDEX idx_question_tags_category ON question_tags(category_id);
CREATE INDEX idx_question_tags_relationship ON question_tags(relationship_id);
CREATE INDEX idx_question_data_question ON question_data(question_id);
CREATE INDEX idx_question_raw_question_source ON raw_questions(source_id);
CREATE INDEX idx_question_raw_question_id ON raw_questions(question_id);
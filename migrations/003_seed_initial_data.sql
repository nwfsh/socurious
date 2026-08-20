INSERT INTO relationship_context(name) VALUES 
    ('friends'),
    ('strangers'),
    ('family'),
    ('partner')
ON CONFLICT DO NOTHING;

ALTER TABLE sources DROP COLUMN default_topic_hint; 
ALTER TABLE raw_questions DROP COLUMN raw_body;
ALTER TABLE questions DROP COLUMN is_rant;
ALTER TABLE questions ADD COLUMN is_specific BOOLEAN NOT NULL DEFAULT FALSE;


INSERT INTO sources(name, platform, url, default_severity_hint) VALUES
    ('r/AskReddit', 'reddit', 'https://www.reddit.com/r/AskReddit/', 2),
    ('r/AskMen', 'reddit', 'https://www.reddit.com/r/AskMen/', 3),
    ('r/AskWomen', 'reddit', 'https://www.reddit.com/r/AskWomen/', 3),
    ('r/TooAfraidToAsk', 'reddit', 'https://www.reddit.com/r/TooAfraidToAsk/', 3),
    ('r/NoStupidQuestions', 'reddit', 'https://www.reddit.com/r/NoStupidQuestions/', 1),
    ('r/questions', 'reddit', 'https://www.reddit.com/r/questions/', 1)
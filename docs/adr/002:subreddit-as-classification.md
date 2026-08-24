Subreddit origin as a classification prior. Your idea, and the distinction you drew is the whole point — it's a soft prior that text-based rules adjust from, not a filter and not a trust score. Worth writing down precisely, because the sloppy version of this idea (source reputation as a quality gate) is a genuinely worse design and you'll want to show you avoided it deliberately.


WRITE THIS IN DETAIL LATER 
Raw SQL migrations over an ORM. Short one. Existing SQL experience, and schema design is the thing this project is meant to demonstrate — an ORM would abstract away the part being shown off.

No orchestration or cloud tooling. Airflow, Glue, AWS — deliberately excluded, with the scale argument. This one preempts the obvious interview question, and "I considered it and here's why not" reads far better than never having thought about it.

Rules-based classification before ML. Cheap filtering before expensive inference, and sentiment being the wrong axis for questions. Some of this is already in your project doc, so it may not need duplicating — depends whether you want the doc or the ADRs to be the record.
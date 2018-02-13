import cPickle
from request import generate_member_test_uids, get_results

def _run_once(test_id):
    

def add_questions(num):
    data = []
    for i in enum(num):
        for q in questions_with_answers:
            try:
                existing = next(item for item in dicts if item["question"] == q["question"])
                existing["count"] += 1
            except StopIteration:
                q.update({"count": 1})
                data.append(q)
    return data

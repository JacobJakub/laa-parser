import pickle

from request import generate_member_test_uids, get_results
from collections import OrderedDict
from sys import argv

test = argv[1]
iterations = int(argv[2])

def questions_with_answers(test_id):
    a,b,c = generate_member_test_uids(test_id)
    return get_results(a,b,c)

def add_questions(data, test_id, num):
    data['iterations'] += num

    for i in range(num):
        print('Doing test ', i)
        for q in questions_with_answers(test_id):
            try:
                existing = next(item for item in data['qas'] if item["question"] == q["question"])
                existing["count"] += 1
            except StopIteration:
                q.update({"count": 1})
                data['qas'].append(q)
    return data

# Writes final markdown from question_asnwers and adds few extra statistics
def markdown_questionanswers(question_answers, iterations):
    lines = []

    lines.append("Otazek celkem: %s \n\n" % len(question_answers))

    for qa in question_answers:
        question = qa['question']
        answers = qa['answers']

        lines.append("#### %s \n" % question)
        lines.append(
            "*(%s/%s) - %s%%* \n" % (
                qa['count'],
                iterations,
                round((qa['count'] / iterations * 100), 1)
            )
        )
        for a in answers:
            if a["is_correct"]:
                lines.append("* **%s** \n" % a['text'].rstrip())
            else:
                lines.append("* %s \n" % a['text'].rstrip())
        lines.append("\n")

    return lines

def _get_db_path(test_id):
    return r"database/%s.data" % test

def read_database(test_id):
    import os

    path = _get_db_path(test_id)

    if not os.path.exists(path):
        os.mknod(path)
        return {'iterations': 0, 'qas': []}
    else:
        with open(path, "rb") as f:
          return pickle.load(f)

def write_database(data, test_id):
    with open(_get_db_path(test_id), "wb") as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    # Read from database
    data = read_database(test)

    # Append new data
    data = add_questions(data, test, iterations)

    #Store to database
    write_database(data, test)

    # Sort questions by occurence
    qas = sorted(data['qas'], key=lambda t: t['count'], reverse=True)

    # Translate to markdown
    markdown = markdown_questionanswers(qas, data['iterations'])

    #Write results
    with open(r"results/%s.md" % test, "w") as f:
        f.writelines(markdown)

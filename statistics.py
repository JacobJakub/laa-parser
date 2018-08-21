from request import generate_member_test_uids, get_results
from collections import OrderedDict
from sys import argv

test = argv[1]
iterations = int(argv[2])

def questions_with_answers(test_id):
    a,b,c = generate_member_test_uids(test_id)
    return get_results(a,b,c)

def add_questions(test_id, num):
    data = []
    for i in range(num):
        print('Doing test ', i)
        for q in questions_with_answers(test_id):
            try:
                existing = next(item for item in data if item["question"] == q["question"])
                existing["count"] += 1
            except StopIteration:
                q.update({"count": 1})
                data.append(q)
    return data

def markdown_questionanswers(question_answers, iterations):
    lines = []

    lines.append("Otazek celkem: %s \n\n" % len(question_answers))

    for qa in question_answers:
        question = qa['question']
        answers = qa['answers']

        lines.append("#### %s \n" % question)
        lines.append("*(%s/%s)* \n" % (qa['count'], iterations))
        for a in answers:
            if a["is_correct"]:
                lines.append("* **%s** \n" % a['text'])
            else:
                lines.append("* %s \n" % a['text'])
        lines.append("\n")

    return lines

if __name__ == "__main__":
    data = add_questions(test, iterations)

    data = sorted(data, key=lambda t: t['count'], reverse=True)
    markdown = markdown_questionanswers(data, iterations)

    with open(r"results/%s.md" % test, "w") as f:
        f.writelines(markdown)

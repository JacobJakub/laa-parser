import re

from bs4 import BeautifulSoup

def find_input_val(soup, did):
    return soup.find("input", id=did).get("value")

def get_member_test_ids(html_data):
    soup = BeautifulSoup(html_data)

    member_id = find_input_val(soup, "osoba")
    test_uid = find_input_val(soup, "prezkouseni")

    return (member_id, test_uid)

def get_questions_context(html_data):
    soup = BeautifulSoup(html_data)

    answer_elements = soup.find_all("div", id=re.compile("divodpovedi_"))
    for answer_element in answer_elements:
        question_element = answer_element.parent.parent.find_previous_sibling("tr").span
        question_text = question_element.text.encode('UTF-8')[4:]
        answers = list(map(_get_answer, answer_element.find_all("li")))

        yield {
            "question": question_text,
            "answers": answers
        }

def _get_answer(elem):
    return {
        "text": elem.text.encode("utf-8"),
        "is_correct": elem.get("style") is not None
    }

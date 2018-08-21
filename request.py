import requests

from parse import get_member_test_ids, get_questions_context


def generate_member_test_uids(test_id):
    html_res = requests.post(
        "https://zkouseni.laacr.cz/Zkouseni/index.html?page=volnytest",
        data=dict(test=test_id, ok="OK"),
        allow_redirects=True
    ).content

    return (test_id,) + get_member_test_ids(html_res)

def get_results(test_id, member_id, test_uid):
    html_res = requests.post(
        "https://zkouseni.laacr.cz/Zkouseni/index.html?page=provedtest",
        data=dict(
            test=test_id,
            ok="OK",
            osoba=member_id,
            prezkouseni=test_uid
        ),
        allow_redirects=True
    ).content

    data = get_questions_context(html_res)

    return data

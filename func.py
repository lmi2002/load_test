from datetime import datetime
import itertools


def get_text_from_file(file_name):
    """
    :rtype: object
    """
    with open(file_name, encoding='utf-8') as f:
        return f.read()


def get_now_strftime(form):
    now = datetime.now()
    return now.strftime(form)


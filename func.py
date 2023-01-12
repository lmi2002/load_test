from datetime import datetime, timedelta
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

def get_date_strftime(form, days):
    start_date = datetime.now()  # год, месяц, число
    result_date = start_date - timedelta(days=days)
    return result_date.strftime(form)



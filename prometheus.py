# This approach is for making requests to the Prometheus API
# Usage: python prometheus.py -u <prometheus_url>
# Example: python prometheus.py -u http://localhost:9090

# script has two options: get last 30 days of data or input range of dates

# script getting few queries from prometheus
# 1. query maximum and average number of sessions in last 30 days during 1 minute;
# 2. count of queries to methods;
# 3. average duration of queries to methods;
# 4. maximum value of queries to methods;

import datetime
import getopt
import requests
import sys

URL: str = ''  # prometheus endpoint url

# ask user about next step of program with only 2 options
def ask_user():
    print("What would you like to do next?")
    print("1. Get last 30 days of data")
    print("2. Input range of dates")
    print("3. Exit")

    # get user input
    user_input = input("Enter 1, 2, or 3: ")

    # check if user input is valid
    if user_input == "1":
        get_last_30_days()
    elif user_input == "2":
        get_date_range()
    elif user_input == "3":
        sys.exit()
    else:
        print("Invalid input. Please try again.")
        ask_user()


# get last 30 days of data
def get_last_30_days():
    # Prometheus query maximum number of sessions in last 30 days during 1 minute
    promql_max = {'query': 'max by (job) (max_over_time(unitybase_sessions_total[30d:1m]))'}
    # Prometheus query average number of sessions in last 30 days during 1 minute
    promql_avg = {'query': 'avg by (job) (avg_over_time(unitybase_sessions_total[30d:1m]))'}

    print('')
    print("-- Unity-base maximum and average number of session during 1 minute in last 30 days --")
    print("[job, max value, avg value]")

    r1 = requests.get(url=URL, params=promql_max)
    r2 = requests.get(url=URL, params=promql_avg)

    r1_json = r1.json()['data']['result']
    r2_json = r2.json()['data']['result']

    rows = []
    for result in r1_json:
        l = []
        l.append(result['metric'].get('job', ''))
        l.append(result['value'][1])
        # find row in r2_json with same job
        for result2 in r2_json:
            if result2['metric'].get('job', '') == result['metric'].get('job', ''):
                l.append(result2['value'][1])
        rows.append(l)

    for ro in rows:
        print(ro)

    # Prometheus count of queries to methods in last 30 days
    promql_count = {
        'query': 'topk(1000, sort_desc(sum by (job, entity, method) (increase(unitybase_method_duration_seconds_count[30d]))))'}
    # Prometheus average duration of queries to methods in last 30 days
    promql_avg = {'query': '''topk(1000, sort_desc(
  avg by(job, entity, method) (
        rate(
          unitybase_method_duration_seconds_sum[30d]
        )
      /
        rate(
          unitybase_method_duration_seconds_count[30d]
        )
  )))'''}
    # Prometheus maximum value of queries to methods in last 30 days
    promql_max = {'query': '''topk(1000, sort_desc(
    max by(job, entity, method) (
            max_over_time(
            unitybase_method_duration_seconds_sum[30d]
            )
        /
            avg_over_time(
            unitybase_method_duration_seconds_count[30d]
            )
    )))'''}

    r1 = requests.get(url=URL, params=promql_count)
    r2 = requests.get(url=URL, params=promql_avg)
    r3 = requests.get(url=URL, params=promql_max)

    r1_json = r1.json()['data']['result']
    r2_json = r2.json()['data']['result']
    r3_json = r3.json()['data']['result']

    rows = []
    for result in r1_json:
        l = []
        l.append(result['metric'].get('job', ''))
        l.append(result['metric'].get('entity', ''))
        l.append(result['metric'].get('method', ''))
        try:
            l.append(round(float(result['value'][1]), 0))
        except:
            l.append(0)
        rows.append(l)

    print('')
    print("-- count of queries to methods in last 30 days --")
    print("[job, entity, method, count of queries]")
    for ro in rows:
        print(ro)

    rows = []
    for result in r2_json:
        if result['value'][1] != '+Inf' and result['value'][1] != 'NaN':
            l = []
            l.append(result['metric'].get('job', ''))
            l.append(result['metric'].get('entity', ''))
            l.append(result['metric'].get('method', ''))
            try:
                l.append(round(float(result['value'][1]), 4))
            except:
                l.append(0)
            rows.append(l)

    print('')
    print("-- average duration of queries to methods in last 30 days --")
    print("[job, entity, method, average duration]")
    for ro in rows:
        print(ro)

    rows = []
    for result in r3_json:
        if result['value'][1] != '+Inf' and result['value'][1] != 'NaN':
            l = []
            l.append(result['metric'].get('job', ''))
            l.append(result['metric'].get('entity', ''))
            l.append(result['metric'].get('method', ''))
            try:
                l.append(round(float(result['value'][1]), 4))
            except:
                l.append(0)
            rows.append(l)

    print('')
    print("-- maximum duration of queries to methods in last 30 days --")
    print("[job, entity, method, max duration]")
    for ro in rows:
        print(ro)

    sys.stdout.flush()
    ask_user()


# get date range of data
def get_date_range():
    start_date = input("Enter start date (yyyy-mm-dd): ")
    end_date = input("Enter end date (yyyy-mm-dd): ")
    # days between start and end date
    days = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
    # check if days is equal 0 display error message
    if days == 0:
        print("Start date and end date can't be the same. Please try again.")
        get_date_range()
    # offset between start date and today
    offset = (datetime.datetime.today() - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
    # if offset is not equal 0 create offset string else create empty string
    if offset != 0:
        offset = ' offset ' + str(offset) + 'd'
    else:
        offset = ''
    # Prometheus query maximum number of sessions in date range during 1 minute
    promql_max = {'query': 'max by (job) (max_over_time(unitybase_sessions_total[' + str(days) + 'd:1m]' + offset + '))'}
    # Prometheus query average number of sessions in date range during 1 minute
    promql_avg = {'query': 'avg by (job) (avg_over_time(unitybase_sessions_total[' + str(days) + 'd:1m] ' + offset + '))'}

    print('')
    print("Unity-base maximum and average number of session during 1 minute in range " + start_date + " - " + end_date)
    print("[job, max value, avg value]")

    r1 = requests.get(url=URL, params=promql_max)
    r2 = requests.get(url=URL, params=promql_avg)

    r1_json = r1.json()['data']['result']
    r2_json = r2.json()['data']['result']

    rows = []
    for result in r1_json:
        l = []
        l.append(result['metric'].get('job', ''))
        try:
            l.append(round(float(result['value'][1]), 0))
        except:
            l.append(0)
        # find row in r2_json with same job
        for result2 in r2_json:
            if result2['metric'].get('job', '') == result['metric'].get('job', ''):
                try:
                    l.append(round(float(result2['value'][1]), 0))
                except:
                    l.append(0)
        rows.append(l)

    for ro in rows:
        print(ro)

    # Prometheus count of queries to methods in date range
    promql_count = {
        'query': 'topk(1000, sort_desc(sum by (job, entity, method) (increase('
                 'unitybase_method_duration_seconds_count[' + str(days) + 'd] ' + offset + '))))'}
    # Prometheus average duration of queries to methods in date range
    promql_avg = {'query': '''topk(1000, sort_desc(
      avg by (job, entity, method)(
        rate(unitybase_method_duration_seconds_sum[''' + str(days) + '''d] ''' + offset + ''')
        / rate(unitybase_method_duration_seconds_count[''' + str(days) + '''d] ''' + offset + ''')
       )))'''}
    # Prometheus maximum duration of queries to methods in date range
    promql_max = {'query': '''topk(1000, sort_desc(
      max by (job, entity, method)(
         max_over_time(unitybase_method_duration_seconds_sum[''' + str(days) + '''d] ''' + offset + ''')
        / avg_over_time(unitybase_method_duration_seconds_count[''' + str(days) + '''d] ''' + offset + ''')
        )))'''}

    print(promql_avg)

    r1 = requests.get(url=URL, params=promql_count)
    r2 = requests.get(url=URL, params=promql_avg)
    r3 = requests.get(url=URL, params=promql_max)

    r1_json = r1.json()['data']['result']
    r2_json = r2.json()['data']['result']
    r3_json = r3.json()['data']['result']

    print('')
    print("-- count of queries to methods in range of dates --")
    print("[job, entity, method, count of queries]")

    rows = []
    for result in r1_json:
        if result['value'][1] != '+Inf' and result['value'][1] != 'NaN':
            l = []
            l.append(result['metric'].get('job', ''))
            l.append(result['metric'].get('entity', ''))
            l.append(result['metric'].get('method', ''))
            try:
                l.append(round(float(result['value'][1]), 0))
            except:
                l.append(0)
            rows.append(l)

    for ro in rows:
        print(ro)

    print('')
    print("-- average duration of queries to methods range of dates --")
    print("[job, entity, method, average duration]")

    rows = []
    for result in r2_json:
        if result['value'][1] != '+Inf' and result['value'][1] != 'NaN':
            l = []
            l.append(result['metric'].get('job', ''))
            l.append(result['metric'].get('entity', ''))
            l.append(result['metric'].get('method', ''))
            try:
                l.append(round(float(result['value'][1]), 4))
            except:
                l.append(0)
            rows.append(l)

    for ro in rows:
        print(ro)

    print('')
    print("-- maximum duration of queries to methods range of dates --")
    print("[job, entity, method, maximum duration]")

    rows = []
    for result in r3_json:
        if result['value'][1] != '+Inf' and result['value'][1] != 'NaN':
            l = []
            l.append(result['metric'].get('job', ''))
            l.append(result['metric'].get('entity', ''))
            l.append(result['metric'].get('method', ''))
            try:
                l.append(round(float(result['value'][1]), 4))
            except:
                l.append(0)
            rows.append(l)

    for ro in rows:
        print(ro)

    sys.stdout.flush()
    ask_user()


# get prometheus endpoint url from command line argument -url
def get_url():
    global URL
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:", ["url="])
    except getopt.GetoptError:
        print('Usage: python prometheus.py -u <prometheus_url>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            URL = arg
        else:
            print('Usage: python prometheus.py -u <prometheus_url>')
            sys.exit(2)

    if URL == '':
        print('Usage: python prometheus.py -u <prometheus_url>')
        sys.exit(2)

    if URL[-1] != '/':
        URL += '/'
    URL += 'api/v1/query'

    print('Prometheus URL: ' + URL)
    print('')
    sys.stdout.flush()


# main function
def main():
    get_url()
    ask_user()


if __name__ == "__main__":
    main()  # run main function

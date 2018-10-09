import re
import numpy as np
from itertools import islice
from datetime import datetime


def create_summ_dic(file, regex_pattern, num_lines):
    """
    :param file: log file to parse
    :param regex_pattern:
    :param num_lines: first n lines to read
    :return: Two dictionaries:
                1. For month - key : [sum_of_bytes, number of requests(lines)]
                2. For exec - key : [List of all request sizes]
    Chose to use list of all request sizes for exec dictionary because had to calculate 95th percentile.
    Otherwise would have used the month dictionary for summing exec categories as well.
    """
    date_dic = {}
    exec_dic = {}
    regex = re.compile(regex_pattern)
    with open(file, 'r') as f:
        for line in islice(f, num_lines):
            match = regex.search(line)
            if match:
                resp_size = int(match.group(3))
                if resp_size > 0:  # only average non 0-sized lines
                    date_obj = datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S')
                    month = date_obj.strftime('%b')  # Extract month as three chr string

                    # Fill Date Dictionary
                    if month in date_dic:
                        date_dic[month][0] += resp_size
                        date_dic[month][1] += 1
                    else:
                        date_dic[month] = [resp_size, 1]

                    # Fill Exec Dictionary
                    exec_type = match.group(1)
                    tod = 'AM' if date_obj.hour < 12 else 'PM'

                    key = exec_type + '_' + tod
                    exec_dic.setdefault(key, []).append(resp_size)

    return date_dic, exec_dic


def create_date_summary(dic):
    """
    :param dic: Date dictionary
    Prints summary report:
    Avg response size for every month available in the dictionary
    Total average response size
    """
    total_sum = 0
    total_num_lines = 0
    for month in dic:
        total_sum += dic[month][0]
        total_num_lines += dic[month][1]
        print('%s - avg response size: %d bytes' % (month, int(dic[month][0]/dic[month][1])))
    print('Total avg response size:', int(total_sum/total_num_lines), 'bytes')


def create_exec_summary(dic):
    """
    :param dic: Exec dictionary
    Prints summary report:
    Avg response times for AM and PM calls of each type of exec
    95th percentile for each type of exec
    """
    remote = []
    local = []
    remote_AM = []
    local_AM = []
    remote_PM = []
    local_PM = []
    for item in dic:
        if 'remote' in item:
            remote += dic[item]
            if 'AM' in item:
                remote_AM += dic[item]
            elif 'PM' in item:
                remote_PM += dic[item]
        elif 'local' in item:
            local += dic[item]
            if 'AM' in item:
                local_AM += dic[item]
            elif 'PM' in item:
                local_PM += dic[item]

    print('Local exec AM - avg response size:', int(sum(local_AM)/len(local_AM)), 'bytes')
    print('Local exec PM - avg response size:', int(sum(local_PM) / len(local_PM)), 'bytes')
    print('Remote exec AM - avg response size:', int(sum(remote_AM) / len(remote_AM)), 'bytes')
    print('Remote exec PM - avg response size:', int(sum(remote_PM) / len(remote_PM)), 'bytes')
    print('95th p of all remote calls:', int(np.percentile(remote, 95)))
    print('95th p of all local calls:', int(np.percentile(local, 95)))


if __name__ == "__main__":

    file_name = 'access_log.log'
    regex_pattern = r'(.+) - - \[(.*) -0.* (\d+$)'
    num_of_lines = 150000  # picked to only read first 150000 lines because something wrong with unicode encoding of log

    date_dic, exec_dic = create_summ_dic(file_name, regex_pattern, num_of_lines)

    create_date_summary(date_dic)
    create_exec_summary(exec_dic)

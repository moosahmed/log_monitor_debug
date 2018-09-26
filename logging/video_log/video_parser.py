import re
from datetime import datetime, timedelta
import operator


def parser(file):
    pattern = re.compile(r'(.*) *(userid.*) *(start|stop) *(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2})')
    start = {}
    stop = {}
    for line in file:
        match = pattern.search(line)
        if match:
            dt_obj = datetime.strptime(match.group(4), '%m/%d/%Y-%H:%M:%S')  # Read time as datetime_obj
            if datetime.today() - dt_obj <= timedelta(7):  # Use only the dates within the last 7 days

                # Within the start and stop dictionary, initiate a dictionary per video_id
                # Where the key is user id and value is a list of times
                if match.group(3) == 'start':
                    start.setdefault(match.group(1), {}).setdefault(match.group(2), []).append(dt_obj)
                elif match.group(3) == 'stop':
                    stop.setdefault(match.group(1), {}).setdefault(match.group(2), []).append(dt_obj)

    return start, stop


def calc_duration(start_dic, stop_dic):
    duration = {}
    for video_id in start_dic:
        for user_id in start_dic[video_id]:

            # Zip start and stop times for the same user for a particular video
            for start_time, stop_time in zip(start_dic[video_id][user_id], stop_dic[video_id][user_id]):
                td = stop_time - start_time
                duration[video_id] = duration.get(video_id, timedelta()) + td  # Add all durations for the same video
    max2 = dict(sorted(duration.items(), key=operator.itemgetter(1), reverse=True)[:2])  # Selecting top 2
    print(max2)


if __name__ == '__main__':
    file = open('./video.log', 'r')
    start, stop = parser(file)
    calc_duration(start, stop)
    file.close()

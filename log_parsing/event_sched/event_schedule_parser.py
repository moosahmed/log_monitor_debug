import re

from collections import namedtuple
from datetime import datetime, timedelta

entry = namedtuple('entry', ['time', 'name'])


def parser(file, pattern):
    """
    :param file: file to parse
    :param pattern: regex pattern to match
    :return: a list of named tuples with the timestamp of start of event and name of event
    """
    infile = open(file, 'r')
    regex = re.compile(pattern)

    sced_list = []
    for line in infile:
        match = regex.search(line)

        if match:
            datetime_obj = datetime.strptime(match.group(1), '%H:%M')  # Extract time as datetime obj
            in_tup = entry(datetime_obj, match.group(2))               # Group date and event in a namedtuple
            sced_list.append(in_tup)                                   # Add tuple to schedule  list

    return sced_list


def process_events(event_list, writefile):
    """
    :param event_list: list from parser()
    :param writefile: output file to write to
    :return: A dictionary with events and their time duration as well as the total time of the event
    Writes to the output file the schedule in the desired format
    """
    summary_dict = {}
    total_time = timedelta()
    for event, next_event in zip(event_list, event_list[1:]):  # Zip through same list with one offset to use next event
        if event.name != 'End':
            writefile.write('%02d:%02d-%02d:%02d %s\n' % (
                event.time.hour, event.time.minute, next_event.time.hour, next_event.time.minute, event.name))

            # Populate a dictionary with event name and total duration
            summary_dict[event.name] = summary_dict.get(event.name, timedelta()) + (next_event.time - event.time)
            total_time += (next_event.time - event.time)
        else:
            writefile.write('\n')  # Add a new line between days

    return summary_dict, total_time


def write_summary_out(summary_dict, time, writefile):
    """
    :param summary_dict: dictionary from process_events()
    :param time: total time of the event
    :param writefile: output file to write to
    Writes the summary portion of the desired output
    """
    writefile.write('\n')  # Add a line between timeline and summary
    for key, value in summary_dict.items():
        writefile.write('%-20s %3s minutes %4d%%\n' % (key, (value.seconds//60), ((value/time)*100)))


if __name__ == "__main__":
    pattern = r'(\d*:\d*) (\w*)'
    infile = './event_schedule.log'
    outfile = './event_schedule_out.log'

    writefile = open(outfile, "w")
    summary_dict, total_time = process_events(parser(infile, pattern), writefile)
    write_summary_out(summary_dict, total_time, writefile)
    writefile.close()

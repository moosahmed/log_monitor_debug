import re

from datetime import datetime


def run_re(pattern, file):

    re_obj = re.compile(pattern)
    infile = open(file, 'r')

    match_count = 0
    cron_dict = {}

    for line in infile:
        match = re_obj.search(line)
        if match:
            match_count += 1

            tmp_time = line[:15]
            datetime_obj = datetime.strptime(tmp_time, '%b %d %H:%M:%S')

            cron_dict.setdefault(match.group(1), []).append(datetime_obj)

    infile.close()
    return match_count, len(cron_dict), cron_dict


def calc(dix, outfile):
    outfile = open(outfile, "w")
    for key, value in dix.items():
        count = len(value)
        dtdelta = abs(value[-1] - value[0])
        delay = dtdelta/(count - 1)

        outfile.write('command: %s...\ncount: %d\ndelay: %s\n\n' % (key[:50], count, delay))

    outfile.close()


if __name__ == "__main__":
    pattern = "CROND\[[0-9]*\]: \(root\) CMD (.*)"
    file = "../files/cron/cron_for_parsing_exercise.log"
    out_file = "../files/cron/cron_out.log"

    match_count, unq_cron, result_dict = run_re(pattern, file)
    print('Matches:', match_count)
    print('Unique Crons:', unq_cron)

    calc(result_dict, out_file)

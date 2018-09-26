import re


def parser(file):
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(\d{3}) (\d+)')
    dic = {}
    for line in file:
        match = pattern.search(line)
        if match:
            dic[match.group(1)] = dic.get(match.group(1), 0) + int(match.group(3))
            print(dic)


file = open('./apache.log', 'r')
parser(file)
file.close()
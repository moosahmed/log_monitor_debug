# get number of requests per IP

import re

regex = re.compile(r'^(\d+\.\d+\.\d+\.\d+)')

file = open('apache.log', 'r')

dic = {}
for line in file:
    match = regex.search(line)
    if match:
        dic[match.group(1)] = dic.get(match.group(1), 0) + 1
file.close()

print(dic)

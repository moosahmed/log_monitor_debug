import regex

arr = ['({(){([])}[]})','(a)d[b]e{c}','()]','([)]','{a[b]c}']

pattern = regex.compile(r'^((?:[^{\[()\]}]*|\((?1)\)|\[(?1)\]|\{(?1)\})*)$')

for i in arr:
    match = pattern.search(i)
    if match:
        print(match.group(), 'True')
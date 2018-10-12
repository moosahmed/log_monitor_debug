import regex

subjects = ['dontmatchme','kook','book','paper','kayak','okonoko','aaaaa','bbbb']

pattern = regex.compile(r'\b((\w)(?:(?1)|\w?)\2)\b')

for sub in subjects:
    match = pattern.search(sub)
    print(match)
    if match:
        print(match.group(), 'True')
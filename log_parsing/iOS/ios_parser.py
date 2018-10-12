import re
import regex

reg = regex.compile(r'<property name="(.*?)">(.*?)</property>')

out = []

with open('sfbios.log', 'r') as f:
    for line in f:
        match = reg.search(line)
        if match and match.group(2) == "Enabled":
            out.append((match.group(1), match.group(2)))

with open('filtered.txt', 'w') as f:
    f.write("EXPORTED DATA:\n")
    out_clean = list(set(out))
    for item in out_clean:
        print(item)
        f.write(str(item) + "\n")

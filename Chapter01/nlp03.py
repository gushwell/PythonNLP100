import re

text = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
array = re.split(r'\s|,|\.', text)

lens = [len(x) for x in array if len(x) > 0]
print(lens)
   
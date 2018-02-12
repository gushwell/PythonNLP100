import re

text = "Hi He Lied Because Boron Could Not Oxidize Fluorine. "\
       "New Nations Might Also Sign Peace Security Clause. Arthur King Can."
array = re.split(r'\s|,|\.', text)
words = [s for s in filter(lambda w: len(w) > 0, array)]
worddict = {}
for i, e in enumerate(words, 1):
    length = 1 if i in [1, 5, 6, 7, 8, 9, 15, 16, 19] else 2
    worddict[e[0:length]] = i
print(worddict.items())

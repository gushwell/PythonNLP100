def ngram(s, n):
    items = []
    last = len(s) - n + 1
    for i in range(last):
        items.append(s[i: i+n])
    return items
 
text = "I am an NLPer"
x = ngram(text, 2)
print(x)
x = ngram(text.split(), 2)
print(x)
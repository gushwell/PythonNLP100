def ngram(s, n):
    items = []
    last = len(s) - n + 1
    for i in range(last):
        items.append(s[i: i+n])
    return items
 
text1 = "paraparaparadise"
text2 = "paragraph"
x = set(ngram(text1, 2))
y = set(ngram(text2, 2))
 
print("x:", x)
print("y:", y)
 
union = x | y
print("\n和集合(x | y):")
print(union)
 
intersection = x & y
print("\n積集合(x & y):")
print(intersection)
 
difference1 = x - y
print("\n差集合(x - y):")
print(difference1)
 
print('')
print('seがxに含まれる:', ('se' in x))
 
issubset = {'se'} <= y
print('seがyに含まれる:', issubset)

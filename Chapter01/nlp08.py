def cipher(s):
    r = ''
    for c in s:
        r += chr(219 - ord(c)) if c.islower() else c
    return r
 
def main():
    x = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    r = cipher(x)
    print(r)
    print(cipher(r))
 
main()

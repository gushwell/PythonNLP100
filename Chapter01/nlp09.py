import random
 
def Typoglycemia(word):
    length = len(word)
    if length < 5:
        return word
    s = word[0]
    e = word[-1:]
    m = list(word[1:-1])
    random.shuffle(m)
    return s + "".join(m) + e
 
def main():
    text = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    words = text.split(' ')
    result = []
    for word in words:
        result.append(Typoglycemia(word))
    print(" ".join(result))
 
if __name__ == '__main__':
    main()
    
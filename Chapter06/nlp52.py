from nltk import stem

def enumStem():
    stemmer = stem.PorterStemmer()
    #stemmer = stem.LancasterStemmer()
    with open('result51.txt', 'r', encoding='utf8') as fin:
        for line in fin:
            word = line.rstrip('\n')
            if word != '':
                yield word, stemmer.stem(word)

def main():
    with open('result52.txt', 'w', encoding='utf8') as w:
        for word, stm in enumStem():
            w.write(f'{word}\t{stm}\n')

if __name__ == '__main__':
    main()

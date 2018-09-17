

class Stopwords:
    words = ['a', 'about', 'all', 'an', 'and', 'any', 'are', 'as', \
            'at', 'be', 'been', 'but', 'by', 'can', 'could', 'do', \
            'does', 'for', 'from', 'has', 'have', 'he', 'her', 'his', \
            'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'made', \
            'make', 'may', 'me', 'my', 'no', 'not', 'of', 'on', 'one', \
            'or', 'out', 'she', 'should', 'so', 'some', 'than', 'that', \
            'the', 'their', 'them', 'there', 'then', 'they', 'this', \
            'those', 'to', 'too', 'us', 'was', 'we', 'what', 'when',\
            'which', 'who', 'with', 'would', 'you', 'your', ''
        ]

    @staticmethod
    def exists(word):
        return word in  Stopwords.words

def test():
    w = 'in'
    print(w, Stopwords.exists(w))
    w = 'what'
    print(w, Stopwords.exists(w))
    w = 'list'
    print(w, Stopwords.exists(w))
    w = 'yes'
    print(w, Stopwords.exists(w))

def main():
    test()

if __name__ == '__main__':
    main()

import re

def enumWords():
    with open('result50.txt', 'r', encoding='utf8') as fin:
        for line in fin:
            words = re.split(r'[\s\.",:;()]+', line)
            for w in words:
                if re.match(r'^[a-zA-Z]', w):
                    yield w

def main():
    with open('result51.txt', 'w', encoding='utf8') as w:
        w.writelines([x + '\n' for x in enumWords()])

if __name__ == '__main__':
    main()

import random

def AddPlus():
    lines = []
    with open('rt-polarity.pos', 'r', encoding='cp1252') as fin:
        for line in fin:
            lines.append('+1 ' + line)
    return lines

def AddMinus():
    lines = []
    with open('rt-polarity.neg', 'r', encoding='cp1252') as fin:
        for line in fin:
            lines.append('-1 ' + line)
    return lines

def CreateText():
    lines = AddPlus() + AddMinus()
    random.shuffle(lines)
    with open('chap08/sentiment.txt', 'w') as fout:
        fout.writelines(lines)


def main():
    CreateText()

if __name__ == '__main__':
    main()

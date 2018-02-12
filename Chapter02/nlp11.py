import re

def tabToSpace(source):
    return re.sub(r'\t', ' ', source)

def main():
    with open('hightemp.txt', 'r', encoding='utf8') as f:
        for line in f:
            print(tabToSpace(line.rstrip()))

    with open('hightemp.txt', 'r', encoding='utf8') as f:
        print(tabToSpace(f.read()))

if __name__ == '__main__':
    main()

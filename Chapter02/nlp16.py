import sys
import os.path

def split(filename, n):
    with open(filename, 'r', encoding='utf8') as fin:
        lines = fin.readlines()
        total = len(lines)
        div = [(total + i) // n for i in range(n)]
    start = 0
    for i in range(n):
        end = start + div[i]
        with open(getFileName(filename, i+1), 'w', encoding='utf8') as fout:
            fout.writelines(lines[start:end])
        start = end

def getFileName(filename, n):
    name, ext = os.path.splitext(filename)
    return name + str(n) + ext

def main():
    n = int(sys.argv[1])
    split('hightemp.txt', n)

if __name__ == '__main__':
    main()

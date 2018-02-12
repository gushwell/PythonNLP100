import sys

def head(fin, fout, count):
    for _ in range(count):
        line = fin.readline()
        fout.write(line)

def main():
    n = int(sys.argv[1])
    with open('hightemp.txt', 'r', encoding='utf8') as f:
        head(f, sys.stdout, n)

if __name__ == '__main__':
    main()

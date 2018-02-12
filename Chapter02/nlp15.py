import sys
 
def tail(fin, fout, count):
    lines = fin.readlines()
    fout.writelines(lines[-count:])

def main():
    n = int(sys.argv[1])
    with open('hightemp.txt', 'r', encoding='utf8') as f:
        tail(f, sys.stdout, n)

if __name__ == '__main__':
    main()

def sortBytemp(filename):
    with open(filename, 'r', encoding='utf8') as fin:
        lines = fin.readlines()
        #lines.sort(key=lambda x: float(x.split()[2]))
        #return lines
        return sorted(lines, key=lambda x: float(x.split()[2]))

def main():
    lines = sortBytemp('hightemp.txt')
    for line in lines:
        print(line.rstrip())

if __name__ == '__main__':
    main()

def solve(infile, outfile1, outfile2):
    with open(infile, 'r', encoding='utf8') as f, \
         open(outfile1, 'w', encoding='utf8') as fw0, \
         open(outfile2, 'w', encoding='utf8') as fw1:
        for line in f:
            words = line.split('\t')
            fw0.write(words[0] + '\n')
            fw1.write(words[1] + '\n')
def main():
    solve('hightemp.txt', 'col1.txt', 'col2.txt')

if __name__ == '__main__':
    main()

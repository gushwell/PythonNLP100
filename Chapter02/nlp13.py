def solve(infile1, infile2, outfile):
    with open(outfile, 'w', encoding='utf8') as fw, \
         open(infile1, 'r', encoding='utf8') as fr1, \
         open(infile2, 'r', encoding='utf8') as fr2:
        for word1, word2 in zip(fr1, fr2):
            fw.write(word1.rstrip() + '\t' + word2)

def main():
    solve('col1.txt', 'col2.txt', 'connected.txt')

if __name__ == '__main__':
    main()

def gatherPrefecture(filename):
    collection = set([])
    with open(filename, 'r', encoding='utf8') as fin:
        for line in fin:
            pref = line.split()[0]
            collection.add(pref)
    return collection

def main():
    prefs = gatherPrefecture('hightemp.txt')
    for name in prefs:
        print(name)

if __name__ == '__main__':
    main()

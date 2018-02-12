def appearanceRate(filename):
    prefDict = {}
    with open(filename, 'r', encoding='utf8') as fin:
        for line in fin:
            pref = line.split()[0]
            if pref in prefDict:
                prefDict[pref] += 1
            else:
                prefDict[pref] = 1
    return sorted(prefDict.items(), key=lambda x: x[1], reverse=True)

def main():
    lines = appearanceRate('hightemp.txt')
    for k, _ in lines:
        print(k)

if __name__ == '__main__':
    main()

def countLine(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        count = 0
        for _ in f:
            count += 1
    return count
 
def main():
    count = countLine('hightemp.txt')
    print(count)
 
if __name__ == '__main__':
    main()

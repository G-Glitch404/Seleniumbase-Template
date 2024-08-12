def extract_links(keyword: str = "http", filename: str = "'logger.log'"):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if keyword not in line: continue
            yield 'http' + line.split('http')[-1].split(' ', 1)[0]


if __name__ == '__main__':
    for data in extract_links():
        print(data)

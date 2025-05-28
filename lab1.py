d = {'0':'ноль', '2':'два', '4':'четыре', '6':'шесть', '8':'восемь',
     'A':'десять', 'C':'двенадцать', 'E':'четырнадцать'}

numbers = []
buffer = ''

with open('text.txt', 'r') as f:
    while block := f.readline(1024):
        for c in block:
            if c.upper() in '0123456789ABCDEF':
                buffer += c.upper()
            else:
                if len(buffer) > 1 and buffer[1] == 'B':
                    try:
                        num = int(buffer, 16)
                        numbers.append(num)
                    except ValueError:
                        pass
                buffer = ''

for num in sorted(numbers):
    s = hex(num)[2:].upper()
    res = ' '.join(d.get(c, c) for c in s)
    print(res)
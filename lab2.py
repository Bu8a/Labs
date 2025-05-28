import re

d = {'0':'ноль', '2':'два', '4':'четыре', '6':'шесть', '8':'восемь',
     'A':'десять', 'C':'двенадцать', 'E':'четырнадцать'}

with open('text.txt') as f:
    nums = sorted(int(m.group(), 16) for m in re.finditer(r'\b[0-9A-Fa-f][Bb][0-9A-Fa-f]*\b', f.read()))

for num in nums:
    s = hex(num)[2:].upper()
    res = ' '.join(d.get(c, c) for c in s)
    print(res)
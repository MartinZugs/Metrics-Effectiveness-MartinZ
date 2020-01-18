import random

with open('node.csv', 'r',encoding="utf8") as r, open('nodeshuffled.csv', 'w',encoding="utf8") as w:
    data = r.readlines()
    header, rows = data[0], data[1:]
    random.shuffle(rows)
    rows = '\n'.join([row.strip() for row in rows])
    w.write(header + rows)

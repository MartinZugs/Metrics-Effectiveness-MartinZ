import random

with open('oh-my-zshshuffled.csv', 'r',encoding="utf8") as r, open('iptvshuffled.csv', 'r',encoding="utf8") as r4, open('jqueryshuffled.csv', 'r',encoding="utf8") as r3, open('nodeshuffled.csv', 'r',encoding="utf8") as r2, open('ziplineshuffled.csv', 'r',encoding="utf8") as r1, open('ML CSVs/new.csv', 'w',encoding="utf8") as w:
    data1 = r.readlines()
    data2 = r1.readlines()
    data3 = r2.readlines()
    data4 = r3.readlines()
    data5 = r4.readlines()
    header, rows = data1[0], data1[1:] + data2[1:] + data3[1:] + data4[1:] + data5[1:]
    random.shuffle(rows)
    rows = '\n'.join([row.strip() for row in rows])
    w.write(header + rows)

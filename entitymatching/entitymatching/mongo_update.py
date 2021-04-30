from pymongo import MongoClient
from bibtexparser.bparser import BibTexParser

conn = MongoClient("localhost", 27017)
print("Connected successfully!")

final_db = conn.final_em_test

old_db = conn.em_test

bib_item = old_db.bibtexitem
main_item = old_db.mainitem
pub_item = old_db.publicationitem


# author's item as list
author_info = []
author_new = []
Author = main_item.find({})
for name in Author:
    author_info.append(name.values())

for e in author_info:
    for r in e:
        author_new.append(r)
author_new.pop(0)


# pub's item as list
pub_info = []
pub_new = []
Pub = pub_item.find({})
for n in Pub:
    pub_info.append([n.values()])

for li in pub_info:
    for e in li:
        t = []
        for r in li:
            for v in r:
                t.append(v)
        pub_new.append(t)


for i in range(len(pub_info)):
    pub_new[i].pop(0)


# bib items as list
bib_info = []
bib_new = []
Bib = bib_item.find({})
for n in Bib:
    bib_info.append([n.values()])

for li in bib_info:
    for e in li:
        t = []
        for r in li:
            for v in r:
                t.append(v)
        bib_new.append(t)

bib_ids = []

for i in range(len(bib_info)):
    bib_new[i].pop(0)
    bib_ids.append(bib_new[i][-1])
    bib_new[i].pop(-1)

parser = BibTexParser()

db = []
db_new = []
for article in bib_new:
    for s in article:
        db.append([parser.parse(s).entries])
for i in db:
    for e in i:
        for o in e:
            if o not in db_new:
                db_new.append(o)

bfp = []
j = 0
count = 0
while True:
    a = pub_new[j][5]
    a = int(a)
    if a > 0:
        bfp.append(a)
        j = j + 1
    else:
        break


bib_titles = []
tem = []
a = 0
b = 0
for v in bfp:
    for j in range(b + v):
        tem.append((db_new[j + a]))
    bib_titles.append(tem.copy())
    tem.clear()
    a = a + v


an = {"ID": author_new[2], "Author": author_new[0], "Url": author_new[1], "Citations": author_new[3],
      "H index": author_new[4], "i10-index": author_new[5], "Publication": []}

k = -1
for e in pub_new:
    k = k + 1
    if "Publication" in an:
        an["Publication"].append(
            {"Author_id": e[1], "Publication_id": e[6], "Title": e[0], "Authors": e[2], "Journal": e[3],
             "Year": e[4], "BibTex Citations": e[5], "Bib": [bib_titles[k]] if k < len(bib_titles) else []})

collection = final_db["Scholar Author"]

collection.insert_many(an)


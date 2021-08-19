from pymongo import MongoClient
from bibtexparser.bparser import BibTexParser


#   Connecting to MongoDB
conn = MongoClient("localhost", 27017)
print("Connected successfully!")

# TODO: verificare che non ci siano duplicati in bib

#   Saving the db. The form is conn.<db name>.
#   TODO: change it in order to make it change when the scrapy db name changes
origin_db = conn.em_test


#   Saving collection names
bibtex_fields = origin_db.bibtexitem
publication_fields = origin_db.publicationitem
author_fields = origin_db.mainitem


#   Saving in a dictionary the publication id (k) and how many bibtex fields they have (v)[Saving only if the v > 0)
n_of_bibtex_cits = {}
pubs = publication_fields.find({})
for publication in pubs:
    if publication["N_Citations"] != 0:
        n_of_bibtex_cits[publication["p_ID"]] = int(publication["N_Citations"])


#   Saving bibtex ids in order to match them with the publication associated to them
bib_ids = []
bib = bibtex_fields.find({})
for field in bib:
    bib_ids.append(field["_id"])


# #   Updating all bibtex articles with the publication that they cite
# minimum = 0
# maximum = 0
# k = 0
# for j in n_of_bibtex_cits:
#     maximum = maximum + n_of_bibtex_cits[j]
#     for i in range(minimum, maximum):
#         test = bibtex_fields.find_one_and_update(
#             {"_id": bib_ids[i]},
#             {"$set": {"p_ID": j}},
#             upsert=True
#         )
#     minimum = minimum + maximum
#     k = k + 1


#   Parsing "Type" field in order to make it a BibTex item. Then removing old "Type" field.
#   If Key Error then this operation was already done.
try:
    parser = BibTexParser()
    ids = []
    p_ids = []
    bib = bibtex_fields.find({})
    for field in bib:
        ids.append(field["_id"])
        to_add = field["Type"]
        p_ids.append(field["p_ID"])
        parsed_bib = parser.parse(to_add).entries

    j = 0
    for i in ids:
        bibtex = bibtex_fields.find_one_and_update(
            {"_id": i},
            {"p_ID": p_ids[i]},
            {"$set": {"BibTex Info": parsed_bib[j]}},
            upsert=True
        )
        j = j + 1

    bibtex = bibtex_fields.update_many(
        {},
        {"$unset": {"Type": 1}},
    )

except KeyError:
    pass


#   Create a dictionary that is composed by author, publication and bibtex with a nested structure
final_author = {}
authors = author_fields.find({})
publications = publication_fields.find({})
bibtexs = bibtex_fields.find({})
count = 0

bibtexs2 = []
for b in bibtexs:
    bibtexs2.append(b)


publications2 = []
for publication in publications:
    publications2.append(publication)

for publication in publications2:
    temp = []
    for b in bibtexs2:
        copy = {}
        if b["p_ID"] == publication["p_ID"]:
            b_keys = list(b.keys())
            b_values = list(b.values())
            i = 0
            for i in range(len(b.keys())):
                copy[b_keys[i]] = b_values[i]
            temp.append(copy)
    publication["BibTexs"] = temp

for author in authors:
    id_number = author["a_ID"]
    a_keys = list(author.keys())
    a_values = list(author.values())
    for a_key in a_keys:
        final_author[a_key] = a_values[count]
        for publication in publications2:
            if publication["a_ID"] == id_number:
                final_author["Publications"] = publications2
        count = count + 1


final_db = conn.final_em_test
collection = final_db["Scholar Author 1"]

collection.insert_one(final_author)

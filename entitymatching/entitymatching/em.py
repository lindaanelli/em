import py_stringmatching as sm
from pymongo import MongoClient


conn = MongoClient("localhost", 27017)
print("Connected successfully!")

scholar_db = conn.final_simonini3
scopus_db = conn.scopus

scholar_coll = scholar_db.Simonini
scholar_records = scholar_coll.find({})
publications = scholar_records.distinct("Publications")
scholar_titles = []
for publication in publications:
    scholar_titles.append(publication["Title"])

scopus_coll = scopus_db.Simonini
scopus_records = scopus_coll.find({})
scopus_titles = []
for r in scopus_records:
    for i in r:
        if i == "_id":
            continue
        scopus_titles.append(r[i]["Title"])

alphabet_tok_set = sm.AlphabeticTokenizer(return_set=True)
jac = sm.Jaccard()
for scht in scholar_titles:
    for sct in scopus_titles:
        score = jac.get_raw_score(alphabet_tok_set.tokenize(scht), alphabet_tok_set.tokenize(sct))
        if score > 0.5:
            print(score)
            print(scht)
            print(sct)
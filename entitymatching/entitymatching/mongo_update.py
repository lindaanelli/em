from pymongo import MongoClient


conn = MongoClient("localhost", 27017)
print("Connected successfully!")

final_db = conn.final_em_test

sa = final_db.scholar_author


old_db = conn.em_test

bib_item = old_db.bibtexitem
main_item = old_db.mainitem
pub_item = old_db.publicationitem


author = {
    "ID": "",
    "Author": "",
    "Url": "",
    "Citations": "",
    "H index": "",
    "i10-index": "",
    "Publications": {
        "Title": "",
        "Authors": "",
        "Journal": "",
        "Year": "",
        "Number of citations": "",
        "BibTeX citations": {
            "Type": ""
        }
    }
}




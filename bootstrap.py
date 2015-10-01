#!/usr/bin/python

import csv
from tokenizer import tokenize
from datetime import datetime
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

csv.field_size_limit(1000000000)

# Returns an iterator for the docs to tokenize/process
# Each iteration returns a dict with {id: "", text: "", date: ""}
def get_docs():
    # Fields:
    # RequestID,StartDate,EndDate,AgencyName,AgencyDivision,               [0-4]
    # TypeOfNoticeDescription,CategoryDescription,ShortTitle,              [5-7]
    # SelectionMethodDescription,SectionName,                              [8-9]
    # SpecialCaseReasonDescription,PIN,DueDate,AddressToRequest,         [10-13]
    # ContactName,ContactPhone,Email,ContractAmount,ContactFax           [11-15]
    # AdditionalDescription1,AdditionalDesctription2,                    [16-17]
    # AdditionalDescription3,OtherInfo1,OtherInfo2,OtherInfo3,           [18-21]
    # VendorName,VendorAddress,Printout1,Printout2,Printout3,            [22-26]
    # DocumentLinks,EventDate,EventBuildingName,EventStreetAddress1,     [27-30]
    # EventStreetAddress2,EventCity,EventStateCode,EventZipCode          [31-34]
    data_file = open('data.csv', 'rb')
    docs = []
    with data_file as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            if index == 0:
                continue

            id = row[0]
            date = row[1]
            string = row[3] + row[4] + row[7] + row[16] + row[17] + \
                  row[18] + row[19] + row[20] + row[21] + row[24] + \
                  row[25] + row[26]

            docs.append({
                'id': id,
                'date': datetime.strptime(date, "%m/%d/%Y"),
                'text': string,
                'agency': row[3],
                'shortTitle': row[7],
                'description': row[16] + ("\n" + row[17] if row[17] else "") + ("\n" + row[18] if row[18] else "")
            })

    data_file.close()
    return docs

# Make the doc vectors using tfidf weights + insert them in mongo
def train_model_and_save():
    hearings = MongoClient().hearings.hearings

    doc_objects = get_docs()
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english', ngram_range=(1,3))
    doc_term_weighted_matrix = tfidf.fit_transform(map(lambda x: x["text"], doc_objects))

    feature_names = tfidf.get_feature_names()
    for row in xrange(0, len(doc_objects)):
        doc = doc_objects[row]
        doc_dict = {}
        doc_row = doc_term_weighted_matrix.getrow(row)

        for nonzero_col in doc_row.nonzero()[1]:
            doc_dict[feature_names[nonzero_col]] = doc_row[0, nonzero_col]

        hearings.insert({
            "_id": doc["id"],
            "human_info": {
                "agency": doc["agency"],
                "shortTitle": doc["shortTitle"],
                "description": doc["description"]
            },
            "features": doc_dict,
            "date": doc["date"]
        })

if __name__ == '__main__':
    train_model_and_save()

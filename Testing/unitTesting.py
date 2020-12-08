from datetime import date
from util.DBconnector import DBConnector

import firebase_admin

from firebase_admin import credentials, firestore , storage

import uuid
'''
today = date.today()

# dd/mm/YY
d1 = today.strftime("%Y-%m-%d 00:00")
print("d1 =", d1)

# Textual month, day and year
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)
'''

db = DBConnector()
#db.uploadDocToCollection("videos",doc="test1",data={"test": 1})
#db.uploadDataToDoc("videos/"+str(uuid.uuid4()),{"test": 1})

blob = storage.bucket(db.bucket_name).blob(blob_name="ooooo1")
#print(blob)

blob.metadata = {

        "downloadURLs":[ str(uuid.uuid4())]

  }
blob.upload_from_filename("wordBank.txt")




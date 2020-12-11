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

#db = DBConnector()
#db.upload(r"C:\Users\User\Desktop\youtube\Beginners Back Exercises that Strengthen your Back-TGI5TFnY8Ck.mp4","llll")
#db.uploadDocToCollection("videos",doc="test1",data={"test": 1})
#db.uploadDataToDoc("videos/"+str(uuid.uuid4()),{"test": 1})
'''
bloblist = []
blobs = storage.bucket(db.bucket_name).list_blobs()
for blob in blobs:
    print(blob.metadata)
    bloblist.append(blob.name)



blob1 = storage.bucket(db.bucket_name).blob(bloblist[0])

blob1.metadata={'type': "uuu"}
blob1.patch()
#blob1.update()

blobs = storage.bucket(db.bucket_name).list_blobs()
for blob in blobs:
    print(blob.metadata)


{'firebaseStorageDownloadTokens': '87972122-aed8-4cbd-b54c-dc4ab3ecfa5f'}
{'downloadURLs': "['cb4a2cf5-b687-4ccb-8e0e-4f39a0bc2d2f']", 'firebaseStorageDownloadTokens': '229a875b-c1ef-4bb8-af4f-583ebafba6ef,f8fa53bf-1127-40cf-9157-fb6bcd75b9f4'}
{'firebaseStorageDownloadTokens': '778ad74f-0010-411d-b667-3f2ef561e2b0'}
{'firebaseStorageDownloadTokens': '87972122-aed8-4cbd-b54c-dc4ab3ecfa5f'}
{'downloadURLs': "['cb4a2cf5-b687-4ccb-8e0e-4f39a0bc2d2f']", 'firebaseStorageDownloadTokens': 'a0ebbbf4-0cdd-402f-97b8-d42557997be1'}
{'firebaseStorageDownloadTokens': '778ad74f-0010-411d-b667-3f2ef561e2b0'}
'''

print(date.today())


import firebase_admin

from firebase_admin import credentials, firestore , storage


class DBConnector:

    #bucket_name = 'pythontest-672b7.appspot.com'
    bucket_name='physovid.appspot.com'
    #certificate = 'pythontest-672b7-firebase-adminsdk-yg99h-31b07b33ca.json'
    certificate=r"C:\Users\User\PycharmProjects\FinalProject\util\physovid-firebase-adminsdk-nufmg-b1bd2eb903.json"
    TIME_OUT_DEF = 300000
    def __init__(self):
        cred = credentials.Certificate(self.certificate)
        firebase_admin.initialize_app(cred, {'storageBucket': self.bucket_name})
        self.db = firestore.client()





    def upload(self,name_of_file,name_to_Blob):
       blob = storage.bucket(self.bucket_name).blob(blob_name=name_to_Blob,chunk_size=262144*4)
       blob.upload_from_filename(name_of_file, timeout=DBConnector.TIME_OUT_DEF)





    def download(self,name_of_file_in_bucket,name_of_path_to):
        storage.bucket(self.bucket_name).blob(name_of_file_in_bucket).download_to_filename(name_of_path_to, timeout=DBConnector.TIME_OUT_DEF)


    def uploadDocToCollection(self,toCollection,doc,data):
      self.db.collection(toCollection).document(doc).set(data)

    def delete(self,name_of_file):
        storage.bucket(self.bucket_name).delete_blob(name_of_file)


    def uploadDataToDoc(self,toDocPath,data):
      self.db.document(toDocPath).set(data)

    def upDateDataToDoc(self, toDocPath, data):
        self.db.document(toDocPath).update(data)


    # users_ref = db.
    # docs = users_ref.stream()

    # for doc in docs:
    #    print(f'{doc.id} => {doc.to_dict()}')
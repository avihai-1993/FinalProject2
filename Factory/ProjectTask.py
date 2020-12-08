from util.Craweler import Craweler
from util.YouTubeDownLoader import YouTubeDownLoader
from util.DBconnector import DBConnector
import uuid
class Task:
    def __init__(self,searchWord , wordbank,outputDir):
        self.searchWord = searchWord
        self.wordbank = wordbank
        self.keys = set()
        self.urls = set()
        self.output_dir = outputDir


    def start(self,depth,startURL=None):
         downloader = YouTubeDownLoader(self.output_dir)
         c = Craweler()
         DBcon = DBConnector()
         if startURL == None:
          starturl = c.getOnlyYTFromGoogleVids(self.searchWord)
          c.findkeysCrawel(starturl, depth, self.keys)

         else:
            c.findkeysCrawel(startURL, depth, self.keys)


         for key in self.keys:
             file_output_path, data = downloader.downloadViaPytube(key,self.output_dir,self.wordbank,self.searchWord)
             if file_output_path is not None and data is not None:
                 DBcon.upload(name_of_file=file_output_path, name_to_Blob=key)
                # blob1 = DBcon.storage.bucket(DBcon.bucket_name).blob(key)
                 #blob1.metadata = {'firebaseStorageDownloadTokens': uuid.uuid4()}
                 #blob1.patch()

                 DBcon.uploadDataToDoc("pathDB", data)
                #DBcon.uploadDocToCollection("colllction","doc",data)

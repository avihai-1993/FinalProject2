from util.Craweler import Craweler
from pytube import *
from util.DBconnector import DBConnector
import uuid
class Task:
    def __init__(self,searchWord , type):
        self.searchWord = searchWord
        self.type = type
        self.keys = set()
        self.urls = set()

    def start(self,depth,startURL=None):
         c = Craweler()
         if startURL == None or startURL == '':
              starturl = c.getOnlyYTFromGoogleVids(self.searchWord)
              c.findkeysCrawel(starturl, depth, self.keys)
         else:
              c.findkeysCrawel(startURL, depth, self.keys)

        #TODO key Sync


        #TODO save the last url Done vvvv

         save_dict_to_setting = {
             'lastTaskUrl': c.lastSearchUrlFromCrawelingOpartion
         }
         DBConnector().uploadDataToDoc("settings/"+self.type+"/keywords/"+self.searchWord,save_dict_to_setting)

         for key in self.keys:
             self.upload_via_key_strem(key,self.type)




    def upload_via_key_strem(self,youtubeKeyStream, videotype):
        try:
            url = "https://www.youtube.com/watch?v=" + youtubeKeyStream
            youTubeVideoRef = YouTube(url)
            data = {
                "title": youTubeVideoRef.title,
                "length": youTubeVideoRef.length / 60 ,
                "publishDate": youTubeVideoRef.publish_date,
                "views": 0,
                "rating": None,
                "YTSK": youtubeKeyStream,
                "type": videotype,
            }
            print(data)
            db = DBConnector()
            db.uploadDataToDoc("videos/" + str(uuid.uuid4()), data)
        except Exception as e:
            print(e.__str__())
            return


from util.Craweler import Crawler
from pytube import *
from util.DBconnector import DBConnector
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp


class Task:
    def __init__(self, searchWord ,type):
        self.searchWord = searchWord
        self.type = type
        self.keys = set()
        self.backup = SqlLiteKeyBackUp()
        self.c = Crawler()
        self.fsdb = DBConnector()


    def start(self,depth,startURL=None):
         if startURL is None or startURL == '':
              starturl = self.c.getGoogleVidYTUrl(self.searchWord)
              self.c.crawel(starturl, depth, self.keys)
         else:
              self.c.crawel(startURL, depth, self.keys)

         save_dict_to_setting = {
             'lastTaskUrl': self.c.nexturl
         }
         self.fsdb.uploadDataToDoc("settings/"+self.type+"/keywords/"+self.searchWord,save_dict_to_setting)

         for key in self.keys:
             self.upload_via_key_strem(key,self.type)
             self.backup.addKey(key)




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
            self.fsdb.uploadDataToDoc("videos/" + youtubeKeyStream, data)
        except Exception as e:
            print(e.__str__())
            return


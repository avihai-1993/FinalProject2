from util.Craweler import Crawler
from pytube import *
from util.DBconnector import DBConnector


class Task():
    def __init__(self,searchWord , type):

        self.searchWord = searchWord
        self.type = type
        self.keys = set()


    def start(self,depth,startURL=None):
         c = Crawler()
         if startURL == None or startURL == '':
              starturl = c.getGoogleVidYTUrl(self.searchWord)
              c.crawel(starturl, depth, self.keys)
         else:
              c.crawel(startURL, depth, self.keys)

         save_dict_to_setting = {
             'lastTaskUrl': c.nexturl
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
            db.uploadDataToDoc("videos/" + youtubeKeyStream, data)
        except Exception as e:
            print(e.__str__())
            return


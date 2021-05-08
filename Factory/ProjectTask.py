from util.Craweler import Crawler
from util.DBconnector import DBConnector
from util.ProjectFunctionsMoudle import upload_via_key_strem


class Task:
    def __init__(self, searchWord ,type):
        self.searchWord = searchWord
        self.type = type
        self.keys = set()
        self.c = Crawler()
        self.fsdb = DBConnector()


    def start(self,depth,startURL=None):

        print(int(depth))
        print(startURL)
        print(self.searchWord)

        if startURL is None or startURL == '':
              starturl = self.c.getGoogleVidYTUrl(self.searchWord)
              self.c.crawel(int(depth),starturl, self.keys)
        else:
              self.c.crawel(int(depth),startURL, self.keys)

        save_dict_to_setting = {
             'lastTaskUrl': self.c.nexturl
        }
        self.fsdb.uploadDataToDoc("settings/"+self.type+"/keywords/"+self.searchWord,save_dict_to_setting)

        for key in self.keys:
             print(key)
             upload_via_key_strem(key,self.type)
             

            
       





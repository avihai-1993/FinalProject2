import os
from pytube import *
from util.descriptionAnalysis import Analyst

class YouTubeDownLoader:


    normalYTWatchUrl = "https://www.youtube.com/watch?v="

    def __init__(self, pathToSaveVideos):
        self.pathToSaveVideos = pathToSaveVideos

    def downloadToWithKey(self,pathToDownLoader,key):
        args = " "+self.normalYTWatchUrl+key+" -o "+self.pathToSaveVideos+"/"+key+".mp4"
        os.system(pathToDownLoader + args)
        print(key, "download succsfully")
        return self.pathToSaveVideos+"/"+key+".mp4"



    def downloadViaPytube(self,key,pathToSaveVideos,keywordsBank,type):
       url = self.normalYTWatchUrl+key
       blobName = key
       youTubeVideoRef = YouTube(url)
       analyst = Analyst(keywordsBank)
       score=analyst.calculateScore(youTubeVideoRef.keywords,youTubeVideoRef.title)
       if score >= 75:
           data = {"title": youTubeVideoRef.title,
                   "length": youTubeVideoRef.length / 60,
                   "publishDate": youTubeVideoRef.publish_date,
                   "views": 0,
                   "rating": None,
                   "nameInStorage": blobName,
                   "type": type,
                   "url" : self.genrate_Media_url(blobName)
                   }
           return youTubeVideoRef.streams.first().download(output_path=pathToSaveVideos, filename=key), data
       else:
           return None ,None

    def genrate_Media_url(self, blobName):
        return "https://firebasestorage.googleapis.com/v0/b/physovid.appspot.com/o/"+blobName+".mp4?alt=media"



'''
    def downloadAll(self,keys):
        for key in keys:
            self.downloadToWithKey(key)

    def downloadAllviaPytube(self,keys,pathToSaveVideos):
        for key in keys:
            self.downloadViaPytube(key,pathToSaveVideos)

'''

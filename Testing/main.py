#crawler demonstration
from pytube import *
from util.Craweler import Crawler
inputSt = "dog"
depth = 2
t = set()
c = Crawler()
starturl = c.getGoogleVidYTUrl(inputSt)
c.crawel(depth,starturl,t)
for i in t:
      url = "https://www.youtube.com/watch?v=" + i
      youTubeVideoRef = YouTube(url)
      print("key :  ",i ,"  title: ", youTubeVideoRef.title)










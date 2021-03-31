#crawler demonstration

from util.Craweler import Crawler

inputSt = "cat"
depth = 5

t = set()

c = Crawler()

starturl = c.getGoogleVidYTUrl(inputSt)


c.crawel(depth,starturl,t)

for i in t:
      print(i)










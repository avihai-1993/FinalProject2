from util.DBconnector import DBConnector

from util.Craweler import Crawler

def importFileTolist(file_name):
    res = []
    file = open(file_name,'r')
    numOfLines = int(file.readline())
    for i in range(numOfLines):
        res.append(file.readline().replace("\n", ""))
    return res

#print(importFileTolist("searchExpressions.txt"))

#ytdl = YouTubeDownLoader("C:/Users/User/PycharmProjects/FinalProject/youtube-dl.exe", "C:/Users/User/Desktop/youtube/FP_youtube")
#ytdl.downloadToWithKey("KFof8aaUvGY")

#con = DBConnector()

#con.upload("wordBank.txt")
#con.upload("C:/Users/User/Desktop/youtube/FP_youtube/KFof8aaUvGY.mp4","KFof8aaUvGY")

#pathToDownLoader = "C:/Users/User/PycharmProjects/FinalProject/youtube-dl.exe"
#args = " https://www.youtube.com/watch?v=TGI5TFnY8Ck -o C:/Users/User/Desktop/youtube/FP_youtube/yy.mp4"



#חיפןש בגוגל סרטונים

#db = DBConnector()
#db.upload("wordBank.txt","test2")


inputSt = "cat"
t = set()
c = Crawler()
starturl = c.getGoogleVidYTUrl(inputSt)
c.crawel(5,starturl,t)
#
for i in t:
      print(i)
#
#
# print(c.lastSearchUrlFromCrawelingOpartion)

#r = requests.get("https://firebasestorage.googleapis.com/v0/b/pythontest-672b7.appspot.com/o/test2")
#print(json.loads(r.text)['downloadTokens'])

#
# # #url ="https://www.youtube.com/results?search_query=dog"
# # # #url1="https://www.google.com/search?rlz=1C1CHZL_iwIL910IL911&biw=1093&bih=526&tbm=vid&sxsrf=ALeKk03xaT9lGSty_7YZm_7Qd8aJDDUPug%3A1598476948215&ei=lNJGX4nPDJDzkwXCsISICA&q=dog&oq=dog&gs_l=psy-ab.3...0.0.0.233511.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.fa6augxI_Fc"
# url2="https://www.google.com/search?q="+inputSt+"&rlz=1C1CHZL_iwIL910IL911&sxsrf=ALeKk01dYowsHmlHmiiDcKBEv_cG_bzi1Q:1598479794858&source=lnms&tbm=vid&sa=X&ved=2ahUKEwiapumi8bnrAhVR2aQKHYGUBwIQ_AUoAnoECB4QBA&biw=1093&bih=526"
# only= "https://www.google.com/search?q="+inputSt+"&rlz=1C1CHZL_iwIL910IL911&tbm=vid&sxsrf=ALeKk00UQkIFsUUkOIMKkCqFsYZF92i-Dg:1599225569738&source=lnt&tbs=srcf:H4sIAAAAAAAAANOuzC8tKU1K1UvOz1UrT03KTQGzkhNLivXyi9L1SrPV8hJLMvPzEnPSU_1PTixILMjKTYUrAdFpicmpSfn42mAMAetRY408AAAA&sa=X&ved=0ahUKEwi2zP-_y8_rAhWJ_qQKHalOCAIQpwUIIg&biw=1366&bih=657&dpr=1"
# r = requests.get(url2)
# # # keys = set()
# bs = BeautifulSoup(r.content, 'html.parser')
# #print(bs.find_all(name="a"))
# # #
# e = "https://www.google.com/search?q=cat&rlz=1C1CHZL_iwIL910IL911&biw=1366&bih=657&tbm=vid&sxsrf=ALeKk00tRX1DZewyKKnFmVW20Zr2K5FblA:1599225155427&ei=Qz1SX4XOGZKxkwXl4KuoDA&start=10&sa=N&ved=0ahUKEwjF-7f6yc_rAhWS2KQKHWXwCsUQ8NMDCIgB"
#
# for l in bs.find_all('a'):
#     print(l)
#     if(str(l.get("aria-label"))== "הדף הבא"):
#         print("https://www.google.com",l.get("href"))




# #  for s in re.findall("https://www.youtube.com/watch%3Fv%3D.*[&]",l.get("href")):
# #    keys.add(str(s).split("&",1)[0].replace("https://www.youtube.com/watch%3Fv%3D",""))
# #
# #
# # print(keys)
#
#urls = set()
#print(bs.find_all("table"))
# # r = requests.get(url2) bs = BeautifulSoup(r.content, 'html.parser')
# for i in bs.find_all("table"):
#  print(i)
#  if(str(i.get("href")).__contains__("")):
#         urls.add("https://www.google.com"+i.get("href"))
#
# for u in urls:
#     print(u)
#
#
# def getUrlForGoogleVid(inputStr):
#     return "https://www.google.com/search?q=" + inputStr + "&rlz=1C1CHZL_iwIL910IL911&sxsrf=ALeKk01dYowsHmlHmiiDcKBEv_cG_bzi1Q:1598479794858&source=lnms&tbm=vid&sa=X&ved=2ahUKEwiapumi8bnrAhVR2aQKHYGUBwIQ_AUoAnoECB4QBA&biw=1093&bih=526"
#
#
# def searchYouTubeVideosKeysInGoogleVideos(url,keys):
#     r = requests.get(url)
#     if(r.status_code == 200):
#      bs = BeautifulSoup(r.content, 'html.parser')
#      for l in bs.find_all('a'):
#        for s in re.findall("https://www.youtube.com/watch%3Fv%3D.*[&|%]",l.get("href")):
#          keys.add(str(s).split("&",1)[0].replace("https://www.youtube.com/watch%3Fv%3D",""))
#
#
#     else:
#         print("somthing wrong --- bad url")
#
#
# def findNextUrlsForSearch(startUrl,urls):
#     r = requests.get(startUrl)
#     if(r.status_code == 200):
#         bs = BeautifulSoup(r.content, 'html.parser')
#         for i in bs.find_all('a'):
#              if (str(i.get("href")).__contains__("search?q=")):
#                 urls.add("https://www.google.com" + i.get("href"))
#
#     else:
#         print("somthing wrong --- bad url")

#
#
# k = set()
# u = set()
# cr = Craweler()
# t = cr.getUrlForGoogleVid(inputSt)
# cr.searchYouTubeVideosKeysInGoogleVideos(t , k)
# cr.findNextUrlsForSearch(t , u)

# t = getUrlForGoogleVid(inputSt)
# searchYouTubeVideosKeysInGoogleVideos(t,k)
# findNextUrlsForSearch(t,u)
#
#
#print("keys \n" , k)
#print("urls \n",u)


#
# for url in u:
#         searchYouTubeVideosKeysInGoogleVideos(url, k)



#print("keys \n",k)



#des = descriptionAnalysis.importBankfromFile("wordBank.txt")

#print(des.sumOfMatchesInString('can get why i love u'))




#print(YouTube("https://www.youtube.com/watch?v=kCtoc1oFTvQ").title)

##TODO Main script will do
##TODO  work crawler to find youtube stream keys //optinal Analysis here
##TODO  downLoad video with steam key //or optinal Analysis here
##TODO  upload videos with metadeta to firebase


##TODO claen Script
##TODO chack FB for wike videos and delete them











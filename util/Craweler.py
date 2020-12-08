import requests
import re
from bs4 import BeautifulSoup

class Craweler:

    lastSearchUrlFromCrawelingOpartion = ""
    def getUrlForGoogleVid(self,inputStr):
        return "https://www.google.com/search?q=" + inputStr + "&rlz=1C1CHZL_iwIL910IL911&sxsrf=ALeKk01dYowsHmlHmiiDcKBEv_cG_bzi1Q:1598479794858&source=lnms&tbm=vid&sa=X&ved=2ahUKEwiapumi8bnrAhVR2aQKHYGUBwIQ_AUoAnoECB4QBA&biw=1093&bih=526"

    def getOnlyYTFromGoogleVids(self, inputStr):
       return "https://www.google.com/search?q="+inputStr+"&rlz=1C1CHZL_iwIL910IL911&tbm=vid&sxsrf=ALeKk00UQkIFsUUkOIMKkCqFsYZF92i-Dg:1599225569738&source=lnt&tbs=srcf:H4sIAAAAAAAAANOuzC8tKU1K1UvOz1UrT03KTQGzkhNLivXyi9L1SrPV8hJLMvPzEnPSU_1PTixILMjKTYUrAdFpicmpSfn42mAMAetRY408AAAA&sa=X&ved=0ahUKEwi2zP-_y8_rAhWJ_qQKHalOCAIQpwUIIg&biw=1366&bih=657&dpr=1"

    def searchYouTubeVideosKeysInGoogleVideos(self,url, keys):
        r = requests.get(url)
        if r.status_code == 200:
            bs = BeautifulSoup(r.content, 'html.parser')
            for l in bs.find_all('a'):
                for s in re.findall("https://www.youtube.com/watch%3Fv%3D.*[&|%]", l.get("href")):
                    keys.add(str(s).split("&", 1)[0].replace("https://www.youtube.com/watch%3Fv%3D", ""))


        else:
            print("somthing wrong --- bad url")

    def findNextUrlForSearch(self,startUrl, urls):
        r = requests.get(startUrl)
        if r.status_code == 200:
            bs = BeautifulSoup(r.content, 'html.parser')
            for i in bs.find_all('a'):
                if str(i.get("href")).__contains__("search?q=") :
                    urls.add("https://www.google.com" + i.get("href"))

        else:
            print("somthing wrong --- bad url")

    def findNextUrlForSearch(self, startUrl):
        r = requests.get(startUrl)
        if r.status_code == 200:
            bs = BeautifulSoup(r.content, 'html.parser')
            for i in bs.find_all('a'):
                if str(i.get("href")).__contains__("search?q=") and str(i.get("aria-label")) == "הדף הבא":
                    return "https://www.google.com" + i.get("href")

        else:
            print("somthing wrong --- bad url")

    def findkeysCrawel(self,url,depth,keys):
        if depth == 0 :
            return
        else:
            self.searchYouTubeVideosKeysInGoogleVideos(url,keys)
            self.lastSearchUrlFromCrawelingOpartion = self.findNextUrlForSearch(url)
            self.findkeysCrawel(self.lastSearchUrlFromCrawelingOpartion,depth - 1,keys)


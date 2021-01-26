
from bs4 import BeautifulSoup
import requests


class Crawler:

    def __init__(self):
        self.nexturl = ""

    def getGoogleVidYTUrl(self,inputStr):
        return 'https://www.google.com/search?q=' + inputStr + '&tbm=vid&sxsrf=ALeKk03mqj8CnGxXPjzaB5JsHKU22Loj2A:1611354521040&source=lnt&tbs=srcf:H4sIAAAAAAAAANOuzC8tKU1K1UvOz1UrT03KTQGzSjJS00sTi1IyE_1PA_1LTE5NSk_1PxsMKcgtaQ4sSQjPzcVKpeXkp8LZgIAKrN1hE4AAAA&sa=X&ved=0ahUKEwjXpNWuy7DuAhWkQxUIHVUACmQQpwUIJg&biw=1707&bih=821&dpr=0.8'

    def getStreamKeys(self,inputUrl,l):
        try:
            html = requests.get(inputUrl).text
            page = BeautifulSoup(html, 'html.parser')
            hebrewNext = "הדף הבא"
            googleprifix =  "https://www.google.com"
            prifix = "/url?q=https://www.youtube.com/watch%3Fv%3D"
            for link in page.find_all('a'):
                if prifix in link["href"]:
                    if '%' in link["href"].split('&')[0].replace(prifix, ''):
                        l.add(link["href"].split('&')[0].replace(prifix, '').split('%')[0])
                    else:
                        l.add(link["href"].split('&')[0].replace(prifix, ''))
                elif hebrewNext in link.__str__():
                    self.nexturl = googleprifix+link["href"]

        except Exception as e:
            print("somthing want Wrong : " +e.__str__())




    def crawel(self, depth, url, keySet):
        if depth == 0:
            return
        self.getStreamKeys(url, keySet)
        self.crawel(depth - 1, self.nexturl, keySet)

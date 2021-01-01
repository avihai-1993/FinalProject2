from util.YouTubeDownLoader import YouTubeDownLoader as dl
from pytube import YouTube as yt
saver = "C:/Users/User/Desktop/PhsoVid"
teststring = "https://www.youtube.com/watch?v=A4xzkIC-Erg"
st = "Jonas Brothers, Diplo – Lonely (Lyrics)-wNAOI-tRHcg"

#print(dl("").genrate_Media_url(blobName=st))
#downLoader = dl("",pathToSaveVideos=saver)
#res=downLoader.downloadViaPytube("7Qp5vcuMIlk",saver)
#print(res)
#"https://www.youtube.com/watch?v=7Qp5vcuMIlk"
print("str")
y = yt(teststring)

#print(y.title)
#print(y.metadata)
#print(y.description)
print(y.keywords.__str__())
#print(y.length/60)
#print(y.author)
#print(y.captions)
#print(y.publish_date)
#print(y.check_availability())
#print(y.vid_info)
#print(y.rating)
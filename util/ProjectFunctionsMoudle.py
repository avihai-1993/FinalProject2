from util.DBconnector import DBConnector
from pytube import *
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp as BackUp

def strOnlydigAndAlpha(s):
    if type(s) is not str:
        return False
    for i in range(len(s)):
        if not s[i].isdigit() and not s[i].isalpha() and not s[i].isspace():
            return False

    return True

def upload_via_key_strem(youtubeKeyStream,videotype,backup = True,listener = None):
    try:
        url = "https://www.youtube.com/watch?v=" + youtubeKeyStream
        youTubeVideoRef = YouTube(url)
        data = {
            "title": youTubeVideoRef.title,
            "length": youTubeVideoRef.length / 60,
            "publishDate": youTubeVideoRef.publish_date,
            "ratedNum": 0,
            "avgRating": None,
            "YTSK": youtubeKeyStream,
            "type": videotype,
        }
        db = DBConnector()
        db.uploadDataToDoc("videos/" + youtubeKeyStream, data)
        if backup:
            dbBack = BackUp()
            dbBack.addKey(youtubeKeyStream,videotype)
        if listener is not None:
           listener(youtubeKeyStream+ " video up loaded")
    except Exception as e:
        if listener is not None:
           listener(e)
           return
        raise e

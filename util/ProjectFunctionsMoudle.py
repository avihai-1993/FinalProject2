from util.DBconnector import DBConnector
from pytube import *
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp as BackUp

def strOnlydigAndAlpha(s):
    if type(s) is not str:
        return False
    for i in range(len(s)):
        if not s[i].isdigit() and not s[i].isalpha():
            return False

    return True

def upload_via_key_strem(youtubeKeyStream,videotype , backup = True):
    try:
        url = "https://www.youtube.com/watch?v=" + youtubeKeyStream
        youTubeVideoRef = YouTube(url)
        data = {
            "title": youTubeVideoRef.title,
            "length": youTubeVideoRef.length / 60,
            "publishDate": youTubeVideoRef.publish_date,
            "views": 0,
            "rating": None,
            "YTSK": youtubeKeyStream,
            "type": videotype,
        }

        db = DBConnector()
        db.uploadDataToDoc("videos/" + youtubeKeyStream, data)
        if backup:
            dbBack = BackUp()
            dbBack.addKey(youtubeKeyStream,videotype)

    except Exception as e:
        raise e

from util.DBconnector import DBConnector
from pytube import *
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp as BackUp


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
            dbBack.addKey(youtubeKeyStream)

    except Exception as e:
        raise e

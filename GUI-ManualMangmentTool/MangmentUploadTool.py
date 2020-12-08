import tkinter as tk
from tkinter import IntVar,StringVar,ttk ,filedialog
from util.DBconnector import DBConnector
from util.YouTubeDownLoader import YouTubeDownLoader
from moviepy.editor import VideoFileClip
from datetime import date
from pytube import *
import uuid



ON_PATH_VALUE = 1
OFF_PATH_VALUE = 0
ON_YTSK_VALUE = 2
OFF_YTSK_VALUE = 0

def getTypeVideosList():
    return  ["neck" , "lower back" , "upper back" , "knee"]


# {"title" : title , "path" : path , "YTKS" : ytks}
def uplaodFunction(valuesDict,option,typeVid,logView):

    title = valuesDict["title"].get()
    pathToLocalFile = valuesDict["path"].get()
    youtubeKeyStream = valuesDict["YTKS"].get()
    optionValue = option.get()
    videoType = typeVid.get()
    print(title, pathToLocalFile ,youtubeKeyStream,optionValue,videoType)

    if optionValue == OFF_PATH_VALUE and optionValue == OFF_YTSK_VALUE :
        logView.set("No upload method has being selected")

    elif optionValue == ON_YTSK_VALUE:
        logView.set("uploading via Youtube key stream method \n")
        try:
            '''
            TODO
            uplading via streak key
            '''
            url = "https://www.youtube.com/watch?v="+youtubeKeyStream
            youTubeVideoRef = YouTube(url)
            data = {"title": youTubeVideoRef.title,
                    "length": youTubeVideoRef.length / 60,
                    "publishDate": youTubeVideoRef.publish_date,
                    "views": 0,
                    "rating": None,
                    "nameInStorage": youtubeKeyStream,
                    "type": type,
                    "url": YouTubeDownLoader("").genrate_Media_url(youtubeKeyStream)
                    }
            saveDir = r"C:\Users\User\Desktop\PhsoVid"
            pathToFile = youTubeVideoRef.streams.first().download(output_path=saveDir, filename=youtubeKeyStream)
            print(data)
            db = DBConnector()
            db.upload(pathToFile, youtubeKeyStream)
            db.uploadDataToDoc("videos/"+youtubeKeyStream, data)
            logView.set("Done \n")
        except Exception:
            logView.set(Exception.__str__())



    elif optionValue == ON_PATH_VALUE:
        logView.set("uploading via local file ")
        try:
            '''
            TODO
            upladind via path
            '''

            v = VideoFileClip(pathToLocalFile)
            #db.upload(pathToLocalFile ,title)
            data = {"title": title,
                    "length": v.duration/60 ,
                    "publishDate": date.today().strftime("%Y-%m-%d 00:00"),
                    "views": 0,
                    "rating": None,
                    "nameInStorage":title,
                    "type": videoType,
                    "url": YouTubeDownLoader("").genrate_Media_url(title)
                    }
            print(data)

            db = DBConnector()
            db.upload(pathToLocalFile,title)
            #db.uploadDataToDoc("videos/"+str(uuid.uuid4()),data)

            logView.set("Done \n")
        except Exception:
            logView.set(Exception.__str__())



    valuesDict["title"].set("")
    valuesDict["path"].set("")
    valuesDict["YTKS"].set("")





mainWindow = tk.Tk()

title = StringVar()
titleLable = tk.Label(mainWindow, text ="Title : ")
titleEntry = tk.Entry(mainWindow,width = 50 ,textvariable= title)

ytks = StringVar()
ytksLable = tk.Label(mainWindow, text ="YouTube Stream key : ")
ytksEntry = tk.Entry(mainWindow,width = 50,textvariable= ytks)

path = StringVar()
pathLable = tk.Label(mainWindow  ,text = "Local Path to video  : ")
pathEntry = tk.Entry(mainWindow,width = 50,textvariable= path)


option = IntVar()
withPathCB =tk.Checkbutton(mainWindow, text="via Local Path" ,variable = option ,onvalue =ON_PATH_VALUE, offvalue = OFF_PATH_VALUE,)
withYTKSCB =tk.Checkbutton(mainWindow, text="via YouTube key Stream" ,variable = option ,onvalue = ON_YTSK_VALUE, offvalue = OFF_YTSK_VALUE)


typevar = StringVar()
selectTypeOfVideoLable = tk.Label(mainWindow, text ="select the type of video : ")
typeOfVideoCB = ttk.Combobox(mainWindow, textvariable=typevar)
typeOfVideoCB['values'] = getTypeVideosList()

log = StringVar()
logger = tk.Label(mainWindow,textvariable= log)


entryDict = {"title" : title , "path" : path , "YTKS" : ytks}

f = lambda : uplaodFunction(entryDict,option,typevar,log)

def getFilePath():
  path.set(str(tk.filedialog.askopenfilename()))

uploadButton = tk.Button(mainWindow,text= "upload",command=f)
BrowesButton = tk.Button(mainWindow,text= "Browes to local file",command=getFilePath)

in_side_spaceingX = 6
in_side_spaceingY = 6
out_side_spaceingX = 9
out_side_spaceingY = 9

titleLable.grid(row = 0, column = 0 ,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY ,padx = out_side_spaceingX ,pady = out_side_spaceingY)
titleEntry.grid(row = 0, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

pathLable.grid(row = 1, column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
pathEntry.grid(row = 1, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

ytksLable.grid(row = 2, column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
ytksEntry.grid(row = 2, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

withPathCB.grid(row = 3, column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
withYTKSCB.grid(row = 3, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

selectTypeOfVideoLable.grid(row =4,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
typeOfVideoCB.grid(row = 4, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

uploadButton.grid(row = 5 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
BrowesButton.grid(row = 5 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

logger.grid(row = 6 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)


mainWindow.mainloop()
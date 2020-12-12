import tkinter as tk
from tkinter import IntVar,StringVar,ttk ,filedialog
from util.DBconnector import DBConnector
from moviepy.editor import VideoFileClip
from datetime import date
from pytube import *
import threading
import uuid
import time


ON_PATH_VALUE = 1
OFF_PATH_VALUE = 0
ON_YTSK_VALUE = 2
OFF_YTSK_VALUE = 0


def makeCustomFormatString(arr):
    s = str()
    for word in arr:
        s = s + word + ","

    s = s[:len(s) - 1]
    return s

def getTypesKewords():
    db = DBConnector()
    settings = db.readCollaction("settings")
    res = dict()
    for k in settings:
        res[k] = makeCustomFormatString(settings[k]['keywords'])

    return res



def getTypeVideosList():
    db = DBConnector()
    return list(db.readCollaction("settings").keys())

def commitSettingButtonFunction(typeToAddOrChange, moreKeywords , currentTypeList,typeComboBox1,typeComboBox2):
    db = DBConnector()

    if typeToAddOrChange is None or typeToAddOrChange=='':
        return

    if typeToAddOrChange in currentTypeList:
        dataToUpdate = {
            "keywords":moreKeywords
        }
        db.upDateDataToDoc("settings/"+typeToAddOrChange, dataToUpdate)
    else:
        data = {
                "keywords": moreKeywords,
                "lastTaskUrl": ""

        }
        db.uploadDocToCollection("settings",typeToAddOrChange,data)

    typeComboBox1["values"] = getTypeVideosList()
    typeComboBox2["values"] = getTypeVideosList()


#_------------- oparete
# {"title" : title , "path" : path , "YTKS" : ytks}

def upload_via_key_strem(youtubeKeyStream,videotype,logView):
    start = time.perf_counter()
    try:
        url = "https://www.youtube.com/watch?v=" + youtubeKeyStream
        youTubeVideoRef = YouTube(url)
        data = {
            "title": youTubeVideoRef.title,
            "length": youTubeVideoRef.length / 60,
            "publishDate": youTubeVideoRef.publish_date,
            "views": 0,
            "rating": None,
            "nameInStorage": youtubeKeyStream,
            "type": videotype,
        }
        saveDir = r"C:\Users\User\Desktop\PhsoVid"
        pathToFile = youTubeVideoRef.streams.first().download(output_path=saveDir, filename=youtubeKeyStream)
        print(data)
        db = DBConnector()
        db.upload(pathToFile, youtubeKeyStream)
        db.uploadDataToDoc("videos/" + str(uuid.uuid4()), data)
    except Exception:
        logView.set("somethig wrong happend")
        return

    end = time.perf_counter()
    logView.set(f"{youtubeKeyStream} has being uploaded ... Done in {round(end - start)} seconds \n")

def upload_via_local_file(pathToLocalFile,name,videoType,logView):
    start = time.perf_counter()
    try:
        v = VideoFileClip(pathToLocalFile)
        data = {"title": name,
                "length": v.duration / 60,
                "publishDate": date.today().strftime("%Y-%m-%d 00:00"),
                "views": 0,
                "rating": None,
                "nameInStorage": name,
                "type": videoType,
                }

        print(data)
        db = DBConnector()
        db.upload(pathToLocalFile, name)
        db.uploadDataToDoc("videos/" + str(uuid.uuid4()), data)

    except Exception:
        logView.set("somethig wrong happend")
        return

    end = time.perf_counter()
    logView.set(f"{name} has being uploaded ... Done in {round(end - start)} seconds \n")

def uplaodFunction(valuesDict,option,typeVid,logView):

    title = valuesDict["title"].get()
    pathToLocalFile = valuesDict["path"].get()
    youtubeKeyStream = valuesDict["YTKS"].get()
    optionValue = option.get()
    videoType = typeVid.get()

    print(title, pathToLocalFile,youtubeKeyStream,optionValue,videoType)


    if optionValue == OFF_PATH_VALUE and optionValue == OFF_YTSK_VALUE:
        logView.set("No upload method has being selected")
        return

    elif optionValue == ON_YTSK_VALUE:

        if youtubeKeyStream is None or youtubeKeyStream == "":
            logView.set("You must give a stream key to video that exist in youtube")
            return

        try:
            t_task = threading.Thread(target=upload_via_key_strem, args=[youtubeKeyStream,videoType, logView])
            t_task.start()
            logView.set("uploading.... \n")
        except Exception:
            logView.set("somethig wrong happend")

    elif optionValue == ON_PATH_VALUE:
        if title is None or title == "":
            logView.set("You must give a title to video ")
            return

        if pathToLocalFile is None or pathToLocalFile == "" :
            logView.set("You must give a valid path to local video file in mp4 format")
            return

        if pathToLocalFile[len(pathToLocalFile) - 4 : len(pathToLocalFile)] != ".mp4":
            logView.set("You must give a valid path to local video file in mp4 format")
            return
        try:
            t_task = threading.Thread(target=upload_via_local_file,args=[pathToLocalFile,title,videoType,logView])
            t_task.start()
            logView.set("uploading.... \n")
        except Exception:
            logView.set("somethig wrong happend")


    valuesDict["title"].set("")
    valuesDict["path"].set("")
    valuesDict["YTKS"].set("")



#------------------------GUI INIT
values_type_list = getTypeVideosList()
keywords_info = getTypesKewords()

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
typeOfVideoCB = ttk.Combobox(mainWindow, textvariable=typevar ,state="readonly" , values = values_type_list)
typevar.set(values_type_list[0])

log = StringVar()
logger = tk.Label(mainWindow,textvariable= log)


#---------------------Editing setting add types of videos and keyWords for the batch craweler task
key_words_for_entry = StringVar()
edit_typevar = StringVar()

editTypeLabel = tk.Label(mainWindow, text ="select the type to edit / add to settings : ")

edit_typeOfVideo_CB = ttk.Combobox(mainWindow, textvariable=edit_typevar , values = values_type_list)

handler = lambda event : key_words_for_entry.set(getTypesKewords()[event.widget.get()])

edit_typeOfVideo_CB.bind(sequence="<<ComboboxSelected>>",func=handler)

edit_typevar.set(values_type_list[0])


edit_key_words_Label = tk.Label(mainWindow, text ="put keywords for new type format is word1,word2,...,wordN")
edit_key_words_Entry = tk.Entry(mainWindow,width = 90,textvariable= key_words_for_entry)

key_words_for_entry.set(keywords_info[edit_typevar.get()])

entryDict = {"title" : title , "path" : path , "YTKS" : ytks}

f = lambda : uplaodFunction(entryDict,option,typevar,log)

f1 = lambda : commitSettingButtonFunction(edit_typevar.get(),key_words_for_entry.get().split(','),getTypeVideosList(),typeOfVideoCB,edit_typeOfVideo_CB)


def delTypeInSettings(typeToDelete,typeComboBox1,typeComboBox2):
    l = getTypeVideosList()
    if typeToDelete in l:
        db = DBConnector()
        db.deleteDoc("settings/"+typeToDelete)

    typeComboBox1["values"] = getTypeVideosList()
    typeComboBox2["values"] = getTypeVideosList()


f2 = lambda : delTypeInSettings(edit_typevar.get(),typeOfVideoCB,edit_typeOfVideo_CB)

def getFilePath():
  path.set(str(tk.filedialog.askopenfilename()))

uploadButton = tk.Button(mainWindow,text= "upload",command=f)
BrowesButton = tk.Button(mainWindow,text= "Browes to local file",command=getFilePath)
commitSettingButton = tk.Button(mainWindow,text= "commit to batch job setting",command=f1)
deleteTypeInSettingsButton = tk.Button(mainWindow,text= "delete selected type",command=f2)

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

editTypeLabel.grid(row = 7 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
edit_typeOfVideo_CB.grid(row = 7 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

edit_key_words_Label.grid(row = 8 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
edit_key_words_Entry.grid(row = 9 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
commitSettingButton.grid(row = 9 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
deleteTypeInSettingsButton.grid(row = 10 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
mainWindow.mainloop()
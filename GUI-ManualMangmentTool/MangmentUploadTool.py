import tkinter as tk
from tkinter import StringVar,ttk
from util.DBconnector import DBConnector
from pytube import *
import threading
import uuid
import time


ON_PATH_VALUE = 1
OFF_PATH_VALUE = 0
ON_YTSK_VALUE = 2
OFF_YTSK_VALUE = 0

#no C
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

    #TODO validete key words here

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
#no C

#_------------- oparete

def get_YTV_key_words(ytks,ytks_strVar,logView):
    start = time.perf_counter()
    try:
        print(ytks,ytks_strVar)
        url = "https://www.youtube.com/watch?v=" + ytks
        youTubeVideoRef = YouTube(url)
        ytks_strVar.set(youTubeVideoRef.keywords.__str__())
        end = time.perf_counter()
        logView.set(f"getiing video key words {round(end - start)} seconds \n")
    except Exception as e:
        logView.set("somethig wrong happend  " + e.__str__())
        return
    pass


def upload_via_key_strem(youtubeKeyStream,videotype,logView):

    start = time.perf_counter()
    #TODO chack if already in db
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

        print(data)
        db = DBConnector()
        db.uploadDataToDoc("videos/" + str(uuid.uuid4()), data)
    except Exception as e:
        logView.set("somethig wrong happend  "+ e.__str__() )
        return

    end = time.perf_counter()
    logView.set(f"{youtubeKeyStream} has being uploaded ... Done in {round(end - start)} seconds \n")


def uplaodFunction(youtubeKeyStream,typeVid,logView):
    if youtubeKeyStream is None or youtubeKeyStream.get() == "":
        logView.set("You must give a stream key to video that exist in youtube")
        return
    try:
        t_task = threading.Thread(target=upload_via_key_strem, args=[youtubeKeyStream.get(),typeVid, logView])
        t_task.start()
        logView.set("uploading.... \n")

    except Exception as e :
        logView.set("somethig wrong happend  " + e.__str__())

    youtubeKeyStream.set("")



#------------------------GUI INIT
values_type_list = getTypeVideosList()
keywords_info = getTypesKewords()

mainWindow = tk.Tk()
mainWindow.title("Manual Management Tool - MMT")

log = StringVar()
logger = tk.Label(mainWindow,textvariable= log ,fg = "purple" )
log.set("log messages here")

ytks = StringVar()
ytksLable = tk.Label(mainWindow, text ="YouTube Stream key : ")
ytksEntry = tk.Entry(mainWindow,width = 50,textvariable= ytks)


#need
typevar = StringVar()
selectTypeOfVideoLable = tk.Label(mainWindow, text ="select the type of video : ")
typeOfVideoCB = ttk.Combobox(mainWindow, textvariable=typevar ,state="readonly" , values = values_type_list)
typevar.set(values_type_list[0])



key_words_strVar = StringVar()
get_YTVKW = lambda : get_YTV_key_words(ytks.get(),key_words_strVar,log)
YTVideo_key_words_Entry = tk.Entry(mainWindow,width = 50 ,textvariable=key_words_strVar )
get_YTVideo_key_wordsButton = tk.Button(mainWindow,text= "find video key words" , command=get_YTVKW)



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


f = lambda : uplaodFunction(ytks,typevar.get(),log)

f1 = lambda : commitSettingButtonFunction(edit_typevar.get(),key_words_for_entry.get().split(','),getTypeVideosList(),typeOfVideoCB,edit_typeOfVideo_CB)


def delTypeInSettings(typeToDelete,typeComboBox1,typeComboBox2):
    l = getTypeVideosList()
    if typeToDelete in l:
        db = DBConnector()
        db.deleteDoc("settings/"+typeToDelete)

    typeComboBox1["values"] = getTypeVideosList()
    typeComboBox2["values"] = getTypeVideosList()


f2 = lambda : delTypeInSettings(edit_typevar.get(),typeOfVideoCB,edit_typeOfVideo_CB)

uploadButton = tk.Button(mainWindow,text= "upload",command=f)

commitSettingButton = tk.Button(mainWindow,text= "commit to batch job setting",command=f1)
deleteTypeInSettingsButton = tk.Button(mainWindow,text= "delete selected type",command=f2)

in_side_spaceingX = 6
in_side_spaceingY = 6
out_side_spaceingX = 9
out_side_spaceingY = 9

ytksLable.grid(row = 0, column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
ytksEntry.grid(row = 0, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

selectTypeOfVideoLable.grid(row =1,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
typeOfVideoCB.grid(row = 1, column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)

uploadButton.grid(row = 2 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx = out_side_spaceingX ,pady = out_side_spaceingY)
logger.grid(row =2 ,column =1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

YTVideo_key_words_Entry.grid(row = 3 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
get_YTVideo_key_wordsButton.grid(row = 3 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

editTypeLabel.grid(row = 4 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
edit_typeOfVideo_CB.grid(row = 4 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

edit_key_words_Label.grid(row = 5 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

edit_key_words_Entry.grid(row = 6 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
commitSettingButton.grid(row = 6 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

deleteTypeInSettingsButton.grid(row = 7 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

mainWindow.mainloop()
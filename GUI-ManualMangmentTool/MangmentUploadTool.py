import tkinter as tk
from tkinter import StringVar,ttk
from util.DBconnector import DBConnector
import threading
from util.ProjectFunctionsMoudle import upload_via_key_strem
from util.ProjectFunctionsMoudle import strOnlydigAndAlpha
import sys
import os
import webbrowser


def makeCustomFormatString(arr):
    s = str()
    for word in arr:
        s = s + word + ","

    s = s[:len(s) - 1]
    return s


def getTypesKewords():
    try:
        settings = DBConnector().readCollaction("settings")
        dict_key_word = {}
        for type_in_settings in settings:
            dict_key_word[type_in_settings] = []
            keywords = DBConnector().readCollaction("settings/"+type_in_settings+"/keywords")
            for kw in keywords:
                dict_key_word[type_in_settings].append(kw)

            dict_key_word[type_in_settings] = makeCustomFormatString(dict_key_word[type_in_settings])


        return dict_key_word

    except Exception as e:
        print(e.__str__())


def getTypeVideosList():
    try:
        db = DBConnector()
        return list(db.readCollaction("settings").keys())
    except:
        return []





def commitSettingButtonFunction(typeToAddOrChange, keywordListInEntry, typeComboBox1, typeComboBox2,logView):
    db = DBConnector()
    if typeToAddOrChange is None or typeToAddOrChange==''  or typeToAddOrChange.isspace():
        logView.set("cant add or change type ")
        return

    if not strOnlydigAndAlpha(typeToAddOrChange):
        logView.set("type can only contains chars and numbers ")
        return


    if keywordListInEntry is None or len(keywordListInEntry) == 0 or keywordListInEntry[0] == '':
        logView.set("cant add type with empty key words ")
        return

    for w in keywordListInEntry:
        if not strOnlydigAndAlpha(w):
            logView.set("key words only contains chars and numbers ")
            return

    try:
        task = threading.Thread(target=db.uploadDataToDoc, args=["settings/" + typeToAddOrChange, {"onlyForCreate": "a"}])
        task.start()
        task.join()
        keywords_json_fb = db.readCollaction("settings/" + typeToAddOrChange + "/keywords")
        keywords_fb  = keywords_json_fb.keys()
        # adding new key word for the type
        for kw in keywordListInEntry:
            if kw not in keywords_fb:
                data = {
                    'lastTaskUrl': ''
                }
                db.uploadDocToCollection("settings/" + typeToAddOrChange + "/keywords", kw, data)

        # removing thing that are not in the entry fro fb
        for kw in keywords_fb:
            if kw not in keywordListInEntry:
                db.deleteDoc("settings/" + typeToAddOrChange + "/keywords/" + kw)

        typeComboBox1["values"] = getTypeVideosList()
        typeComboBox2["values"] = getTypeVideosList()
        logView.set("changes commited")


    except Exception as e:
        logView.set("something want wrong" , e.__str__())


def uplaodFunction(youtubeKeyStream,typeVid,logView,mw,err):
    if youtubeKeyStream is None or youtubeKeyStream.get() == "":
        logView.set("You must give a stream key to video that exist in youtube")
        return


    try:

        t_task = threading.Thread(target=upload_via_key_strem, args=[youtubeKeyStream.get(),typeVid,True,err])
        t_task.start()
        logView.set("video sent to database wait for it to upload")
        mw.update()




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

def errhandler(e):
    log.set(e.__str__())

ytks = StringVar()
ytksLable = tk.Label(mainWindow, text ="YouTube Stream key : ")
ytksEntry = tk.Entry(mainWindow,width = 50,textvariable= ytks)


#need
typevar = StringVar()
selectTypeOfVideoLable = tk.Label(mainWindow, text ="select the type of video : ")
typeOfVideoCB = ttk.Combobox(mainWindow, textvariable=typevar ,state="readonly" , values = values_type_list)
typevar.set(values_type_list[0])



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
key_words_for_entry.set(getTypesKewords()[edit_typevar.get()])


f = lambda : uplaodFunction(ytks,typevar.get(),log,mainWindow,errhandler)

f1 = lambda : commitSettingButtonFunction(edit_typevar.get(),key_words_for_entry.get().split(','),typeOfVideoCB,edit_typeOfVideo_CB,log)


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

editTypeLabel.grid(row = 3 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
edit_typeOfVideo_CB.grid(row = 3 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

edit_key_words_Label.grid(row = 4 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

edit_key_words_Entry.grid(row = 5 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
commitSettingButton.grid(row = 5 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

deleteTypeInSettingsButton.grid(row = 6 ,column = 1,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)

mainWindow.mainloop()

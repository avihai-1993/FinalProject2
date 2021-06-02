import tkinter as tk
from tkinter import StringVar,IntVar,ttk
from Factory.TaskFactory import TaskFactory
from util.DBconnector import DBConnector
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp as BackUp
from util.ProjectFunctionsMoudle import upload_via_key_strem
from threading import Thread


def ivaluaetFanction(rating,views,*args):

    return rating <= int(args[1]) and views >= int(args[0])


def clean_Op(log,*args):
    log.set("start cleaning the DB")
    try:
        db = DBConnector()
        vids = db.readCollaction("videos")
        for v in vids:
            if ivaluaetFanction(vids[v]['avgRating'],vids[v]['ratedNum'], args[0].get(), args[1].get()):
                    db.deleteDoc("videos/"+v)


    except Exception as e:
        print(e)
        log.set(e.__str__())
        return

    log.set("FINISHED cleaning the DB")

def runSearchAndUpload(log):
    log.set("start search and upload data")
    settings = DBConnector().readCollaction("settings")
    TaskFactory(settings).startWork()



def upLoapFromBackUp(log):
    try:

        b = BackUp()
        keys = b.getAllkeys()
        log.set("upload all from backup "+str(len(keys)))
        for k in keys:
            Thread(target=upload_via_key_strem, args=[keys[k]['key'], keys[k]['type'], False]).start()
    except Exception as e:
        log.set(e.__str__())
        return

    log.set("all key as been diploaed")



mainWindow = tk.Tk()
mainWindow.title("Auto Managment Upload Tool  - AMUT")

log = StringVar()
logger = tk.Label(mainWindow,textvariable= log ,fg = "purple" )
log.set("log messages here")

numOfRateds = IntVar()
rating = IntVar()
rating.set(1)
cleanOp = lambda : clean_Op(log,numOfRateds,rating)
S_U_Op = lambda : runSearchAndUpload(log)
uploadFromBackUpFileOp = lambda : upLoapFromBackUp(log)



numOfRatedsLable = tk.Label(mainWindow, text ="number Of users that raited  : ")
numOfRatedsEntry = tk.Entry(mainWindow,width = 50,textvariable= numOfRateds)

ratingLable = tk.Label(mainWindow, text ="rating max limit : ")
ratingCombobox = ttk.Combobox(mainWindow,width = 50,values = [0,1,2,3,4,5],textvariable=rating,state="readonly")

cleandb = tk.Button(mainWindow, text="clean DB" , command=cleanOp)


searchAndUpload = tk.Button(mainWindow, text="stars search and upload data",command=S_U_Op)
uploadFromKeyBackUP = tk.Button(mainWindow, text="upload all from backup",command=uploadFromBackUpFileOp)


in_side_spaceingX = 6
in_side_spaceingY = 6
out_side_spaceingX = 9
out_side_spaceingY = 9

searchAndUpload.grid(row = 0, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)

numOfRatedsLable.grid(row = 1, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
numOfRatedsEntry.grid(row = 1, column = 1, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
ratingLable.grid(row = 2, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
ratingCombobox.grid(row = 2, column = 1, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)

cleandb.grid(row = 3, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
uploadFromKeyBackUP.grid(row = 4, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
logger.grid(row = 5 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
mainWindow.mainloop()
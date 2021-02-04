import tkinter as tk
from tkinter import StringVar,ttk
from Factory.TaskFactory import TaskFactory
from util.DBconnector import DBConnector
from util.sqlite3BackUpYTStreamKey import SqlLiteKeyBackUp as BackUp
from util.ProjectFunctionsMoudle import upload_via_key_strem
from threading import Thread





def clean_Op(log,*args):
    log.set("start cleaning the DB")
    pass

def runSearchAndUpload(log):
    log.set("start search and upload data")
    #TODO get setting
    settings = DBConnector().readCollaction("settings")
    TaskFactory(settings).startWork()
    pass


def upLoapFromBackUp(log):
    try:
        log.set("upload all from backup")
        b = BackUp()
        keys = b.getAllkeys()
        for k in keys:
            Thread(target=upload_via_key_strem, args=[k['key'], k['type'], False]).start()
    except Exception as e:
        log.set(e.__str__())
        return

    log.set("all key as been diploaed")



mainWindow = tk.Tk()
mainWindow.title("Auto Managment Upload Tool  - AMUT")

log = StringVar()
logger = tk.Label(mainWindow,textvariable= log ,fg = "purple" )
log.set("log messages here")

cleanOp = lambda : clean_Op(log)
S_U_Op = lambda : runSearchAndUpload(log)
uploadFromBackUpFileOp = lambda : upLoapFromBackUp(log)

cleandb = tk.Button(mainWindow, text="clean DB" , command=cleanOp)
searchAndUpload = tk.Button(mainWindow, text="stars search and upload data",command=S_U_Op)
uploadFromKeyBackUP = tk.Button(mainWindow, text="upload all from backup",command=uploadFromBackUpFileOp)


in_side_spaceingX = 6
in_side_spaceingY = 6
out_side_spaceingX = 9
out_side_spaceingY = 9

searchAndUpload.grid(row = 0, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
cleandb.grid(row = 1, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
uploadFromKeyBackUP.grid(row = 2, column = 0, ipadx= in_side_spaceingX, ipady = in_side_spaceingY, padx =out_side_spaceingX, pady =out_side_spaceingY)
logger.grid(row = 3 ,column = 0,ipadx= in_side_spaceingX ,ipady = in_side_spaceingY,padx =out_side_spaceingX,pady =out_side_spaceingY)
mainWindow.mainloop()
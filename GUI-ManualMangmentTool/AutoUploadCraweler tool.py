import tkinter as tk
from tkinter import StringVar,ttk
from Factory.TaskFactory import TaskFactory
from util.DBconnector import DBConnector

import threading
import uuid
import time




def clean_Op(log,*args):
    log.set("start cleaning the DB")
    pass

def runSearchAndUpload(log):
    log.set("start search and upload data")
    #TODO get setting
    settings = DBConnector.readCollaction("settings")
    TaskFactory(settings).startWork()
    pass


def upLoapFromBackUp(log):
    log.set("upload all from backup")
    pass



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
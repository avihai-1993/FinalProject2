from Factory.ProjectTask import Task
from util.DBconnector import DBConnector
from threading import Thread


class TaskFactory():
   def __init__(self,settings):
      self.settings = settings

   def create_task(self,search_word,type_classifer):
       return Task(search_word,type_classifer)


   def startWork(self):
       for setting_type in self.settings:
           keywords = DBConnector().readCollaction("settings/" + setting_type + "/keywords")
           for kw in keywords:
               myTask = self.create_task(kw,setting_type)
               t = Thread(target=myTask.start, args=[1,keywords[kw]['lastTaskUrl']])
               t.start()

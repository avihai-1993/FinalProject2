from Factory.ProjectTask import Task
from util.DBconnector import DBConnector

class TaskFactory:
   def __init__(self,settings):
      self.settings = settings

   def create_task(self,search_word,type_classifer):
       return Task(search_word,type_classifer)


   def startWork(self):
       for setting_type in self.settings:
           keywords = DBConnector().readCollaction("settings/" + setting_type + "/keywords")
           for kw in keywords:
               self.create_task(kw,setting_type).start(5,keywords[kw]['lastTaskUrl'])

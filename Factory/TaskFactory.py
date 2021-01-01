from Factory.ProjectTask import Task


class TaskFactory:
   def __init__(self,settings):
      self.settings = settings

   def create_task(self,search_word,type_classifer):
       return Task(search_word,type_classifer)


   def startWork(self):
       for setting in self.settings:
           for kw in setting["keywords"]:
             self.create_task(kw,setting).start(5,setting["lastTaskUrl"])

from Factory.ProjectTask import Task


class TaskFactory:
   def __init__(self,outputDir,settings):
      self.outputdir = outputDir
      self.settings = settings

   def create_task(self,search_word,bank_of_words):
       return Task(search_word,bank_of_words,self.outputdir)


   def startWork(self):
       for setting in self.settings:
           pass
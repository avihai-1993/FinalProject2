from Factory.ProjectTask import Task


class TaskFactory:
   def __init__(self,outputDir):
      self.outputdir = outputDir

   def create_task(self,search_word,bank_of_words):
       return Task(search_word,bank_of_words,self.outputdir)



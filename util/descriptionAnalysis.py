import re


def importBankfromFile(file_name):
    bank = []
    file = open(file_name,'r')
    numOfLines = int(file.readline())
    for i in range(numOfLines):
        bank.append(file.readline().replace("\n", ""))
    return Analyst(bank)


class Analyst:

    bank = []
    def __init__(self,bank_of_term):
        self.bank = bank_of_term


    def sumOfMatchesInString(self, inputString):
        s = 0
        for term in self.bank:
           s = s + len(re.findall(term, inputString))


        return s

    def calculateScore(self,youTubeVideoRefKeywords,youTubeVideoRefTitle):
        pass
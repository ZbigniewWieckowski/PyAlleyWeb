
import random

class Player:
    def __init__(self,name,nationality,suppressPrint=0,playerType=''):
        self.suppressPrint = suppressPrint
        self.sprint('Starting player initialization ...')
        # Initialize player
        self.name = name
        self.nationality = nationality
        self.playerType = playerType
        self.savedChallengesByOthers = []
        self.savedChallengesOfOthers = []
        self.sprint('Finished player initialization ...')
    def sprint(self,msg,end='\n'):
        if 0 == self.suppressPrint:
            print(msg,end)
    def getName(self):
        return self.name
    def setName(self,name):
        self.name = name
    def getNationality(self):
        return self.nationality
    def setNationality(self,nationality):
        self.nationality = nationality
    def getPlayerType(self):
        return self.playerType
    def setPlayerType(self,playerType):
        self.playerType = playerType
    def __str__(self):
        return '{0} is a {1} {2}'.format(self.name, self.nationality, self.playerType)
    def move(self,board):
        # TBD - implement player move
        self.sprint('Player:move() - TBD')
    def saveChallengeByOthers(self,byPlayer,guessedNationality):
        self.savedChallengesByOthers.append([byPlayer.getName(),guessedNationality])
    def getSavedChallengesByOthers(self):
        return self.savedChallengesByOthers;
    def saveChallengeOfOthers(self,playerChallenged,guessedNationality,success):
        self.savedChallengesOfOthers.append([playerChallenged.getName(),guessedNationality,success])
    def getSavedChallengesOfOthers(self):
        return self.savedChallengesOfOthers;
    def printResources(self, board):
        if self.suppressPrint == 0:
            print('')
            pRes = board.getPlayersResources(self)
            print('            ', end='')
            for nat in board.getAllAvailableNationalities():
                print(' ' + nat[0], end='')
            print('')
        
            resType = 'Password'
            print(resType + '   :', end='')
            for nat in board.getAllAvailableNationalities():
                print(' ' + str(pRes[nat][resType]), end='')
            print('')

            resType = 'Disguise'
            print(resType + '   :', end='')
            for nat in board.getAllAvailableNationalities():
                print(' ' + str(pRes[nat][resType]), end='')
            print('')

            resType = 'CodeBook'
            print(resType + '   :', end='')
            for nat in board.getAllAvailableNationalities():
                print(' ' + str(pRes[nat][resType]), end='')
            print('')

            resType = 'Key'
            print(resType + '        :', end='')
            for nat in board.getAllAvailableNationalities():
                print(' ' + str(pRes[nat][resType]), end='')
            print('')

            print('')
            print('Move Cards : ' + str(len(board.getPlayersMoveCards(self))) + ' ' + str(board.getPlayersMoveCards(self)))
            print('Money      : $' + str(board.getPlayersMoney(self)))
            print('Wild Cards : ' + str(board.getPlayersWildCards(self)))
            print('')
    def hasAllResourcesOfType(self,board,resType):
        pRes = board.getPlayersResources(self)
        hasAll = 1
        for nat in board.getAllAvailableNationalities():
            if 0 == pRes[nat][resType]:
                hasAll = 0
                break
        return hasAll
    def checkWinningCriteria(self,board):
        numberOfWildcards = board.getPlayersWildCards(self)
        pRes = board.getPlayersResources(self)
        numberOfNatResources = 0
        for resType in board.getPlayersResourceTypes():
            numberOfNatResources = numberOfNatResources + pRes[self.nationality][resType]
        if numberOfNatResources + numberOfWildcards >= 4:
            self.sprint('Player ' + self.name + ' collected all item and exited through embassy !!!')
            board.recordExitThroughEmbassy(self)


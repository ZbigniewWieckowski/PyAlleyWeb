# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.11.2 (main, Nov 30 2024, 21:22:50) [GCC 12.2.0]
# Embedded file name: Z00_Bot.py
# Compiled at: 2017-03-04 23:07:34
import random
from Player import Player
from ComputerPlayer import ComputerPlayer

class Z00_Bot(ComputerPlayer):

    def __init__(self, name, nationality, suppressPrint=0):
        ComputerPlayer.__init__(self, name, nationality, suppressPrint)
        self.priorCombinations = []

    def handleChallengePhase(self, board):
        combinationsToCheck = []
        plist = list(board.getActivePlayers())
        plist.remove(self)
        for p in plist:
            self.sprint('Checking player ' + p.getName())
            natToCheck = list(board.getAllAvailableNationalities())
            natToCheck.remove(self.getNationality())
            for ch in self.getSavedChallengesOfOthers():
                if (1 == ch[2] or p == ch[0]) and natToCheck.count(ch[1]) == 1:
                    natToCheck.remove(ch[1])

            for ch in self.getSavedChallengesByOthers():
                if p == ch[0] and natToCheck.count(ch[1]) == 1:
                    natToCheck.remove(ch[1])

            for nat in natToCheck:
                numberOfWildcards = board.getPlayersWildCards(p)
                pRes = board.getPlayersResources(p)
                numberOfNatResources = 0
                for resType in board.getPlayersResourceTypes():
                    numberOfNatResources = numberOfNatResources + pRes[nat][resType]

                if numberOfNatResources + numberOfWildcards >= 4:
                    initPos = board.getPlayersPosition(p)
                    if initPos == nat + 'Embassy':
                        self.appendToPriorCombinations([p, nat])
                    for mv in board.getPlayersMoveCards(p):
                        pos = initPos
                        for i in range(1, mv + 1):
                            if pos == 'SpyAlleyEntrance':
                                pos = 'Collect$20'
                            else:
                                pos = board.nextSpace(pos)[0]

                        if pos == nat + 'Embassy':
                            previouslyConsidered = 0
                            for pc in self.getPriorCombinations():
                                if pc[0] == p and pc[1] == nat:
                                    previouslyConsidered = 1
                                    break

                            if 0 == previouslyConsidered:
                                combinationsToCheck.append([p, nat])
                                self.appendToPriorCombinations([p, nat])

        combCount = len(combinationsToCheck)
        if combCount > 0:
            combPick = combinationsToCheck[round(random.random() * combCount - 0.5)]
            self.sprint('Picked comb = ' + combPick[0].getName() + ' ' + combPick[1])
            p = combPick[0]
            nat = combPick[1]
            self.sprint('')
            self.sprint('!!! Challenging player ' + p.getName())
            if p.getPlayerType() == 'Human':
                input('Summon human player ' + p.getName() + ', press [Enter] when ready ...')
                self.sprint('')
                self.sprint('Guessing s/he is a ' + nat)
                input(p.getName() + ' - Please confirm by pressing [Enter] ...')
                for i in range(1, 100):
                    self.sprint('')

                self.sprint('')
            if nat == p.getNationality():
                self.sprint('Challenge successful - player ' + p.getName() + ' is out!')
                self.saveChallengeOfOthers(p, nat, 1)
                board.deactivatePlayer(p)
                board.transferResources(p, self)
                if random.random() > 0.5:
                    board.switchNationalities(p, self)
            else:
                self.sprint('Challenge was not successful, current player is out!')
                p.saveChallengeByOthers(self, nat)
                board.deactivatePlayer(self)
                board.transferResources(self, p)
                if 'Human' == p.getPlayerType():
                    completedSwitch = 0
                    while 0 == completedSwitch:
                        switchAnswer = input('Question for ' + p.getName() + ' - do you want to switch nationalities with ' + self.getName() + ' and become ' + self.getNationality() + '? (y/n): ')
                        if 'y' == switchAnswer or 'Y' == switchAnswer:
                            self.sprint('Switched nationality to ' + self.getNationality())
                            board.switchNationalities(p, self)
                            input('Acknowledge switching to new nationality. Press [Enter]')
                            for i in range(1, 100):
                                self.sprint('')

                            completedSwitch = 1
                        elif 'n' == switchAnswer or 'N' == switchAnswer:
                            for i in range(1, 100):
                                self.sprint('')

                            completedSwitch = 1
                        else:
                            self.sprint('Unrecognized answer, please try again ...')

                else:
                    p.decideWhetherToSwitchNationality(board, self)
        self.sprint('Did not challenge')
        return 0

    def getPriorCombinations(self):
        return self.priorCombinations

    def appendToPriorCombinations(self, comb):
        self.priorCombinations.append(comb)

# okay decompiling Z00_Bot.pyc

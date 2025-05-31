
import math
import random
from Player import Player
from ComputerPlayer import ComputerPlayer
from Z00_Bot import Z00_Bot


class J00_Bot(ComputerPlayer):
    def __init__(self,name,nationality,suppressPrint=0):
        ComputerPlayer.__init__(self, name, nationality, suppressPrint);
    # custom methods to override
    # def handleChallengePhase(self,board):
    # def pickMoveCardToUse(self,board):
    # def pickNextPosition(self,board,nextPos):
    # def isBuyPassword(self,board):
    # def buyMultipleResources(self,board,resType):
    # def buyResourcesOnBlackMarket(self,board):
    # def pickNationalityToChallengePlayer(self,board,player):
    # def pickPlayerToConfiscateWildCardFrom(self,board,playersWithWildCards):
    # def handleConfiscateMaterials(self,board):
    # def decideWhetherToSwitchNationality(self,board,otherPlayer):
    

class HumanPlayer(Player):
    def __init__(self,name,nationality,suppressPrint=0,playerType='Human'):
        self.sprint('Starting computer player initialization ...')
        # Initialize computer player        
        Player.__init__(self, name, nationality, suppressPrint, playerType)
        self.sprint('Finished computer player initialization ...')
    def move(self,board,printResources='yes'):
        self.sprint('')
        self.sprint('Starting move of ' + self.name)
        # Challenge phase
        challengeInProgress = 1
        while (challengeInProgress == 1):
            isChallenge = input('Challenge phase - do you want to challenge? (y/n)?')
            if isChallenge == 'n' or isChallenge == 'N':
                challengeInProgress = 0
                self.sprint('Skipped the challenge phase')
            elif isChallenge == 'y' or isChallenge == 'Y':
                foundPlayer = 0
                challengedName = input('Name player to be challenged: ')
                for p in board.getActivePlayers():
                    if (challengedName == p.getName()):
                        if (p == self):
                            self.sprint('Sorry, you cannot challenge yourself')
                        else:
                            foundPlayer = 1
                            playerToBeChallenged = p
                            break
                if (foundPlayer == 0):
                    self.sprint('Name is not one of the active players'' names ...')
                else:
                    challengedNationality = input('What are you guessing the players nationality is? : ')
                    foundNationality = 0
                    for n in board.getAllAvailableNationalities():
                        if (challengedNationality == n):
                            foundNationality = 1
                    challengeInProgress = 0
                    if (foundNationality == 0):
                        self.sprint('Not one of the nationalities in the game: ')
                    else:
                        self.sprint('')
                        self.sprint('!!! Challenging player ' + playerToBeChallenged.getName() + ', guessing s/he is a ' + challengedNationality)
                        self.sprint('')
                        if (challengedNationality == playerToBeChallenged.getNationality()):
                            self.sprint('Challenge successful - player ' + playerToBeChallenged.getName() + ' is out!')
                            self.saveChallengeOfOthers(playerToBeChallenged,challengedNationality,1)
                            board.deactivatePlayer(playerToBeChallenged)
                            board.transferResources(playerToBeChallenged,self)
                            completedSwitch = 0
                            while 0 == completedSwitch:
                                switchAnswer = input('Do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                                if 'y' == switchAnswer or 'Y' == switchAnswer:
                                    board.switchNationalities(playerToBeChallenged, self)
                                    completedSwitch = 1
                                elif 'n' == switchAnswer or 'N' == switchAnswer:
                                    completedSwitch = 1
                                else:
                                    self.sprint('Unrecognized answer, please try again ...')
                        else:
                            self.sprint('Challenge was not successful, current player is out!')
                            playerToBeChallenged.saveChallengeByOthers(self,challengedNationality)
                            board.deactivatePlayer(self)
                            board.transferResources(self, playerToBeChallenged)
                            if 'Human' == playerToBeChallenged.getPlayerType():
                                completedSwitch = 0
                                while 0 == completedSwitch:
                                    switchAnswer = input('Question for ' + playerToBeChallenged.getName() + ' - do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                                    if 'y' == switchAnswer or 'Y' == switchAnswer:
                                        board.switchNationalities(playerToBeChallenged, self)
                                        self.sprint('Switched nationality to ' + self.getNationality())
                                        input('Acknowledge switching to new nationality. Press [Enter]')
                                        for i in range(1,100):
                                            self.sprint('')
                                        completedSwitch = 1
                                    elif 'n' == switchAnswer or 'N' == switchAnswer:
                                        completedSwitch = 1
                                    else:
                                        self.sprint('Unrecognized answer, please try again ...')
                            else:
                                playerToBeChallenged.decideWhetherToSwitchNationality(board,self)
                    return 
            else:
                self.sprint('Unrecognized answer - please try again ...')
        # Advance stage
        if board.isPlayerActive(self) and len(board.getActivePlayers()) > 1:
            moveCards = board.getPlayersMoveCards(self)
            isMoveCardUsed = 0
            moveCardCount = len(moveCards)
            if moveCardCount > 0:
                self.sprint('You have the following move cards: ' + str(moveCards))
                gotUseMoveCardDecision = 0
                while 0 == gotUseMoveCardDecision:
                    useMoveCard = input('Your position is ' + board.getPlayersPosition(self) + '. Use move card? (y/n)')
                    if useMoveCard == 'Y' or useMoveCard == 'y':
                        isMoveCardUsed = 1
                        gotUseMoveCardDecision = 1
                    elif useMoveCard == 'N' or useMoveCard == 'n':
                        gotUseMoveCardDecision = 1
                    else:
                        self.sprint('Incorrect answer - please try again ...')
                if 1 == isMoveCardUsed:
                    allSame = 1
                    firstCard = moveCards[0]
                    for ix in range(1, moveCardCount):
                        if moveCards[ix] != firstCard:
                            allSame = 0
                            break
                    if 1 == allSame:
                        moveCardValue = moveCards[0]
                    else:
                        gotMoveCardValue = 0
                        while 0 == gotMoveCardValue:
                            moveCardValue = eval(input('Which move card to use?'))
                            foundValue = 0
                            for ix in range(0, moveCardCount):
                                if moveCards[ix] == moveCardValue:
                                    foundValue = 1
                                    break
                            if 1 == foundValue:
                                gotMoveCardValue = 1
            if 1 == isMoveCardUsed:
                diceRoll = moveCardValue
                board.discardMoveCard(self, moveCardValue)
                self.sprint('Used move card of value ' + str(moveCardValue))
            else:   
                diceRoll = round(random.random()*6+0.5)
                self.sprint('Human advance phase - rolled ' + str(diceRoll))
            posList = []
            posList.append(board.getPlayersPosition(self))
            for i in range(1, diceRoll+1):
                if i == 1 and posList[0] == 'SpyAlleyEntrance':
                    posList = ['Collect$20']
                else:
                    # self.sprint('posList = ' + str(posList))
                    nextPos = []
                    for pos in posList:
                        for next in board.nextSpace(pos):
                            nextPos.append(next)
                    posList = nextPos
                    if posList[0] == 'Start':
                        board.passingStart(self)
            # self.sprint('posList = ' + str(posList))
            if (len(posList) == 1):
                pos = posList[0]
            else:
                gotDecision = 0
                while (gotDecision == 0):
                    moveDecision = input('(1) move to ' + str(posList[0]) + ' or (2) move to ' + str(posList[1]) + ' ? : ')
                    if (moveDecision == '1' or moveDecision == '2'):
                          gotDecision = 1
                    else:
                          self.sprint('Invalid choice: ' + moveDecision + ', try again')
                pos = posList[eval(moveDecision)-1]
                self.sprint('Decided to move to ' + pos)
            board.setPlayersPosition(self, pos)
            self.sprint('Ended up on ' + pos)
            # Check for winning criteria
            if pos == self.nationality + 'Embassy':
                self.checkWinningCriteria(board)
            # Action for current position
            if len(board.getActivePlayers()) > 1:                   
                # Handle landing on password space
                if pos in board.getAllAvailableNationalities():
                    if 0 == board.getPlayersResources(self)[pos]['Password']:
                        self.buyingPassword(board,pos)
                # Handle landing on move card space
                if 'MoveCard' == pos[0:8]:
                    board.assignMoveCard(self)
                # Handle landing on resource space
                if 'Disguises' == pos or 'CodeBooks' == pos or 'Keys' == pos:
                    resType = pos[0:len(pos)-1]                
                    if 0 == self.hasAllResourcesOfType(board, resType):
                        amountPerResource = board.getAmountPerResourceType(resType)
                        if board.getPlayersMoney(self) < amountPerResource:
                            self.sprint('Not enough money to buy ' + resType + ' at this time.')
                        else:
                            self.buyingResource(board, resType)
                    else:
                        self.sprint('Already have all ' + resType + 's. Moving on')
                # Handle landing on collect $10 space
                if 'Collect$10' == pos:
                    board.updateFunds(self,10)
                # Handle landing on collect $20 space
                if 'Collect$20' == pos:
                    board.updateFunds(self,20)
                # Handle landing on border crossing space
                if 'BorderCrossing' == pos:
                    if board.getPlayersMoney(self) < 5:
                        self.sprint('Not enough funds for crossing the border - landing on Spy Alley Entrance instead.')
                        board.setPlayersPosition(self, 'SpyAlleyEntrance')
                    else:
                        self.sprint('Collecting $5 for border crossing')
                        board.updateFunds(self,-5)
                # Handle landing on move back 2 spaces space
                if 'MoveBack2Spaces' == pos:
                    self.sprint('Moving back 2 spaces to Spy Alley Entrance')
                    board.setPlayersPosition(self, 'SpyAlleyEntrance')
                # Handle landing on black market space
                if 'BlackMarket' == pos[0:11]:
                    # Buy resource at random\
                    self.buyResourceOnBlackMarket(board)
                # Handle landing on spy eliminator space
                if 'SpyEliminator' == pos:
                    for p in board.getActivePlayers():
                        if p != self and board.isSpaceInSpyAlley(board.getPlayersPosition(p)):                            
                            self.freeChallenge(board, p);
                # Handle landing on free gift space
                if 'FreeGift' == pos[0:8]:
                    gc = board.getRandomGiftCard()
                    if 'WildCard' == gc[0]:
                        board.assignWildCard(self,'no')
                    else:
                        if 0 == board.getPlayersResources(self)[gc[0]][gc[1]]:
                            board.assignResource(self,gc[0],gc[1],'no')
                        else:
                            self.sprint('Already had ' + gc[0] + ' ' + gc[1])
                    board.discardGiftCard(gc)
                # Handle landing on confiscate materials space
                if 'ConfiscateMaterials' == pos:
                    self.confiscateMaterials(board)
                # Handle landing on take another turn space
                if 'TakeAnotherTurn' == pos:
                    self.sprint('Taking another turn...')
                    self.move(board,'no')
                if self.sprintResources == 'yes':
                    self.self.sprintResources(board)
                    self.sprint('Finished move of ' + self.name)
    def buyingPassword(self,board,nat):               
        buyPasswordInProgress = 1
        while (buyPasswordInProgress == 1):
            buyPassword = input('Do you want to buy ' + nat + ' password? (y/n)?')
            if buyPassword == 'n' or buyPassword == 'N':
                buyPasswordInProgress = 0
                self.sprint('Skipped buying password')
            elif buyPassword == 'y' or buyPassword == 'Y':
                board.assignPassword(self, nat)
                buyPasswordInProgress = 0
            else:
                self.sprint('Unrecognized answer - please try again ...')
    def buyingResource(self,board,resType):
        pRes = board.getPlayersResources(self)
        amountPerResource = board.getAmountPerResourceType(resType)
        self.sprint('Available funds: $' + str(board.getPlayersMoney(self)))
        self.sprint('You have the following ' + resType + 's:')
        self.sprint('')
        self.sprint('            ', end='')
        for nat in board.getAllAvailableNationalities():
            self.sprint(' ' + nat[0], end='')
        self.sprint('')
        self.sprint(resType + ('        :' if 'Key' == resType else '   :'), end='')
        for nat in board.getAllAvailableNationalities():
            self.sprint(' ' + str(pRes[nat][resType]), end='')
        self.sprint('')
        buyResourceInProgress = 1
        another = ''
        while (buyResourceInProgress == 1):
            buyResource = input('Do you want to buy ' + another + resType + '? (y/n)?')
            if buyResource == 'n' or buyResource == 'N':
                buyResourceInProgress = 0
                self.sprint('Done buying ' + resType + 's')
            elif buyResource == 'y' or buyResource == 'Y':
                # Check if only one missing
                numberMissing = 0
                lastNatMissing = ''
                for nat in board.getAllAvailableNationalities():
                    if 0 == pRes[nat][resType]:
                        numberMissing += 1
                        lastNatMissing = nat
                        if numberMissing > 1:
                            break
                if 1 == numberMissing:
                    if board.getPlayersMoney(self) >= amountPerResource:
                        board.assignResource(self, lastNatMissing, resType)
                    else:
                        self.sprint('Not enough funds for buying another ' + resType)
                else:
                    gotResourceNationality = 0
                    while 0 == gotResourceNationality:
                        nat = input('Enter nationality for ' + resType + ' , first letters, or qQ:')
                        if 'q' == nat or 'Q' == nat:
                            buyResourceInProgress = 0
                            break
                        elif nat in board.getAllAvailableNationalities():
                            if 0 == pRes[nat][resType]:
                                board.assignResource(self, nat, resType)
                                gotResourceNationality = 1
                                another = 'another '
                            else:
                                self.sprint('You already have ' + nat + ' ' + resType)
                        else:
                            natList = []
                            error = 0
                            for n in list(nat.upper()):
                                if n in ['A', 'F', 'G', 'I', 'R', 'S']:
                                    n1 = board.lookupNationality(n)
                                    if not n1 in natList:
                                        natList.append(n1)
                                else:
                                    error = 1
                                    break
                            if 1 == error:
                                self.sprint('Incorrectly entered nationality. Try again:')
                            else:
                                if board.getPlayersMoney(self) >= len(natList) * amountPerResource:
                                    for n in natList:
                                        board.assignResource(self, n, resType)
                                    buyResourceInProgress = 0
                                    break
                                else:
                                    self.sprint('Not enough funds for buying + nat ' + resType)
                    if buyResourceInProgress and board.getPlayersMoney(self) < amountPerResource:
                        self.sprint('Not enough funds for buying another ' + resType)
                        buyResourceInProgress = 0
            else:
                self.sprint('Unrecognized answer - please try again ...')
    def buyResourceOnBlackMarket(self,board):
        pRes = board.getPlayersResources(self)
        availableFunds = board.getPlayersMoney(self)
        if availableFunds == 0:
            self.sprint('No funds. Skipping ...')
        else:
            buyResourceInProgress = 1
            while (buyResourceInProgress == 1):
                buyResource = input('You have $' + str(availableFunds) + '. Do you want to buy resource on black market? (y/n)?')
                if buyResource == 'n' or buyResource == 'N':
                    buyResourceInProgress = 0
                    self.sprint('Done buying resource on black market')
                elif buyResource == 'y' or buyResource == 'Y':
                    gotResourceType = 0
                    while 0 == gotResourceType:
                        resTypeAnswer = input('Enter resource type (1) Password, (2) Disguise, (3) Code Book, (4) Key:')
                        resType = 'Password' if '1' == resTypeAnswer else ('Disguise' if '2' == resTypeAnswer else ('CodeBook' if '3' == resTypeAnswer else ('Key' if '4' == resTypeAnswer else 'Error')))
                        if 'Error' == resType:
                            self.sprint('Incorrect response, please retry')
                        else:
                           gotResourceType = 1
                    amountPerResource = board.getAmountPerResourceType(resType)
                    if 'WildCard' == resType:
                        if availableFunds >= amountPerResource:
                            board.assignWildCard(self)
                            break
                    gotResourceNationality = 0
                    while 0 == gotResourceNationality:
                        nat = input('Enter nationality , first letter, or qQ:')
                        if 'q' == nat or 'Q' == nat:
                            buyResourceInProgress = 0
                            break
                        elif nat in board.getAllAvailableNationalities():
                            if 0 == pRes[nat][resType]:
                                board.assignResource(self, nat, resType)
                                gotResourceNationality = 1
                                another = 'another '
                            else:
                                self.sprint('You already have ' + nat + ' ' + resType)
                        else:
                            error = 1 != len(nat)
                            if 0 == error:
                                natList = []
                                error = 0
                                for n in list(nat.upper()):
                                    if n in ['A', 'F', 'G', 'I', 'R', 'S']:
                                        n1 = board.lookupNationality(n)
                                        if not n1 in natList:
                                            natList.append(n1)
                                    else:
                                        error = 1
                                        break
                            if 1 == error:
                                self.sprint('Incorrectly entered nationality. Try again:')
                            else:
                                if availableFunds >= len(natList) * amountPerResource:
                                    for n in natList:
                                        if 0 == pRes[n][resType]:
                                            board.assignResource(self, n, resType)
                                        else:
                                            self.sprint('You already have ' + n + ' ' + resType)
                                    buyResourceInProgress = 0
                                    break
                                else:
                                    self.sprint('Not enough funds for buying' + str(natList) + ' ' + resType)
                else:
                    self.sprint('Unrecognized answer - please try again ...')
    def freeChallenge(self,board,challengedOpponent):
        completedChallenge = 0
        while 0 == completedChallenge:
            self.sprint('Freely challenging ' + challengedOpponent.getName())
            self.sprint('Challenges of others: ' + str(self.getSavedChallengesOfOthers()))
            self.sprint('Challenges by others: ' + str(self.getSavedChallengesByOthers()))
            challengedNationality = input('What are you guessing the players nationality is, or first letter? : ')
            foundNationality = 0
            if 1 == len(challengedNationality):
                challengedNationality = board.lookupNationality(challengedNationality)
            for n in board.getAllAvailableNationalities():
                if (challengedNationality == n):
                    foundNationality = 1
            if (foundNationality == 0):
                    self.sprint('Not one of the nationalities in the game: ')
            else:
                self.sprint('')
                self.sprint('!!! Challenging player ' + challengedOpponent.getName() + ', guessing s/he is a ' + challengedNationality)
                self.sprint('')
                if (challengedNationality == challengedOpponent.getNationality()):
                    self.sprint('Challenge successful - player ' + challengedOpponent.getName() + ' is out!')
                    self.saveChallengeOfOthers(challengedOpponent,challengedNationality,1)
                    board.deactivatePlayer(challengedOpponent)
                    board.transferResources(challengedOpponent, self)
                    completedSwitch = 0
                    while 0 == completedSwitch:
                        switchAnswer = input('Do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                        if 'y' == switchAnswer or 'Y' == switchAnswer:
                            board.switchNationalities(challengedOpponent, self)
                            completedSwitch = 1
                            self.sprint('Switched nationality to ' + self.getNationality())
                            input('Acknowledge switching to new nationality. Press [Enter]')
                            for i in range(1,100):
                                self.sprint('')
                        elif 'n' == switchAnswer or 'N' == switchAnswer:
                            completedSwitch = 1
                        else:
                            self.sprint('Unrecognized answer, please try again ...')
                else:
                    self.saveChallengeOfOthers(challengedOpponent,challengedNationality,0)
                    challengedOpponent.saveChallengeByOthers(self,challengedNationality)
                    self.sprint('Challenge was not successful')
                completedChallenge = 1
    def confiscateMaterials(self,board):
        availableFunds = board.getPlayersMoney(self)
        transferDone = 0
        while 0 == transferDone:
            pickedPlayer = 0
            while 0 == pickedPlayer:
                confMatPlayer = input('Which player to confiscate materials from, or Qq?: ')
                if 'q' == confMatPlayer or 'Q' == confMatPlayer:
                    transferDone = 1
                    break
                else:
                    foundPlayer = 0
                    for p in board.getActivePlayers():
                        if p.getName() == confMatPlayer:
                            foundPlayer = 1
                            break
                    if 0 == foundPlayer:
                        self.sprint('Invalid player, try again ...')
                    else:
                        pickedPlayer = 1 
                        gotResourceType = 0
                        while 0 == gotResourceType:
                            resTypeAnswer = input('Enter resource type (1) Password, (2) Disguise, (3) Code Book, (4) Key, (5) WildCard :')
                            resType = 'Password' if '1' == resTypeAnswer else ('Disguise' if '2' == resTypeAnswer else ('CodeBook' if '3' == resTypeAnswer else ('Key' if '4' == resTypeAnswer else ('WildCard' if '5' == resTypeAnswer else 'Error'))))
                            if 'Error' == resType:
                                self.sprint('Incorrect response, please retry')
                            else:
                               gotResourceType = 1
                        amountPerResource = board.getConfiscateMaterialsPrices(resType)
                        if 'WildCard' == resType:
                            if availableFunds >= amountPerResource:
                                if board.getPlayersWildCards(p) > 0:
                                    board.confiscateWildCard(p)
                                    board.updateFunds(self, -amountPerResource)
                                    board.assignWildCard(self,'no')
                                    transferDone = 1
                                    self.sprint('Confiscated Wild Card from ' + p.getName())
                        else:
                            pickedNationality = 0
                            while 0 == pickedNationality:
                                nat = input('Pick nationality, first letter, or Qq:')
                                if 'q' == nat or 'Q' == nat:
                                    pickedPlayer = 1
                                    transferDone = 1
                                    break
                                elif nat.upper() in ['A', 'F', 'G', 'I', 'R', 'S']:
                                    nat = board.lookupNationality(nat)
                                    pickedNationality = 1
                                elif nat in board.getAllAvailableNationalities():
                                    pickedNationality = 1
                                else:
                                    self.sprint('Invalid nationality, try again ...')
                                if 1 == pickedNationality:
                                    if 1 == board.getPlayersResources(self)[nat][resType]:
                                          self.sprint('You already have ' + nat + ' ' + resType)
                                    else:
                                          if 0 == board.getPlayersResources(p)[nat][resType]:
                                              self.sprint(p.getName() + ' does not have ' + nat + ' ' + resType)
                                          else:
                                              board.confiscateMaterial(p, nat, resType)
                                              board.updateFunds(self, -amountPerResource)
                                              board.assignResource(self, nat, resType, 'no')
                                              transferDone = 1
                                              self.sprint('Confiscated ' + nat + ' ' + resType + ' from ' + p.getName())


class SpyAlleyBoard:
    def __init__(self, suppressPrint=0):
        self.suppressPrint = suppressPrint
        self.sprint('Starting game board initialization ...')
        # Initialize game board
        self.players = []
        self.activePlayers = []
        self.allAvailableNationalities = ['American', 'French', 'German', 'Italian', 'Russian', 'Spanish']
        self.nationalityLookup = { 'A':'American', 'F':'French', 'G':'German', 'I':'Italian', 'R':'Russian', 'S':'Spanish' }
        self.nextSpaceLookup = {
              'Start'               : ['Russian'],
              'Russian'             : ['MoveCard#1'],
              'MoveCard#1'          : ['Disguises'],
              'Disguises'           : ['American'],
              'American'            : ['MoveCard#2'],
              'MoveCard#2'          : ['TakeAnotherTurn'],
              'TakeAnotherTurn'     : ['FreeGift#1'],
              'FreeGift#1'          : ['Collect$10'],
              'Collect$10'          : ['Italian'],
              'Italian'             : ['Keys'],
              'Keys'                : ['Spanish'],
              'Spanish'             : ['MoveCard#3'],
              'MoveCard#3'          : ['BlackMarket#1'],
              'BlackMarket#1'       : ['SpyAlleyEntrance'],
              'SpyAlleyEntrance'    : ['Collect$20', 'BorderCrossing'],
              'Collect$20'          : ['SpyEliminator'],
              'SpyEliminator'       : ['FrenchEmbassy'],
              'FrenchEmbassy'       : ['GermanEmbassy'],
              'GermanEmbassy'       : ['ConfiscateMaterials'],
              'ConfiscateMaterials' : ['SpanishEmbassy'],
              'SpanishEmbassy'      : ['ItalianEmbassy'],
              'ItalianEmbassy'      : ['AmericanEmbassy'],
              'AmericanEmbassy'     : ['RussianEmbassy'],
              'RussianEmbassy'      : ['MoveCard#5'],
              'BorderCrossing'      : ['MoveBack2Spaces'],
              'MoveBack2Spaces'     : ['German'],
              'German'              : ['CodeBooks'],
              'CodeBooks'           : ['MoveCard#4'],
              'MoveCard#4'          : ['FreeGift#2'],
              'FreeGift#2'          : ['French'],
              'French'              : ['MoveCard#5'],
              'MoveCard#5'          : ['BlackMarket#2'],
              'BlackMarket#2'       : ['Start']
            }
        self.moveCards = [ 5, 4, 5, 2, 3, 4, 2, 1, 4, 3, 2, 6, 1, 6, 2, 6, 2, 1, 3, 5, 5, 3, 3, 1, 4, 6, 5, 4, 5, 1, 3, 2, 6, 1, 4, 6 ]
        self.moveCardsDiscardPile = []
        self.giftCards = [
            ['American', 'Disguise'],
            ['Russian',  'CodeBook'],
            ['Spanish',  'Disguise'],
            ['French',   'Disguise'],
            ['Italian',  'CodeBook'],
            ['French',   'CodeBook'],
            ['Russian',  'CodeBook'],
            ['Italian',  'Disguise'],
            ['German',   'Disguise'],
            ['Russian',  'Disguise'],
            ['Spanish',  'CodeBook'],
            ['Italian',  'Disguise'],
            ['German',   'Key'],
            ['Spanish',  'Key'],
            ['Italian',  'Disguise'],
            ['Russian',  'Key'],
            ['Russian',  'Disguise'],
            ['Italian',  'CodeBook'],
            ['French',   'Disguise'],
            ['Spanish',  'CodeBook'],
            ['French',   'Key'],
            ['Russian',  'Disguise'],
            ['German',   'CodeBook'],
            ['Spanish',  'Disguise'],
            ['American', 'Disguise'],
            ['WildCard'],
            ['WildCard'],
            ['Spanish',  'Disguise'],
            ['German',   'Disguise'],
            ['French',   'Disguise'],
            ['WildCard'],
            ['Italian',  'Key'],
            ['American', 'CodeBook'],
            ['German',   'Disguise'],
            ['German',   'CodeBook'],
            ['French',   'CodeBook'],
            ['American', 'Disguise'],
            ['American', 'Key'],
            ['WildCard'],
            ['American', 'CodeBook'],
          ]     
        self.giftCardsDiscardPile = []
        self.positions = {}
        self.playersResourceTypes = [ 'Password', 'Disguise', 'CodeBook', 'Key' ]
        self.playersResources = {}
        self.playersMoney = {}
        self.playersMoveCards = {}
        self.playersWildCards = {}
        self.sprint('Finished game board initialization ...')
    def sprint(self,msg,end='\n'):
        if 0 == self.suppressPrint:
            print(msg,end)
    def getAmountPerResourceType(self,resType):
        return 1 if 'Password' == resType else (5 if 'Disguise' == resType else (15 if 'CodeBook' == resType else (30 if 'Key' == resType else 10000)))
    def getConfiscateMaterialsPrices(self,resType):
        return 5 if 'Password' == resType else (5 if 'Disguise' == resType else (10 if 'CodeBook' == resType else (25 if 'Key' == resType else (50 if 'WildCard' == resType else 10000))))
    def lookupNationality(self,firstLetter):
        return self.nationalityLookup[firstLetter.upper()]
    def initializeFunds(self):
        startingFunds = 10*len(self.getPlayers())
        for p in self.getPlayers():
            self.playersMoney[p] = startingFunds
    def getPlayers(self):
        return self.players
    def getActivePlayers(self):
        return self.activePlayers
    def addPlayer(self,player):
        self.players.append(player)
        self.activePlayers.append(player)
        self.positions[player] = 'Start'
        self.playersResources[player] = {}
        for nat in self.allAvailableNationalities:
            self.playersResources[player][nat] = {}
            for resType in self.playersResourceTypes:
                self.playersResources[player][nat][resType] = 0
        self.playersMoveCards[player] = [ ]
        self.playersWildCards[player] = 0
    def deactivatePlayer(self,player):
        self.activePlayers.remove(player)
        self.sprint('Deactivating player ' + player.getName() + ', remaining are', end='')
        sep = ''
        for p in self.activePlayers:
            self.sprint(sep + ' ' + p.getName(), end='')
            sep = ','
        self.sprint('')
    def isPlayerActive(self,player):
        # Uncomment the next two lines, if debugging is needed
        # self.sprint('player = ' + player.getName())
        # self.sprint('active players = ' + str(self.activePlayers))
        return self.activePlayers.count(player) == 1
    def getPlayersPosition(self,player):
        return self.positions[player]
    def getPlayersResourceTypes(self):
        return self.playersResourceTypes
    def getPlayersMoney(self,player):
        return self.playersMoney[player]
    def getPlayersResources(self,player):
        return self.playersResources[player]
    def getPlayersMoveCards(self,player):
        return self.playersMoveCards[player]
    def getPlayersWildCards(self,player):
        return self.playersWildCards[player]
    def getMoveCardsDiscardPile(self):
        return self.moveCardsDiscardPile
    def getGiftCardsDiscardPile(self):
        return self.giftCardsDiscardPile
    def setPlayersPosition(self,player,space):
        self.positions[player] = space
    def getAllAvailableNationalities(self):
        return self.allAvailableNationalities
    def nextSpace(self,space):
        return self.nextSpaceLookup.get(space)
    def setPlayersPositionadvancePlayer(self,player,space):
        self.positions[player] = space
    def passingStart(self,player):
        self.playersMoney[player] += 15
        self.sprint(player.getName() + ' received $15 for passing Start')
    def assignPassword(self,player,nat):
        self.playersResources[player][nat]['Password'] = 1
        self.playersMoney[player] -= 1
        self.sprint(player.getName() + ' received ' + nat + ' Password')
    def assignResource(self,player,nat,resType,charge='yes'):
        self.playersResources[player][nat][resType] = 1
        if charge == 'yes':
            self.playersMoney[player] = self.playersMoney[player] - self.getAmountPerResourceType(resType)
        self.sprint(player.getName() + ' received ' + nat + ' ' + resType)
    def assignMoveCard(self,player):
        if 0 == len(self.moveCards):
            self.moveCards = self.moveCardsDiscardPile
            self.moveCardsDiscardPile = []
        pick = round(len(self.moveCards) * random.random() - 0.5)
        mc = self.moveCards[pick]
        self.moveCards.remove(mc)
        self.playersMoveCards[player].append(mc)
        self.sprint(player.getName() + ' received Move Card')
    def discardMoveCard(self, player, moveCardValue):
        self.playersMoveCards[player].remove(moveCardValue)
        self.moveCardsDiscardPile.append(moveCardValue)
    def assignWildCard(self,player,charge='yes'):
        self.playersWildCards[player] += 1
        if charge == 'yes':
            self.playersMoney[player] -= 50
        self.sprint(player.getName() + ' received Wild Card')
    def recordExitThroughEmbassy(self,winningPlayer):
        playersList = []
        for p in self.activePlayers:
            if p != winningPlayer:
                playersList.append(p)
        for p in playersList:
                self.deactivatePlayer(p)
    def updateFunds(self,player,amount):
        self.playersMoney[player] += amount
    def isSpaceInSpyAlley(self,pos):
        return 'Collect$20' == pos or 'SpyEliminator' == pos or 'FrenchEmbassy' == pos or 'GermanEmbassy' == pos or 'ConfiscateMaterials' == pos or 'SpanishEmbassy' == pos or 'ItalianEmbassy' == pos or 'AmericanEmbassy' == pos or 'RussianEmbassy' == pos
    def getRandomGiftCard(self):
        if 0 == len(self.giftCards):
            self.giftCards = self.giftCardsDiscardPile
            self.giftCardsDiscardPile = []
        pick = round(random.random()*len(self.giftCards)+0.5)-1
        gc = self.giftCards[pick]
        self.giftCards.remove(gc)
        return gc
    def discardGiftCard(self,gc):
        self.giftCardsDiscardPile.append(gc)
    def confiscateWildCard(self,player):
        amountPerResource = self.getConfiscateMaterialsPrices('WildCard')
        self.playersWildCards[player] -= 1
        self.playersMoney[player] += amountPerResource
    def confiscateMaterial(self,player,nat,resType):
        amountPerResource = self.getConfiscateMaterialsPrices(resType)
        self.playersResources[player][nat][resType] = 0
        self.playersMoney[player] += amountPerResource
    def transferResources(self,p1,p2):
        for nat in self.allAvailableNationalities:
            for resType in self.playersResourceTypes:
                if 1 == self.playersResources[p1][nat][resType]:
                    self.playersResources[p2][nat][resType] = 1
                    self.playersResources[p1][nat][resType] = 0
        for mc in self.playersMoveCards[p1]:
            self.playersMoveCards[p2].append(mc)
        self.playersMoveCards[p1] = []
        self.playersMoney[p2] += self.playersMoney[p1]
        self.playersMoney[p1] = 0
        self.playersWildCards[p2] += self.playersWildCards[p1]
        self.playersWildCards[p1] = 0
        self.sprint('Transferred resources from ' + p1.getName() + ' to ' + p2.getName())
    def switchNationalities(self,p1,p2):
        temp = p1.getNationality()
        p1.setNationality(p2.getNationality())
        p2.setNationality(temp)
    def hasAllResources(self,player):
        hasAll = 1
        for nat in self.allAvailableNationalities:
            if 0 == hasAll:
                break
            for resType in self.playersResourceTypes:
                if 0 == self.playersResources[player][nat][resType]:
                    hasAll = 0
                    break
        return hasAll


class SpyAlleyGame:
    def __init__(self,suppressPrint=0):
        self.suppressPrint = suppressPrint
        self.sprint('In SpyAlleyGame __init__')
    def sprint(self,msg,end='\n'):
        if 0 == self.suppressPrint:
            print(msg,end)
    def getBoard(self):
        return self.board
    def getActivePlayers(self):
        return self.ActivePlayers
    def play(self):
        self.sprint('Starting game initialization ...')
        self.board = SpyAlleyBoard(self.suppressPrint)
        # Initialize human players - ask them for names and secretly inform
        #    them of their nationality
        self.humanCount = 0
        if self.suppressPrint == 0:
            self.humanCount = eval(input('Enter number of human players: '))
        availableNationalities = list(self.board.getAllAvailableNationalities())
        for pn in range(1, self.humanCount+1):
            name = input('Name the human player #' + str(pn) + ": ")
            # Randomly select nationality
            pos = round(random.random()*len(availableNationalities)+0.5)
            #self.sprint('pos = ' + str(pos))
            nat = availableNationalities[pos-1]
            player = HumanPlayer(name, nat, self.suppressPrint)
            self.board.addPlayer(player)
            self.sprint(name + "'s position is " + self.board.getPlayersPosition(player))
            self.sprint(name + "'s nationality is " + nat)
            availableNationalities.remove(nat)
            input('Confirm receiving nationality. Press [Enter]')
            for i in range(1,100):
                self.sprint('')
        
        # Remaining players are computers
        for pn in range(0,6-self.humanCount):
            # Randomly select nationality
            # print('pn = ' + str(pn) + ', nats = ' + str(availableNationalities))
            if len(availableNationalities) == 1:
                nat = availableNationalities[0]
            else:
                pos = round(random.random()*len(availableNationalities)+0.5)
                #self.sprint("pos = " + str(pos))
                nat = availableNationalities[pos-1]
            if pn % 2 == 0:
                player = J00_Bot('J-bot #' + str(math.ceil((pn + 1) / 2)), nat, self.suppressPrint)
            else:
                player = Z00_Bot('Z-bot #' + str(math.ceil((pn + 1) / 2)), nat, self.suppressPrint)
            self.board.addPlayer(player)
            # Uncomment the next line for debug, otherwise nationalities are secret
            # print(player.getName() + "'s nationality is " + nat)
            availableNationalities.remove(nat)
            self.sprint(player.getName() + "'s position is " + self.board.getPlayersPosition(player))
        self.sprint('Finished game initialization ...')
        # Game loop
        self.getBoard().initializeFunds()
        gameInProgress = 1
        while (gameInProgress == 1):
            for p in self.getBoard().getPlayers():
                if (self.getBoard().isPlayerActive(p)):
                    p.move(self.getBoard())
                    if (len(self.getBoard().getActivePlayers()) == 1):
                        gameInProgress = 0
                        break
                    self.sprint('')
                    if 0 != self.humanCount:
                        input('Paused ... - press {Enter]')
        self.sprint('')
        self.sprint('!!! The winner is ' + self.getBoard().getActivePlayers()[0].getName())
        self.sprint('')
        if 0 != self.humanCount:
            input('Paused ... - press {Enter]')

batch=1
g=SpyAlleyGame(batch)
stats = { }
for i in range(0,1 if batch == 0 else 1000):
    print(str(i))
    g.play()
    win = g.getBoard().getActivePlayers()[0].getName()
    if win in stats:
        stats[win] += 1
    else:
        stats[win] = 1
for p in g.getBoard().getPlayers():
    if not p.getName() in stats:
        stats[p.getName()] = 0
for k in stats.keys():
    print(k + ' : ' + str(stats[k]) + ' wins')
print('')

if batch == 0:
    b=g.getBoard()
    # Get players
    for p in b.getPlayers():
        #print("# Get player's name")
        #print('p.getName():')
        print(p.getName())
        #print("# Get player's nationality")
        #print('p.getNationality():')
        print(p.getNationality())    
        #print("# Get player's last position")
        #print('b.getPlayersPosition(p):')
        print(b.getPlayersPosition(p))
        print('')
        print('Challenges of others: ' + str(p.getSavedChallengesOfOthers()))
        print('Challenges by others: ' + str(p.getSavedChallengesByOthers()))
        print('')
        print(p.getName() + "'s Resources:")
        p.printResources(b)
    print('Move card discard pile: ' + str(b.getMoveCardsDiscardPile()))
    print('Gift card discard pile: ' + str(b.getGiftCardsDiscardPile()))



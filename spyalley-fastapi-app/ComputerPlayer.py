
import random
from Player import Player

class ComputerPlayer(Player):
    def __init__(self,name,nationality,suppressPrint=0,playerType='Computer'):
        Player.__init__(self, name, nationality, suppressPrint, playerType)
        self.sprint('Starting computer player initialization ...')
        # Initialize computer player
        self.sprint('Finished computer player initialization ...')
    def move(self,board,printResources='yes'):
        self.sprint('')
        self.sprint('Starting move of ' + self.name)
        # Challenge phase
        if (self.handleChallengePhase(board)):
            return
        # Advance phase
        if board.isPlayerActive(self) and len(board.getActivePlayers()) > 1:
            moveCards = board.getPlayersMoveCards(self)
            moveCardCount = len(moveCards)
            # Pick move card to use, if any
            moveCardToUse = self.pickMoveCardToUse(board) if moveCardCount > 0 else []
            if 0 == len(moveCardToUse):
                diceRoll = round(random.random()*6+0.5)
                self.sprint('Bot advance phase - rolled ' + str(diceRoll))
            else:
                diceRoll = moveCardToUse[0]
                board.discardMoveCard(self, moveCardToUse[0])
                self.sprint('Bot advance phase - used move card of value ' + str(moveCardToUse[0]))
            pos = board.getPlayersPosition(self)
            for i in range(1, diceRoll+1):
                if i == 1 and pos == 'SpyAlleyEntrance':
                    pos = 'Collect$20'
                else:
                    nextPos = board.nextSpace(pos)
                    if (len(nextPos) == 1):
                        pos = nextPos[0]
                    else:
                        pos = self.pickNextPosition(board,nextPos)
                        self.sprint('Decided to enter ' + pos)
                    if pos == 'Start':
                        board.passingStart(self)
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
                        if (self.isBuyPassword(board)):
                            if board.getPlayersMoney(self) > 0:
                                board.assignPassword(self, pos)
                        else:
                            self.sprint('Did not buy password')
                # Handle landing on move card space
                if pos[0:8] == 'MoveCard':
                    board.assignMoveCard(self)
                # Handle landing on resource space
                if 'Disguises' == pos or 'CodeBooks' == pos or 'Keys' == pos:
                    resType = pos[0:len(pos)-1]
                    if 0 == self.hasAllResourcesOfType(board,resType):
                        self.buyMultipleResources(board,resType)
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
                if pos[0:11] == 'BlackMarket':
                    self.buyResourcesOnBlackMarket(board)
                # Handle landing on spy eliminator space
                if 'SpyEliminator' == pos:
                    # challenge all active players in Spy Alley spaces
                    for p in board.getActivePlayers():
                        if p != self and board.isSpaceInSpyAlley(board.getPlayersPosition(p)):                            
                            n = self.pickNationalityToChallengePlayer(board,p)
                            self.sprint('')
                            self.sprint('!!! Challenging player ' + p.getName())
                            if (p.getPlayerType() == 'Human'):
                                input('Summon human player ' + p.getName() + ', press [Enter] when ready ...')
                                self.sprint('')
                                self.sprint('Guessing s/he is a ' + n)
                                input(p.getName() + ' - Please confirm by pressing [Enter] ...')
                                for i in range(1,100):
                                    self.sprint('')
                                self.sprint('')
                            if (n == p.getNationality()):
                                self.sprint('Challenge successful - player ' + p.getName() + ' is out!')
                                self.saveChallengeOfOthers(p,n,1)
                                board.deactivatePlayer(p)
                                board.transferResources(p,self)
                                # Switch nationality 50% of the time
                                if random.random() > 0.5:
                                    board.switchNationalities(p,self)
                            else:
                                self.saveChallengeOfOthers(p,n,0)
                                p.saveChallengeByOthers(self,n)
                                self.sprint('Challenge was not successful')
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
                    availableFunds = board.getPlayersMoney(self)
                    if board.hasAllResources(self):
                        # Check for wild cards
                        playersWithWildCards = []
                        for p in board.getActivePlayers():
                            if board.getPlayersWildCards(p) > 0:
                               playersWithWildCards.append(p)
                        if len(playersWithWildCards) > 0:
                            amountPerResource = board.getConfiscateMaterialsPrices('WildCard')
                            if availableFunds >= amountPerResource:
                                pick = self.pickPlayerToConfiscateWildCardFrom(board,playersWithWildCards)
                                if board.getPlayersWildCards(pick) > 0:
                                    board.confiscateWildCard(pick)
                                    board.updateFunds(self, -amountPerResource)
                                    board.assignWildCard(self,'no')
                                    self.sprint('Confiscated Wild Card from ' + pick.getName())
                    else:
                        self.handleConfiscateMaterials(board)
                # Handle landing on take another turn space
                if 'TakeAnotherTurn' == pos:
                    self.sprint('Taking another turn...')
                    self.move(board,'no')
                if printResources == 'yes':
                    self.printResources(board)
                    self.sprint('Finished move of ' + self.name)
    def handleChallengePhase(self,board):
        if (random.random() > 0.9):
            # Only challenge part of the time
            self.sprint('Challenge random player for random nationality ...')
            plist = board.getActivePlayers()
            foundPlayer = 0
            while (foundPlayer == 0):
                p = plist[round(random.random()*len(plist)-0.5)]
                if (p != self):
                    foundPlayer = 1
            nlist = list(board.getAllAvailableNationalities())
            nlist.remove(self.getNationality())
            n = nlist[round(random.random()*len(nlist)-0.5)]
            self.sprint('')
            self.sprint('!!! Challenging player ' + p.getName())
            if (p.getPlayerType() == 'Human'):
                input('Summon human player ' + p.getName() + ', press [Enter] when ready ...')
                self.sprint('')
                self.sprint('Guessing s/he is a ' + n)
                input(p.getName() + ' - Please confirm by pressing [Enter] ...')
                for i in range(1,100):
                    self.sprint('')
            self.sprint('')
            if (n == p.getNationality()):
                self.sprint('Challenge successful - player ' + p.getName() + ' is out!')
                self.saveChallengeOfOthers(p,n,1)
                board.deactivatePlayer(p)
                board.transferResources(p,self)
                # Switch nationality 50% of the time
                if random.random() > 0.5:
                    board.switchNationalities(p,self)
            else:
                self.sprint('Challenge was not successful, current player is out!')
                p.saveChallengeByOthers(self,n)
                board.deactivatePlayer(self)
                board.transferResources(self,p)
                if 'Human' == p.getPlayerType():
                    completedSwitch = 0
                    while 0 == completedSwitch:
                        switchAnswer = input('Question for ' + p.getName() + ' - do you want to switch nationalities with ' + self.getName() + ' and become ' + self.getNationality() + '? (y/n): ')
                        if 'y' == switchAnswer or 'Y' == switchAnswer:
                            self.sprint('Switched nationality to ' + self.getNationality())
                            board.switchNationalities(p, self)
                            input('Acknowledge switching to new nationality. Press [Enter]')
                            for i in range(1,100):
                                self.sprint('')
                            completedSwitch = 1
                        elif 'n' == switchAnswer or 'N' == switchAnswer:
                            for i in range(1,100):
                                self.sprint('')
                            completedSwitch = 1
                        else:
                            self.sprint('Unrecognized answer, please try again ...')
                else:
                    p.decideWhetherToSwitchNationality(board,self)
            return 1
        else:
            self.sprint('Did not challenge')
            return 0
    def pickMoveCardToUse(self,board):
        # Use move card 20% of the time at random, if available
        moveCards = board.getPlayersMoveCards(self)
        moveCardCount = len(moveCards)
        if random.random() > 0.8:
            pick = round(random.random() * moveCardCount - 0.5)
            return [ moveCards[pick] ]
        else:
            return []
    def pickNextPosition(self,board,nextPos):
        # Pick each path 50% of the time
        if (random.random() > 0.5):
            return nextPos[0]
        else:
            return nextPos[1]
    def isBuyPassword(self,board):
        # Buy password 90% of time, if funds are available
        return random.random() > 0.1
    def buyMultipleResources(self,board,resType):
        # Spend 50% of funds on resources
        availableFunds = board.getPlayersMoney(self)
        amountToSpend = round(availableFunds/2)
        amountPerResource = board.getAmountPerResourceType(resType)
        unfilledNationalities = []
        for nat in board.getAllAvailableNationalities():
            if 0 == board.getPlayersResources(self)[nat][resType]:
                unfilledNationalities.append(nat)
        while len(unfilledNationalities) > 0 and amountToSpend >= amountPerResource:
            pick = round(random.random() * len(unfilledNationalities) + 0.5) - 1
            pickedNationality = unfilledNationalities[pick]
            board.assignResource(self, pickedNationality, resType)
            unfilledNationalities.remove(pickedNationality)
            amountToSpend = amountToSpend - amountPerResource
    def buyResourcesOnBlackMarket(self,board):
        # Buy resource at random
        pRes = board.getPlayersResources(self)
        availableFunds = board.getPlayersMoney(self)
        notBoughtYet = []
        for resType in board.getPlayersResourceTypes():
            if availableFunds >= board.getAmountPerResourceType(resType):
                for nat in board.getAllAvailableNationalities():
                    if 0 == pRes[nat][resType]:
                        notBoughtYet.append([nat, resType])
        # Randomly select nat/resType combination
        if len(notBoughtYet) == 0:
            self.sprint('Already bought all')
        else:
            pick = round(random.random()*len(notBoughtYet)+0.5)-1
            pickNat = notBoughtYet[pick][0]
            pickResType = notBoughtYet[pick][1]
            board.assignResource(self, pickNat, pickResType)
            self.sprint('Bought ' + pickNat + ' ' + pickResType)
    def pickNationalityToChallengePlayer(self,board,player):
        nlist = list(board.getAllAvailableNationalities())
        nlist.remove(self.getNationality())
        return nlist[round(random.random()*len(nlist)+0.5)-1]
    def pickPlayerToConfiscateWildCardFrom(self,board,playersWithWildCards):
        return playersWithWildCards[round(random.random()*len(playersWithWildCards)+0.5)-1]
    def handleConfiscateMaterials(self,board):
        # Pick at random
        availableFunds = board.getPlayersMoney(self)
        activePlayers = board.getActivePlayers()
        resourceTypes = []
        for rt in board.getPlayersResourceTypes():
            resourceTypes.append(rt)
        resourceTypes.append('WildCard')
        nationalities = board.getAllAvailableNationalities()
        transferDone = 0
        cnt = 0
        while 0 == transferDone and cnt < 10:
            cnt += 1
            playerPick = round(random.random()*len(activePlayers)+0.5)-1
            p = activePlayers[playerPick]
            resourcePick = round(random.random()*len(resourceTypes)+0.5)-1
            resType = resourceTypes[resourcePick]
            amountPerResource = board.getConfiscateMaterialsPrices(resType)
            if availableFunds >= amountPerResource:
                if 'WildCard' == resType:
                    if board.getPlayersWildCards(p) > 0:
                        board.confiscateWildCard(p)
                        board.updateFunds(self, -amountPerResource)
                        board.assignWildCard(self,'no')
                        transferDone = 1
                        self.sprint('Confiscated Wild Card from ' + p.getName())
                else:
                    nationalityPick = round(random.random()*len(nationalities)+0.5)-1
                    nat = nationalities[nationalityPick]
                    if 0 == board.getPlayersResources(self)[nat][resType]:
                        if 1 == board.getPlayersResources(p)[nat][resType]:
                            board.confiscateMaterial(p, nat, resType)
                            board.updateFunds(self, -amountPerResource)
                            board.assignResource(self, nat, resType, 'no')
                            transferDone = 1
                            self.sprint('Confiscated ' + nat + ' ' + resType + ' from ' + p.getName())
            else:
                transferDone = 1
    def decideWhetherToSwitchNationality(self,board,otherPlayer):
        # Switch nationalities 50% of the time
        if random.random() > 0.5:
            board.switchNationalities(self, otherPlayer)

import random
import time

ranks = '23456789TJQKA'
hexVals  = '23456789abcde'

class player:
    def __init__(self,pos):
        self.holes = [52,52]
        self.commCards = [52,52,52]
        self.stack = 0
        self.bet = 0
        self.pos = pos
        self.active = False
        self.seated = False
        self.name = 'Unknown ' + str(pos)

class pot:
    def __init__(self,amt = 0, plyrs = []):
        self.amount = amt
        self.players = plyrs
        

class table:
    def __init__(self,size):
        self.players = []
        for i in range(size):
            self.players.append(player(i))   

class game:
    def __init__(self,size,bb,sb,startStack = 0):
        gameNum = 0
        self.tb = table(size)
        self.bb = bb
        self.sb = sb
        self.deck = []
        self.deckPos = 0
        for i in range(52):
            self.deck.append(i)
        self.pots = []
        self.topBet = 0
        self.board = [52,52,52,52,52]
        self.button = [0]
        self.startStack = startStack
        
    def addPlayer(self,pos,startStack,active=True, name = ''):
        self.tb.players[pos].stack = startStack
        self.tb.players[pos].active = active
        self.tb.players[pos].seated = True
        if name:
            self.tb.players[pos].name = name

    def removePlayer(self,pos):
        self.tb.players[pos].stack = 0
        self.tb.players[pos].active = False
        self.tb.players[pos].seated = False
        self.tb.players[pos].holes = [52,52]
        self.tb.players[pos].bet = 0
        
        
    def awardPot(self,pos,amount):
        self.tb.players[pos].stack +=amount
        
    def placeBet(self,pos,betSize):
        self.tb.players[pos].bet += betSize
        self.tb.players[pos].stack -= betSize
        
    def reportEmpty(self):
        emptySeats = []
        for plyr in self.tb.players:
            if not plyr.seated:
                emptySeats.append(plyr.pos)
        return emptySeats
    
    def reportPlayers(self):
        print ('Seat ' + str(self.button) + ' is the dealer')
        for plyr in self.tb.players:
            print ('Seat ' + str(plyr.pos))
            print ('Name ' + plyr.name)
            print ('Hole Cards: ' + self.idCard(plyr.holes[0]) + ' ' + self.idCard(plyr.holes[1]))
            print ('Seated: ' + str(plyr.seated) + ', Active: ' + str(plyr.active) + ', Stack: ' + str(plyr.stack) + ', Bet: ' + str(plyr.bet) + '\n')
            
    def getActive(self):
        activeList = []
        for plyr in self.tb.players:
            if  plyr.active:
                activeList.append(plyr.pos)
        return activeList

    def getSeated(self):
        seatedList = []
        for plyr in self.tb.players:
            if  plyr.seated:
                seatedList.append(plyr.pos)
        return seatedList    
    
    def initButton(self):
        self.shuffle()
        dealer = (0,0)
        for i,pos in enumerate(self.getActive()):
            if self.deck[i]%13 >= dealer[1]:
                dealer = (pos,self.deck[i]%13)
        self.button = dealer[0]
    
    def shuffle(self,numSuffs = 5, getseed = False):
        if getseed:
            random.seed(self.getSeed())
        for i in range(numSuffs):
            random.shuffle(self.deck)
            
    def getSeed(self,base = 10):
        seeds = ''
        for i in range(base):
            time.sleep(random.random())
            input(str(i) + ' of ' + str(base) + ': Press Return') 
            seeds+=str(time.time()).partition('.')[2]
        return seeds

    def findSuit(self,card):
        if card < 13: 
            return 'c' 

            return 'd' 
        elif card < 39: 
            return 'h' 
        else: 
            return 's'

    def idCard(self,card):
        if card == 52:
            return 'XX'
        else:
            return ranks[card%13]+self.findSuit(card)

    def deal(self):
        self.shuffle()
        self.deckPos = 0
        for i in range(2):
            for plyr in self.tb.players:
                if plyr.active:
                    plyr.holes[i] = self.deck[self.deckPos]
                    self.deckPos +=1 
                
            
    
    def findTopHand(self,holes):
        topHand = []
        typeCode = 0
        cards = []
        value = '0x'
        for card in holes + self.board:
            if card != 52:
                cards.append(card)
        cards.sort(reverse=True,key = lambda x:x%13)
        print('Cards: ' + str(cards))        
        if len(cards) < 5:
            print ('Not enough hole and community cards to make a hand.')
            return
        
        else:

            # Check pairs, sets, boats, 4 of a kind
            pairs = {}
            for card in cards:
                if card % 13 not in pairs:
                    pairs[card % 13] = [card]
                else:
                    pairs[card % 13].append(card)
            for pair in pairs:
                if len(pairs[pair]) == 4:
                    print('four of a kind ' + ranks[pairs[pair][0]%13])
                elif len(pairs[pair]) == 3:
                    print('three of a kind ' + ranks[pairs[pair][0]%13])
                elif len(pairs[pair]) == 2:
                    print('pair of ' + ranks[pairs[pair][0]%13])
                else:
                    print('possible kicker ' + ranks[pairs[pair][0]%13])

            # Check flush
            suits = {'c':0,'d':0,'h':0,'s':0}
            for card in cards:
                suits[self.findSuit(card)] +=1
            for suit in suits:
                if suits[suit] > 4:
                    flush = []
                    for card in cards:
                        if self.findSuit(card) == suit:
                            flush.append(card)
                    flush.sort(reverse=True,key = lambda x:x%13)
                    topHand = flush[:5]
                    value += 5
                    for card in topHand:
                        value += card % 13
                    
            # Find Straight TODO: Correct to use low ace
            straight = False
            for i in range(len(cards)-4):
                print('i: ' +str(i))
                chk = True
                hand = [cards[i]]
                for c in range(1+i,5+i):
                    print(c)
                    hand.append(cards[c])
                    if cards[c] % 13 != (cards[c-1] % 13) - 1:
                        chk = False
                        print('Nope')
                if chk:
                    straight = True
                    strHand = hand
                    print(hand)
            print(straight)
            # Check Straight Flush
            if straight:
                print('checking flush')
                flush = True
                suit = self.findSuit(strHand[0])
                for card in strHand:
                    if self.findSuit(card) != suit:
                        flush = False
                print(straightFlush)

            # Check pairs, sets, boats, 4 of a kind
            pairs = {}
            for card in cards:
                if card % 13 not in pairs:
                    pairs[card % 13] = [card]
                else:
                    pairs[card % 13].append(card)
            for pair in pairs:
                if len(pairs[pair]) == 4:
                    print('four of a kind ' + ranks[pairs[pair][0]%13])
                elif len(pairs[pair]) == 3:
                    print('three of a kind ' + ranks[pairs[pair][0]%13])
                elif len(pairs[pair]) == 2:
                    print('pair of ' + ranks[pairs[pair][0]%13])
                else:
                    print('possible kicker ' + ranks[pairs[pair][0]%13])



def initGame(size,bb, sb, startStack = 0):
    print ('Initializing game')
    print ('Creating players')
    gm = game(size,bb,sb)
    if startStack > 0:
        for i in range(size):
            gm.addPlayer(i,startStack)
    else:
        number = str(input('How many players to add? '))
        for i in range(int(number)):
            try:
                pos = random.choice(gm.reportEmpty())
                gm.addPlayer(random.choice(gm.reportEmpty()),input('Starting stack for player ' + str(i) + '? '))
            except IndexError:
                print('No more empty seats')
                break
    print('Setting button')
    gm.initButton()
    print ('Button is on seat ' + str(gm.button))
    return gm
                             
            

def playHand(gm):
    while(True):
        print('Hand Actions')
        print('--------------------------------------')
        print('L: List Players')
        print('S: Seat Player')
        print('R: Remove Player')
        print('A: Activate Player')
        print('D: Deactivate Player')
        print('S: Change Stack')
        print('B: Change Blinds')
        print('P: Play Hand')
        print('--------------------------------------')
        s = input('Enter Selection: ')
        if s.upper() not in ['L','A','R','S','B','P']:
            print('Bad selection. Try again')
            continue
        else:
            if s.upper() == 'L':
                gm.reportPlayers()
                continue
            elif s.upper() == 'S':
                try:
                    pos = random.choice(gm.reportEmpty())
                    gm.addPlayer(random.choice(gm.reportEmpty()),input('Starting stack for player? '))
                    continue
                except IndexError:
                    print('No more empty seats')
                    continue
            elif s.upper() == 'R':
                pos = input('Seat to remove? ' )
                if int(pos) not in gm.getSeated():
                    print('That seat is already empty')
                    continue
                else:
                    gm.removePlayer(int(pos))
            elif s.upper() == 'A':
                if len(gm.getActive()) < 3:
                    pass
            elif s.upper == 'P':
                pass

        
    

#!/usr/bin/python2.7

from textwrap import wrap
from time import time, sleep
import start
import save
import sys
try:
    # taken from http://stackoverflow.com/questions/3471461/raw-input-and-timeout/3911560#3911560
    import msvcrt
    def timeInput(timeout):
        start_time = time()
        sys.stdout.write('> ')
        input = ''
        while True:
            if msvcrt.kbhit():
                chr = msvcrt.getche()
                if ord(chr) == 13:
                    break
                elif ord(chr) >= 32:
                    input += chr
            if len(input) == 0 and (time() - start_time) > timeout:
                print 
                return False,(timeout+start_time-time())
        return input,(timeout+start_time-time())
except:
    # taken from http://stackoverflow.com/questions/3471461/raw-input-and-timeout
    from select import select
    def timeInput(timeout):
        start_time=time()
        sys.stdout.write('> ')
        sys.stdout.flush()
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            s = sys.stdin.readline()
            return s[:-1],(timeout+start_time-time())
        elif (time() - start_time) <= timeout:
            return '',(timeout+start_time-time())
        else:
            return False,(timeout+start_time-time())

def view(arg):
    '''displays arg within width of 70'''
    if game.timeLeft < 0:
        print ' '
        if type(arg) is str:
            arg=[arg]
        for x in arg:
            for y in wrap(x):
                print y
        print ' '
    elif game.timeLeft>0:
        print ' '
        if type(arg) is str:
            arg=[arg]
        for x in arg:
            for y in wrap(x):
                print y
        print '\nYou have %d seconds left\n'%game.timeLeft
    elif not game.dead:
        deadMsg()

class data:
    def __init__(self):
        self.new()
    def new(self):
        self.options=list(start.options)
        self.notes=list(start.notes)
        self.items=list(start.items)
        self.bkpk=list(start.bkpk)
        self.rmCount=list(start.rmCount)
        self.rmName=list(start.rmName)
        self.rmAct=list(start.rmAct)
        self.rmMsg=list(start.rmMsg)
        self.vaultCode=list(start.vaultCode)
        self.otherCode=list(start.otherCode)
        self.finalCode=start.finalCode
        self.birYear=start.birYear
        self.deathYear=start.deathYear
        self.curRoom=start.curRoom
        self.valid=[]
        self.timeLeft=-1
        self.placedBomb = False
        self.timeoutMsg = 'You died'

end=False
game=data()

def new():
    game.new()
    view('* New Game *')

def resetTimer():
    game.timeLeft = -1

resetTimer()

def inp():
    try:
        if game.timeLeft >= 0:
            t=time()
            ipt,game.timeLeft=timeInput(game.timeLeft)
            game.timeLeft+=t-time()
            if ipt != False:
                ipt = ipt.lower()
                if ipt=='save':
                    view('No saving while on timer')
                    return True
                elif ipt=='eval':
                    ipt=raw_input('What would you like to evaluate?\n> ')
                    try: print eval(ipt)
                    except: print "Didn't work"
                    return True
                elif ipt=='quit':
                    1/0
                elif ipt=='load':
                    loadGame()
                    return True
                elif ipt=='new':
                    new()
                    return True
                elif ipt=='inventory':
                    # inventory items are returned as lists
                    if len(game.bkpk)>2:
                        game.bkpk[0]='These are the items in your inventory'
                    else: game.bkpk[0]='Your have nothing in your inventory'
                    view(game.bkpk+['Select item:'])
                    ipt,game.timeLeft=timeInput(game.timeLeft)
                    while check(game.bkpk,ipt)==False:
                        view('Try again')
                        ipt,game.timeLeft=timeInput(game.timeLeft)
                    valInp([check(game.bkpk,ipt)])
                    return True
                elif ipt=='notes':
                    view('Start writing your note')
                    notes(raw_input('> '))
                    return True
                elif ipt=='rnotes':
                    notes()
                    return True
                else:
                    valInp(ipt)
                    return True
            else:
                view('')
        else:
            ipt=raw_input("> ").lower()
            if ipt=='menu':
                return False
            elif ipt=='eval':
                ipt=raw_input('What would you like to evaluate?\n> ')
                try: print eval(ipt)
                except: print "Didn't work"
                return True
            elif ipt=='quit':
                1/0
            elif ipt=='save':
                saveGame()
                return True
            elif ipt=='load':
                loadGame()
                return True
            elif ipt=='new':
                new()
                return True
            elif ipt=='inventory':
                #inventory items are returned as a list
                if len(game.bkpk)>2:
                    game.bkpk[0]='These are the items in your inventory'
                else: game.bkpk[0]='Your have nothing in your inventory'
                view(game.bkpk)
                view('Select item:')
                ipt=raw_input('> ')
                while check(game.bkpk,ipt)==False:
                    view('Try again')
                    ipt=raw_input('> ')
                valInp([check(game.bkpk,ipt)])
                return True
            elif ipt=='notes':
                view('Start writing your note')
                notes(raw_input('> '))
                return True
            elif ipt=='rnotes':
                notes()
                return True
            else:
                valInp(ipt)
                return True
            return False
    except KeyboardInterrupt:
        global end
        end=True
        return False
    except ZeroDivisionError:
        global end
        end=True
        return False
def deadMsg():
    game.dead=True
    game.timeLeft=-1
    if game.curRoom==game.rmName.index('freezer'):
        if check(game.rmAct[game.rmName.index('orchard')],'.bomb'): #check if player picked up bomb
            if check(game.bkpk,'MONKEY'): #secret stuck finale
                view(game.rmMsg[game.rmName.index('finale')][3])
            else: #stuck finale
                view(game.rmMsg[game.rmName.index('finale')][1])
        elif game.placedBomb:
            if check(game.bkpk,'MONKEY'):
                view(game.rmMsg[game.rmName.index('finale')][2])
            else:
                view(game.rmMsg[game.rmName.index('finale')][0])
        else:
            view('You froze to death')
    elif check(game.bkpk,'BOMB'):
        view('You died with the bomb in your pocket, idiot. Sorry.')
    else:
        view('You died')
    sleep(30)
    new()
def valInp(ipt):
    if check(game.valid,ipt):
        if type(ipt)==list:
            if ipt[0].lower()=='gun':
                if game.rmName[game.curRoom]=='library':
                    game.options[game.curRoom].append('inlibrary')
                    game.bkpk.remove('GUN')
                    view('You shoot the padlock.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    leave('inlibrary')
                else: view('The shotgun has one bullet.')
            elif ipt[0].lower()=='leg':
                if game.rmName[game.curRoom]=='lounge':
                    game.options[game.curRoom].append('inlounge')
                    game.bkpk.remove('LEG')
                    view('You wedged the door open.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    leave('inlounge')
                    game.timeLeft=300
                else: view('You are carrying a table leg.')
            elif ipt[0].lower()=='ladder':
                if game.rmName[game.curRoom]=='up':
                    game.bkpk.remove('LADDER')
                    view('You used the ladder to reach the pannel.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    game.rmAct[game.curRoom]='code'
                else: view('You are awkwardly carrying a ladder around with you.')
            elif ipt[0].lower()=='screwdriver':
                if game.rmName[game.curRoom]=='vent':
                    game.bkpk.remove('SCREWDRIVER')
                    view('You used the screwdriver to open the vent.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    game.bkpk.insert(-1, 'CARD')
                else: view('You are holding a screwdriver.')
            elif ipt[0].lower()=='card':
                if game.rmName[game.curRoom]=='freezer':
                    if game.timeLeft:
                        leave('infreezer')
                        resetTimer()
                    else:
                        view('You used the card to open the door.')
                        game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                        leave('infreezer')
                elif game.rmName[game.curRoom]=='door':
                    view('You used the card to open the door.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    leave('end')
                    resetTimer()
                elif game.rmName[game.curRoom]=='lab':
                    view('The card doesnt work on this door.')
                elif game.rmName[game.curRoom]=='ordoor':
                    view('The card doesnt work. You must have to enter the password.')
                elif game.rmName[game.curRoom]=='orchard':
                    view('You used the card to open the door.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    leave('inorchard')
                    if game.rmCount[game.curRoom]==0:
                        game.timeLeft=180
                    else:
                        game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                else: view('You are holding a key card')
            elif ipt[0].lower()=='monkey':
                if game.rmName[game.curRoom]=='lab':
                    view('The monkey found something.')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                else: view('Mr. Moodles throws feces at the wall.')
            elif ipt[0].lower()=='paper':
                view('The paper has the final two digits of the code: %d, %d. On the back it says "In loving memory of John Stranger, %d-%d"'%(game.otherCode[2],game.otherCode[3],game.birYear,game.deathYear))
            elif ipt[0].lower()=='bomb':
                print 'HERE AT THE BOMB'
                if game.rmName[game.curRoom]=='exit':
                    print 'HERE AT THE EXIT'
                    game.bkpk.remove('BOMB')
                    game.placedBomb = True
                    game.rmMsg[game.curRoom][1]='You put the bomb next to the collapsed tunnel. Find somewhere safe.'
                else:
                    view('The bomb will go off in %d seconds'%int(game.timeLeft))
            elif ipt[0].lower()=='exit': pass
        elif check(game.items,ipt):
            game.bkpk.insert(1,ipt.upper())
            game.rmAct[game.curRoom]='done'
            view('%s has been added to your inventory'%ipt.title())
            if game.rmName[game.curRoom]=='inorchard':
                game.rmMsg[game.curRoom][0]='You have picked up the bomb, now you need to find a place to put it.'
            else:
                game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
            if ipt=='monkey':
                game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][2]
        elif ipt=='leave':
            leave(game.options[game.curRoom][0][5:])
        elif ipt=='code':
            valCode()
        else:
            leave(ipt)
    else:
        view('Invalid Input, try NOTES, RNOTES, SAVE, QUIT, LOAD, NEW')

#checks input for validity and performs action
def codeInp(code):
    if game.timeLeft >= 0:
        t=time()
        ipt,game.timeLeft=timeInput(game.timeLeft)
        while ipt!=str(code):
            if not ipt or game.timeLeft<=5:
                return False
            elif ipt=='leave':
                return False
            elif ipt=='rnotes':
                notes()
                msg=['Input code']
            else:
                game.timeLeft-=5
                msg=['5 second penalty']
                msg.append('Try again')
            view(msg)
            ipt,game.timeLeft=timeInput(game.timeLeft)
        return True
    else:
        ipt=raw_input('> ')
        while ipt!=str(code):
            if ipt=='leave':
                return False
            elif ipt=='rnotes':
                notes()
                msg='Input code'
            else:
                msg='Try again'
            view(msg)
            ipt=raw_input('> ')
        return True

def valCode():
    curRoom=game.curRoom
    ansVault=game.vaultCode
    ansSafe='strangers'
    ansPicture='turkey'
    ansFix=['up','right','left']
    ansCode=['garden',game.finalCode,game.deathYear-game.birYear]
    if game.rmName[game.curRoom]=='safe':
        view('Enter the 9 letter word, LEAVE, or RNOTES')
        if codeInp(ansSafe):
            view('You opened the safe.')
            game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
            game.rmAct[curRoom]='done'
        else:
            return leave('safe')
    elif game.rmName[game.curRoom]=='vault':
        view('Enter the first vault code, LEAVE, or RNOTES')
        if codeInp(ansVault[0]):
            view('You entered the first code correctly. Please enter the second code')
            if codeInp(ansVault[1]):
                view('You entered the second code correctly. Please enter the third code')
                if codeInp(ansVault[2]):
                    view('You entered the third code correctly. To your surprise, the vault only required three numbers')
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
                    game.options[game.curRoom].append('invault')
                    leave('invault')
                    game.rmAct[curRoom]='done'
                else:
                    return leave('vault')
            else:
                return leave('vault')
        else:
            return leave('vault')
    elif game.rmName[game.curRoom]=='picture':
        view('Enter the 6 letter word, LEAVE, or RNOTES')
        if codeInp(ansPicture):
            view('You opened the safe.')
            game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
            game.options[game.rmName.index('end')].append('up')
            game.rmAct[curRoom]='done'
        else:
            return leave('picture')
    elif game.rmName[game.curRoom]=='up':
        view('Enter the 3 digit number, LEAVE, or RNOTES')
        if codeInp(ansVault[3]):
            view('You opened the freezer.')
            game.options[game.rmName.index('end')].remove('up')
            leave('infreezer')
            game.timeLeft=210
            game.rmAct[curRoom]='done'
        else:
            return leave('up')
    elif game.rmName[game.curRoom]=='fix':
        view('%s, UP, RIGHT, LEFT, DOWN, LEAVE, or RNOTES'%game.rmMsg[game.curRoom][1])
        if codeInp(ansFix[0]):
            view(game.rmMsg[game.curRoom][2])
            if codeInp(ansFix[1]):
                view(game.rmMsg[game.curRoom][3])
                if codeInp(ansFix[2]):
                    leave('middle')
                    view('Door opens and you walk out')
                    game.options[game.rmName.index('inlounge')].insert(0,'leavemiddle')
                    resetTimer()
                    game.rmAct[curRoom]='done'
                else:
                    return leave('picture')
            else:
                return leave('picture')
        else:
            return leave('picture')
    elif game.rmName[game.curRoom]=='console':
        view(game.rmMsg[game.curRoom][0])
        if codeInp(ansCode[0]):
            view(game.rmMsg[game.curRoom][1])
            if codeInp(ansCode[1]):
                view(game.rmMsg[game.curRoom][2])
                if codeInp(ansCode[2]):
                    view('%s %d seconds'%(game.rmMsg[game.curRoom][3],game.timeLeft))
                    leave('inorchard')
                    game.rmMsg[game.curRoom][0]='You have entered the code and the bomb is ticking on the ground.'
                    game.rmAct[game.curRoom]='.bomb'
                    game.options[game.curRoom].insert(0,'leaveend')
                    game.options[game.curRoom].remove('ordoor')
                    game.options[game.curRoom].remove('console')
                else:
                    return leave('inorchard')
            else:
                return leave('inorchard')
        else:
            return leave('inorchard')
def notes(*args):
    '''no args views notes, arg is input to add to notes'''
    try:
        for x in wrap(args[0]):
            game.notes.append(x)
        game.notes[0]='Your notes are:'
    except IndexError: pass
    view(game.notes)
def loadGame():
    reload(save)
    '''loads save vars'''
    game.options=list(save.options)
    game.notes=list(save.notes)
    game.bkpk=list(save.bkpk)
    game.rmCount=list(save.rmCount)
    game.rmAct=list(save.rmAct)
    game.rmMsg=list(save.rmMsg)
    game.vaultCode=list(save.vaultCode)
    game.otherCode=list(save.otherCode)
    game.finalCode=save.finalCode
    game.birYear=save.birYear
    game.deathYear=save.deathYear
    game.curRoom=save.curRoom
    view('* Game Loaded *')
def check(arr,s):
    '''searches arr for s, returns s or False if not found'''
    a=[]
    try:
        try:
            for x in arr:
                a.append(x.lower())
            return a[a.index(s.lower())]
        except AttributeError:
            for x in arr:
                a.append(x)
            return a[a.index(s)]
    except ValueError:
        return False
def leave(st):
    '''leaves the room to st and makes a note of it'''
    game.rmCount[game.curRoom]+=1
    game.curRoom=game.rmName.index(st)
def options():
    '''displays message and options for the current room'''
    name=game.rmName[game.curRoom]
    if name == 'freezer':
        if game.placedBomb:
            deadMsg()
    game.valid=[]
    msg=[game.rmMsg[game.curRoom][0],'Your options are:']
    # valid room options and msg to display
    for x in game.options[game.curRoom][1:]:
        if x!='':
            msg.append('Go to '+x.upper())
            game.valid.append(x)
    if game.options[game.curRoom][0].startswith('leave'):
        msg.append('LEAVE '+game.rmName[game.curRoom])
        game.valid.append('leave')
    else:
        msg.insert(2,'Go to '+start.options[game.curRoom][0].upper())
        game.valid.append(start.options[game.curRoom][0])
    # add options, leave option is not applicable to corridors
    msg.append('View INVENTORY')
    if game.rmAct[game.curRoom]=='code':
        msg.append('Enter CODE')
        game.valid.append('code')
    elif game.rmAct[game.curRoom]=='done': None
    elif game.rmAct[game.curRoom][0]=='.':
        game.valid.append(game.rmAct[game.curRoom][1:])
        msg.append('Pick up '+game.rmAct[game.curRoom][1:].upper())
    else:
        try:
            viewRoom=int(game.rmAct[game.curRoom])
            if game.rmCount[game.curRoom]>=viewRoom:
                msg[0]=game.rmMsg[game.curRoom][1]
                if game.rmName[game.curRoom]=='hole':
                    game.rmAct[game.curRoom]='.monkey'
                    game.valid.append(game.rmAct[game.curRoom][1:])
                    msg.append('Pick up '+game.rmAct[game.curRoom][1:].upper())
                    game.rmMsg[game.curRoom][0]=game.rmMsg[game.curRoom][1]
        except ValueError:pass
    # add action, changes message
    for x in game.items:
        game.valid.append([x.lower()])
    view(msg)

def saveGame():
    '''saves current vars to file and save vars'''
    save.options=list(game.options)
    save.notes=list(game.notes)
    save.bkpk=list(game.bkpk)
    save.rmCount=list(game.rmCount)
    save.rmAct=list(game.rmAct)
    save.rmMsg=list(game.rmMsg)
    save.vaultCode=list(game.vaultCode)
    save.otherCode=list(game.otherCode)
    save.finalCode=game.finalCode
    save.birYear=game.birYear
    save.deathYear=game.deathYear
    save.curRoom=game.curRoom
    info='''options=%r
notes=%r
bkpk=%r
rmCount=%r
rmAct=%r
rmMsg=%r
vaultCode=%r
otherCode=%r
finalCode=%r
birYear=%r
deathYear=%r
curRoom=%r''' % (game.options,game.notes,game.bkpk,game.rmCount,
         game.rmAct,game.rmMsg,game.vaultCode,game.otherCode,
         game.finalCode,game.birYear,game.deathYear,game.curRoom)
    open('save.py','w+').write(info)
    view('* Game Saved *')

def menu():
    print """\33c
_________            _______
    |      |      |  |
    |      |      |  |
    |      |------|  |-----
    |      |      |  |
    |      |      |  |______
_______    ____      ____            _____    _______
|         /    \    /    \     /\    |    \   |
|         |        /          /  \   |    |   |
|-----    \----\   |         /____\  |____/   |-----
|              |   \         |    |  |        |
|______   \____/    \____/   |    |  |        |______"""
    if check(game.bkpk,'MONKEY')!=False:
        print 'With Mr. Moodles'
    view(['Your current options are:','NEW, LOAD, QUIT, MENU, SAVE, NOTES, RNOTES'])


def play():
    while not end:
        game.dead=False
        game.valid=[]
        menu()
        while not game.dead and inp():
            options()

play()

quit()


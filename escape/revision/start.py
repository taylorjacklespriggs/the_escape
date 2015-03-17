from random import randint

options='''gallery,library,middle
leaveexit
exit,vault,lounge,end
leavemiddle
leavemiddle
middle,freezer,orchard,lab
leaveend
leaveend
leaveend
leaveexit,wall,fireplace
leavegallery
leavegallery,safe
leavefireplace
leaveexit,book,walk,hole
leaveinlibrary
leaveinlibrary
leaveinlibrary
leavemiddle,picture,table
leaveinvault
leaveinvault
body,panel
leaveinlounge,look
leaveinlounge
leaveinlounge,schematic,fix
leavepanel
leavepanel
leaveend
search,door
leaveinfreezer
leaveinfreezer,explore,inspect,vent
leavesearch
leaveinfreezer
leavesearch
console,ordoor
leaveinorchard
leaveinorchard
'''.split('\n')
for x in range(len(options)):
    options[x]=options[x].split(',')
story=filter(len, open('gamestory.txt').read().split('\n'))
items='gun.monkey.ladder.leg.paper.screwdriver.card.bomb'.upper().split('.')
rmName=[]
rmAct=[]
rmMsg=[]
for x in range(len(story)):
    rmName.append(story[x].split('*')[0])
    rmAct.append(story[x].split('*')[1])
    rmMsg.append(story[x].split('*')[2:len(story[x].split('*'))])
notes=['You have no notes']
bkpk=['Your have nothing in your inventory','EXIT']
rmCount=[0 for x in range(len(story))]
vaultCode=[randint(10,99) for x in range(3)]
vaultCode.append(randint(100,999))
otherCode=[randint(10,99) for x in range(4)]
finalCode=str(reduce(lambda x,y:x*y,otherCode))[-3:]
birYear=randint(1880,1900)
deathYear=randint(1925,1950)
curRoom=0
rmMsg[12][1]+='The vault code is %d-%d-%d-%d'%(vaultCode[0],vaultCode[1],vaultCode[2],vaultCode[3])
rmMsg[14][0]+='%d, %d'%(otherCode[0],otherCode[1])
rmMsg[14][1]+='%d, %d'%(otherCode[0],otherCode[1])

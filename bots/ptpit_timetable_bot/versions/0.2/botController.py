# ptpit-timetable vk group bot controller v.0.2
import subprocess
import time
import os
from datetime import timedelta 
from datetime import datetime
restarttry=0
# # # # #
dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
logFile=open("botLog.log", "a")
logFile.write("\n["+dateNow+"] [BC] botController was started")
logFile.close()
dateLastRes=datetime.now()+timedelta(hours=5)
# check files
checkEnvFile=os.path.isfile('.env')
checkChatIDsFile=os.path.isfile('chatIDs.py')
checkAdminIDsFile=os.path.isfile('adminIDs.py')
checkGroupIDFile=os.path.isfile('groupID.py')

if checkChatIDsFile == False:
    # log
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] start without groupID file, creating")
    logFile.close()
    # input groupID
    groupID=input("[BC] Input your group ID (only numbers): ")
    # create groupID
    logFile=open("groupID.py", "a")
    logFile.write("owner_id=-"+groupID)
    logFile.close()
    print("[BC] You can change group ID in groupID.py file\n")

if checkChatIDsFile == False:
    # log
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] start without chatIDs file, creating")
    logFile.close()
    # create chatIDs
    logFile=open("chatIDs.py", "a")
    logFile.write("chatIDs={ \n}")
    logFile.close()
    
if checkAdminIDsFile == False:
    # log
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] start without adminIDs file, creating")
    logFile.close()
     # input adminID
    adminID=input("[BC] Input your account ID: ")
    # create adminIDs
    logFile=open("adminIDs.py", "a")
    logFile.write("admins=[ \n'472153219', \n'"+adminID+"', \n]")
    logFile.close()
    print("[BC] You can change admims ID in adminIDs.py file\n")
    
if checkEnvFile == False:
    # log
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] start without .env file, creating")
    logFile.close()
    # input token
    token=input("[BC] Input your token: ")
    # create .env
    logFile=open(".env", "a")
    logFile.write("TOKEN=\""+token+"\"")
    logFile.close()
    print("[BC] You can change token in .env file\n")
    
# start bot
while 1>0:
    if restarttry > 100:
        break
    os.system("python3 bot.py")
    print("[BC] bot was closed")
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] bot was closed")
    logFile.close()
    #dateNow=datetime.now()+timedelta(hours=5)
    #if dateLastRes-dateNow < 5min:
    #    print('wait '+str(5+restarttry*3))
    #    time.sleep(5+restarttry*3)
    #print(str(dateLastRes-dateNow))
    #dateLastRes=datetime.now()+timedelta(hours=5)
    time.sleep(restarttry)
    restarttry+=1
    dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
    logFile=open("botLog.log", "a")
    logFile.write("\n["+dateNow+"] [BC] trying restart bot "+str(restarttry))
    logFile.close()
    print("[BC] trying restart bot")
    
# # # # #
dateNow=str((datetime.now()+timedelta(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
logFile=open("botLog.log", "a")
logFile.write("\n["+dateNow+"] [BC] botController was closed")
logFile.close()
# ptpit-timetable vk group bot v.0.2
import os
import requests
import vk_api
import subprocess
import time
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from chatIDs import chatIDs
from adminIDs import admins
from groupID import owner_id
load_dotenv(".env")

vk_session = vk_api.VkApi(token=os.environ.get("TOKEN"))
api = vk_session.get_api()
longpoll_owner_id = int(str(owner_id)[1:])
longpoll = VkBotLongPoll(vk_session, longpoll_owner_id)


def worker(event):
    message = event.obj['message']
    pattern =  message['text'].lower()
    if message['from_id'] == owner_id: return
    if not pattern: return
    
    # расписание звонков для пар 
    times = {
        1: "1&#8419; 08:30-10:05",
        2: "2&#8419; 10:25-12:00",
        3: "3&#8419; 12:20-14:10",
        4: "4&#8419; 14:15-15:50",
        5: "5&#8419; 16:10-17:55",
        6: "6&#8419; 18:00-19:35",
        }
    # дни недели 
    weekDays={
        0:'понедельник',
        1:'вторник',
        2:'среду',
        3:'четверг',
        4:'пятницу',
        5:'субботу',
        6:'воскресенье',
    }
    # установка переменных
    fromid = str(message['from_id'])
    peerid = str(message['peer_id'])
    randomid=get_random_id()
    
    # установка группы
    if pattern.startswith("бот группа "):
        gr0up=pattern[11:]
        #логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошена установка группы "+gr0up+" для чата "+peerid)
        logFile.close()
        #поиск
        groups = requests.get("https://api.ptpit.ru/groups")
        groups = groups.json()
        groups_format = {}
        for group in groups:
            id = group.get("id")
            name = group.get("name").lower()
            groups_format.update({name: id})
        text = "&#10006; Группа "+gr0up+" не найдена.\nОбратите внимание что скобки писать не надо. Пример: 18сзи1п"
        if not gr0up in groups_format:
            gr0up=gr0up+"п"
            if not gr0up in groups_format:
                return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=text)
        ###
        IDsFile=open("chatIDs.py", "r+")
        IDs=IDsFile.read()[:-1]
        IDs=IDs+peerid+":\""+gr0up+"\",\n}"
        IDsFile.close()
        IDsFile=open("chatIDs.py", "w")
        IDsFile.write(IDs)
        IDsFile.close()
        #from chatIDs import chatIDs
        text="&#9745; Установлена группа "+gr0up
        if fromid in admins:
            text+=" для чата "+peerid
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] установлена группа "+gr0up+" для "+peerid)
        logFile.close()
        # вывод
        api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=text)
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] выход после добавления группы")
        logFile.close()
        os._exit(0)
        
    # выбор группы
    gr0up=int(message['peer_id'])
    if gr0up in chatIDs:
        gr0up=str(chatIDs[gr0up])
    else:
        if "бот" in pattern:
            text="Ваш ID не найден в боте. Установите группу:\nБот группа <имя группы>"
            return api.messages.send(peer_id=message['peer_id'],random_id=0,message=text)
        else:
            return
    
    # корректировка времени под UTC+5
    datenow=datetime.now()+td(hours=5)
    
    
# # # # # # # # # #
    if pattern.startswith("добавить админа "):
        admID=pattern[16:]
        # проверка на админа
        if not fromid in admins:
            return api.messages.send(peer_id=message['peer_id'], random_id=0, message='&#10006; Только для админов')
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] добавление "+admID+" в админы "+fromid)
        logFile.close()
        # запись
        IDsFile=open("adminIDs.py", "r+")
        IDs=IDsFile.read()[:-1]
        IDs=IDs+"\'"+admID+"\',\n]"
        IDsFile.close()
        IDsFile=open("adminIDs.py", "w")
        IDsFile.write(IDs)
        IDsFile.close()
        return api.messages.send(peer_id=message['peer_id'], random_id=0, message="&#9745; "+admID+" добавлен в админы")
        

# # # # #

    
    if "помощь" in pattern and "бот" in pattern:
        text='[ Доступные команды: ]\n• Расписание/пары сегодня/завтра\n• Пара/пары сейчас/следующие\n• Расписание на <дд.мм.гг>\n\n• Бот помощь\n• Бот статус\n• Бот группа <группа>\n'
        if fromid in admins:
            text+='• Бот рестарт\n• Добавить админа <id>\n'
            text+='\n[ В разработке: ]\n'
            text+='\n[ В планах: ]\n'
        return api.messages.send(peer_id=message['peer_id'],random_id=0,message=text)
        
        
# # # # #
        
        
    if pattern.startswith("расписание на "):
        mess_date=pattern[14:]
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошено расписание на дату в чате "+peerid+" ("+gr0up+")")
        logFile.close()
        # настрока даты
        dateneed=datetime.strptime(mess_date,"%d.%m.%y")
        datestrf = dateneed.strftime("%Y-%m-%d")
        # запрос данных
        groups = requests.get("https://api.ptpit.ru/groups")
        groups = groups.json()
        groups_format = {}
        for group in groups:
            id = group.get("id")
            name = group.get("name").lower()
            groups_format.update({name: id})
        while True:
            group = gr0up
            if group in groups_format:
                break
        dates = requests.get("https://api.ptpit.ru/timetable/weeks?visible=1")
        dates = dates.json()
        # поиск даты в свитче
        dates2 = dates[0]["start_week"]
        datecounter=0
        while dates2 > datestrf:
            datecounter+=1
            dates2 = dates[datecounter]["start_week"]
            if datecounter>10:
                break
        # запрос расписания  
        timetable = requests.get(f"https://api.ptpit.ru/timetable/groups/" + str(groups_format[group]) + "/" + dates2)
        timetable = timetable.json()
        text = ""
        for r in timetable:
            room=r['room_name']
            if r['date'] == datestrf:
                subgroup=str(r['subgroup'])
                if subgroup == "0":
                    subgroup=" "
                else:
                    subgroup="("+subgroup+"П)"
                text += f"{times[r['num']]}\n"
                text += f"{r['subject_name']} {subgroup}\n"
                if r['room_name'] != None:
                    if r['room_name'] == "ДО":
                        if (r['moodle']) != None:
                            link="ссылка"
                            #link=str(r['moodle["url"]'])
                        else:
                            link="нет ссылки"
                        text += "["+room+"| "+link+" ]"
                    else:
                        text += "[к."+room+"]"
                if r['teacher_surname'] != None:
                    text += f" {r['teacher_surname']} {r['teacher_name'][0]}. {r['teacher_secondname'][0]}.\n\n"
        # вывод
        dateneed=str(weekDays[dateneed.weekday()])+dateneed.strftime(", %d.%m.%y")
        if text != "":
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=f"Расписание на {dateneed}\n\n{text}")
        else:
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=f"Расписание на {dateneed} не найдено")
        
        
# # # # #


    if "пар" in pattern  and ("сейчас" in pattern or "следующ" in pattern):
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошены пары в чате "+peerid+" ("+gr0up+")")
        logFile.close()
        # настройка даты
        dateneed=datenow
        datestrf = dateneed.strftime("%Y-%m-%d")
        # поиск
        groups = requests.get("https://api.ptpit.ru/groups")
        groups = groups.json()
        groups_format = {}
        for group in groups:
            id = group.get("id")
            name = group.get("name").lower()
            groups_format.update({name: id})
        while True:
            group = gr0up
            if group in groups_format:
                break
        dates = requests.get("https://api.ptpit.ru/timetable/weeks?visible=1")
        dates = dates.json()
        # поиск даты для запроса
        dates2 = dates[0]["start_week"]
        datecounter=0
        while dates2 > datestrf:
            datecounter+=1
            dates2 = dates[datecounter]["start_week"]
            if datecounter>10:
                break
        # запрос расписания
        timetable = requests.get(f"https://api.ptpit.ru/timetable/groups/" + str(groups_format[group]) + "/" + dates2)
        timetable = timetable.json()
        text = ""
        # получение текущих пар
        for r in timetable:
            if r['date'] == datestrf:
                timeend=str(times[r['num']])[-5:]
                timenow=datenow.strftime("%H:%M")
                room=r['room_name']
                if timeend > timenow:
                    subgroup=str(r['subgroup'])
                    if subgroup == "0":
                        subgroup=" "
                    else:
                        subgroup="("+subgroup+"П)"
                    text += f"{times[r['num']]}\n"
                    text += f"{r['subject_name']} {subgroup}\n"
                    if r['room_name'] != None:
                        if r['room_name'] == "ДО":
                            if (r['moodle']) != None:
                                link="ссылка"
                                #link=str(r['moodle["url"]'])
                            else:
                                link="нет ссылки"
                            text += "["+room+"| "+link+" ]"
                        else:
                            text += "[к."+room+"]"
                    if r['teacher_surname'] != None:
                        text += f" {r['teacher_surname']} {r['teacher_name'][0]}. {r['teacher_secondname'][0]}.\n\n"
                    if "пара" in pattern:
                        title="Текущая пара:\n\n"
                        if subgroup == " ":
                            break
                    else:
                        title="Текущие пары:\n\n"
        # вывод
        if text != "":
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=title+text)
        else:
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=f"Пар на сегодня не найдено")


# # # # #


    if ("расписание" in pattern or "пары" in pattern) and ("сегодня" in pattern or "завтра" in pattern):
        if "сегодня" in pattern and "завтра" in pattern:
             return
        # логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошено расписание в чате "+peerid+" ("+gr0up+")")
        logFile.close()
        # настрока даты
        if "сегодня" in pattern:
            dateneed=datenow
        if "завтра" in pattern:
            dateneed=datenow +td(days=1)
        # корректировка вс>>>пн
        if dateneed.weekday() == 6:
            dateneed=dateneed+td(days=1)
        datestrf = dateneed.strftime("%Y-%m-%d")
        # запрос данных
        groups = requests.get("https://api.ptpit.ru/groups")
        groups = groups.json()
        groups_format = {}
        for group in groups:
            id = group.get("id")
            name = group.get("name").lower()
            groups_format.update({name: id})
        while True:
            group = gr0up
            if group in groups_format:
                break
        dates = requests.get("https://api.ptpit.ru/timetable/weeks?visible=1")
        dates = dates.json()
        # поиск даты в свитче
        dates2 = dates[0]["start_week"]
        datecounter=0
        while dates2 > datestrf:
            datecounter+=1
            dates2 = dates[datecounter]["start_week"]
            if datecounter>10:
                break
        # запрос расписания  
        timetable = requests.get(f"https://api.ptpit.ru/timetable/groups/" + str(groups_format[group]) + "/" + dates2)
        timetable = timetable.json()
        text = ""
        for r in timetable:
            if r['date'] == datestrf:
                room=r['room_name']
                subgroup=str(r['subgroup'])
                if subgroup == "0":
                    subgroup=" "
                else:
                    subgroup="("+subgroup+"П)"
                text += f"{times[r['num']]}\n"
                text += f"{r['subject_name']} {subgroup}\n"
                if r['room_name'] != None:
                    if r['room_name'] == "ДО":
                        if (r['moodle']) != None:
                            link="ссылка"
                            #link=str(r['moodle["url"]'])
                        else:
                            link="нет ссылки"
                        text += "["+room+"| "+link+" ]"
                    else:
                        text += "[к."+room+"]"
                if r['teacher_surname'] != None:
                    text += f" {r['teacher_surname']} {r['teacher_name'][0]}. {r['teacher_secondname'][0]}.\n\n"
        # вывод
        dateneed=str(weekDays[dateneed.weekday()])+dateneed.strftime(", %d.%m.%y")
        if text != "":
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=f"Расписание на {dateneed}\n\n{text}")
        else:
            return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=f"Расписание на {dateneed} не найдено")


# # # # #

    
    if "статус" in pattern and "бот" in pattern:
        text=" "
         #логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошен статус в чате "+peerid+" ("+gr0up+")")
        logFile.close()
        # проверка сайтов - главный
        site_main_code = subprocess.check_output('curl -is https://ptpit.ru | head -n 1', shell=True).decode("UTF-8")
        site_main_code=site_main_code[:-2]
        if site_main_code == "HTTP/1.1 200 OK":
            text+="\n&#127383; ptpit.ru: "+site_main_code[9:]
        else:
            text+="\n&#9888; ptpit.ru: "+site_main_code
        # проверка сайтов - расписание
        site_timetable_code = subprocess.check_output("curl -is https://timetable.ptpit.ru | head -n 1", shell=True).decode("UTF-8")
        site_timetable_code=site_timetable_code[:-2]
        if site_timetable_code == "HTTP/1.1 200 OK":
            text+="\n&#127383; timetable.ptpit.ru: "+site_timetable_code[9:]
        else:
            text+="\n&#9888; timetable.ptpit.ru: "+site_timetable_code
        # проверка сайтов - мудл
        site_moodle_code = subprocess.check_output("curl -is https://moodle.ptpit.ru | head -n 1", shell=True).decode("UTF-8")
        site_moodle_code=site_moodle_code[:-2]
        if site_moodle_code == "HTTP/1.1 200 OK":
            text+="\n&#127383; moodle.ptpit.ru: "+site_moodle_code[9:]
        else:
            text+="\n&#9888; moodle.ptpit.ru: "+site_moodle_code
        # батарея
        battery_capacity = subprocess.check_output("cat /sys/class/power_supply/battery/capacity", shell=True).decode("UTF-8")
        battery_percent=int(battery_capacity[:-1])
        battery_status = subprocess.check_output("cat /sys/class/power_supply/battery/status", shell=True).decode("UTF-8")
        battery_status=battery_status[:-2]
        if battery_status=="Chargin":
            text+="\n&#9889; "
        else:
            if battery_percent<=20:
                text+="\n&#9888; "
            else:
                text+="\n&#128267; "
        battery_percent=str(battery_percent)
        text+=battery_percent+'% | '+battery_status
        if fromid in admins:
            # дата
            text+="\n&#128368; "+str(datenow.strftime("%d.%m.%y %H:%M:%S %Z"))
            # кол-во админов
            text+="\n&#128110; "+str(len(admins))
        # разделитель
        text+="\n"+"    —    "*4
        # чат
        text+="\n&#128101; "+gr0up+" | &#127380; "+str(message['peer_id'])
        # вывод
        return api.messages.send(peer_id=message['peer_id'],random_id=randomid,message=text,dont_parse_links=1)

    
# # # # #
    
    
    if "рестарт" in pattern and "бот" in pattern:
        #логгирование
        dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
        logFile=open("botLog.log", "a")
        logFile.write("\n["+dateNow+"] [bot] запрошен рестарт "+fromid+" в чате "+peerid+" ("+gr0up+")")
        logFile.close()
        
        for i in admins:
            if i in fromid:
                api.messages.send(peer_id=message['peer_id'], random_id=0, message='&#9745; Выход...')
                #логгирование
                dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
                logFile=open("botLog.log", "a")
                logFile.write("\n["+dateNow+"] [bot] выход...")
                logFile.close()
                os._exit(0)
        return api.messages.send(peer_id=message['peer_id'], random_id=0, message='&#10006; Только для админов')


# # # # # # # # # # #
dateNow=str((datetime.now()+td(hours=5)).strftime("%d-%m-%y %H:%M:%S"))
logFile=open("botLog.log", "a")
logFile.write("\n["+dateNow+"] [bot] бот запущен")
logFile.close()
print("[bot] bot started")
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        multiprocess_worker = Thread(target=worker, args=(event,))
        multiprocess_worker.start()

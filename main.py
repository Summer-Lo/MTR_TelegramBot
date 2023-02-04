# Library
import asyncio
from datetime import datetime
import json
import requests
import telegram
from telegram.ext import Updater, CommandHandler
import telepot
from telepot.loop import MessageLoop
import time
# function file
import client_config as hc
import station_info as info

# variables
allowable_order = []
allowable_data = []
telepot_bot = telepot.Bot(hc.tg_bot_id)

def information(chat_msg):
    global telepot_bot, allowable_order, allowable_data
    # ---------------------------- Data from Station on the Line ----------------------------
    msg = requests.get("https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line="+str(hc.user_line)+"&sta="+str(hc.user_sta))
    msg_dict = json.loads(msg.text)
    msg_data = msg_dict['data']
    msg_dir = msg_data[hc.station]
    msg_dir_up = msg_dir['UP']      # UP : e.g. TUM == Tuen Mun
    msg_dir_down = msg_dir['DOWN']  # DOWN : e.g. WKS == Wu Kai Sha
    now = datetime.now()
    
    # ---------------------------- Telegram Bot infotmation ----------------------------
    #print(chat_msg['chat'])
    chat_id = chat_msg['chat']['id']
    text = chat_msg['text']
    print("Sender: ",chat_id)
    print("Received text: ",text)
    if (str(chat_id) == str(hc.chat_id)):
    # Information Function from user input
        if(str(text) == "Information" or str(text) == "information"):
            print("Information Message Received!")
            response = "[INFO]  The Next Train time information \nLine:            " + info.line[hc.user_line] + " \nStation:      " + info.sta[hc.user_sta]
            telepot_bot.sendMessage(hc.chat_id, response)
        # ---------------- Down Case ----------------
            if(hc.DIR == 'Down'):
                if(len(msg_dir_down) == 0):
                    response = "[INFO] ---------- Out of working hour ----------"
                    telepot_bot.sendMessage(hc.chat_id, response)
                elif(msg_dir_down[1]['dest'] != hc.dest):
                    response = "[INFO] ---------- Invalid Input ----------"
                    telepot_bot.sendMessage(hc.chat_id, response)
                else:
                    for i in range(len(msg_dir_down)):
                        if (msg_dir_down[i]['valid'] == 'Y' and datetime.strptime(msg_dir_up[i]['time'],"%Y-%m-%d %H:%M:%S") >= datetime.now()):
                            allowable_order.append(i)
                            allowable_data.append(msg_dir_down[i])
                    response = "[INFO]  The Next Train time information \nLine:            " + info.line[hc.user_line] + " \nStation:      " + info.sta[hc.user_sta]
                    telepot_bot.sendMessage(hc.chat_id, response)
                    for i in range(len(allowable_data)):
                        response = "Order :                " + allowable_data[i]['seq'] + "\n"
                        response = response + "Destination :   " + allowable_data[i]['dest'] + "\n"
                        response = response + "Arrive Time :   " + allowable_data[i]['time']
                        telepot_bot.sendMessage(hc.chat_id, response)

            # ---------------- Up Case----------------
            elif (hc.DIR == 'Up'):
                if(len(msg_dir_up) == 0):
                    response = "[INFO] ---------- Out of working hour ----------"
                    telepot_bot.sendMessage(hc.chat_id, response)
                elif(msg_dir_up[1]['dest'] != hc.dest):
                    response = "[INFO] ---------- Invalid Input ----------"
                    #print(response)
                    telepot_bot.sendMessage(hc.chat_id, response)
                else:
                    for i in range(len(msg_dir_up)):
                        if (msg_dir_up[i]['valid'] == 'Y' and datetime.strptime(msg_dir_up[i]['time'],"%Y-%m-%d %H:%M:%S") >= datetime.now()):
                            allowable_order.append(i)
                            allowable_data.append(msg_dir_up[i])
                    response = "[INFO] The Next Train time information in \nLine:            " + info.line[hc.user_line] + " \nStation:      " + info.sta[hc.user_sta]
                    telepot_bot.sendMessage(hc.chat_id, response)
                    for i in range(len(allowable_data)):
                        response = "Order :               " + allowable_data[i]['seq'] + "\n"
                        response = response + "Destination :   " + allowable_data[i]['dest'] + "\n"
                        response = response + "Arrive Time :   " + allowable_data[i]['time']
                        telepot_bot.sendMessage(hc.chat_id, response)

            # ---------------- No Data Case ----------------
            if(len(allowable_data) == 0):
                response = "[INFO] ------------------- No Data -------------------"
                telepot_bot.sendMessage(hc.chat_id, response)
            # ---------------- Reset ----------------
            allowable_order = []            # Reset
            allowable_data = []             # Reset
        # ---------------- Config stage  = 1 ---------------- 
        if(str(text) == "Config" or str(text) == "config"):         
            print("Config Message Received!")
            hc.config_stage = 1
            response = "[Config] Please input the Line for Configuration!"
            telepot_bot.sendMessage(hc.chat_id, response)

        # ---------------- Config stage  = 2 ---------------- 
        if(hc.config_stage == 1):
            if str(text) in info.line:              # check user input line vaild or not
                hc.config_stage = 2
                hc.user_line_temp = str(text)
                response = "[Config] Please input the Station for Configuration!"
                telepot_bot.sendMessage(hc.chat_id, response)
            elif (str(text) not in info.line and str(text) != "Config" and str(text) != "config"):
                response = "[Config] --------- Invalid Input ---------\n[Config] ------- Please try again -------"
                telepot_bot.sendMessage(hc.chat_id, response)

        # ---------------- Config stage  = 3 ---------------- 
        if(hc.config_stage == 2):
            if str(text) in info.sta:           # check user input station valid or not
                hc.config_stage = 3
                hc.user_sta_temp = str(text)
                response = "[Config] Please type OK for confirm: \n"
                response = response + "Inputed Line:          " + info.line[hc.user_line_temp] + "\n"
                response = response + "Inputed Station:     " + info.sta[hc.user_sta_temp] + "\n"
                telepot_bot.sendMessage(hc.chat_id, response)
            elif (str(text) not in info.line and str(text) not in info.sta and str(text) != "Config" and str(text) != "config"):
                response = "[Config] --------- Invalid Input ---------\n[Config] -------- Please try again --------"
                telepot_bot.sendMessage(hc.chat_id, response)
        
        # ---------------- Config stage  = 4 ---------------- 
        if(hc.config_stage == 3):
            if(str(text) == "OK" or str(text) == "Ok" or str(text) == "ok"):
                hc.config_stage = 0
                hc.user_line = str(hc.user_line_temp)
                hc.user_sta = str(hc.user_sta_temp)
                hc.station = hc.user_line+"-"+hc.user_sta
                hc.user_line_temp = ""
                hc.user_sta_temp = ""
                response = "[Config] Configuration have been done!"
                telepot_bot.sendMessage(hc.chat_id, response)
                response = "[Info] ---------- Information for " + str(hc.user_sta) + " in " + str(hc.user_line) + " ----------"
                telepot_bot.sendMessage(hc.chat_id, response)
            
async def main():
    global telepot_bot
    bot = telegram.Bot(hc.tg_bot_id)

    async with bot:
        pass
        #print(await bot.get_me())
        #await bot.send_message(text="Hello", chat_id=hc.chat_id)

if __name__ == '__main__':
    MessageLoop(telepot_bot, information).run_as_thread()
    while(True):
        asyncio.run(main())
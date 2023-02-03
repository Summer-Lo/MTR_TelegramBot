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

# variables
allowable_order = []
allowable_data = []
telepot_bot = telepot.Bot(hc.tg_bot_id)

def information(chat_msg):
    global telepot_bot
    # ---------------------------- Data from Siu Hong Station on the Tuen Ma Line ----------------------------
    msg = requests.get("https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line=TML&sta=SIH")
    msg_dict = json.loads(msg.text)
    msg_data = msg_dict['data']
    msg_dir = msg_data[hc.station]
    msg_dir_up = msg_dir['UP']      # UP : TUM == Tuen Mun
    msg_dir_down = msg_dir['DOWN']  # DOWN : WKS == Wu Kai Sha
    now = datetime.now()
    
    # ---------------------------- Telegram Bot infotmation ----------------------------
    #print(chat_msg['chat'])
    chat_id = chat_msg['chat']['id']
    text = chat_msg['text']
    print("Sender: ",chat_id)
    print("Received text: ",text)
    if (str(chat_id) == str(hc.chat_id)):
        if(str(text) == "Information" or str(text) == "information"):
            print("Message Received!")
        # ---------------- Down Case ----------------
            if(hc.DIR == 'Down'):
                if(msg_dir_down[1]['dest'] != hc.dest):
                    response = "[INFO] ---------- Invalid Input ----------"
                    #print(response)
                    telepot_bot.sendMessage(hc.chat_id, response)
                else:
                    for i in range(len(msg_dir_down)):
                        if (msg_dir_down[i]['valid'] == 'Y' and msg_dir_down[i]['dest'] == hc.dest and datetime.strptime(msg_dir_up[i]['time'],"%Y-%m-%d %H:%M:%S") >= datetime.now()):
                            allowable_order.append(i)
                            allowable_data.append(msg_dir_down[i])

                    #print(allowable_order)
                    #print(allowable_data)
                    for i in range(len(allowable_data)):
                        response = "Order :                " + allowable_data[i]['seq'] + "\n"
                        response = response + "Destination :    " + allowable_data[i]['dest'] + "\n"
                        response = response + "Arrive Time :     " + allowable_data[i]['time']
                        #print(response)
                        telepot_bot.sendMessage(hc.chat_id, response)

            # ---------------- Up Case----------------
            elif (hc.DIR == 'Up'):
                if(msg_dir_up[1]['dest'] != hc.dest):
                    response = "[INFO] ---------- Invalid Input ----------"
                    #print(response)
                    telepot_bot.sendMessage(hc.chat_id, response)
                else:
                    for i in range(len(msg_dir_up)):
                        if (msg_dir_up[i]['valid'] == 'Y' and msg_dir_up[i]['dest'] == hc.dest and datetime.strptime(msg_dir_up[i]['time'],"%Y-%m-%d %H:%M:%S") >= datetime.now()):
                            allowable_order.append(i)
                            allowable_data.append(msg_dir_up[i])

                    #print(allowable_order)
                    #print(allowable_data)
                    for i in range(len(allowable_data)):
                        response = "Order :                " + allowable_data[i]['seq'] + "\n"
                        response = response + "Destination :    " + allowable_data[i]['dest'] + "\n"
                        response = response + "Arrive Time :     " + allowable_data[i]['time']
                        #print(response)
                        telepot_bot.sendMessage(hc.chat_id, response)

            if(len(allowable_data) == 0):
                response = "[INFO] ------------- No Data -------------"
                #print(response)
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
'''
Implementation Decode Image Text To Audio Speecch
Code by sandroputraa
'''


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import base64
from gtts import gTTS
import random
import os
import time
import requests

TOKEN = "BOT TOKEN"

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    calldata = call.data
    split = calldata.split("|")
    Lang = split[0]
    FileName = split[1]
    Type = split[2]

    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,text="You Select " + Lang + " Language, Please Wait Processing Your Audio 😁")
    if Type == "Img":

        url = "http://sandroputraa.my.id/API/OCR.php"

        with open(str(FileName), 'rb') as file:
            encoded_string = base64.b64encode(file.read())

        payload = {"img": "" + encoded_string.decode('utf-8') + ""}
        headers = {
            "Auth": "sandrocods",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        text = response.json()['Data']

        bot.delete_message(call.message.chat.id, call.message.message_id)

        if len(text) <= 1:
            print(f"No Text", flush=True)
            bot.send_message(call.message.chat.id, '<b> Try Another Image <b>')
        else:
            print(f"Length String : {len(text)}", flush=True)
            fix_text = ' '.join(text.split('\n'))
            print(f"Text : {fix_text}", flush=True)
            try:
                bot.send_chat_action(call.message.chat.id, 'record_audio')
                audio = gTTS(text, lang=Lang)
                bot.send_chat_action(call.message.chat.id, 'upload_audio')
                audio.save(str(FileName) + '.mp3')
                bot.send_audio(call.message.chat.id, open(str(FileName) + '.mp3', 'rb'),
                               "Success Decode Image To Audio", performer='Sandro ITS Bot', title="Decode Result")
            except:
                bot.send_message(call.message.chat.id, '<b> Try Another Image </b>')

        os.remove(str(FileName))
        os.remove(str(FileName) + ".mp3")
    elif Type == "Txt":

        text = open(FileName, 'r').read()
        print(f"Length String : {len(text)}", flush=True)
        fix_text = ' '.join(text.split('\n'))
        print(f"Text : {fix_text}", flush=True)
        try:
            bot.send_chat_action(call.message.chat.id, 'record_audio')
            audio = gTTS(text, lang=Lang)
            bot.send_chat_action(call.message.chat.id, 'upload_audio')
            audio.save(str(FileName) + '.mp3')
            bot.send_audio(call.message.chat.id, open(str(FileName) + '.mp3', 'rb'), "Success Decode Text To Audio",
                           performer='Sandro ITS Bot', title="Decode Result")
        except:
            bot.send_message(call.message.chat.id, '<b> Try Another Text </b>')

        os.remove(str(FileName))
        os.remove(str(FileName) + ".mp3")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome " + message.chat.first_name + " To <b> ITS </b> ( Image To Speech ) Bot 🤖\n"
                                                                 "How To Use Image To Audio : \n"
                                                                 "~ Send pictures\n"
                                                                 "~ Select Language\n"
                                                                 "~ Waitting Bot Send Audio\n\n"
                                                                 "How To Use Text To Audio : \n"
                                                                 "~ Type <code>/text YOUR TEXT</code>\n"
                                                                 "~ Select Language\n"
                                                                 "~ Waitting Bot Send Audio\n\n\n"
                                                                 "Author : <a href='https://t.me/Sandroputraaa'>Sandro Putraa</a>")


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    print(f"File ID : {message.photo[1].file_id}", flush=True)
    file_info = bot.get_file(message.photo[1].file_id).file_path
    PhotoRandom = "Photo" + str(random.randint(0, 1000)) + ".png"
    save = bot.download_file(file_info)
    with open(str(PhotoRandom), 'wb') as simpan:
        simpan.write(save)

    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Indonesia", callback_data="id|" + PhotoRandom + "|Img"),
        InlineKeyboardButton("English United States", callback_data="en|" + PhotoRandom + "|Img"),
    )
    bot.send_message(message.chat.id, "Select Language :", reply_markup=markup)


# Handles all text messages that match the regular expression
@bot.message_handler(regexp=r"/text ((.|\n)*)")
def handle_message(message):
    FileRandom = "File" + str(random.randint(0, 1000)) + ".txt"
    text = message.text
    fix_text = text.split("/text ")
    with open(str(FileRandom), "w") as text_file:
        text_file.write(fix_text[1])

    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Indonesia", callback_data="id|" + FileRandom + "|Txt"),
        InlineKeyboardButton("English United States", callback_data="en|" + FileRandom + "Txt"),
    )
    bot.send_message(message.chat.id, "Select Language :", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def command_default(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


try:
    print(f"Bot Still Running", flush=True)
    bot.infinity_polling()
except:
    time.sleep(3)

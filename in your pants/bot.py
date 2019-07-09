token='807872051:AAGaedVqrwtwVfKRgwygTzwGTSsOh3JVjGU'
import telebot
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlretrieve
import os
import random
import telebot
from telebot import apihelper
from PIL import Image
import cv2
import numpy as np
import requests
session = requests.Session()
i = 0

def download_picture(text):
    os.system('python downloader.py -s {} -o pics --limit 1'.format(text.replace(' ', '+')))
    
def get_picture(text):
    response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': text,
                    'format': 'json'
                }
            ).json()
    image_url = response.get('Image')
    urlretrieve(image_url, 'img.jpeg')    
    
def put_into_pants(text):
    try:
        get_picture(text)
        print('dick api')
    except:
        download_picture(text)
        print('bing api')
    download_picture(text)
    text=text.upper()
    print(text)
    back = Image.open('jeans.png').resize((512,512))
    # background = Image.new('RGBA', size=(512,512))
    front = Image.open('pics/img.png', 'r').resize((160,160))
    back.paste(front, (175,5))
    # background.paste(back,(0,0))
    fnt = ImageFont.truetype('/Library/Fonts/Impact.ttf', 30)
    d = ImageDraw.Draw(back)
    d.text((100,420), "    {}\n    У ТЕБЯ В ШТАНАХ".format(text.upper()), font=fnt, fill=(0, 0, 0))
    name = 'stickers/curr{}.png'.format(random.randint(0,400))
    back.save('result.png', format='png')
    os.system('rm -r pics/*')
    
def break_if_too_long(string, widthsize = 38):
    if len(string) > widthsize*2:
        string = string[:38]+'\n         '+string[38:76]+'\n         '+string[76:]
        return string
    if len(string) > widthsize:
        string = string[:38]+'\n         '+string[38:]
    return string
def cut_into_sticker(path):
    basewidth = 512
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    if img.size[1] > 512:
        img=img.crop((0,0,512,512))
    print(img.size)
    img.save(path) 

def delete_background(path):
    print('running')
    os.system('python3 /Users/n.zueva/Desktop/image-background-removal/seg.py \
    {} {} 1'.format(path, path))
    
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=["text", "photo"])
def handle(message, i=0): 
    # print(message)
    try:
        print('direct recieved')
        i += 1
        text = message.text.split(' ')[0]
        
        bot.send_photo(chat_id=message.chat.id, photo=open(name, 'rb'))
    except:
        try:
            print('photo recieved')
            file_path = bot.get_file(message.photo[1].file_id).file_path
            link = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)
            tmp_name = '{}{}.png'.format('file_' + message.from_user.first_name,random.randint(24,42))
            urlretrieve(link, tmp_name)
            print('saved at {}'.format(tmp_name))
            delete_background(tmp_name)
            cut_into_sticker(tmp_name)
            print('alalala')
            bot.send_photo(chat_id=message.chat.id, photo=open(tmp_name, 'r'))
        except:
            try:
                print('direct recieved')
                i += 1
                print('-'*80)
                print(message.from_user)
                text = message.text
                put_into_pants(text)
                bot.send_photo(chat_id=message.chat.id, photo=open('result.png', 'rb'))
            except:
                bot.send_message(chat_id=message.chat.id, text = 'oops. Something went wrong!')
                
                
if __name__ == '__main__':
    bot.polling(none_stop=True,  timeout=123)

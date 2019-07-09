token=''
import telebot
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlretrieve
import os
import random
import telebot
from telebot import apihelper
from PIL import Image
i = 0

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
        print('-'*80)
        print(message.forward_from)
        file_id = bot.get_user_profile_photos(message.forward_from.id).photos[0][0].file_id
        file_path = bot.get_file(file_id).file_path
        link = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)
        tmp_name = '{}.png'.format(message.forward_from.first_name)
        urlretrieve(link, tmp_name)
        name = message.forward_from.first_name
        text = message.text
        filename = '{}.png'.format(name)
        ironman = Image.open(filename, 'r').resize((70,70))
        text_img = Image.new('RGBA', (512,120), (0, 0, 0, 0))
        text_img.paste(ironman, (0,0))
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
        d = ImageDraw.Draw(text_img)
        d.text((40,12), "         {}\n         {}".format(name,break_if_too_long(text)), font=fnt, fill=(0, 0, 0))
        name = 'stickers/curr{}.png'.format(random.randint(0,400))
        i += 1
        text_img.save(name, format="png")
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
            bot.send_photo(chat_id=message.chat.id, photo=open(tmp_name, 'rb'))
        except:
            try:
                print('direct recieved')
                i += 1
                print('-'*80)
                print(message.from_user)
                text = message.text
                filename = '{}.png'.format(name)
                ironman = Image.open(filename, 'r').resize((70,70))
                text_img = Image.new('RGBA', (512,120), (0, 0, 0, 0))
                text_img.paste(ironman, (0,0))
                fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
                d = ImageDraw.Draw(text_img)
                d.text((40,12), "         {}\n         {}".format(name,break_if_too_long(text)), font=fnt, fill=(0, 0, 0))
                name = 'stickers/curr{}.png'.format(random.randint(0,400))
                i += 1
                text_img.save(name, format="png")
                bot.send_photo(chat_id=message.chat.id, photo=open(name, 'rb'))
            except:
                bot.send_message(chat_id=message.chat.id, text = 'oops, error!')
                
if __name__ == '__main__':
    bot.polling(none_stop=True,  timeout=123)
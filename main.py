import telebot as tb
import os
from dotenv import load_dotenv
import json
import os
import time
from telebot import apihelper
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InlineQueryResultArticle, InputTextMessageContent
import requests
import traceback
from urllib.parse import urlparse, unquote
from gtts import gTTS
from openai import OpenAI
import re
import shutil
import tempfile
import traceback
import apihelper as ah
import regexp as rx
import yt_dlp
from telebot.types import ChatPermissions

INSTAGRAM_RE = re.compile(r"https?://(www\.)?instagram\.com/(p|reel|reels|tv)/[\w-]+")
MAX_SIZE = 50 * 1024 * 1024 * 1024 # Telegram bot upload limit



if not os.path.exists("DOWNLOAD_PATH"):
    os.makedirs("DOWNLOAD_PATH", exist_ok=True)


logger = tb.logger
tb.logger.setLevel(logging.INFO)

load_dotenv()


token = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = tb.TeleBot(token)


group_of_junk = ["کص", "کس", "کیر", "کیرم", "کیرم تو", "کیرم تو سرت", "کیرم تو سرتو", "کیرم تو سرتو گوه", "کیرم تو سرتو گوه بخور", "کیرم تو سرتو گوه بخور گوه بخور", "کیرم تو سرتو گوه بخور گوه بخور گوه بخور", "کیرم تو سرتو گوه بخور گوه بخور گوه بخور گوه بخور", "کیرم تو سرتو گوه بخور گوه بخور گوه بخور گوه بخور گوه بخور","کص", "کصکش", "کسکش", "کسخل", "کسشر", "کسشعر", "کسمغز", "کسننه",
    "جنده", "جندگی", "جاکش", "جاکشی", "قحبه", "قحبگی",
    "گایید", "میگایم", "بگایم", "بگاد", "میگام",
    "حرومزاده", "حرومزادگی", "حرامزاده", "حرامزادگی", "زنازاده",
    "دیوث", "دیوثی", "فاحشه",
    "کونکش", "کونگشاد", "کونده",
    "خایه", "خایهمال", "خایمال",
    "بیناموس", "بی ناموس",
    "پدرسگ", "پدر سگ", "ننهسگ", "ننه سگ",
    "مادرخراب", "مادر خراب",  "کس", "کسم", "کست", "کسش",
    "کیر", "کیری", "کیرم", "کیرت", "کیرش", "کیرمو", "کیرتو", "کیرخر",
    "کون", "کونی", "کونم", "کونت", "کونش",
    "کوس", "کوص",
    "گه", "گوه",
    "جق", "جقی", "جقم", "kir", "kiri", "kiram", "kir khar",
    "kos", "kose", "kosse", "koskesh", "kos nane",
    "kooni", "kuni", "koon",
    "jende", "jakesh",
    "haromzade", "haramzade",
    "goh", "gaidam", "gayidam",
    "madar jende", "pedar sag", "عوضی", "بیشعور", "بی شعور", "کثافت", "نکبت", "لاشی", "پفیوز",
    "بیغیرت", "بی غیرت", "پدرسوخته", "اسکل", "گاگول", "احمق", "پستفطرت"]

if not token:
    raise RuntimeError("the token is not exosted")

@bot.message_handler(commands=['protofile'])
def pager(message):
    markup = InlineKeyboardMarkup(row_width=2)
    telegram = InlineKeyboardButton("Telegram", url="https://t.me/ARASHDRG") 
    instagram = InlineKeyboardButton("Instagram", url="https://instagram.com/profile/Arash_drg_")
    linkedin = InlineKeyboardButton("Linkedin",url="https://linkedin.com")
    Email = InlineKeyboardButton("Email", url="https://arashdargi52.com")
    next = InlineKeyboardButton("Next", callback_data="next")
    cancel = InlineKeyboardButton("Cancel", callback_data="cancel")
    markup.add(telegram , instagram, linkedin, Email, next, cancel)
    bot.send_message(message.chat.id, "Here is the Arash Dargi protofile link", reply_markup=markup)

@bot.callback_query_handler(func= lambda call : True)
def handles_querys(call):
    if call.data == "next":
        bot.answer_callback_query(call.id, text="go to the next page")
        mkp = InlineKeyboardMarkup(row_width=2)
        facebook = InlineKeyboardButton("facebook", url="https://facebook.com")
        twitch = InlineKeyboardButton("twitch", url="https://twitch.com")
        next2 = InlineKeyboardButton("Next", callback_data="next")
        back = InlineKeyboardButton("Back", callback_data="back")
        mkp.add(facebook, twitch, next2, back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Here is the next page",  reply_markup=mkp)
    elif call.data == "cancel":
        bot.answer_callback_query(call.id, "cancel the proccess",cache_time=0)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id, timeout=0)
    elif call.data == "back":
        bot.answer_callback_query(call.id, text="go back to the previous page")
        markup = InlineKeyboardMarkup(row_width=2)
        telegram = InlineKeyboardButton("Telegram", url="https://t.me/ARASHDRG") 
        instagram = InlineKeyboardButton("Instagram", url="https://instagram.com/profile/Arash_drg_")
        linkedin = InlineKeyboardButton("Linkedin",url="https://linkedin.com")
        Email = InlineKeyboardButton("Email", url="https://arashdargi52.com")
        next = InlineKeyboardButton("Next", callback_data="next")
        cancel = InlineKeyboardButton("Cancel", callback_data="cancel")
        markup.add(telegram , instagram, linkedin, Email, next, cancel)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text= "first page",  reply_markup=markup)

def download_instagram_video(url, out_dir):
    opts = {
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "quiet": True,
        "socket_timeout": 30,
        # "cookiefile": "cookies.txt",  # needed if Instagram asks for login
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


@bot.message_handler(func=lambda m: m.text and INSTAGRAM_RE.search(m.text))
def handle_instagram(message):
    url = INSTAGRAM_RE.search(message.text).group(0)
    tmp_dir = tempfile.mkdtemp()  # unique folder per request
    try:
        bot.send_chat_action(message.chat.id, action="upload_video")
        file_path = download_instagram_video(url, tmp_dir)

        if os.path.getsize(file_path) > MAX_SIZE:
            bot.reply_to(message, "The video is larger than 50 MB, so I can't send it.")
            return

        with open(file_path, "rb") as f:
            bot.send_video(
                chat_id=message.chat.id,
                video=f,
                caption="here is your video",
                reply_to_message_id=message.message_id,
            )
    except Exception:
        traceback.print_exc()  # real error shows in your console
        bot.reply_to(message, "Couldn't download this link. It may be private or not a video.")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

warnings = []


@bot.message_handler(func=lambda message: any(junk in message.text for junk in group_of_junk))
def handle_junk_message(message):
    if message.from_user.id in warnings:
        warnings[message.from_user.id] =+1
    else:
        warnings[message.from_user.id] = 1

    if warnings[message.from_user.id > 3]:

        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=300)
        bot.send_message(message.chat.id, "لطفا از استفاده از کلمات زشت خودداری کنید.")
        bot.delete_message(message.chat.id, message.message_id)
    else:
        bot.send_message(message.chat.id, f"please dont say bad word its your {message.from_user.id} time if you say for the third timme you will restricted for five minute")


@bot.message_handler(commands=['start', 'help'])
def send_message(message):
    logger.info(message.chat.__dict__)
    bot.send_message(message.chat.id, "Hello Welcome to the Digaily Shop How Could i help you ?")
    bot.delete_message(message.chat.id, message.message_id)



@bot.message_handler(commands=['give'])
def send_message(message):
    bot.reply_to(message, "Https://DiagialyShop.com")


@bot.message_handler(commands=['details'])
def send_message(message):
    bot.send_message(message.chat.id, json.dumps(message.chat.__dict__ ,indent=4,  ensure_ascii=False))

hello_words = list(["hi", "hello", "hey", "salam", "salaam", "salaam", "salam", "سلام", "سلام", "سلام", "سلام", "سلام", "سلام", "سلام"])

@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in hello_words))
def send_message(message):
    bot.send_message(message.chat.id, "salam")

@bot.message_handler(content_types=['image'])
def send_message(message):
    bot.send_message(message.chat.id, "Nice Image")


how_are_you_words = list(["how are you", "how r u", "how r you", "how are u", "چطوری", "چطوری؟", "چطوری", "چطوری؟", "چطوری", "چطوری؟", "چطوری", "چطوری؟", "چطوری", "چطوری؟", "چطوری", "چطوری", "khoobi", "khoobi", "khoobi?", "khoobi", "khoobi?", "khoobi", "khoobi?", "khoobi", "khoobi?", "khoobi", "khoobi?", "khoobi", "khoobi?"])

@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in how_are_you_words))
def send_message(message):
    bot.reply_to(message, "I'm good, thanks! how about you?")

@bot.message_handler(commands=['delete'])
def delete_message(message):
    bot.delete_message(message.chat.id, json.loads(message.json).get("message_id"))


def status_user(message):
    return message.new_chat_member.status in ['kicked', 'member']

@bot.my_chat_member_handler(func = status_user)
def handle_my_chat_member(message):
    if message.new_chat_member.status == 'kicked':
        bot.send_message(message.chat.id, "I have been removed from the group.")
    elif message.new_chat_member.status == 'member':
        bot.send_message(message.chat.id, "I have been added to the group.")


@bot.message_handler(content_types=['new_chat_members'])
def on_join(message):

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass

    for user in message.new_chat_members:

        if user.is_bot and user.id != bot.get_me().id:
            bot.ban_chat_member(message.chat.id, user.id)

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.chat.type in ['group', 'supergroup']:
        sender = bot.get_chat_member(message.chat.id, message.from_user.id)
        if sender.status in ['administrator', 'creator']:
            bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name} unbanned.")
    elif sender.status not in ['administrator', 'creator']:
        bot.reply_to(message, "فقط ادمین‌ها می‌توانند از این دستور استفاده کنند.")
    else:
        bot.reply_to(message, "این دستور فقط در گروه کار می‌کند.")



@bot.message_handler(commands=['setname'])
def handle_the_desire_message(message):
    bot.send_message(message.chat.id, "what is your name ?")
    bot.register_next_step_handler(message, set_name, "text", number=-3)
def set_name(message, name, number):
    logger.info(name)
    logger.info(number)
    bot.send_message(message.chat.id, f"hello {message.text}")


@bot.message_handler(commands=['choose'])
def choose_desire_option(message):
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        input_field_placeholder="یکی را انتخاب کنید"
    )
    markup.add(
        KeyboardButton("help"),
        KeyboardButton("about"),
        KeyboardButton("Download"), 
        KeyboardButton('commands details')
    )
    bot.send_message(message.chat.id, "یکی را انتخاب کنید:", reply_markup=markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: message.text in ["help", "about", "Download", "commands details"])
def handle_choice(message):
    if message.text == "help":
        bot.send_message(
            message.chat.id,
            "برای دریافت کمک به این کاربر پیام دهید: @arashdrg"
        )
    elif message.text == "about":
        bot.send_contact(
            message.chat.id,
            phone_number="09938429323",
            first_name="Contact"
        )
    elif message.text == "Download":
        send_message = bot.send_message(message.chat.id, "please enter your desire link to download : ")
        if send_message == True:
            bot.delete_message(message.chat.id, message.message_id)
            bot.register_next_step_handler(message=message.message_id, callback=handle_instagram)
    elif message.text == "commands details":
        send_message = bot.send_message(message.chat.id, f" click on the query  /{"detcomm"} please wait i will send you")
        if send_message == True:
            bot.register_next_step_handler(message=message.message_id, callback=handle_commands)
            bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(func= lambda message : message == "help")
def send_help(message):
    send_message(message.chat.id, "how can i help you ?")
@bot.message_handler(func= lambda message:message=="about")
def send_about(message):
    send_message(message.chat.id, "here is the digaily bot to help you in shopping")


@bot.message_handler(commands=['ban'])
def ban_for_minutes(message):

    if message.chat.type not in ['group', 'supergroup']:
        logger.warning("Command used outside a group.")
        bot.reply_to(message, "این دستور فقط در گروه کار می‌کند.")
        return

    sender = bot.get_chat_member(message.chat.id, message.from_user.id)
    if sender.status not in ['administrator', 'creator']:
        logger.warning("User is not an administrator.")
        bot.reply_to(message, "فقط ادمین‌ها می‌توانند از این دستور استفاده کنند.")
        return

    target = message.reply_to_message.from_user
    try:
        bot.restrict_chat_member(
            message.chat.id,
            target.id,
            until_date=int(time.time()) + 300
        )
        bot.send_message(message.chat.id, f"{target.first_name} برای ۵ دقیقه بن شد.")
    except Exception as e:
        bot.reply_to(message, f"بن انجام نشد: {e}")

@bot.message_handler(commands=['URL'])
def send_URL(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Diagily Shop", url="http://digikala.com"))
    markup.add(InlineKeyboardButton("google", url="https://google.com"))
    markup.add(InlineKeyboardButton("Amooozeshyar", url="https://stdn.ir"))
    markup.add(InlineKeyboardButton("Next", callback_data="next"))
    bot.send_message(message.chat.id, "please choose your desire url", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_the_callback(call):
    if call.data == "next":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Back", callback_data="back"))
        markup.add(InlineKeyboardButton("Cancel", callback_data="cancel"))
        bot.edit_message_text(call.message.chat.id, call.message.id, "another step begun", reply_markup=markup)
    if call.data == "cancel":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="done", reply_markup=markup)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id, timeout=5)
    if call.data == "back2":
        bot.edit_message_text(chat_id = call.message.chat.id, message_id= call.message.id, text="done", reply_markup=markup)
        bot.send_message(call.message.chat.id, "go back to the prevous page")
    
@bot.message_handler(commands=["file"])
def send_file(file):
    file_op = open("./text/2mb.pdf", "rb")
    bot.send_chat_action(file.chat.id, action="upload_document")
    bot.send_document(file.chat.id, document=file_op)
    file_op.close()

@bot.message_handler(regexp=r"^\s*(send\s+file|ارسال\s+فایل|send|file)\s*$")
def file_darsi_send(file):
    des_file = open("./text/DPL2-ArashDargi-SRB.pdf", "rb")
    markup = InlineKeyboardMarkup()
    download_btn = InlineKeyboardButton("Download", callback_data="Download")
    like_btn = InlineKeyboardButton("like", callback_data="like")
    markup.add(download_btn, like_btn)
    bot.send_chat_action(file.chat.id, action="upload_document")
    bot.send_document(file.chat.id, document=des_file, reply_markup=markup, caption="this file is the second endivisual excersize for msr sharifan")
    if file.data == "Download":
        bot.download_file(des_file)
    elif file.data == "like":
        bot.add_message_reaction_count_handler()
    des_file.close()


@bot.message_handler(content_types=['photo', 'document', 'audio', 'video', 'voice'])
def send_detail_file(message):
    logger.info(message.__dict__)
    
@bot.inline_handler(func= lambda query : True)
def bot_inline_works(query):
    results =[]
    results.append(InlineQueryResultArticle(
        id=1, 
        title="join the bot", 
        input_message_content=InputTextMessageContent(message_text="click to join the bot"),  
        description="bot URL", 
        url="https://t.me/Digaily_bot"
    ))
    results.append(InlineQueryResultArticle(id=2, 
                   title="welcome message",
                   input_message_content=InputTextMessageContent(message_text="welcoming")))

    results.append(InlineQueryResultArticle(id=3, 
                   title="bot URL",
                   input_message_content=InputTextMessageContent(message_text="https://t.me/digaily_bot")))
    
    bot.answer_inline_query(query.id, results=results, cache_time=0)

@bot.message_handler(regexp="profile photo")
def send_profile_photo(message):
    photos = bot.get_user_profile_photos(user_id=message.from_user.id)

    if not photos.photos:
        bot.send_message(message.chat.id, "No profile photos found.")
        return
    file_id = photos.photos[1][1].file_id 
    bot.send_chat_action(message.chat.id, "upload_photo")
    bot.send_photo(message.chat.id, file_id)

@bot.message_handler(regexp=r"all profile")
def send_all_user_profile(message):
    user_id = message.from_user.id
    offset = 0
    limit = 100

    while True:
        result = bot.get_user_profile_photos(
            user_id=user_id,
            offset=offset,
            limit=limit
        )
        bot.delete_message(message.chat.id, message.message_id)

        if not result.photos:
            if offset == 0:
                bot.send_message(message.chat.id, "No profile photos found.")
            break

        for photo_sizes in result.photos:
            file_id = photo_sizes[-1].file_id
            bot.send_chat_action(message.chat.id, action="upload_photo")
            bot.send_photo(message.chat.id, photo=file_id)

        offset += len(result.photos)

        if offset >= result.total_count:
            break


DOWNLOAD_PATH = "DOWNLOAD_PATH/"

def download_file_link(url):
    local_filename = urlparse(url).path.split('/')[-1] or "downloaded_file"
    file_path = DOWNLOAD_PATH + local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return file_path

@bot.message_handler(regexp=r"^(https://www\.instagram\.com/.*|\S+\.(mp4))$")
def download_movie(message):
    url = message.text
    try:
        file_path = download_file_link(url)
        bot.send_chat_action(message.chat.id, action="upload_video")
        bot.send_video(chat_id=message.chat.id, video=open(file_path, "rb"), caption="here is your movie",reply_to_message_id=message.message_id)
        os.remove(file_path)
    except Exception as f:
        bot.reply_to(message, f"there was some invalid details : {f}")


@bot.message_handler(regexp=r"https://|mkv$")
def download_file(message):
    url = message.text
    try:
        file_path = download_file_link(url)
        bot.send_chat_action(message.chat.id, action="upload_document")
        bot.send_document(chat_id=message.chat.id, document=open(file_path, 'rb'), caption="here is your desire file", reply_to_message_id=message.message_id)
        os.remove(file_path)
    except Exception as e:
        bot.reply_to(message, f"your link is not valid  : {e}")

if not os.path.exists("voices"):
    os.makedirs("voices")

@bot.message_handler(func= lambda message : len(message.text) > 20 and len(message.text) < 200)
def message_to_audio(message):
    text = message.text
    output = gTTS(text=text, lang="en")
    file_path = "voices/output.mp3"
    output.save(file_path)
    bot.send_chat_action(message.chat.id, action="record_voice")
    bot.send_voice(message.chat.id, voice=open(file_path, "rb"), reply_to_message_id=message.id, caption="here is your voice of the desire text")
    os.remove(file_path)

"""@bot.message_handler(func=lambda message : True)
def divar_commercial(message):
    bot.send_message(message.chat.id, text="send me a query tio show you alist of the product in the digikala")
"""

'''def request_to_digikala(text_query):
    url = "https://api-dwid.digikala.com/search/category-mobile-phone/apple/"
    params = {
        "p" : text_query
    }
    response = requests.get(url=url, params=params)
    return response.json
'''
"""@bot.message_handler(func= lambda message :True)
def handlle_product_digi(text):
    text =text.text
    data = request_to_digikala(text)
    for item in data['data']['children'][1:21] :
        title = item["data"]["title"]
        image = item["data"]["image"]
        url = item["data"]["url"]
        token = item["data"]["token"]
        description = f"{title}\n{image}\n{url}\n'https://www.digikala.com/v/{token}'"
        bot.send_message(text.chat.id, text=description)
    """

@bot.chat_join_request_handler(func= lambda request : request.chat.type in ['supergroup', "group"])
def new_user(request):
    listts = ["arashdrrrg", "arashdrrg", "arashdrrrrg","nimao_o"]
    if request.from_user.username in listts :
       bot.approve_chat_join_request(request.chat.id, user_id=request.from_user.id)
       bot.send_message(request.chat.id, f"welcome to our group Mrs or Ms {request.from_user.username}")
       logger.info("accepted")
    else:
        bot.decline_chat_join_request(request.chat.id, request.from_user.id)
        logger.info("declined")

@bot.message_handler(func=lambda m:
    m.chat.type in ("supergroup", "group")
    and m.content_type == "text"
    and m.text.startswith("***")
)
def chat_group(message):
    bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


@bot.message_handler(func=lambda m:
    m.chat.type in ("supergroup", "group")
    and m.content_type == "text"
    and m.text.startswith("unpin")
)
def unpin_message(message):
    member = bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status in ("administrator", "creator"):
        bot.unpin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,

        )
    else:
        bot.reply_to(message, "Only admins can unpin messages.")

premission = ChatPermissions(
    can_send_messages=False

)

'''@bot.message_handler(commands=['resctrict'])
def restrict_chat(message):
'''

@bot.message_handler(commands=['detcomm'])
def handle_commands(message):
    logger.info(msg=message.__dict__)
    bot.send_message(chat_id=message.chat.id, text="here is the details of each desire commands that you want to use : ", timeout=2)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler()
def channel_handler(message):
    return 1




bot.infinity_polling()


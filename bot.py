import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чата.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: "https://" in message.text or "http://" in message.text)
def ban_link(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ссылки запрещены! Но команда должна быть ответом на сообщение пользователя.")
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_status = bot.get_chat_member(chat_id, user_id).status

    if user_status in ['administrator', 'creator']:
        bot.reply_to(message, "Невозможно забанить администратора.")
    else:
        bot.ban_chat_member(chat_id, user_id)
        bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен за ссылку.")

@bot.message_handler(commands=['uprank'])
def uprank_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status

        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно повысить администратора.")
        else:
            bot.promote_chat_member(chat_id, user_id, can_change_info=True, can_post_messages=True, can_edit_messages=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был повышен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")

bot.infinity_polling(none_stop=True)

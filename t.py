import telebot
import json
import os
from datetime import datetime

# Инициализация бота
bot_token = '6910923926:AAFcgCawjsfhuxVzWetDBSCuau4nuIybFnU'
admin_id = 6578018656  # Ваш ID Telegram
channel_id = '@GameDevAssetsHub'  # ID канала, куда будет отправляться сообщение
bot = telebot.TeleBot(bot_token)

# Путь к файлу для хранения данных
data_file = 'bot_data.json'

# Загрузка данных из JSON файла
def load_data():
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as f:
        return json.load(f)

# Сохранение данных в JSON файл
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Загрузка данных при запуске
data = load_data()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    if user_id not in data:
        data[user_id] = {
            'balance': 0.0,
            'tasks': {
                'subscriptions': 0,
                'views': 0,
                'bots': 0,
                'groups': 0,
                'links': 0
            },
            'bonuses': 0,
            'joined': str(datetime.now().date())
        }
        save_data(data)
    
    bot.send_message(message.chat.id, "🚀 Добро пожаловать!", reply_markup=main_menu())

# Главное меню
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💵 Заработать', '📱 Мой кабинет')
    markup.row('👥 Партнёры', '📚 О боте')
    if str(admin_id) == str(admin_id):  # Добавляем кнопку только для админа
        markup.row('Отправить на начисление')
    return markup

# Обработка кнопки 'Отправить на начисление' (только для админа)
@bot.message_handler(func=lambda message: message.text == 'Отправить на начисление')
def send_payment_request(message):
    if message.chat.id == admin_id:
        markup = telebot.types.InlineKeyboardMarkup()
        # В callback_data передаем ID пользователя, чтобы потом его идентифицировать
        markup.add(telebot.types.InlineKeyboardButton("🔘 Начислить 0.01₽", callback_data=f"add_payment_{message.chat.id}"))
        bot.send_message(channel_id, "Для начисления нажмите на кнопку снизу:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой функции.")

# Обработка нажатия на инлайн-кнопку "Начислить 0.01₽"
@bot.callback_query_handler(func=lambda call: call.data.startswith("add_payment_"))
def add_payment_callback(call):
    # Извлекаем ID пользователя из callback_data
    user_id = call.data.split('_')[2]
    if user_id in data:
        data[user_id]['balance'] += 0.01
        save_data(data)
        bot.answer_callback_query(call.id, "Баланс пополнен на 0.01₽")
        bot.edit_message_text("✅ Баланс успешно пополнен на 0.01₽", chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Ошибка: пользователь не найден")

# Обработка кнопки '💵 Заработать'
@bot.message_handler(func=lambda message: message.text == '💵 Заработать')
def earn(message):
    bot.send_message(message.chat.id, "🚀 Как Вы хотите заработать?", reply_markup=main_menu())

# Обработка кнопки '📱 Мой кабинет'
@bot.message_handler(func=lambda message: message.text == '📱 Мой кабинет')
def my_cabinet(message):
    user_data = data.get(str(message.chat.id), {})
    bot.send_message(message.chat.id, f"📱 Ваш кабинет:\n\n"
                                      f"💳 Баланс: {user_data.get('balance', 0.0)}₽", reply_markup=main_menu())

# Запуск бота
bot.polling(none_stop=True)

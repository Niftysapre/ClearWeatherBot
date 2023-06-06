import telebot
import requests
import json

API = None
TOKEN = None

with open("token.txt") as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)

with open("API.txt") as f:
    API = f.read().strip()


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Напишите название города ')


@bot.message_handler(content_types=['text'])
def pogoda(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')

        image = ''
        if temp > 10.0:
            image = 'sunny.png'
        elif temp > 0.0:
            image = 'cloudy.png'
        elif temp < -1.0:
            image = 'snow.png'
        else:
            image = 'default.png'

        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else: bot.reply_to(message, f'Город указан неверно')



bot.polling(none_stop=True)
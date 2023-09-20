import telebot
import os
import time
import requests
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot('YOUR_TOKEN')
@bot.message_handler(commands=['start', 'go'])

def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Сохраняю страницы в пдф, ограничение 20 мб')
@bot.message_handler(content_types='text')
def handle_file3(message):
    chat_id = message.chat.id
    text = message.text
    try:
        bot.send_message(chat_id, 'Получаю заголовок')
        time.sleep(1)
        reqs = requests.get(text, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MAR-LX1H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.4103.106 Mobile Safari/537.36'})
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for title in soup.find_all('title'):
            a = (title.get_text())
        print(a)
    except:
        bot.send_message(chat_id, 'Получить заголовок не удалось')
    try:
        filename = time.strftime("%d-%m-%Y_%H-%M-%S")
        print(filename)
        bot.send_message(chat_id, 'Скачиваю в страницу')
        time.sleep(1)
        os.system(f'xvfb-run wkhtmltopdf {text} {filename}.pdf')
        bot.send_message(chat_id, 'конвертирую в PDF')
        time.sleep(2)
        bot.send_message(chat_id, 'Готовлю к отправки')
        bot.send_document(chat_id, data=open(f'{filename}.pdf', 'rb'))
        time.sleep(2)
        try:
            bot.send_message(chat_id, f'{a}')
        except:
            pass
        try:
            os.system(f'rm {filename}.pdf')
        except:
            bot.send_message(chat_id, 'ошибка удаления')
    except Exception as eee1:
        bot.send_message(chat_id, f'Ошибка{eee1}')
if __name__ == '__main__':
     bot.polling(none_stop=True)
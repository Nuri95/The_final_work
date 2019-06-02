import pprint
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ChatAction

import telegram
import requests


token = '899979051:AAFn4mmftZNrTRLWTEm-BoVd7FJcye2WTPo'


def answer(bot, update):

    # for attr, value in update.__dict__.items():
    #     if attr is not None and value is not None:
    #         print('  a=   ',attr, '     v=    ',value)
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    data={'id':user_id,
          'first_name':first_name,
          }

    add_bd = requests.post('http://127.0.0.1:8080/users',
                                data=data )
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    menu()


def menu():
    bot.send_chat_action(
        chat_id=update.message.chat_id,
        action=telegram.ChatAction.TYPING)  # Показать действие бота write пользователю
    time.sleep(1)
    custom_keyboard = [
        ['Subscriptions'],
        ['Keywords']
    ]  # Клавиатура из двух кнопок
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=10,
                                                one_time_keyboard=True)
    # one_time_keyboard-клавиатура исчезнет после выбора пользователя
    bot.send_message(
        chat_id=update.message.chat_id,
        text="What do you want to do?",
        reply_markup=reply_markup
    )


def subscriptions(bot, update):
    user_id = update.message.from_user.id

    get_user = requests.get('http://127.0.0.1:8080/subscriptions/categories', user_id)



def main():
    bot = telegram.Bot(token)
    print(bot.get_me())
    updater = Updater(token)

    dp = updater.dispatcher  # Этот класс отправляет все виды обновления в свои зарегистрированные обработчики

    dp.add_handler(MessageHandler(Filters.text, answer))
    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('subscriptions', subscriptions))
    updater.start_polling()  # Запускает опрос обновлений от Telegram.
    updater.idle()  # Программу обновления останаливает
    print('hello')


if __name__ == '__main__':
    main()
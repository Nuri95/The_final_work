import pprint
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ChatAction

import telegram
import requests


token = '899979051:AAFn4mmftZNrTRLWTEm-BoVd7FJcye2WTPo'



def registration(bot, update):

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
    update.message.reply_text(menu())


def menu(bot, update):
    print(123)
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
    return ACTION

def action(bot, update):
    if update.message.text == 'Categories':
        bot.send_message(chat_id=update.message.chat_id,
                         text=update.message.text)
    elif update.message.text == 'Keywords':
        bot.send_message(chat_id=update.message.chat_id,
                         text=update.message.text)
    return ANSWER


def answer_check(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='answer_check'
                     )
    return ANSWER


def cancel(bot, update):
    print('cancel')
    # user = update.message.from_user
    # logger.info("User %s canceled conversation",user.first_name)
    update.message.reply_text('This conversation is over')
    print('cancel_end')
    return ConversationHandler.END


def subscriptions(bot, update):
    print('1')
    user_id = update.message.from_user.id
    print('2')
    # get_user = requests.get('http://127.0.0.1:8080/subscriptions/categories', user_id)
    bot.send_message(chat_id=update.message.chat_id,
                    parse_mode='markdown',
                     text='[inline mention of a user](tg://user?id=899979051)'
                     )
                     # text='[okkk](https://vk.com)')


CATEGORIES_LIST, CATEGORIES_MOVE = range(2)
KEYWORDS_LIST, KEYWORDS_MOVE = range(2)
def categories(bot,update):
    user_id = str(update.message.from_user.id)
    try:
        a = requests.get('http://127.0.0.1:8080/categories').json()
        print(a)
        all_categories = 'All categories:\n'+ '\n'.join([str(v[0]) + ' ' + str(v[1]) for v in a])

        bot.send_message(chat_id=update.message.chat_id,
                         text=all_categories)
    except e:
        print(e)
    try:
        a = requests.get('http://127.0.0.1:8080/user/'+user_id+'/categories').json()

        if a:
            subscribed_categories = 'Your categories:\n'+ '\n'.join([str(v[0]) + ' ' + str(v[1]) for v in a])
        else:
            subscribed_categories = 'You are not subscribed to any category'
        bot.send_message(chat_id=update.message.chat_id,
                         text=subscribed_categories)
    except e:
        print(e)
    return CATEGORIES_MOVE
def move_category(bot,update):
    print('move_CATEGORT')
    text = update.message.text
    user_id= str(update.message.from_user.id)
    print('move_CATEGORT2')
    if -1 != text.find('add'):
        print('move_CATEGORT3')
        text = text[text.find('add')+3:].strip()
        print('user ' + user_id + ' add category ' +text)
        try:
            cat_id = int(text)
            requests.post('http://127.0.0.1:8080/user/'+user_id+'/categories/add',data={"id":cat_id})
        except e:
            print(e)
    elif -1 != text.find('remove'):
        print('move_CATEGORT4')
        text = text[text.find('remove')+6:].strip()
        try:
            print('move_CATEGORT5')
            cat_id = int(text)
            requests.post('http://127.0.0.1:8080/user/' + user_id+'/categories/remove', data={"id": cat_id})
        except e:
            print('move_CATEGORT6')
            print(e)
    elif (text == 'list'):
        print('move_CATEGORT7')
        categories(bot,update)

    print('move_CATEGORT8')
    #elif(text == 'cancel') :
    #    return cancel()
    return CATEGORIES_LIST


def keywords(bot,update):
    user_id = str(update.message.from_user.id)
    try:
        a = requests.get('http://127.0.0.1:8080/keywords').json()
        print(a)
        all_keywords = 'All keywords:\n'+ '\n'.join([str(v[0]) + ' ' + str(v[1]) for v in a])

        bot.send_message(chat_id=update.message.chat_id,
                         text=all_keywords)
    except e:
        print(e)
    try:
        a = requests.get('http://127.0.0.1:8080/user/'+user_id+'/keywords').json()

        if a:
            subscribed_keywords = 'Your keywords:\n'+ '\n'.join([str(v[0]) + ' ' + str(v[1]) for v in a])
        else:
            subscribed_keywords = 'You are not subscribed to any keywords'
        bot.send_message(chat_id=update.message.chat_id,
                         text=subscribed_keywords)
    except e:
        print(e)
    return KEYWORDS_MOVE


def move_keyword(bot,update):
    print('move_KEYWORD1')
    text = update.message.text
    user_id= str(update.message.from_user.id)
    print('move_KEYWORD2')
    if -1 != text.find('add'):
        print('move_KEYWORD3')
        text = text[text.find('add')+3:].strip()
        print('user ' + user_id + ' add keyword ' +text)
        try:
            cat_id = int(text)
            requests.post('http://127.0.0.1:8080/user/'+user_id+'/keywords/add',data={"id":cat_id})
        except e:
            print(e)
    elif -1 != text.find('remove'):
        print('move_KEYWORD4')
        text = text[text.find('remove')+6:].strip()
        try:
            print('move_KEYWORD5')
            cat_id = int(text)
            requests.post('http://127.0.0.1:8080/user/' + user_id+'/keywords/remove', data={"id": cat_id})
        except e:
            print('move_KEYWORD6')
            print(e)
    elif text == 'list':
        print('move_KEYWORD7')
        categories(bot,update)
    print('move_KEYWORD8')
    #elif(text == 'cancel') :
    #    return cancel()

    return KEYWORDS_LIST


#
# def news(bot, update):
#     params={
#             "pagesize": 5,
#             "page":1,
#             "category": "business",
#             "country": "us",
#             "keywor": "trump"
#         }
#     response = requests.get('http://127.0.0.1:8080/news', json=params)
#     update.message.reply_text('\n'.join(response.json()))

def news(bot, update):
    user_id = update.message.from_user.id
    response = requests.get('http://127.0.0.1:8080/user/'+user_id + '/news')
    update.message.reply_text('\n'.join(response.json()))
def main():
    bot = telegram.Bot(token)
    print(bot.get_me())
    updater = Updater(token)

    dp = updater.dispatcher  # Этот класс отправляет все виды обновления в свои зарегистрированные обработчики

    category_handler = ConversationHandler(
        entry_points=[CommandHandler('categories', categories)],
        states={
            CATEGORIES_MOVE: [MessageHandler(Filters.text, move_category)],
            CATEGORIES_LIST: [MessageHandler(Filters.text, categories)],

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    keyword_handler = ConversationHandler(
        entry_points=[CommandHandler('keywords', keywords)],
        states={
            KEYWORDS_MOVE: [MessageHandler(Filters.text, move_keyword)],
            KEYWORDS_LIST: [MessageHandler(Filters.text, keywords)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(CommandHandler('register', registration))
    dp.add_handler(category_handler)
    dp.add_handler(keyword_handler)
    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('news', news))
    dp.add_handler(CommandHandler('subscriptions', subscriptions))
    updater.start_polling()  # Запускает опрос обновлений от Telegram.
    updater.idle()  # Программу обновления останаливает
    print('hello')


if __name__ == '__main__':
    main()
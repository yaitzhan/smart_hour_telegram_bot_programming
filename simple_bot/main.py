"""
Простой echo бот.

Смартчас "Telegram Chat Bot Programming (advanced)"
"""

import logging

from aiogram import Bot, Dispatcher, executor, types


# скопируйте токен полученный от @BotFather
BOT_TOKEN = ''

# логгирование
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

USER_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True)
USER_MENU.add(types.KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
USER_MENU.add(types.KeyboardButton('Отправить свою локацию 🗺️', request_location=True))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Оператор, отслеживающий событие: пользователь ввел `/start`
    """
    kbd = types.ReplyKeyboardRemove()  # убрать текущие кнопки
    text = "Я простой бот!"  # можно поменять текст
    await message.reply(text, reply_markup=USER_MENU)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    Оператор, отслеживающий событие: пользователь ввел `/help`
    """
    text = "Спешу на помощь!"  # можно поменять текст
    await message.reply(text)


@dp.message_handler(regexp='кот')
async def cats(message: types.Message):
    # открывает файл, который находится в папке data
    with open('data/cat.jpg', 'rb') as photo:
        """
        Напишите боту "кот" и посмотрите что получится
        """
        await message.reply_photo(photo, caption='Not bad 😺')


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def content_contact_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы отправили контактные данные')


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def content_contact_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы отправили гео-локацию')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def content_contact_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы отправили фото')


@dp.message_handler(regexp='стикер')
async def content_contact_handler(message: types.Message):
    await bot.send_sticker(message.chat.id, '')


@dp.message_handler()
async def echo(message: types.Message):
    """
    Простой оператор, который отправляет введенный раннее юзером текст
    """
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

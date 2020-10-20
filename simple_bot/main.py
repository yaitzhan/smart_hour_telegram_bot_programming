"""
Обзор библиотеки aiogram.

https://github.com/aiogram/aiogram

- 100% асихронность
- встроенные FSM
- middleware
- логирование
- регулярные апдейты

Смартчас "Telegram Chat Bot Programming (advanced)"
"""

import logging

from aiogram import Bot, Dispatcher, executor, types


# скопируйте токен полученный от @BotFather
BOT_TOKEN = ''


# регулярное выражение для email-адресов (https://emailregex.com/)
EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

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
    kbd = types.ReplyKeyboardRemove()  # убрать текущие кнопки
    text = "Я простой бот!"  # можно поменять текст
    await message.reply(text, reply_markup=kbd)


@dp.message_handler(commands=['menu'])
async def send_welcome(message: types.Message):
    text = "Простое меню"
    await message.reply(text, reply_markup=USER_MENU)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    text = "Спешу на помощь!"
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
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, 'Вы отправили гео-локацию')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def content_contact_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы отправили фото')


@dp.message_handler(regexp='стикер')
async def content_contact_handler(message: types.Message):
    await bot.send_sticker(message.chat.id, 'https://raw.githubusercontent.com/yaitzhan/smart_hour_telegram_bot_programming/main/simple_bot/data/sample_sticker.webp?token=AHFRIIVDL3GFDVM5WPWD6F27R2FVW')


@dp.message_handler(regexp=EMAIL_REGEX)
async def email_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы отправили валидный email-адрес')


@dp.message_handler()
async def echo(message: types.Message):
    """
    Простой оператор, который отправляет введенный раннее юзером текст
    """
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

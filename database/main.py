"""
Работа с БД.

Смартчас "Знакомство с Python"

Смартчас "Telegram Chat Bot Programming (advanced)"
"""
import logging
import asyncio

from database.models import TelegramUser

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tortoise import Tortoise

# скопируйте токен полученный от @BotFather
BOT_TOKEN = ''

# логгирование
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def init_db():
    # Here we create a SQLite DB using file "database.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite',
        modules={'models': ['database.models']}
    )

    await Tortoise.generate_schemas()


loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())


async def on_shutdown():
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()


USER_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True)
USER_MENU.add(types.KeyboardButton('Отправить свой контакт ☎️', request_contact=True))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = "Работа с БД"
    await message.reply(text, reply_markup=USER_MENU)


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def save_number(message: types.Message):
    user = await TelegramUser.filter(user_id__contains=message.contact.user_id)
    if user:
        await bot.send_message(message.chat.id, 'Введенный номер уже существует')
    else:
        new_user = TelegramUser(
            user_id=message.contact.user_id,
            first_name=message.contact.first_name,
            last_name=message.contact.last_name,
            phone_number=message.contact.phone_number,
        )
        await new_user.save()
        await bot.send_message(message.chat.id, 'Номер записан')


@dp.message_handler(commands=['search'])
async def show_users_command(message: types.Message):

    await bot.send_message(message.chat.id, 'Введите имя')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)

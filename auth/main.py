"""
Пример авторизации.

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

# пароль, который будет прислан по смс
GENERATED_PASSWORD = 'qwerty'

# состояния
AWAIT_CONTACT = 'send contact'
AWAIT_PASSWORD = 'send password'

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

AUTHORIZED_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True)
AUTHORIZED_MENU.add(types.KeyboardButton('Секретная кнопка'))


async def check_if_user_exist(user_id):
    user = await TelegramUser.get_or_none(user_id__contains=user_id, authorized=True)
    return user


async def check_if_authorized(user_id):
    user = await TelegramUser.filter(user_id__contains=user_id, authorized=True)
    if user:
        return True
    else:
        return False


async def check_if_unauthorized(user_id):
    return not check_if_authorized(user_id)


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(AWAIT_CONTACT)
    text = "Пример авторизации"
    await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove)


@dp.message_handler(state=AWAIT_CONTACT, content_types=types.ContentTypes.CONTACT)
async def check_user_existence(message: types.Message):
    user_object = await check_if_user_exist(message.from_user.id)
    if user_object is not None:
        state = dp.current_state(chat=message.chat.id, user=message.chat.id)
        await state.set_state(AWAIT_PASSWORD)
        await bot.send_message(message.chat.id, 'Введите пароль, присланный по смс')
    else:
        await bot.send_message(message.chat.id, 'Пользователь с таким номером не найден')


@dp.message_handler(state=AWAIT_PASSWORD, content_types=types.ContentTypes.CONTACT)
async def check_user_password(message: types.Message):
    if message.text == GENERATED_PASSWORD:
        user_object = await check_if_user_exist(message.from_user.id)
        user_object.authorized = True
        await user_object.save()
        await bot.send_message(message.chat.id, 'Тссс! Показываю скрытое меню', reply_markup=AUTHORIZED_MENU)
    else:
        await bot.send_message(message.chat.id, 'Неправильный пароль')


@dp.message_handler(commands=['menu'])
async def show_menu_authorized(message: types.Message):
    await bot.send_message(message.chat.id, 'Тссс! Показываю скрытое меню', reply_markup=AUTHORIZED_MENU)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

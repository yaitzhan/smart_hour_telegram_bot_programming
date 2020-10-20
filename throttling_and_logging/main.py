"""
Пример троттлинга ("антифлуд").

Смартчас "Telegram Chat Bot Programming (advanced)"
"""

import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import Throttled

# скопируйте токен полученный от @BotFather
BOT_TOKEN = ''

# логгирование
logging.basicConfig(level=logging.DEBUG)

storage = MemoryStorage()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_shutdown():
    await dp.storage.close()
    await dp.storage.wait_closed()


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    # rate limit можно подкрутить
    # def __init__(self, limit=1.5, key_prefix='antiflood_'):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! ')

        # Sleep.
        await asyncio.sleep(delta)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Оператор, отслеживающий событие: пользователь ввел `/start`
    """
    text = "Пример антифлуда"  # можно поменять текст
    keyboard_markup = types.ReplyKeyboardMarkup()

    keyboard_markup.add(types.KeyboardButton('flood'))

    await message.reply(text, reply_markup=keyboard_markup)


@dp.message_handler()
async def echo(message: types.Message):
    """
    Простой оператор, который отправляет введенный раннее юзером текст
    """
    await message.answer(message.text)


if __name__ == '__main__':
    # Setup middleware
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(LoggingMiddleware())

    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)

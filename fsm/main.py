"""
Finite State Machine (Конечный автомат).

https://ru.wikipedia.org/wiki/Конечный_автомат

Смартчас "Telegram Chat Bot Programming (advanced)"
"""
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

# скопируйте токен полученный от @BotFather
BOT_TOKEN = ''

storage = MemoryStorage()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

# список состояний
# доп. пример смотрите также https://github.com/aiogram/aiogram/blob/1e2fe72aca12a3fc6f2d1f66c71539af5a84ea00/examples/finite_state_machine_example.py
CHOOSE_MENU = 'choose_menu'
CHOSEN_INLINE_MENU = 'chosen_inline_menu'
CHOSEN_REPLY_MENU = 'chosen_reply_menu'


# основное меню
MAIN_MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
MAIN_MENU_KEYBOARD.add(types.KeyboardButton('Обычные кнопки'))
MAIN_MENU_KEYBOARD.add(types.KeyboardButton('Инлайн кнопки'))


REPLY_KEYBOARD_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
REPLY_KEYBOARD_MENU.add(types.KeyboardButton('1'))
REPLY_KEYBOARD_MENU.add(types.KeyboardButton('2'))
REPLY_KEYBOARD_MENU.add(types.KeyboardButton('3'))


INLINE_KEYBOARD_MENU = types.InlineKeyboardMarkup()
INLINE_KEYBOARD_MENU.add(types.InlineKeyboardButton('Первая кнопка!', callback_data='button1'))
INLINE_KEYBOARD_MENU.add(types.InlineKeyboardButton('Вторая кнопка!', callback_data='button2'))
INLINE_KEYBOARD_MENU.add(types.InlineKeyboardButton('Третья кнопка!', callback_data='button3'))


CANCEL_MENU = types.ReplyKeyboardMarkup()
CANCEL_MENU.add(types.KeyboardButton('Отмена'))


def on_shutdown():
    await dp.storage.close()
    await dp.storage.wait_closed()


@dp.message_handler(state='*', commands=['start'])
@dp.message_handler(state='*', regexp=r'^Отмена$')
async def send_menus(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(CHOOSE_MENU)
    current_state = await state.get_state()
    text = "Пример конечного автомата, веберите меню (состояние: {})".format(current_state)
    await message.reply(text, reply_markup=MAIN_MENU_KEYBOARD)


@dp.message_handler(state=CHOOSE_MENU, regexp=r'^Обычные кнопки$')
async def reply_keyboard_menu_handler(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(CHOSEN_REPLY_MENU)
    current_state = await state.get_state()
    text = 'Вы выбрали меню: "{}" (состояние {})'.format(message.text, current_state)
    await bot.send_message(message.chat.id, text, reply_markup=REPLY_KEYBOARD_MENU)


@dp.message_handler(state=CHOOSE_MENU, regexp=r'^Инлайн кнопки$')
async def inline_keyboard_menu_handler(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    await state.set_state(CHOSEN_INLINE_MENU)
    current_state = await state.get_state()
    text = 'Вы выбрали меню: "{}" (состояние: {})'.format(message.text, current_state)
    await bot.send_message(message.chat.id, text, reply_markup=INLINE_KEYBOARD_MENU)


@dp.message_handler(state=CHOSEN_REPLY_MENU)
async def reply_messages_handler(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    current_state = await state.get_state()
    await bot.send_message(message.chat.id, "Нажата кнопка: {} (состояние: {})".format(message.text, current_state))


@dp.callback_query_handler(lambda c: c.data == 'button1', state=CHOSEN_INLINE_MENU)
async def inline_callback_button_1(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback.from_user.id)
    await state.set_state(CHOSEN_INLINE_MENU)
    current_state = await state.get_state()
    await bot.send_message(callback.from_user.id, "Нажата кнопка: 1 (состояние: {})".format(current_state))


@dp.callback_query_handler(lambda c: c.data == 'button2', state=CHOSEN_INLINE_MENU)
async def inline_callback_button_2(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback.from_user.id)
    await state.set_state(CHOSEN_INLINE_MENU)
    current_state = await state.get_state()
    await bot.send_message(callback.from_user.id, "Нажата кнопка: 2 (состояние: {})".format(current_state))


@dp.callback_query_handler(lambda c: c.data == 'button3', state=CHOSEN_INLINE_MENU)
async def inline_callback_button_3(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback.from_user.id)
    await state.set_state(CHOSEN_INLINE_MENU)
    current_state = await state.get_state()
    await bot.send_message(callback.from_user.id, "Нажата кнопка: 3 (состояние: {})".format(current_state))


@dp.message_handler(state='*')
async def unknown_message_handler(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.chat.id)
    current_state = await state.get_state()
    await bot.send_message(message.from_user.id, "Не понял Ваше сообщение (состояние: {})".format(current_state))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)

import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor

API_TOKEN = '7208646524:AAHVOvd0QLI3rvcks8W_szRTh0mKwP2wiGs'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def save_user_data(user_data):
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Пожалуйста, зарегистрируйтесь.")

@dp.message_handler(lambda message: message.text.startswith('/register'))
async def register_user(message: types.Message):
    user_data = {}
    save_user_data(user_data)
    await message.answer("Регистрация прошла успешно!")

@dp.message_handler(lambda message: message.text.startswith('/menu'))
async def show_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Актуальные мероприятия"))
    keyboard.add(types.KeyboardButton(text="Предыдущие эфиры"))
    keyboard.add(types.KeyboardButton(text="Забрать подарки"))
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Актуальные мероприятия")
async def show_events(message: types.Message):
    await message.answer("Актуальные мероприятия")

@dp.message_handler(lambda message: message.text == "Предыдущие эфиры")
async def show_previous_broadcasts(message: types.Message):
    await message.answer("Предыдущие эфиры")

@dp.message_handler(lambda message: message.text == "Забрать подарки")
async def claim_gifts(message: types.Message):
    await message.answer("Забрать подарки")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

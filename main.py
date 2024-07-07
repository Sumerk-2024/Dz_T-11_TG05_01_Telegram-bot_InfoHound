import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import logging
import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена для доступа к боту из переменных окружения
API_TOKEN = os.getenv('API_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройка логирования для вывода информации об ошибках и других событий
logging.basicConfig(level=logging.INFO)


# Декоратор для обработки ошибок в командах
def error_handler(func):
    async def wrapper(message: Message):
        try:
            await func(message)
        except Exception as e:
            logging.error(e)
            await message.answer(f'Произошла ошибка: {str(e)}')
    return wrapper


# Функция для перевода текста с помощью GoogleTranslator на русский язык
def translate_to_russian(text):
    return GoogleTranslator(source='auto', target='ru').translate(text)


# Функция для получения случайной шутки и перевода на русский язык
async def get_random_joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    response.raise_for_status()
    joke = response.json()
    joke_setup = translate_to_russian(joke["setup"])
    joke_punchline = translate_to_russian(joke["punchline"])
    return f'{joke_setup} - {joke_punchline}'


# Функция для получения случайной цитаты и перевода на русский язык
async def get_random_quote():
    response = requests.get('https://api.quotable.io/random')
    response.raise_for_status()
    quote = response.json()
    quote_text = translate_to_russian(quote["content"])
    quote_author = translate_to_russian(quote["author"])
    return f'{quote_text} - {quote_author}'


# Функция для получения случайного факта и перевода на русский язык
async def get_random_fact():
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    response.raise_for_status()
    fact = response.json()
    fact_text = translate_to_russian(fact['text'])
    return fact_text


# Функция для получения случайного изображения кота
async def get_random_cat_image():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    response.raise_for_status()
    return response.json()[0]['url']


# Обработчик команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я бот, который может использовать различные API.')


# Обработчик команды /help
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n/start \n/help \n/joke \n/quote \n/fact \n/cat')


# Обработчик команды /joke для получения случайной шутки
@dp.message(Command('joke'))
@error_handler
async def joke_command(message: Message):
    joke = await get_random_joke()
    await message.answer(joke)


# Обработчик команды /quote для получения случайной цитаты
@dp.message(Command('quote'))
@error_handler
async def quote_command(message: Message):
    quote = await get_random_quote()
    await message.answer(quote)


# Обработчик команды /fact для получения случайного факта
@dp.message(Command('fact'))
@error_handler
async def fact_command(message: Message):
    fact = await get_random_fact()
    await message.answer(f'Вот случайный факт: {fact}')


# Обработчик команды /cat для получения случайного изображения кота
@dp.message(Command('cat'))
@error_handler
async def cat_command(message: Message):
    cat_image_url = await get_random_cat_image()
    await message.answer_photo(cat_image_url)


# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Точка входа в программу
if __name__ == '__main__':
    asyncio.run(main())

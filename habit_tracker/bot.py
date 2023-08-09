from aiogram import Bot, Dispatcher, executor
from config.settings import TELEGRAM_BOT_API

bot = Bot(token=TELEGRAM_BOT_API)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(msg):
    """Вывод ответа бота для команды /start"""
    await msg.answer("Привет, я бот - трекер привычек! Давай вырабатывать хорошие привычки вместе")


@dp.message_handler()
async def any_message(msg):
    """Вывод ответа для любого другого запроса"""
    await msg.answer("Если ты зарегистрировался в приложении, скоро появится расписание твоих привычек!")


executor.start_polling(dp)

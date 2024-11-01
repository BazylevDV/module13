from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio

API_TOKEN = ' '
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет, я здесь чтобы помочь Вам!")

@dp.message()
async def all_messages(message: types.Message):
    await message.answer('Ваша заявка принята, наши менеджеры работают над ней!')
    print('Мы получили сообщение')

async def main():
    bot_info = await bot.get_me()  # Получаем информацию о боте
    print(f"Бот {bot_info.username} запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




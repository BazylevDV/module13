from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

API_TOKEN = ''

# Создаем класс состояний
class UserState(StatesGroup):
    start = State()
    age = State()
    growth = State()
    weight = State()

# Создаем клавиатуру с кнопками "Расчитать" и "Информация"
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Расчитать"), KeyboardButton(text="Информация")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Основная часть программы
if __name__ == '__main__':
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Функция для начала общения
    @dp.message(Command("start"))
    async def start(message: types.Message, state: FSMContext):
        await message.answer("Дорогие женщины, ваш слуга - бот посчитает для Вас сейчас оптимальное количество калорий по формуле  Миффлина - Сан Жеора, процедура займет 5 секунд. Далее нажмите кнопку 'Расчитать' чтобы начать подсчет калорий или 'Информация' для получения дополнительной информации.", reply_markup=start_keyboard)
        await state.set_state(UserState.start)

    # Функция для обработки нажатия на кнопку "Начать"
    @dp.message(F.text == "Расчитать", StateFilter(UserState.start))
    async def ask_age(message: types.Message, state: FSMContext):
        await message.answer("Введите свой возраст:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserState.age)

    # Функция для обработки нажатия на кнопку "Информация"
    @dp.message(F.text == "Информация", StateFilter(UserState.start))
    async def show_info(message: types.Message):
        info_text = (
            "Формула Миффлина - Сан Жеора — это одна из наиболее точных формул для расчета суточной нормы калорий. "
            "Она учитывает ваш возраст, рост, вес и пол. "
            "Эта формула была разработана в 1990 году и с тех пор широко используется в диетологии."
        )
        await message.answer(info_text)

    # Функция для установки возраста
    @dp.message(StateFilter(UserState.age))
    async def set_age(message: types.Message, state: FSMContext):
        await state.update_data(age=int(message.text))
        await message.answer("Введите свой рост в сантиметрах:")
        await state.set_state(UserState.growth)

    # Функция для установки роста
    @dp.message(StateFilter(UserState.growth))
    async def set_growth(message: types.Message, state: FSMContext):
        await state.update_data(growth=int(message.text))
        await message.answer("Введите свой вес в килограммах:")
        await state.set_state(UserState.weight)

    # Функция для установки веса
    @dp.message(StateFilter(UserState.weight))
    async def set_weight(message: types.Message, state: FSMContext):
        await state.update_data(weight=int(message.text))
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        # Формула Миффлина - Сан Жеора для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

        # Норма калорий для похудения (уменьшение на 20%)
        calories_for_weight_loss = calories * 0.8

        # Норма калорий для сохранения веса
        calories_for_weight_maintenance = calories

        await message.answer(f"Ваша норма калорий для похудения: {calories_for_weight_loss:.2f} ккал в день.")
        await message.answer(f"Ваша норма калорий для сохранения веса: {calories_for_weight_maintenance:.2f} ккал в день.")
        await state.clear()

    # Запуск бота
    async def main():
        try:
            bot_info = await bot.get_me()  # Получаем информацию о боте
            print(f"Бот {bot_info.username} запущен и готов к работе!")
            await dp.start_polling(bot)
        finally:
            await dp.storage.close()
            await bot.session.close()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
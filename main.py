import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logging import basicConfig, getLogger, INFO
from keyboard import level_keyboard, stop_keyboard

basicConfig(level=INFO)
log = getLogger()

storage = MemoryStorage()

BOT_TOKEN = "7021103475:AAEdeDmISk1idZKo4gYBabNyqu2tLBQhz0U"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class LevelState(StatesGroup):
    question = State()
    answer = State()


@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    await message.answer("Botga xush kelibsiz, bu bot bilan siz oz bilimlaringizni charxlashingiz mumkin",
                         reply_markup=level_keyboard())
    await LevelState.question.set()


@dp.message_handler(state=LevelState.question)
async def handle_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Level 1️⃣":
            question = f"{random.randint(1, 11)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
            await message.answer(question, reply_markup=stop_keyboard())
        elif message.text == "Level 2️⃣":
            question = f"{random.randint(1, 18)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())
        elif message.text == "Level 3️⃣":
            question = f"{random.randint(1, 18)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 18)}"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())
        elif message.text == "Level 4️⃣":
            question = f"{random.randint(1, 40)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 40)}"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())

        data['computer_answer'] = eval(question)

        data['computer_answer'] = eval(question)
        data['level'] = message.text
        data['true'] = 0
        data['false'] = 0

    await LevelState.next()


@dp.message_handler(Text(equals="🛑 stop"), state=LevelState.answer)
async def handle_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(f"Savollar: {data['true'] + data['false']} ta\n"
                             f"To'g'ri javoblar: {data['true']}\n"
                             f"Noto'g'ri javoblar: {data['false']}",
                             reply_markup=level_keyboard())
        await state.finish()


@dp.message_handler(state=LevelState.answer)
async def handle_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if int(message.text) == int(data["computer_answer"]):
            await message.answer("✅")
            data['true'] += 1
        else:
            data['false'] += 1
            await message.answer("❌")

        if data['level'] == "Level 1️⃣":
            question = f"{random.randint(1, 11)} {random.choice(['+', '-', '*'])} {random.randint(1, 11)}"
            await message.answer(question)
        elif data['level'] == "Level 2️⃣":
            question = f"{random.randint(1, 99)} {random.choice(['+', '-', '*'])} {random.randint(1, 99)}"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())
        elif data['level'] == "Level 3️⃣":
            question = f"{random.randint(40, 201)} {random.choice(['+', '-', '*', '/'])} {random.randint(40, 201)}"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())
        elif data['level'] == "Level 4️⃣":
            question = f"({random.randint(1, 99)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 99)}) {random.choice(['+', '-', '*'])} ({random.randint(1, 99)} {random.choice(['+', '-', '*'])} {random.randint(1, 99)})"
            await message.answer(f"{question} = ?", reply_markup=stop_keyboard())

        data['computer_answer'] = eval(question)

    await LevelState.answer.set()


if __name__ == '__main__':
    executor.start_polling(dp)

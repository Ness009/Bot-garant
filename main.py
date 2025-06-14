import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8128924301"))

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

class AppealStates(StatesGroup):
    waiting_for_text = State()

class ComplaintStates(StatesGroup):
    waiting_for_text = State()

class GiftStates(StatesGroup):
    waiting_for_text = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Подать апелляцию", callback_data="appeal")],
        [InlineKeyboardButton(text="⚠️ Отправить жалобу", callback_data="complaint")],
        [InlineKeyboardButton(text="🎁 Отправить подарок", callback_data="gift")]
    ])
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "appeal")
async def handle_appeal(callback_query: types.CallbackQuery):
    await AppealStates.waiting_for_text.set()
    await bot.send_message(callback_query.from_user.id, "✍️ Напишите текст апелляции.")

@dp.message_handler(state=AppealStates.waiting_for_text)
async def receive_appeal(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 <b>Новая апелляция</b> от @{message.from_user.username or message.from_user.id}:

{message.text}")
    await message.answer("✅ Ваша апелляция отправлена администратору.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "complaint")
async def handle_complaint(callback_query: types.CallbackQuery):
    await ComplaintStates.waiting_for_text.set()
    await bot.send_message(callback_query.from_user.id, "✍️ Напишите текст жалобы.")

@dp.message_handler(state=ComplaintStates.waiting_for_text)
async def receive_complaint(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"⚠️ <b>Новая жалоба</b> от @{message.from_user.username or message.from_user.id}:

{message.text}")
    await message.answer("✅ Ваша жалоба отправлена администратору.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "gift")
async def handle_gift(callback_query: types.CallbackQuery):
    await GiftStates.waiting_for_text.set()
    await bot.send_message(callback_query.from_user.id, "🎁 Напишите, что вы хотите отправить в подарок.")

@dp.message_handler(state=GiftStates.waiting_for_text)
async def receive_gift(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"🎁 <b>Подарок</b> от @{message.from_user.username or message.from_user.id}:

{message.text}")
    await message.answer("✅ Ваш подарок отправлен!")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

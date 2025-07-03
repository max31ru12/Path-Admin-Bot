import asyncio
from datetime import datetime

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.config import TOKEN
from app.database.db_config import session_factory
from app.database.models import Meeting
from app.keyboards import base_keyboard, KeyboardMessages, cancel_keyboard

dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(Command("start"))
async def handle_start(message: Message, command: Command):
    await message.answer("Выберите действие...", reply_markup=base_keyboard)


@dp.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def welcome_user(message: Message):
    for user in message.new_chat_members:
        greeting = (
            f"<a href='tg://user?id={user.id}'>{user.full_name}</a>, добро пожаловать в наш чат русскоговорящих патологов США.\n\n"
            "Пожалуйста, ознакомьтесь с правилами чата в закреплённом сообщении. Пожалуйста, представьтесь в одном сообщении\n"
            "с тегом #знакомство, указав ваше имя, где вы находитесь и кратко вашу роль (резидент, феллоу, аттендинг и т.д.).\n"
            "Спасибо, что присоединились к нам — рады сотрудничеству и общению!"
        )

        await message.answer(greeting, parse_mode="HTML")


class AddMeetingState(StatesGroup):
    waiting_for_date = State()
    waiting_for_link = State()


@dp.message(F.text == KeyboardMessages.ORGANIZE_MEETING)
async def handle_start_meeting_organization(message: Message, state: FSMContext):
    await state.set_state(AddMeetingState.waiting_for_date)
    await message.answer(
        text="Введите дату встречи в формате YYYY-MM-DD hh:mm (год-месяц-день час:минута)",
        reply_markup=cancel_keyboard
    )


@dp.message(AddMeetingState.waiting_for_date)
async def process_adding_date(message: Message, state: FSMContext):
    if message.text == KeyboardMessages.CANCEL_ADDING:
        await state.clear()
        await message.answer("Планирование встречи отменено", reply_markup=base_keyboard)
        return

    user_input_date = message.text.strip()
    try:
        dt = datetime.strptime(user_input_date, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("❌ Неверный формат даты. Используй: YYYY-MM-DD HH MM\nПример: 2025-07-04 18:30")
        return

    await state.update_data(date=dt)
    await state.set_state(AddMeetingState.waiting_for_link)
    await message.answer("Введи ссылку для встречи", reply_markup=cancel_keyboard)


@dp.message(AddMeetingState.waiting_for_link)
async def process_adding_link(message: Message, state: FSMContext):
    if message.text == KeyboardMessages.CANCEL_ADDING:
        await state.clear()
        await message.answer("Планирование встречи отменено", reply_markup=base_keyboard)
        return

    state_data = await state.get_data()
    input_user_link = message.text.strip()

    async with session_factory() as session:
        meeting = Meeting(date=state_data["date"], link=input_user_link)
        session.add(meeting)
        await session.commit()

    answer = (
        f"Добавлена встреча\n\n"
        f"Время: <b>{state_data['date']}\n</b>"
        f"Сcылка: <a href='{input_user_link}'>{input_user_link}</a>"
    )

    await message.answer(text=answer, reply_markup=base_keyboard, parse_mode="HTML")


@dp.message(F.text == "healthcheck")
async def check_health(message: Message) -> None:
    await message.answer("Healthy")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

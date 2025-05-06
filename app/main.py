import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ContentType
from aiogram.types import Message

from app.config import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN)


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


@dp.message(F.text == "healthcheck")
async def check_health(message: Message) -> None:
    await message.answer("Healthy")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

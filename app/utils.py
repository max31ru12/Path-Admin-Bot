import asyncio
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot
from sqlalchemy import select

from app.config import TZ_INFO, CHAT_ID
from app.database.db_config import session_factory
from app.database.models import Meeting


def get_answer(m: Meeting):
    return (
        f"Напоминание о запланированной встрече\n\n"
        f"Время: <b>{m.date.astimezone(ZoneInfo(TZ_INFO)).strftime('%Y-%m-%d %H:%M')} (America/New_York)\n</b>"
        f"Сcылка: <a href='{m.link}'>{m.link}</a>"
    )


async def reminder_loop(bot: Bot):

    while True:

        now = datetime.now(timezone.utc)

        async with session_factory() as session:
            meetings: list[Meeting] = (await session.execute(select(Meeting))).scalars().all()

            for m in meetings:
                delta = m.date - now
                if not m.notified_one_day and timedelta(days=0) < delta <= timedelta(days=1):
                    await bot.send_message(chat_id=CHAT_ID, text=get_answer(m), parse_mode="HTML")
                    m.notified_one_day = True

                if not m.notified_two_hours and timedelta(hours=0) < delta <= timedelta(hours=2):
                    await bot.send_message(chat_id=CHAT_ID, text=get_answer(m), parse_mode="HTML")
                    m.notified_two_hours = True

            await session.commit()

        await asyncio.sleep(60)

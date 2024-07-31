import aioschedule
from telebot import types
from datetime import datetime, timedelta, timezone

from database.dal import EmployeeDAL, PauseDAL, ReportDAL
from bot import bot
from middleware import MessageContext
from config import settings


async def pause_manager():
    employees = await EmployeeDAL.get_all()

    for employee in employees:
        active_report = await ReportDAL.get_active(employee.id)

        if active_report:
            pause = await PauseDAL.get_active(active_report.id)
            now = datetime.now(timezone.utc) + timedelta(hours=3)

            before_delta = settings.BREAK - settings.BEFORE_BREAK_FINISH
            if pause and timedelta(minutes=before_delta) < now - pause.start.replace(
                tzinfo=None
            ) < timedelta(minutes=before_delta + settings.SCHEDULER_DELAY):
                msg = await bot.send_message(
                    employee.chat_id,
                    text=f"До окончания перерыва остается минут: {settings.BEFORE_BREAK_FINISH}",
                )
                await MessageContext.update(employee.chat_id, [msg.id])

            if pause and timedelta(hours=1) < now - pause.start.replace(
                tzinfo=None
            ) < timedelta(hours=1, minutes=settings.SCHEDULER_DELAY):
                await PauseDAL.update(pause.id, now)
                await MessageContext.clear(employee.chat_id)

                mp = types.InlineKeyboardMarkup(row_width=1)
                finish = types.InlineKeyboardButton(
                    text="Завершить смену", callback_data="facility_shift_finish"
                )
                pause = types.InlineKeyboardButton(
                    text="Начать перерыв", callback_data="pause_start"
                )
                mp.add(finish, pause)
                msg = await bot.send_message(
                    employee.chat_id,
                    text=f"""Время начала смены: {
                        active_report.shift_start.strftime('%d.%m.%Y, %H:%M:%S')
                    }""",
                    reply_markup=mp,
                )
                await MessageContext.update(employee.chat_id, [msg.id])


if __name__ == "__main__":
    import asyncio
    import logging

    async def main():
        logging.basicConfig(level=logging.INFO)
        logging.info("Starting scheduler...")
        aioschedule.every(settings.SCHEDULER_DELAY).minutes.do(pause_manager)

        while True:
            now = datetime.now(timezone.utc) + timedelta(hours=3)
            logging.info(f"Scheduler has been envoked at {now.strftime('%H:%M:%S')}")

            await aioschedule.run_pending()
            await asyncio.sleep(5)

    asyncio.run(main())

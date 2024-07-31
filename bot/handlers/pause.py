from telebot import types
from datetime import datetime, timedelta, timezone

from bot import bot
from bot.handlers.decorators import is_active_pause
from middleware.message_context import MessageContext
from database.dal import EmployeeDAL, PauseDAL, ReportDAL
from config import settings


async def pause_menu(message: types.Message):
    await MessageContext.clear(message.chat.id)

    now = datetime.now(timezone.utc) + timedelta(hours=3)
    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    report = await ReportDAL.get_active(employee.id)
    pause = await PauseDAL.get_active(report.id)

    if not pause:
        await PauseDAL.create(now, report.id)
        pause = await PauseDAL.get_active(report.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    finish = types.InlineKeyboardButton(
        text="Закончить перерыв", callback_data="pause_finish"
    )

    mp.add(finish)

    msg = await bot.send_message(
        message.chat.id,
        text=f"Время начала перерыва: {pause.start.strftime('%d.%m.%Y, %H:%M:%S')}.\n\n"
        f"❗️Перерыв длиться всего минут: {settings.BREAK}.\n"
        f"Если вы не закончите его самостоятельно, то это область "
        f"закроется автоматиечески и вас переведет на меню смены.",
        reply_markup=mp,
    )

    await MessageContext.update(message.chat.id, [msg.id])


@is_active_pause
async def pause_finish(message: types.Message):
    await MessageContext.clear(message.chat.id)

    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    report = await ReportDAL.get_active(employee.id)
    pause = await PauseDAL.get_active(report.id)
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    await PauseDAL.update(pause.id, now)

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(
        text="🔙 Вернуться в меню смены", callback_data="back_to_facility_shift_menu"
    )
    mp.add(back)

    msg = await bot.send_message(
        message.chat.id, text="Вы успешно завершили перерыв", reply_markup=mp
    )

    await MessageContext.update(message.chat.id, [msg.id])

from math import ceil
from telebot import types
from datetime import datetime, timezone, timedelta

from bot import bot
from bot.markups import InlineMarkup
from bot.handlers.decorators import (
    active_shift_handler,
    active_pause_handler,
)
from bot.middlewares import context_manager
from middleware.message_context import MessageContext
from database.dal import EmployeeDAL, FacilityDAL, ReportDAL

OBJ_PER_PAGE = 5


@active_shift_handler
async def facility_menu(message, page: int):
    await MessageContext.clear(message.chat.id)
    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    facilities = await FacilityDAL.get_all_by_employee_id(employee.id)
    active_facilities = [
        facility for facility in facilities if facility.active is True
    ]
    if not active_facilities:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text="🍃 Вам еще не назначили объекты",
            reply_markup=InlineMarkup.back_to_menu(),
        )
        await MessageContext.update(message.chat.id, [msg.id])
    else:

        amount_of_pages = ceil(len(active_facilities) / OBJ_PER_PAGE)
        chunks = [
            active_facilities[i : i + OBJ_PER_PAGE]
            for i in range(0, len(active_facilities), OBJ_PER_PAGE)
        ]
        data_to_display = chunks[page - 1]

        keyboard = InlineMarkup.facility_slider(
            data_to_display, page, amount_of_pages, OBJ_PER_PAGE
        )

        msg = await bot.send_message(
            chat_id=message.chat.id, text="Выберите объект:", reply_markup=keyboard
        )
        await MessageContext.update(message.chat.id, [msg.id])


@active_shift_handler
async def facility_menu_selection_verification(
    message: types.Message, facility_id: int
):
    await MessageContext.clear(message.chat.id)
    context_manager.set_facility_id(message.chat.id, facility_id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    verify = types.InlineKeyboardButton(
        text="✔️ Потверждаю", callback_data="facility_shift_menu"
    )
    back = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu_facility")
    mp.add(verify, back)

    facility = await FacilityDAL.get(facility_id)
    msg_text = f"""
Предприятие:
    - название: {facility.title}
    - адрес: {facility.address}
    - описание: {facility.description}
    - статус: {"активно" if facility.active else "не активно"}\n
❓Вы уверены, что хотите начать смену на этом предприятии? Время начнется сразу после нажатия на кнопку.
    """

    msg = await bot.send_message(message.chat.id, text=msg_text, reply_markup=mp)

    await MessageContext.update(message.chat.id, [msg.id])


@active_pause_handler
async def facility_shift_menu(message: types.Message):
    await MessageContext.clear(message.chat.id)

    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    report = await ReportDAL.get_active(employee.id)
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    if not report:
        facility_id = context_manager.get_facility_id(message.chat.id)
        facility = await FacilityDAL.get(facility_id)
        await ReportDAL.create(
            title=f"Отчет сотрудника {employee.fio} на объекте {facility.title} от {now.date().strftime('%d.%m.%Y')}",
            employee_id=employee.id,
            facility_id=facility_id,
            shift_start=now,
        )
        report = await ReportDAL.get_active(employee.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    finish = types.InlineKeyboardButton(
        text="Завершить смену", callback_data="facility_shift_finish"
    )
    # implemented in bot.handlers.pause
    pause = types.InlineKeyboardButton(
        text="Начать перерыв", callback_data="pause_start"
    )
    mp.add(finish, pause)
    msg = await bot.send_message(
        message.chat.id,
        text=f"Время начала смены: {report.shift_start.strftime('%d.%m.%Y, %H:%M:%S')}",
        reply_markup=mp,
    )

    await MessageContext.update(message.chat.id, [msg.id])


@active_pause_handler
async def facility_shift_finish_verification(message: types.Message):
    await MessageContext.clear(message.chat.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    verify = types.InlineKeyboardButton(
        text="✔️ Потверждаю", callback_data=f"facility_shift_finish_verified"
    )
    back = types.InlineKeyboardButton(
        text="🔙 Назад", callback_data="back_to_facility_shift_menu"
    )
    mp.add(verify, back)
    msg = await bot.send_message(
        message.chat.id,
        text="Вы уверены, что хотите закончить текущую смену?",
        reply_markup=mp,
    )

    await MessageContext.update(message.chat.id, [msg.id])


@active_pause_handler
async def facility_shift_finish_verified(message: types.Message):
    await MessageContext.clear(message.chat.id)

    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    report = await ReportDAL.get_active(employee.id)
    await ReportDAL.update_shift_end(
        report.id, datetime.now(timezone.utc) + timedelta(hours=3)
    )

    mp = types.InlineKeyboardMarkup(row_width=1)
    reports = types.InlineKeyboardButton(
        text="Перейти в отчеты ➡️", callback_data="menu_report"
    )
    mp.add(reports)
    msg = await bot.send_message(
        message.chat.id,
        text="Вы успешно завершили смену на объекте, теперь вы можете заполнить форму с отчетом в соотвествующей "
        "области!",
        reply_markup=mp,
    )

    await MessageContext.update(message.chat.id, [msg.id])

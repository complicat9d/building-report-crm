import os
from uuid import uuid4
from telebot import types
from telebot.asyncio_handler_backends import StatesGroup, State
from math import ceil

from bot import bot
from bot.markups import InlineMarkup
from bot.middlewares import context_manager
from bot.handlers.decorators import active_shift_handler
from middleware.message_context import MessageContext
from database.dal import ReportDAL, EmployeeDAL, FacilityDAL, FileDAL
from utils import text_parser

OBJ_PER_PAGE = 5


class EditReportStates(StatesGroup):
    EditDescription = State()
    AddPhoto = State()


@active_shift_handler
async def report_menu(message: types.Message, page: int):
    try:
        await MessageContext.clear(message.chat.id)
        employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
        reports = await ReportDAL.get_by_employee_id(employee.id)
        if not reports:
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text="🍃 Вы еще не сделали никаких отчетов",
                reply_markup=InlineMarkup.back_to_menu(),
            )
            await MessageContext.update(message.chat.id, [msg.id])
        else:
            amount_of_pages = ceil(len(reports) / OBJ_PER_PAGE)
            chunks = [
                reports[i : i + OBJ_PER_PAGE]
                for i in range(0, len(reports), OBJ_PER_PAGE)
            ]
            data_to_display = chunks[page - 1]

            msg = await bot.send_message(
                chat_id=message.chat.id,
                text="Выберите отчет:",
                reply_markup=InlineMarkup.report_slider(
                    data_to_display, page, amount_of_pages, OBJ_PER_PAGE
                ),
            )
            await MessageContext.update(message.chat.id, [msg.id])

    except Exception as e:
        logger.log(
            level=LogLevel.ERROR,
            message=f"An error occurred in report_handler.py in report_menu function: {e}",
        )


@active_shift_handler
async def report_selected_menu(message: types.Message):
    msg_ids = []
    await bot.delete_state(message.chat.id)
    await MessageContext.clear(message.chat.id)
    report_id = context_manager.get_report_id(message.chat.id)

    report = await ReportDAL.get(report_id)
    facility = await FacilityDAL.get(report.facility_id)
    msg_text = f"""Отчет:
 - заголовок: {report.title}
 - описание: {report.description if report.description else 'отсутствует'}
 - начало смены: {report.shift_start.strftime('%d.%m.%Y, %H:%M:%S')}
 - конец смены: {report.shift_end.strftime('%d.%m.%Y, %H:%M:%S')}

Предприятие:
 - название: {facility.title}
 - описание: {facility.description}
 - адрес: {facility.address}
 - статус: {"активно" if facility.active else "не активно"}"""

    mp = types.InlineKeyboardMarkup(row_width=1)
    photos = types.InlineKeyboardButton(
        text="Фотографии", callback_data="report_photo_menu"
    )
    add_photos = types.InlineKeyboardButton(
        text="Добавить фотографии", callback_data="add_photos"
    )
    edit_description = types.InlineKeyboardButton(
        text="Редактировать описание отчета", callback_data="edit_description"
    )
    back = types.InlineKeyboardButton(
        text="🔙 Назад", callback_data="back_to_menu_report"
    )
    mp.add(photos, add_photos, edit_description, back)

    texts = text_parser(msg_text)
    for text in texts[:-1]:
        msg = await bot.send_message(message.chat.id, text=text)
        msg_ids.append(msg.id)

    msg = await bot.send_message(message.chat.id, text=texts[-1], reply_markup=mp)
    msg_ids.append(msg.id)

    await MessageContext.update(message.chat.id, msg_ids)


@active_shift_handler
async def report_photo_menu(message: types.Message, page: int):
    msg_ids = []
    await MessageContext.clear(message.chat.id)
    report_id = context_manager.get_report_id(message.chat.id)

    files = await FileDAL.get_by_report_id(report_id)
    mp = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_report")

    if files:
        files_len = len(files)
        file = files[page % files_len]
        file_to_display = open(file.path, "rb")

        msg = await bot.send_photo(
            message.chat.id,
            photo=file_to_display,
        )
        msg_ids.append(msg.id)
        if files_len != 1:
            go_forward = types.InlineKeyboardButton(
                text=">", callback_data=f"slider_photo_menu_{(page + 1) % files_len}"
            )
            go_back = types.InlineKeyboardButton(
                text="<", callback_data=f"slider_photo_menu_{(page - 1) % files_len}"
            )
            mp.add(go_back, go_forward)

        delete_photo = types.InlineKeyboardButton(
            text="Удалить фотографию",
            callback_data=f"slider_photo_menu_delete_{file.id}_{page}",
        )
        mp.add(delete_photo)
        mp.add(back)
        msg = await bot.send_message(
            message.chat.id, text=f"Фотография №{page % files_len + 1}", reply_markup=mp
        )
        msg_ids.append(msg.id)
    else:
        mp.add(back)
        msg = await bot.send_message(
            message.chat.id,
            text=f"🍃 Вы еще не прикрепили никаких фотографий к отчету",
            reply_markup=mp,
        )
        msg_ids.append(msg.id)

    await MessageContext.update(message.chat.id, msg_ids)


@active_shift_handler
async def slider_photo_menu_delete_verification(
    message: types.Message, page_to_go_back: int
):
    await MessageContext.clear(message.chat.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    verify = types.InlineKeyboardButton(
        text="✔️Потверждаю", callback_data="slider_photo_menu_delete_verified"
    )
    back = types.InlineKeyboardButton(
        text="🔙 Назад", callback_data=f"slider_photo_menu_{page_to_go_back}"
    )
    mp.add(verify, back)

    msg = await bot.send_message(
        message.chat.id,
        text="Вы уверены, что хотите удалить данное фото?",
        reply_markup=mp,
    )

    await MessageContext.update(message.chat.id, [msg.id])


@active_shift_handler
async def slider_photo_menu_delete_verified(message: types.Message):
    await MessageContext.clear(message.chat.id)
    await FileDAL.delete(context_manager.get_file_id(message.chat.id))

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(
        text="🔙 Назад", callback_data="report_photo_menu"
    )
    mp.add(back)

    msg = await bot.send_message(
        message.chat.id, text="Фотография была успешно удалена!", reply_markup=mp
    )

    await MessageContext.update(message.chat.id, [msg.id])


@active_shift_handler
async def edit_description(message: types.Message):
    await MessageContext.clear(message.chat.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_report")
    mp.add(back)
    msg = await bot.send_message(
        message.chat.id, "Введите описание для вашего отчета:", reply_markup=mp
    )
    await bot.set_state(message.chat.id, EditReportStates.EditDescription)
    await MessageContext.update(message.chat.id, [msg.id])


@bot.message_handler(state=EditReportStates.EditDescription)
@active_shift_handler
async def description_edited(message: types.Message):
    msg_ids = [message.id]

    await bot.delete_state(message.chat.id)
    await MessageContext.clear(message.chat.id)
    report_id = context_manager.get_report_id(message.chat.id)

    description = message.text
    await ReportDAL.update_description(report_id, description)

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_report")
    mp.add(back)
    msg = await bot.send_message(
        message.chat.id, "Описание для отчета было успешно добавлено!", reply_markup=mp
    )
    msg_ids.append(msg.id)

    await MessageContext.update(message.chat.id, msg_ids)


@active_shift_handler
async def add_photos(message: types.Message):
    await MessageContext.clear(message.chat.id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_report")
    mp.add(back)
    msg = await bot.send_message(
        message.chat.id,
        "Скиньте боту фотграфию, которую хотите прикрепить к отчету",
        reply_markup=mp,
    )
    await bot.set_state(message.chat.id, EditReportStates.AddPhoto)
    await MessageContext.update(message.chat.id, [msg.id])


@bot.message_handler(content_types=["photo"], state=EditReportStates.AddPhoto)
@active_shift_handler
async def photo_added(message: types.Message):
    await bot.delete_state(message.chat.id)
    report_id = context_manager.get_report_id(message.chat.id)

    photo = message.photo[-1]
    # to delete the photo right after it was sent
    await MessageContext.update(message.chat.id, [message.id])
    await MessageContext.clear(message.chat.id)

    file_info = await bot.get_file(photo.file_id)
    file_content = await bot.download_file(file_info.file_path)
    path = os.getcwd() + f"/api/static/{uuid4()}.jpg"
    with open(path, "wb") as temp_file:
        temp_file.write(file_content)
    await FileDAL.create(path, report_id)

    mp = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_report")
    mp.add(back)
    msg = await bot.send_message(
        message.chat.id, "Фотография в отчет была успешно добавлена!", reply_markup=mp
    )

    await MessageContext.update(message.chat.id, [msg.id])

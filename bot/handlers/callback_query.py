from telebot import types

from bot import bot
from bot.middlewares import context_manager
from bot.handlers.facility import (
    facility_menu,
    facility_menu_selection_verification,
    facility_shift_menu,
    facility_shift_finish_verification,
    facility_shift_finish_verified,
)
from bot.handlers.pause import pause_menu, pause_finish
from bot.handlers.help import help_menu
from bot.handlers.main_menu import main_menu
from bot.handlers.profile import profile_menu
from bot.handlers.report import (
    report_menu,
    report_selected_menu,
    report_photo_menu,
    slider_photo_menu_delete_verification,
    slider_photo_menu_delete_verified,
    edit_description,
    add_photos,
)


@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call: types.CallbackQuery):
    if call.data.startswith("main_menu") or call.data.startswith("back_to_main_menu"):
        await main_menu(call.message)

    elif call.data.startswith("profile_menu"):
        await profile_menu(call.message)

    elif call.data.startswith("help_menu"):
        await help_menu(call.message)

    elif call.data.startswith("menu_facility") or call.data.startswith(
        "back_to_menu_facility"
    ):
        await facility_menu(call.message, 1)

    elif call.data.startswith("facility_page_"):
        page = int(call.data.split("_")[-1])
        await facility_menu(call.message, page)

    elif call.data.startswith("facility_shift_menu") or call.data.startswith("back_to_facility_shift_menu"):
        await facility_shift_menu(call.message)

    elif call.data.startswith("facility_shift_finish_verified"):
        await facility_shift_finish_verified(call.message)

    elif call.data.startswith("facility_shift_finish"):
        await facility_shift_finish_verification(call.message)

    elif call.data.startswith("facility_"):
        facility_id = int(call.data.split("_")[-1])
        await facility_menu_selection_verification(call.message, facility_id)

    elif call.data.startswith("pause_start"):
        await pause_menu(call.message)

    elif call.data.startswith("pause_finish"):
        await pause_finish(call.message)

    elif call.data.startswith("menu_report") or call.data.startswith("back_to_menu_report"):
        await report_menu(call.message, 1)

    elif call.data.startswith("report_page_"):
        page = int(call.data.split("_")[-1])
        await report_menu(call.message, page)

    elif call.data.startswith("report_photo_menu"):
        await report_photo_menu(call.message, 0)

    elif call.data.startswith("slider_photo_menu_delete_verified"):
        await slider_photo_menu_delete_verified(call.message)

    elif call.data.startswith("slider_photo_menu_delete_"):
        file_id = int(call.data.split("_")[-2])
        page_to_go_back = int(call.data.split("_")[-1])
        context_manager.set_file_id(call.message.chat.id, file_id)
        await slider_photo_menu_delete_verification(call.message, page_to_go_back)

    elif call.data.startswith("slider_photo_menu_"):
        page = int(call.data.split("_")[-1])
        await report_photo_menu(call.message, page)

    elif call.data.startswith("report_"):
        report_id = int(call.data.split("_")[-1])
        context_manager.set_report_id(call.message.chat.id, report_id)
        await report_selected_menu(call.message)

    elif call.data.startswith("back_to_report"):
        await report_selected_menu(call.message)

    elif call.data.startswith("edit_description"):
        await edit_description(call.message)

    elif call.data.startswith("add_photos"):
        await add_photos(call.message)

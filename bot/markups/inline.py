from typing import List
from telebot import types

from schemas import FacilitySchema, ReportSchema


class InlineMarkup(object):

    @classmethod
    def main_menu(cls):
        mp = types.InlineKeyboardMarkup(row_width=3)

        profile = types.InlineKeyboardButton(
            text="👤 Профиль", callback_data="profile_menu"
        )
        facilities = types.InlineKeyboardButton(
            text="🏢 Объекты", callback_data="menu_facility"
        )
        reports = types.InlineKeyboardButton(
            text="📝 Отчеты", callback_data="menu_report"
        )
        faq = types.InlineKeyboardButton(text="❓ F.A.Q.", callback_data="help_menu")

        mp.add(profile)
        mp.add(facilities, reports)
        mp.add(faq)

        return mp

    @classmethod
    def profile_menu(cls):
        mp = types.InlineKeyboardMarkup(row_width=1)

        back_to_main_menu = types.InlineKeyboardButton(
            text="🔙 Назад", callback_data="back_to_main_menu"
        )

        mp.add(back_to_main_menu)

        return mp

    @classmethod
    def facility_slider(
        cls,
        facilities: List[FacilitySchema],
        page: int,
        amount_of_pages: int,
        objects_per_page: int,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        number = 1 + (page - 1) * objects_per_page

        for facility in facilities:
            keyboard.append(
                types.InlineKeyboardButton(
                    text=f"{number}. {facility.title}",
                    callback_data=f"facility_{facility.id}",
                )
            )
            number += 1

        if page > 1:
            keyboard.append(
                types.InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=f"facility_page_{page - 1}"
                )
            )
        if page < amount_of_pages:
            keyboard.append(
                types.InlineKeyboardButton(
                    text="Вперед ➡️", callback_data=f"facility_page_{page + 1}"
                )
            )

        keyboard.append(
            types.InlineKeyboardButton(
                text="🔙 Назад", callback_data="back_to_main_menu"
            )
        )

        return types.InlineKeyboardMarkup(
            row_width=1, keyboard=[[button] for button in keyboard]
        )

    @classmethod
    def report_slider(
        cls,
        reports: List[ReportSchema],
        page: int,
        amount_of_pages: int,
        objects_per_page: int,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        number = 1 + (page - 1) * objects_per_page

        for report in reports:
            keyboard.append(
                types.InlineKeyboardButton(
                    text=f"{number}. {report.title}",
                    callback_data=f"report_{report.id}",
                )
            )
            number += 1

        if page > 1:
            keyboard.append(
                types.InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=f"report_page_{page - 1}"
                )
            )
        if page < amount_of_pages:
            keyboard.append(
                types.InlineKeyboardButton(
                    text="Вперед ➡️", callback_data=f"report_page_{page + 1}"
                )
            )

        keyboard.append(
            types.InlineKeyboardButton(
                text="🔙 Назад", callback_data="back_to_main_menu"
            )
        )

        return types.InlineKeyboardMarkup(
            row_width=1, keyboard=[[button] for button in keyboard]
        )

    @classmethod
    def back_to_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_main_menu"
                    )
                ],
            ],
        )

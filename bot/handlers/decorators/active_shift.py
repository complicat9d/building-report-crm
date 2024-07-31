from telebot import types

from bot import bot
from middleware.message_context import MessageContext
from database.dal import ReportDAL, EmployeeDAL


def active_shift_handler(func):

    async def decorated(*args, **kwargs):
        try:
            message: types.Message = args[0]
        except IndexError:
            message: types.Message = kwargs["message"]

        employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
        if employee:
            employee_id = employee.id
            reports = await ReportDAL.get_by_employee_id(employee_id)
            for report in reports:
                if report.shift_end is None:
                    msg = await bot.send_message(
                        message.chat.id,
                        text="❌ В настоящий момент у вас есть открытый отчет, вам нужно его закончить перед тем, "
                        "как перейти в другую область в боте",
                    )
                    await MessageContext.update(message.chat.id, [msg.id])
                    return

        return await func(*args, **kwargs)

    return decorated

from telebot import types

from bot import bot
from middleware.message_context import MessageContext
from database.dal import PauseDAL, EmployeeDAL, ReportDAL


def active_pause_handler(func):

    async def decorated(*args, **kwargs):
        try:
            message: types.Message = args[0]
        except IndexError:
            message: types.Message = kwargs["message"]

        employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
        if employee:
            employee_id = employee.id
            active_report = await ReportDAL.get_active(employee_id)
            if active_report:
                pauses = await PauseDAL.get_by_report_id(active_report.id)
                for pause in pauses:
                    if pause.end is None:
                        msg = await bot.send_message(
                            message.chat.id,
                            text="❌ В настоящий момент у вас есть не завершенный перерыв, закончите его, чтобы перейти "
                            "в эту область",
                        )
                        await MessageContext.update(message.chat.id, [msg.id])
                        return

        return await func(*args, **kwargs)

    return decorated

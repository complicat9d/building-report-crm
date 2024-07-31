from bot import bot
from bot.markups import InlineMarkup, MessageText
from bot.handlers.decorators import active_shift_handler
from middleware.message_context import MessageContext
from database.dal import EmployeeDAL


@active_shift_handler
async def profile_menu(message):
    await MessageContext.clear(message.chat.id)

    employee = await EmployeeDAL.get_by_chat_id(message.chat.id)
    if employee:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=MessageText.profile_text(
                chat_id=message.chat.id,
                fio=employee.fio,
                job_title=employee.job_title,
            ),
            reply_markup=InlineMarkup.profile_menu(),
            parse_mode="HTML",
        )
    else:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=MessageText.error_text(),
            reply_markup=InlineMarkup.profile_menu(),
            parse_mode="HTML",
        )
    await MessageContext.update(message.chat.id, [msg.id])


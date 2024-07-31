from bot import bot
from bot.markups import InlineMarkup, MessageText
from bot.handlers.decorators import active_shift_handler
from middleware.message_context import MessageContext


@active_shift_handler
async def main_menu(message):
    await MessageContext.clear(message.chat.id)
    msg = await bot.send_message(
        message.chat.id,
        MessageText.main_user_menu(),
        reply_markup=InlineMarkup.main_menu(),
        parse_mode="HTML",
    )
    await MessageContext.update(message.chat.id, [msg.id])


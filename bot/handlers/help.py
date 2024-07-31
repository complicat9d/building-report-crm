from bot import bot
from bot.markups import InlineMarkup, MessageText
from bot.handlers.decorators import active_shift_handler
from middleware.message_context import MessageContext


@active_shift_handler
async def help_menu(message):
    await MessageContext.clear(message.chat.id)

    msg = await bot.send_message(
        message.chat.id,
        text=MessageText.help_text(),
        reply_markup=InlineMarkup.back_to_menu(),
    )

    await MessageContext.update(message.chat.id, [msg.id])


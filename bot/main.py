import asyncio
from telebot.asyncio_filters import (
    ForwardFilter,
    IsDigitFilter,
    IsReplyFilter,
    StateFilter,
)

from bot import bot
from bot.handlers.command import start_handler, home_handler
from bot.handlers.callback_query import callback_handler
from bot.middlewares import FloodingMiddleware
from utils import logger


bot.add_custom_filter(IsReplyFilter())
bot.add_custom_filter(ForwardFilter())
bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsDigitFilter())

bot.setup_middleware(FloodingMiddleware(1))

if __name__ == "__main__":
    logger.info("Bot is starting...")
    asyncio.run(bot.infinity_polling())

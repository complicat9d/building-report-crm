from telebot.async_telebot import AsyncTeleBot

from config import settings

bot = AsyncTeleBot(token=settings.TOKEN)

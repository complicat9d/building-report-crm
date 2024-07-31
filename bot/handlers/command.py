from bot import bot
from bot.handlers.main_menu import main_menu
from bot.handlers.decorators import active_shift_handler
from database.dal import EmployeeDAL, MessageDAL
from middleware.message_context import MessageContext


@bot.message_handler(commands=["start"])
@active_shift_handler
async def start_handler(message):
    # important to note: MessageContext entity is created after verifying the passed link for registration
    # that's why if user registration fails, we cannot delete error message sent by the bot
    result = await EmployeeDAL.check_by_chat_id(message.chat.id)

    # check if user has already been registered by searching with chat_id: only registered users have it
    if not result:
        token = message.text.split()
        # check if there is a uuid - token - in the passed link
        if len(token) > 1:
            try:
                employee_id = await EmployeeDAL.check_by_token(token[-1])
                # check if such token exists in the database
                if employee_id:
                    msg = await bot.send_message(
                        chat_id=message.chat.id,
                        text="<i>Происходит регистрация пользователя в системе, это может занять некоторое "
                        "время...</i>",
                        parse_mode="HTML",
                    )
                    await EmployeeDAL.update(
                        id=employee_id, chat_id=message.chat.id, is_active=True
                    )
                    await MessageDAL.create(message.chat.id)
                    # message.id: delete /start message
                    await MessageContext.update(
                        message.chat.id, [message.id, msg.id]
                    )
                    await main_menu(message)
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="❌ Указанная ссылка не зарегистрирована. Пожалуйста, проверьте её правильность.",
                    )
            except Exception:
                # the 'token' value is not UUID-like string
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="❌ Неправильная ссылка для регистрации",
                )

        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="❌ Пожалуйста, используйте персональную ссылку для регистрации.",
            )
    else:
        await main_menu(message)


@bot.message_handler(commands=["home"])
@active_shift_handler
async def home_handler(message):
    await MessageContext.clear(message.chat.id)
    result = await EmployeeDAL.check_by_chat_id(message.chat.id)

    if not result:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Вы еще не были зарегистрированы в боте, для начала взаимодействия используйте личную ссылку.",
            parse_mode="HTML",
        )
    else:
        # delete /home message
        await MessageContext.update(message.chat_id, message.id)
        await main_menu(message)


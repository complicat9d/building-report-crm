class MessageText:
    @classmethod
    def main_user_menu(cls):
        cls._menu_text = "<b>Меню</b>"
        return cls._menu_text

    @classmethod
    def profile_text(cls, chat_id: str, fio: str, job_title: str):
        cls._profile_text = f"""
            \n\tID: {chat_id}
            \n\tФИО: {fio}
            \n\tСпециальность: {job_title}
            """
        return cls._profile_text

    @classmethod
    def help_text(cls):
        cls._help_text = f"""
        Мануал по использованию
        """
        return cls._help_text

    @classmethod
    def error_text(cls):
        cls._error_text = (
            "❌ Что-то пошло не так. Пожалуйста, обратитесь в тех. поддержку."
        )
        return cls._error_text

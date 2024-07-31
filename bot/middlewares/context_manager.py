def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ContextManager:
    def __init__(self):
        self._context = {}

    def set_facility_id(self, chat_id: int, facility_id: int):
        if chat_id in self._context.keys():
            self._context[chat_id]["facility_id"] = facility_id
        else:
            self._context[chat_id] = {}
            self._context[chat_id]["facility_id"] = facility_id

    def get_facility_id(self, chat_id: int):
        return self._context[chat_id]["facility_id"]

    def set_report_id(self, chat_id: int, report_id: int):
        if chat_id in self._context.keys():
            self._context[chat_id]["report_id"] = report_id
        else:
            self._context[chat_id] = {}
            self._context[chat_id]["report_id"] = report_id

    def get_report_id(self, chat_id: int):
        return self._context[chat_id]["report_id"]

    def set_file_id(self, chat_id: int, file_id: int):
        if chat_id in self._context.keys():
            self._context[chat_id]["file_id"] = file_id
        else:
            self._context[chat_id] = {}
            self._context[chat_id]["file_id"] = file_id

    def get_file_id(self, chat_id: int):
        return self._context[chat_id]["file_id"]


context_manager = ContextManager()

class ProcessResult():

    def __init__(self, t: str, s: bool, m: str):
        self.type = t
        self.success = s
        self.message = m

    def is_sucess(self) -> bool:
        return self.success

    def is_error(self) -> bool:
        return not self.success

    def get_type(self) -> str:
        return self.type

    def get_message(self) -> str:
        return self.message



class Message:
    
    code = None
    message = None
    level = None   # Info, Warning, Error
    extra = None

    def __init__(self, code, message, level):
        self.code = code
        self.message = message
        self.level = level


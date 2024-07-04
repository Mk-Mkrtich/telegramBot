class BaseHandler:
    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        raise NotImplementedError("This method should be overridden in subclasses")

class EnglishCaptionsAreNotAvailable(Exception):
    MESSAGE = "English Captions are not Available"

    def __init__(self):
        self.message = self.MESSAGE
        super().__init__(self.message)

from requests import HTTPError

class ClientAPIError(HTTPError):

    def __init__(self, message, error, status):
        self.status = status
        self.message = message
        self.error = error
    
    def __repr__(self):
        return f"{self.error}: {self.message}"
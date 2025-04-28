class APIException(Exception):
    """Base class for API exceptions."""
    def __init__(self, message="An error occurred", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UnauthorizedException(APIException):
    """Exception raised for unauthorized access."""
    def __init__(self, message="Unauthorized Access"):
        super().__init__(message, status_code=401)

class BadRequestException(APIException):
    """Exception raised for bad requests."""
    def __init__(self, message="Bad Request"):
        super().__init__(message, status_code=400)

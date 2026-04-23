class MessagePolisherError(Exception):
    """Base exception for message polisher errors."""
    pass

class AIServiceError(MessagePolisherError):
    """Exception raised for errors in the AI service."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class ContentPolicyError(MessagePolisherError):
    """Raised when user input violates safety or content policies."""
    pass

class ConfigurationError(MessagePolisherError):
    """Raised when there is a configuration issue, such as missing API keys."""
    pass

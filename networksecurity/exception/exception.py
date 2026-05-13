import sys

from networksecurity.logging import logger


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line number: {self.lineno} with error message: {self.error_message}".format(
            self.file_name, self.lineno, str(self.error_message)
        )


if __name__ == "__main__":
    try:
        raise Exception("This is a test exception")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

"""
The logging tools used throughout this package.
"""

# Load additional packages
import logging
import sys


class CustomLogging:
    """
    Logging object for the package.
    :param name: name of the logger.
    """

    def __init__(self, name: str):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.DEBUG)

        # Create handlers
        self.__streamHandler = logging.StreamHandler(sys.stdout)
        self.__streamHandler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        self.__briefFormatter = logging.Formatter('%(levelname)-8s %(message)s')
        self.__streamHandler.setFormatter(self.__briefFormatter)

        # Add handlers to logger
        self.__logger.addHandler(self.__streamHandler)

    def get_logger(self):
        """
        Gets the logger object.
        :return: Returns the logger.
        """
        return self.__logger

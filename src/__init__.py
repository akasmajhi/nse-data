from loguru import logger
logger.add("nse-data.log", level="INFO", rotation="100 MB", colorize=True, backtrace=True)

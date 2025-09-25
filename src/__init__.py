from loguru import logger
logger.add("nse-data.log", 
           # filter="src.helpers.file_readers",
           level="DEBUG", 
           rotation="25 MB", 
           colorize=True, 
           backtrace=True)

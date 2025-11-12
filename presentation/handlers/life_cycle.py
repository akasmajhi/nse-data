from loguru import logger
from nicegui import Client
from nicegui import ui


def handle_startup():
    logger.info(f"Into start OR restart")


def handle_shutdown():
    logger.info(f"Into shutdown")


def handle_connect(client: Client):
    logger.info(f"Into connect [{client = }]")


def handle_disconnect(client: Client):
    logger.info(f"Into disconnect [{client = }]")


def handle_delete(client: Client):
    logger.info(f"Into delete [{client = }]")


def handle_exception():
    logger.info(f"Into exception")

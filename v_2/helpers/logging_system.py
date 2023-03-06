import os
import logging


def get_logger(logger_name):
    if not os.path.exists("log"):
        os.mkdir("log")

    logging.basicConfig(
        filename=f"log/{logger_name}.txt",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )

    logger = logging.getLogger(f"{logger_name}")

    return logger
import logging
import os


def setup_logger(log_dir="logs", log_level=logging.INFO):
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, "application.log")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        filename=log_filename,
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Add console handler to print logs to console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))

    logging.getLogger().addHandler(console_handler)
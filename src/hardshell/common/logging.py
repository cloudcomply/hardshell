import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("hardshell.log"),
        # logging.StreamHandler()
    ],
)

# Get a logger instance
logger = logging.getLogger("hardshell")

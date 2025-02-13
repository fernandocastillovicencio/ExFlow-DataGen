import logging
import os

# Define the logs directory
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set default logging level
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)

# Create a logger instance
logger = logging.getLogger("ExFlow-DataGen")

# Example usage
if __name__ == "__main__":
    logger.info("Logger is working correctly!")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

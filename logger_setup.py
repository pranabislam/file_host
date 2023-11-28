import logging
import multiprocessing
from filelock import FileLock

# Initialize the logger and log queue as global variables
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
log_queue = multiprocessing.Queue(-1)  # Use an unlimited size Queue

# Set up a FileHandler with a FileLock for exclusive access to the log file
log_file = 'shared_log.txt'
file_handler = logging.FileHandler(log_file)
file_lock = FileLock(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Log listener function to handle logs from the Queue
def log_listener():
    root = logging.getLogger()
    while True:
        try:
            record = log_queue.get()
            if record is None:
                break
            root.handle(record)
        except Exception as e:
            print(f"Error in log_listener: {e}")

# Start the log listener process
log_listener_process = multiprocessing.Process(target=log_listener)
log_listener_process.start()

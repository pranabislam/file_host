import logging
import logging.handlers
import concurrent.futures
import multiprocessing
from filelock import FileLock  # Import FileLock for file locking

# Initialize the logger
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

# Set up a FileHandler with a FileLock for exclusive access to the log file
log_file = 'shared_log.txt'  # Change to your desired log file path
file_handler = logging.handlers.FileHandler(log_file)
file_lock = FileLock(log_file)  # Create a FileLock for the log file
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the FileHandler to the logger
logger.addHandler(file_handler)

# Log listener function to handle logs from the Queue
def log_listener():
    root = logging.getLogger()
    root.addHandler(logging.StreamHandler())  # Output logs to console

    while True:
        try:
            record = log_queue.get()
            if record is None:  # Terminate when receiving a None record
                break
            root.handle(record)
        except Exception as e:
            print(f"Error in log_listener: {e}")

# Start the log listener process
log_listener_process = multiprocessing.Process(target=log_listener)
log_listener_process.start()

def process_task(task):
    # Perform the task and log using the logger with FileHandler and FileLock
    result = task * 2
    with file_lock:  # Acquire the file lock before writing to the log file
        logger.info(f"Task: {task}, Result: {result}")

if __name__ == "__main__":
    tasks = [1, 2, 3, 4, 5]  # Example tasks

    # Using ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(process_task, task) for task in tasks]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Shutdown log_queue by sending a None record
    log_queue.put_nowait(None)
    log_listener_process.join()  # Wait for the log listener to finish

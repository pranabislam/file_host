import logging
import logging.handlers
import concurrent.futures
import multiprocessing
import subprocess

# Initialize the logger
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

# Create a QueueHandler to send log records to a Queue
log_queue = multiprocessing.Queue(-1)  # Use an unlimited size Queue
queue_handler = logging.handlers.QueueHandler(log_queue)

# Configure the logger
logger.addHandler(queue_handler)

# Log listener function to handle logs from the Queue
def log_listener():
    root = logging.getLogger()
    handler = logging.StreamHandler()  # You can change this to a FileHandler to log to a file
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

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
    # Perform the task and log
    result = task * 2
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

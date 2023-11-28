import logger_setup
from another_module import get_scores  # Import the function from another module

# Your other functions and code here
# ...

def process_task(task):
    # Perform the task and log using the global logger from logger_setup
    result = task * 2
    with logger_setup.file_lock:
        logger_setup.logger.info(f"Task: {task}, Result: {result}")
    # Call get_scores function from another_module
    get_scores(task)

if __name__ == "__main__":
    tasks = [1, 2, 3, 4, 5]

    # Using ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Shutdown log_queue by sending a None record
    logger_setup.log_queue.put_nowait(None)
    logger_setup.log_listener_process.join()

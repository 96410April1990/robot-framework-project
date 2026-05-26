import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def multithreading_example(name):
    print(f"Starting thread-{name}")
    time.sleep(3)
    print(f"Completed thread-{name}")

    return f"thread-{name} result"

def multithreading_one():
    threads = []
    for i in range(3):
        t = threading.Thread(target=multithreading_example, args=(i+1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"All threads completed")

def multiprocessing_example(name):
    print(f"Starting process-{name}")
    time.sleep(3)
    print(f"Completed process-{name}")

    return f"process-{name} result"

def multiprocessing_one():
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=multiprocessing_example, args=(i+1,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"All processes completed")

def threadpoolexecutor_example():
    print("=" * 50)
    print("Starting thread pool executor")
    print("=" * 50)

    tasks = ["Task-1", "Task-2", "Task-3"]

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(multithreading_example, tasks))

    print(f"Results: {results}-Completed")

def processpoolexecutor_example():

    tasks = ["Task A", "Task B", "Task C"]

    with ProcessPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(multiprocessing_example, tasks))

    print(f"Results: {results}-Completed")

if __name__ == "__main__":
    multithreading_one()
    multiprocessing_one()
    threadpoolexecutor_example()
    processpoolexecutor_example()
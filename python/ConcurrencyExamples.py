"""
ConcurrencyExamples.py
Simple side-by-side examples of:
  1. threading.Thread        (raw multithreading)
  2. multiprocessing.Process (raw multiprocessing)
  3. ThreadPoolExecutor      (managed thread pool)
  4. ProcessPoolExecutor     (managed process pool)
"""

import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ---------------------------------------------------------------------------
# Shared task functions
# ---------------------------------------------------------------------------

def io_task(name):
    """Simulates an I/O-bound task (e.g. reading a file, HTTP call)."""
    print(f"  [{name}] starting...")
    time.sleep(1)  # pretend we're waiting for I/O
    print(f"  [{name}] done.")
    return f"{name} result"


def cpu_task(name):
    """Simulates a CPU-bound task (e.g. number crunching)."""
    print(f"  [{name}] starting...")
    total = sum(range(5_000_000))  # burn some CPU cycles
    print(f"  [{name}] done. Sum={total}")
    return total


# ---------------------------------------------------------------------------
# 1. Raw Multithreading — threading.Thread
# ---------------------------------------------------------------------------

def example_raw_threading():
    print("\n" + "=" * 50)
    print("1. Raw Multithreading (threading.Thread)")
    print("=" * 50)
    print("Use case: I/O-bound tasks. Manual thread management.")

    threads = []
    for i in range(3):
        t = threading.Thread(target=io_task, args=(f"Thread-{i + 1}",))
        threads.append(t)
        t.start()           # launch thread immediately

    for t in threads:
        t.join()            # wait for every thread to finish

    print("All threads finished.")


# ---------------------------------------------------------------------------
# 2. Raw Multiprocessing — multiprocessing.Process
# ---------------------------------------------------------------------------

def example_raw_multiprocessing():
    print("\n" + "=" * 50)
    print("2. Raw Multiprocessing (multiprocessing.Process)")
    print("=" * 50)
    print("Use case: CPU-bound tasks. Each process has its own GIL.")

    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=cpu_task, args=(f"Process-{i + 1}",))
        processes.append(p)
        p.start()           # spawn a separate OS process

    for p in processes:
        p.join()            # wait for every process to finish

    print("All processes finished.")


# ---------------------------------------------------------------------------
# 3. ThreadPoolExecutor — managed thread pool
# ---------------------------------------------------------------------------

def example_thread_pool_executor():
    print("\n" + "=" * 50)
    print("3. ThreadPoolExecutor (managed thread pool)")
    print("=" * 50)
    print("Use case: I/O-bound tasks. Easier than raw threading.")

    tasks = ["File-A", "File-B", "File-C"]

    with ThreadPoolExecutor(max_workers=3) as executor:
        # executor.map() runs io_task for each item in parallel
        # and returns results IN ORDER (same as input order)
        results = list(executor.map(io_task, tasks))

    print(f"Results: {results}")


# ---------------------------------------------------------------------------
# 4. ProcessPoolExecutor — managed process pool
# ---------------------------------------------------------------------------

def example_process_pool_executor():
    print("\n" + "=" * 50)
    print("4. ProcessPoolExecutor (managed process pool)")
    print("=" * 50)
    print("Use case: CPU-bound tasks. Bypasses GIL with separate processes.")

    tasks = ["Chunk-A", "Chunk-B", "Chunk-C"]

    with ProcessPoolExecutor(max_workers=3) as executor:
        # Same API as ThreadPoolExecutor — just swaps threads for processes
        results = list(executor.map(cpu_task, tasks))

    print(f"Results: {results}")


# ---------------------------------------------------------------------------
# Run all examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # NOTE: multiprocessing on macOS/Windows requires the if __name__ == "__main__"
    # guard to avoid spawning child processes recursively.

    #example_raw_threading()
    #example_raw_multiprocessing()
    example_thread_pool_executor()
    #example_process_pool_executor()

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    #print("threading.Thread      → manual, I/O-bound, GIL applies")
    #print("multiprocessing.Process → manual, CPU-bound, no shared GIL")
    #print("ThreadPoolExecutor    → automatic pool, I/O-bound, GIL applies")
    print("ProcessPoolExecutor   → automatic pool, CPU-bound, no shared GIL")

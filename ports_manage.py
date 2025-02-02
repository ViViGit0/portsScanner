import json
from multiprocessing.pool import ThreadPool
from rich.console import Console
import os

console = Console()

#Read the file json
def extract_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return(data)

#Progress Bar
def display_progress(iteration, total):
    bar_max_width = 45
    bar_current_width = bar_max_width * iteration // total
    bar = "█" * bar_current_width + "-" * (bar_max_width - bar_current_width)
    progress = "%.1f" % (iteration / total * 100)
    console.print(f"|{bar}| {progress} %", end="\r", style="bold green")
    if iteration == total:
        print()

#Workers
def threadpool_executer(fuction, iterable, iterable_lenght):
    num_workers = os.cpu_count()
    print(f"\nRunning using {num_workers} workers\n")
    with ThreadPool(num_workers) as pool:
        for loop_index, _ in enumerate(pool.imap(fuction, iterable), 1):
            display_progress(loop_index, iterable_lenght)
        
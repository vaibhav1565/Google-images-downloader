import os
import sys
import re
import requests
import urllib3
import threading
from queue import Queue
from crawler import scrape_images

urllib3.disable_warnings()

# Thread-safe queue for URLs
url_queue = Queue()

success = 0
failure = 0
lock = threading.Lock()  # To protect shared counters

query = sys.argv[1]
os.makedirs(query, exist_ok=True)


def download_image(src, idx):
    """
    Downloads an image from the provided src URL and saves it with a unique index.
    """
    global success, failure
    extension = '.png'
    pattern = re.compile(r"\.([a-zA-Z]+)$")
    match = pattern.search(src)
    if match:
        extension = match.group()

    print(f"{idx}. Downloading {src}")
    try:
        response = requests.get(
            src, verify=False, timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
            }
        )
        if response.ok:
            filename = f"{query}/{query}_{idx}{extension}"
            with open(filename, "wb") as file:
                file.write(response.content)
            with lock:
                success += 1
            print(f"{idx}. Finished downloading {src}")
        else:
            print(f"Failed to download {src}: {response.status_code}")
            with lock:
                failure += 1
    except requests.exceptions.RequestException as ex:
        print(f"Error downloading {src}: {ex}")
        with lock:
            failure += 1


def worker():
    """
    Worker thread function that processes URLs from the queue and downloads images.
    """
    while True:
        item = url_queue.get()  # Get a URL from the queue
        if item is None:  # Sentinel to shut down the worker
            break
        idx, url = item
        download_image(url, idx)
        url_queue.task_done()  # Mark the task as done


def main():
    """
    Main function that orchestrates the scraping and downloading process.
    """
    num_workers = 5
    threads = []

    # Start worker threads
    for _ in range(num_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Start the scraping process in a separate thread
    scraper_thread = threading.Thread(target=scrape_images, args=(url_queue, query, False))
    scraper_thread.start()

    # Wait for the scraper to finish
    scraper_thread.join()

    # Wait for all tasks in the queue to be processed
    url_queue.join()

    # Stop workers
    for _ in range(num_workers):
        url_queue.put(None)
    for thread in threads:
        thread.join()

    print('---------- Report ----------')
    print(f'Successfully downloaded {success} images')
    if failure:
        print(f'{failure} images not downloaded')


if __name__ == "__main__":
    main()
import schedule
import time
import threading
import importlib

def run_main():
    # Import the unabated_scraper_autologin module
    unabated_scraper = importlib.import_module('unabated_scraper_autologin')

    # Start the main function in a separate thread to handle timing issues
    thread = threading.Thread(target=unabated_scraper.main)
    thread.start()

    # Wait for 2 hours (7200 seconds)
    time.sleep(7200)

    # Terminate the thread after 2 hours
    if thread.is_alive():
        print("Terminating and restarting...")
        # Reload the module to reset its state
        importlib.reload(unabated_scraper)

def job():
    run_main()

# Schedule the job every 2 hours
schedule.every(2).hours.do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

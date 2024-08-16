import schedule
import time
import threading
import importlib
from pynput import keyboard
import os
import signal
import sys
import subprocess

# Flag to control pausing and stopping
pause_flag = threading.Event()

def run_main():
    # Import the unabated_scraper_autologin module
    unabated_scraper = importlib.import_module('unabated_scraper_autologin')

    # Start the main function in a separate thread to handle timing issues
    thread = threading.Thread(target=unabated_scraper.main)
    thread.start()

    # Wait for 2 hours (7200 seconds)
    time.sleep(7200)

    # Terminate the thread after 2 hours if not paused
    if thread.is_alive():
        print("Terminating and restarting...")
        unabated_scraper.stop_event.set()
        thread.join()
        importlib.reload(unabated_scraper)

def job():
    if not pause_flag.is_set():
        run_main()

# Function to handle key presses
def on_press(key):
    try:
        if key.char == 'p':
            print("Killing all Python processes, Selenium Chrome drivers, and Google Chrome windows...")
            kill_all_related_processes()
            os._exit(0)  # Exit the current script as well
    except AttributeError:
        pass

def kill_all_related_processes():
    # Kill all Python processes, Selenium Chrome drivers, and Google Chrome windows
    if os.name == 'nt':  # Windows
        subprocess.call("taskkill /F /IM python.exe", shell=True)
        subprocess.call("taskkill /F /IM chromedriver.exe", shell=True)
        subprocess.call("taskkill /F /IM undetected_chromedriver.exe", shell=True)
        
        # Kill all Google Chrome processes using PowerShell
        subprocess.call('powershell "Get-Process chrome | Stop-Process -Force"', shell=True)
        
        # If the above doesn't work, try using wmic
        subprocess.call('wmic process where "name=\'chrome.exe\'" delete', shell=True)

    else:  # Unix/MacOS
        os.killpg(0, signal.SIGTERM)
        subprocess.call("pkill chromedriver", shell=True)
        subprocess.call("pkill chrome", shell=True)

# Start the key listener in a separate thread
def start_key_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Run the key listener in the background
key_listener_thread = threading.Thread(target=start_key_listener)
key_listener_thread.daemon = True
key_listener_thread.start()

# Run the task immediately
job()

# Schedule the job to run every 2 hours
schedule.every(2).hours.do(job)

# Keep the script running to continue scheduling
while True:
    schedule.run_pending()
    time.sleep(1)

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
import time
import os
import threading
import keyboard
import psutil  # Import psutil to manage system processes

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pyautogui

def select_match(driver, match_id):
    # Function to select a specific match
    # Implement your logic to select a match based on match_id
    pass


def scrape_matchinfo(driver):
    # Function to scrape match information
    match_info = {}
    # Implement your scraping logic here
    return match_info

def scrape_homepage(driver,sport,quarter_type,bet_type,date):
    # Function to scrape all text on the homepage
    rows_data = []
    columns = {
        '1': 'match_info',
        '2': 'score',
        '3': 'col_3',
        '4': 'col_4'
    }
    column_titles = {}  # To store the column titles found

    try:
        # Wait until the page loads and an element we are interested in is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ag-pinned-left-cols-container')))
        
        # Get the container with all the rows in the pinned left columns
        left_container = driver.find_element(By.CSS_SELECTOR, 'div.ag-pinned-left-cols-container')

        # Iterate through each row in the pinned left columns
        row_index = 0
        while row_index < 100:
            if logged_in(driver) == False:
                    break
            try:
                # Locate each row by row index
                left_row = left_container.find_element(By.CSS_SELECTOR, f'div[row-index="{row_index}"]')
                # Extract the text or any specific data from the row, including column index
                row_data = {'row_index': row_index}
                cells = left_row.find_elements(By.CSS_SELECTOR, 'div[aria-colindex]')
                for cell in cells:
                    col_index = cell.get_attribute('aria-colindex')
                    column_name = columns.get(col_index, f'col_{col_index}')
                    row_data[column_name] = cell.text
                rows_data.append(row_data)
                row_index += 1
            except Exception as e:
                print(f"Left container row parsing ended at index {row_index} with error: {e}")
                break

        # Now, get the container with all the rows in the center columns
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ag-center-cols-container')))
        center_container = driver.find_element(By.CSS_SELECTOR, 'div.ag-center-cols-container')

        # Iterate through each row in the center columns and merge with existing data
        for row in rows_data:
            try:
                # Locate each row by row index
                center_row = center_container.find_element(By.CSS_SELECTOR, f'div[row-index="{row["row_index"]}"]')
                # Extract the text or any specific data from the row, including column index
                cells = center_row.find_elements(By.CSS_SELECTOR, 'div[aria-colindex]')
                for cell in cells:
                    col_index = cell.get_attribute('aria-colindex')
                    column_name = columns.get(col_index, f'col_{col_index}')
                    row[column_name] = cell.text
            except Exception as e:
                print(f"Center container row parsing error for row index {row['row_index']}: {e}")
                continue

        # Get the column titles from the header starting at aria-colindex 5
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ag-header-row.ag-header-row-column')))
        header_rows = driver.find_elements(By.CSS_SELECTOR, 'div.ag-header-row.ag-header-row-column')
        
        #print("Found header rows:", len(header_rows))  # Debugging line
        for header_row in header_rows:
            headers = header_row.find_elements(By.CSS_SELECTOR, 'div[aria-colindex]')
            for header in headers:
                col_index = header.get_attribute('aria-colindex')
                if int(col_index) >= 5:
                    try:
                        # Inspect the header element
                        print(f"Inspecting header with aria-colindex {col_index}: {header.get_attribute('outerHTML')}")
                        title_element = header.find_element(By.CSS_SELECTOR, 'div[title]')
                        column_titles[col_index] = title_element.get_attribute('title')
                    except Exception as e:
                        print(f"Error finding title for col_index {col_index}: {e}")
                        column_titles[col_index] = f'col_{col_index}'
                    # Debug: Print the aria-colindex and the corresponding title
                    print(f'aria-colindex: {col_index}, title: {column_titles[col_index]}')

        # Rename the columns in the DataFrame
        df = pd.DataFrame(rows_data)
        df.rename(columns={f'col_{k}': v for k, v in column_titles.items()}, inplace=True)
        
        # Save the DataFrame to a CSV file
        df.to_csv(f'unabated-database/{sport}/{quarter_type}/{bet_type}/pregame/pregame_{sport}_{quarter_type}_{bet_type}_{date}.csv', index=False)
        print(f"Data saved to pregame_{sport}_{quarter_type}_{bet_type}_{date}.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

def print_currentpage(driver):
    # Function to scrape the current page into text and print it
    try:
        while True:
            # Wait until the page loads and an element we are interested in is present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Get all text content from the body
            body_text = driver.find_element(By.TAG_NAME, "body").text
            
            # Print the text content of the current page
            print(body_text)
            
            # Wait for 10 seconds before the next iteration
            time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_pregame(driver):
    # Function to scrape pregame odds
    pregame_odds = {}
    # Implement your scraping logic here
    return pregame_odds

def scrape_live(driver,sport,quarter_type,bet_type,date):
    # Function to scrape live odds
    all_live_data = []  # To store all parsed DataFrames

    try:
        # Wait until the page loads and the element we are interested in is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ag-center-cols-container')))
        
        # Get the container with all the rows in the center columns
        center_container = driver.find_element(By.CSS_SELECTOR, 'div.ag-center-cols-container')

        row_index = 0
        while row_index<100:
            
            try:
                # Locate each row by row index
                row = center_container.find_element(By.CSS_SELECTOR, f'div[row-index="{row_index}"]')
                
                col_index = 5
                while col_index < 100:
                    try:
                        # Locate each cell by col index
                        cell = row.find_element(By.CSS_SELECTOR, f'div[aria-colindex="{col_index}"]')
                        react_container = cell.find_element(By.CSS_SELECTOR, 'div.ag-react-container')
                        
                        # Hover over and click the cell
                        ActionChains(driver).move_to_element(react_container).click().perform()
                        
                        # Wait for the textbox to appear and parse the data
                        time.sleep(0.5)  # Adjust sleep time as needed
                        df = parse_live_lines(driver,col_index,row_index)
                        all_live_data.append(df)
                        
                        col_index += 1
                    except Exception as e:
                        print(f"End of columns for row index {row_index} with error: {e}")
                        break
                
                row_index += 1
            except Exception as e:
                print(f"End of rows reached with error: {e}")
                break

        # Concatenate all DataFrames
        final_df = pd.concat(all_live_data, ignore_index=True)
        
        # Save the final DataFrame to a CSV file
        final_df.to_csv(f'unabated-database/{sport}/{quarter_type}/{bet_type}/live/live_{sport}_{quarter_type}_{bet_type}_{date}.csv', index=False)
        print(f"Live lines data saved to live_{sport}_{quarter_type}_{bet_type}_{date}.csv")

    except Exception as e:
        print(f"An error occurred while scraping live odds: {e}")

def parse_live_lines(driver, maincol, mainrow):
    
    # Disable PyAutoGUI fail-safe feature
    pyautogui.FAILSAFE = False

    # Function to parse the live lines data
    live_data = []
    read_rows = set()  # To keep track of row indexes that have been read
    try:
        # Wait until the element we are interested in is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jsx-619290666')))
        
        # Get the container with the class jsx-619290666
        try:
            jsx_container = driver.find_element(By.CSS_SELECTOR, 'div.jsx-619290666')
            print("Found jsx_container")
        except Exception as e:
            print(f"Data container not found: {e}")
            return pd.DataFrame()  # Return an empty DataFrame if the container is not found
        
        # Click the button with id="buttonGameStatusLive"
        try:
            live_button = jsx_container.find_element(By.ID, 'buttonGameStatusLive')
            live_button.click()
            print("Clicked live_button")
            time.sleep(1)  # Wait for the data to load
        except Exception as e:
            print(f"Live button not found or not clickable: {e}")
            return pd.DataFrame()  # Return an empty DataFrame if the button is not found or not clickable

        # Wait until the element we are interested in is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ag-center-cols-container')))
        
        # Get the container with all the rows in the center columns
        center_container = jsx_container.find_element(By.CSS_SELECTOR, 'div.ag-center-cols-container')
        print("Found center_container")

        tries = 0
        
        while tries < 100:
            tries+=1
            try:
                # Locate all rows in the center container
                rows = center_container.find_elements(By.CSS_SELECTOR, 'div[role="row"]')
                for row in rows:
                    row_index = int(row.get_attribute('row-index'))
                    if row_index not in read_rows:  # Only process rows that haven't been read
                        try:
                            # Extract the data for each column
                            time_text = row.find_element(By.CSS_SELECTOR, 'div[aria-colindex="1"]').text
                            away_text = row.find_element(By.CSS_SELECTOR, 'div[aria-colindex="2"]').text
                            home_text = row.find_element(By.CSS_SELECTOR, 'div[aria-colindex="3"]').text
                            available = "Closed" if "line-through" in\
                                row.find_element(By.CSS_SELECTOR, 'div[aria-colindex="2"]').find_element(By.CSS_SELECTOR, 'span.pr-2').get_attribute("style") else "Open"
                            
                            
                            live_data.append({
                                "Time": time_text,
                                "Away": away_text,
                                "Home": home_text,
                                "Available": available,
                                "Row": f"row_{mainrow}",
                                "Column": f"col_{maincol}"
                            })
                            #print(f"Parsed row {row_index}: Time={time_text}, Away={away_text}, Home={home_text}, Available={available}, Column=col_{maincol}")
                            read_rows.add(row_index)  # Mark this row as read
                        except Exception as e:
                            print(f"Error parsing row {row_index}: {e}")
                            continue
                
                # Click at the bottom-right to load more rows
                #window_size = driver.get_window_size()
                pyautogui.click()
                print("Clicked at the bottom-right corner to load more rows")
                time.sleep(0.05)

                # Check if new rows have been loaded
                hasnewrow = False
                new_rows = center_container.find_elements(By.CSS_SELECTOR, 'div[role="row"]')
                for row in new_rows:
                    row_index = int(row.get_attribute('row-index'))
                    if row_index not in read_rows:
                        hasnewrow = True
                        
                tries += 1
                
                if (hasnewrow==False):
                    print("No new rows loaded, finishing up")
                    break  # Exit if no new rows were loaded

            except Exception as e:
                print(f"Scroll bar click failed with error: {e}")
                break

        # Click the button with class="close" to close the data table
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, 'button.close')
            close_button.click()
            print("Clicked close_button")
        except Exception as e:
            print(f"Close button not found or not clickable: {e}")

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(live_data)
        return df

    except Exception as e:
        print(f"An error occurred while parsing live lines: {e}")
        return pd.DataFrame()

import pandas as pd
import os

def merge_info(live_path='live.csv', pregame_path='pregame.csv', output_path='merged.csv'):
    print('MERGEINFO')
    try:
        # Check if the input files exist and are not empty
        if os.stat(live_path).st_size == 0 or os.stat(pregame_path).st_size == 0:
            raise ValueError("One of the input files is empty.")

        # Load the live_lines.csv and nba_matches.csv files into DataFrames
        live_df = pd.read_csv(live_path)
        pregame_df = pd.read_csv(pregame_path)

        # Strip whitespace from column names in nba_matches_df
        pregame_df.columns = pregame_df.columns.str.strip()

        # Remove double spaces and leading/trailing spaces from every cell in nba_matches_df
        pregame_df = pregame_df.applymap(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)

        #print(pregame_df.columns)  # For debugging, print the cleaned column names
        #print(live_df.columns)  # For debugging, print the cleaned column names

        # Initialize new columns in live_lines_df for match_info and score
        live_df['match_info'] = ''
        live_df['score'] = ''
        live_df['pregame'] = ''
        live_df['book'] = ''

        # Iterate through each row in live_lines_df
        for index, row in live_df.iterrows():
            try:
                # Extract row and column info from live_lines_df
                row_str = row['Row']
                col_str = row['Column']

                # Extract the row_index and col_index
                row_index = int(row_str.split('_')[1])
                col_index = int(col_str.split('_')[1])

                # Find the corresponding row in nba_matches_df
                match_info = pregame_df.loc[pregame_df['row_index'] == row_index, 'match_info'].values[0]
                score = pregame_df.loc[pregame_df['row_index'] == row_index, 'score'].values[0]

                # Find the corresponding column (e.g., col_5 -> the correct bookmaker)
                col_name = pregame_df.columns[col_index]
                pregame = pregame_df.loc[pregame_df['row_index'] == row_index, col_name].values[0]
                book = pregame_df.columns[col_index]

                # Update the live_lines_df with the matched info
                live_df.at[index, 'match_info'] = match_info
                live_df.at[index, 'score'] = score
                live_df.at[index, 'pregame'] = pregame
                live_df.at[index, 'book'] = book
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                raise

        # Apply cleaning to live_lines_df as well to remove excess spaces
        live_df = live_df.applymap(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)

        # Save the updated DataFrame to a new CSV file
        live_df.to_csv(output_path, index=False)
        print(f"Merged data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}. Saving an empty output CSV.")
        
        # Define the columns that would have been in the merged CSV
        columns = ['match_info', 'score', 'pregame', 'book', 'Time', 'Away', 'Home', 'Available', 'Row', 'Column']
        
        # Create an empty DataFrame with these columns
        empty_df = pd.DataFrame(columns=columns)
        
        # Save the empty DataFrame to the output path
        empty_df.to_csv(output_path, index=False)
        print(f"Empty merged data saved to {output_path}")

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
import time
import os
import threading
import keyboard  # Import the keyboard module for global key listening

# Global variable to control the pause state
pause_flag = False

def change_date(driver, day):
    try:
        print(f"Attempting to change date to: {day}")
        date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__input-container'))
        )
        date_picker.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'react-datepicker'))
        )
        day_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-datepicker__day') and text()='{day}' and not(contains(@class, 'react-datepicker__day--outside-month')) and not(@aria-disabled='true')]"))
        )
        day_element.click()
        print(f"Successfully changed date to: {day}")
        return True
    except TimeoutException:
        print(f"TimeoutException: Failed to find or click the date {day}.")
    except StaleElementReferenceException:
        print(f"StaleElementReferenceException: The page structure might have changed for date {day}.")
    except Exception as e:
        print(f"An error occurred while changing the date to {day}: {e}")
    return False

def go_to_next_month(driver):
    try:
        date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__input-container'))
        )
        date_picker.click()
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.react-datepicker__navigation--next"))
        )
        next_button.click()
        return True
    except Exception as e:
        print(f"Error clicking next month: {e}")
    return False

def go_to_prev_month(driver):
    try:
        date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__input-container'))
        )
        date_picker.click()
        print("Going to the previous month...")
        prev_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.react-datepicker__navigation--previous"))
        )
        prev_button.click()
        print("Moved to the previous month.")
        return True
    except Exception as e:
        print(f"Error clicking previous month: {e}")
    return False

def get_available_days(driver):
    try:
        date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__input-container'))
        )
        date_picker.click()
        available_days_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'react-datepicker__day--outside-month')) and not(@aria-disabled='true')]"))
        )
        available_days = [day.text.strip() for day in available_days_elements if day.text.strip().isdigit()]
        print(f"Found {len(available_days)} available days to scan: {available_days}")
        date_picker.click()  # Close the date picker after fetching the days
        return available_days
    except Exception as e:
        print(f"Error fetching available days: {e}")
        return []

def login(driver, email, password):
    try:
        # Locate the username (email) input field and enter the email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_input.send_keys(email)
        
        # Locate the password input field and enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(password)
        
        # Locate the "Continue" button and click it
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        continue_button.click()
        
        print("Login successful.")
        return True
    except TimeoutException:
        print("TimeoutException: Failed to locate login elements.")
    except Exception as e:
        print(f"An error occurred during login: {e}")
    return False


def select_market(driver, bet_type):
    try:
        bet_type_to_title = {
            "ml": "Moneyline",
            "spread": "Spread",
            "total": "Total",
            "combined": "Combined"
        }
        button_title = bet_type_to_title.get(bet_type.lower())
        if not button_title:
            raise ValueError(f"Invalid bet_type: {bet_type}. Must be 'ml', 'spread', 'total', or 'combined'.")
        print("Locating the second occurrence of the dropdown button...")
        dropdown_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-sm.btn-falcon-primary.dropdown-toggle.btn.btn-secondary"))
        )
        if len(dropdown_buttons) < 2:
            raise Exception("Unable to find the second dropdown button.")
        dropdown_button = dropdown_buttons[1]  # Get the second occurrence
        dropdown_button.click()
        print("Clicked the second dropdown button.")
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'dropdown-menu.show'))
        )
        print(f"Selecting the market with title '{button_title}'...")
        market_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[text()='{button_title}' and @role='menuitem']"))
        )
        market_option.click()
        print(f"Selected market: {button_title}")
        return True
    except Exception as e:
        print(f"Error selecting market: {e}")
    return False

def initialize_scraper():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    return driver

def pause_listener():
    global pause_flag
    # Use the keyboard module to listen globally for the 'p' key press
    while True:
        keyboard.wait('p')
        pause_flag = not pause_flag
        if pause_flag:
            print("Scraping paused. Press 'p' again to resume.")
        else:
            print("Scraping resumed.")
            
def logged_in(driver):
    try:
        # Check if the avatar element is present, indicating that the user is logged in
        WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'avatar.avatar-xl'))
        )
        print("User is logged in.")
        return True
    except TimeoutException:
        print("User is not logged in.")
        return False

def clear_cache_cookies(driver):
    """Clears the browser cache and cookies."""
    try:
        driver.delete_all_cookies()  # Clears all cookies
        driver.execute_cdp_cmd('Network.clearBrowserCache', {})  # Clears the cache
        print("Cache and cookies cleared.")
    except Exception as e:
        print(f"Error clearing cache and cookies: {e}")
        
def kill_chrome_processes():
    """Kill any lingering Chrome or ChromeDriver processes."""
    for proc in psutil.process_iter():
        # Check if process name contains 'chrome' or 'chromedriver'
        if 'chrome' in proc.name().lower() or 'chromedriver' in proc.name().lower():
            try:
                proc.kill()
                print(f"Killed process {proc.name()} with PID {proc.pid}")
            except psutil.NoSuchProcess:
                print(f"Process {proc.name()} with PID {proc.pid} already terminated.")
            except Exception as e:
                print(f"Error killing process {proc.name()}: {e}")




import threading
import time
import os
import signal
import sys

def restart_program():
    """
    Function to restart the program.
    """
    print("Restarting the program...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def time_limited_execution(limit_seconds=3600):
    """
    Function to terminate the program after a certain time limit.
    """
    time.sleep(limit_seconds)
    print(f"Time limit of {limit_seconds/3600} hours reached. Restarting program...")
    restart_program()
    
stop_event = threading.Event()

def main():
    while not stop_event.is_set():
        global pause_flag
        suppress_print = True  # Set to True to suppress print statements

        sport = "nba"
        bet_type = "ml"
        quarter_type = "q4"
        email = "chunkmonkey1303@gmail.com"
        password = "Chunkmonkey1303!"
        total_days_to_scan = 10000
        scanned_days = 0
        months_scan = 7
        month_position = 0

        #threading.Thread(target=pause_listener, daemon=True).start()
        #threading.Thread(target=time_limited_execution, args=(3600,), daemon=True).start()  # Set to 1 hour (3600 seconds)

        def safe_print(*args, **kwargs):
            if not suppress_print:
                print(*args, **kwargs)

        try:
            while months_scan - month_position >= 0 and scanned_days < total_days_to_scan:
                driver = initialize_scraper()
                driver.maximize_window()

                try:
                    driver.get("https://unabated.com/api/auth/login?returnTo=/nba/odds")
                    time.sleep(1)

                    login(driver, email, password)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'react-datepicker__input-container'))
                    )

                    select_market(driver, bet_type)
                    time.sleep(1)

                    for _ in range(months_scan - month_position):
                        go_to_prev_month(driver)
                        time.sleep(0.2)

                    while scanned_days < total_days_to_scan:
                        try:
                            while pause_flag:
                                time.sleep(1)

                            if not logged_in(driver):
                                driver.quit()
                                break

                            safe_print(f"Scanning for available days in month {month_position}...")

                            date_picker_input = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.datepicker.form-control.datepicker-container'))
                            )
                            current_date = date_picker_input.get_attribute('value')
                            current_month = current_date.split('/')[0]
                            date = current_date.replace("/", "-")
                            safe_print(f"Current month: {current_month}")

                            available_days = get_available_days(driver)

                            for day in available_days:
                                if not logged_in(driver):
                                    break

                                if scanned_days >= total_days_to_scan:
                                    break

                                try:
                                     # Periodically check if stop is requested
                                    if stop_event.is_set():
                                        print("Stopping scraper...")
                                        driver.quit()
                                        kill_chrome_processes() 
                                        break
                                    while pause_flag:
                                        time.sleep(1)

                                    safe_print(f"Processing day: {day}")
                                    change_date(driver, day)

                                    current_date = driver.find_element(By.CSS_SELECTOR, 'input.datepicker.form-control.datepicker-container').get_attribute('value')
                                    date = current_date.replace("/", "-")

                                    live_path=f'unabated-database/{sport}/{quarter_type}/{bet_type}/live/live_{sport}_{quarter_type}_{bet_type}_{date}.csv'
                                    merged_csv_path = f'unabated-database/{sport}/{quarter_type}/{bet_type}/merged/merged_{sport}_{quarter_type}_{bet_type}_{date}.csv'

                                    if os.path.exists(live_path) and os.path.getsize(live_path) > 50 * 1024:
                                        safe_print(f"Skipping day {day} because {live_path} is already processed and larger than 50 KB.")
                                        continue

                                    scrape_homepage(driver, sport, quarter_type, bet_type, date)

                                    if not logged_in(driver):
                                        break

                                    scrape_live(driver, sport, quarter_type, bet_type, date)

                                    if not logged_in(driver):
                                        break

                                    merge_info(
                                        live_path=f'unabated-database/{sport}/{quarter_type}/{bet_type}/live/live_{sport}_{quarter_type}_{bet_type}_{date}.csv',
                                        pregame_path=f'unabated-database/{sport}/{quarter_type}/{bet_type}/pregame/pregame_{sport}_{quarter_type}_{bet_type}_{date}.csv',
                                        output_path=f'unabated-database/{sport}/{quarter_type}/{bet_type}/merged/merged_{sport}_{quarter_type}_{bet_type}_{date}.csv'
                                    )

                                    scanned_days += 1

                                    if os.path.exists(live_path) and os.path.getsize(live_path) > 50 * 1024:
                        
                                        driver.quit()
                                        kill_chrome_processes()
                                        "restarting after processing a day"

                                except StaleElementReferenceException as e:
                                    safe_print(f"StaleElementReferenceException encountered. Retrying...")
                                    time.sleep(1)

                            if scanned_days < total_days_to_scan:
                                go_to_next_month(driver)
                                #month_position += 1

                        except Exception as e:
                            safe_print(f"Exception detected: {e}.")
                            break

                except Exception as e:
                    safe_print(f"Crash Detected. Restarting: {e}.")
                    continue

                finally:
                    driver.quit()

        except KeyboardInterrupt:
            safe_print("KeyboardInterrupt detected. Exiting the program...")

        finally:
            kill_chrome_processes()  # Ensure all Chrome processes are terminated when exiting
    print("Scraper has stopped.")
    
if __name__ == "__main__":
    main()

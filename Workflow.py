import sys
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import subprocess
# Configuration Variables - You can change these as needed
CONFIG = {
    'zipcode': '10523',
    'date_to_select': '22',
    'months_duration': '2',
    'unit_quantity': '2',
    'unit_type': '12',  # Options: '12' (3rd option) or '16' (2nd option)
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'zaryabhaider888@gmail.com',
    'phone': '5551234567'
}

main_directory = os.path.join(sys.path[0])

def open_chrome_profile():
    subprocess.Popen(
        [
            'start',
            'chrome',
            '--remote-debugging-port=8989',
            '--user-data-dir=' + os.path.join(main_directory, 'chrome_profile1')
        ],
        shell=True,
    )

def human_type(element, text, delay_min=0.05, delay_max=0.15):
    """Types text with human-like delays between characters"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(delay_min, delay_max))

def scroll_and_interact(driver):
    """Scroll down and up to help with page loading and interaction"""
    try:
        print("Performing scroll interactions...")
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Click somewhere on the document
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
        except:
            pass
        
        time.sleep(1)
    except Exception as e:
        print(f"Error during scroll interaction: {e}")

def wait_for_iframe_and_switch(driver, timeout=30):
    """Wait for iframe to appear and switch to it"""
    print("Waiting for iframe to load...")
    
    # Scroll down and up to help load the iframe faster
    print("Scrolling to help load iframe...")
    try:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Click somewhere on the document to trigger loading
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
            time.sleep(1)
        except:
            pass
        
        # Scroll down again to the form area
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error during scrolling: {e}")
    
    try:
        # Wait for the iframe to be present
        iframe = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='quote-unitsportal']"))
        )
        
        # Wait a bit more for the iframe content to load
        time.sleep(3)
        
        # Switch to iframe
        driver.switch_to.frame(iframe)
        print("Successfully switched to iframe")
        return True
    except Exception as e:
        print(f"Failed to find or switch to iframe: {e}")
        return False

def fill_quote_form(driver):
    """Fill out the entire quote form"""
    try:
        # Step 1: Click Storage Quote button
        print("Clicking Storage Quote button...")
        storage_quote_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[1]/div/div/div[2]/div/div/div[1]/button"))
        )
        storage_quote_btn.click()
        time.sleep(2)

        # Step 2: Click Your Location button
        print("Clicking Your Location button...")
        your_location_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/button"))
        )
        your_location_btn.click()
        time.sleep(2)
        
        # Step 3: Enter zipcode
        print(f"Entering zipcode: {CONFIG['zipcode']}")
        zipcode_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/form/div[1]/div[3]/div/input"))
        )
        zipcode_input.clear()
        human_type(zipcode_input, CONFIG['zipcode'])
        time.sleep(1)
        
        # Step 4: Select Date Needed
        print(f"Selecting date: {CONFIG['date_to_select']}")
        date_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/form/div[4]/div[1]/div[1]/div[1]/div/div/input"))
        )
        date_dropdown.click()
        time.sleep(2)
        
        # Try multiple methods to select the date
        date_selected = False
        
        # Method 1: Try to find date with various selectors
        try:
            # Try different possible selectors for date options
            selectors_to_try = [
                f"//div[contains(@class, 'date-option') and text()='{CONFIG['date_to_select']}']",
                f"//span[text()='{CONFIG['date_to_select']}']",
                f"//div[text()='{CONFIG['date_to_select']}']",
                f"//button[text()='{CONFIG['date_to_select']}']",
                f"//*[text()='{CONFIG['date_to_select']}']"
            ]
            
            for selector in selectors_to_try:
                try:
                    date_option = driver.find_element(By.XPATH, selector)
                    date_option.click()
                    print(f"Date selected using selector: {selector}")
                    date_selected = True
                    break
                except:
                    continue
        except:
            pass
        
        # Method 2: If date selection failed, try typing
        if not date_selected:
            try:
                date_dropdown.clear()
                human_type(date_dropdown, CONFIG['date_to_select'])
                # Try pressing Enter or Tab to confirm
                date_dropdown.send_keys(Keys.TAB)
                print(f"Date typed: {CONFIG['date_to_select']}")
                date_selected = True
            except:
                pass
        
        # Method 3: If still failed, try clicking outside and retry
        if not date_selected:
            try:
                # Click somewhere else to close dropdown
                driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(1)
                
                # Try clicking dropdown again
                date_dropdown.click()
                time.sleep(1)
                
                # Try typing again
                date_dropdown.clear()
                human_type(date_dropdown, CONFIG['date_to_select'])
                date_dropdown.send_keys(Keys.ENTER)
                print(f"Date selected on retry: {CONFIG['date_to_select']}")
            except:
                print(f"Warning: Could not select date {CONFIG['date_to_select']}")
        
        time.sleep(2)
        
        # Step 5: Select months duration
        print(f"Selecting months duration: {CONFIG['months_duration']}")
        months_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/form/div[4]/div[1]/div[1]/div[2]/div/select"))
        )
        months_select = Select(months_dropdown)
        months_select.select_by_value(CONFIG['months_duration'])
        time.sleep(1)
        
        # Step 6: Select unit quantity
        print(f"Selecting unit quantity: {CONFIG['unit_quantity']}")
        unit_qty_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/form/div[4]/div[1]/div[2]/div[2]/div/select"))
        )
        unit_qty_select = Select(unit_qty_dropdown)
        unit_qty_select.select_by_value(CONFIG['unit_quantity'])
        time.sleep(1)
        
        # Step 7: Select unit type
        print(f"Selecting unit type: {CONFIG['unit_type']} ft")
        unit_type_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/form/div[4]/div[1]/div[2]/div[1]/div/select"))
        )
        unit_type_select = Select(unit_type_dropdown)
        
        # Try different methods to select unit type
        unit_selected = False
        
        # Method 1: Try selecting by value
        try:
            unit_type_select.select_by_value(CONFIG['unit_type'])
            print(f"Unit type selected by value: {CONFIG['unit_type']}")
            unit_selected = True
        except:
            pass
        
        # Method 2: If value selection failed, try by index
        if not unit_selected:
            try:
                # Based on your description:
                # 1st option: Not an option (index 0)
                # 2nd option: 16 Ft (index 1) 
                # 3rd option: 12 Ft (index 2)
                if CONFIG['unit_type'] == '12':
                    unit_type_select.select_by_index(2)  # Select 3rd option (12 Ft)
                    print("Unit type selected by index: 12 Ft (3rd option)")
                    unit_selected = True
                elif CONFIG['unit_type'] == '16':
                    unit_type_select.select_by_index(1)  # Select 2nd option (16 Ft)
                    print("Unit type selected by index: 16 Ft (2nd option)")
                    unit_selected = True
            except:
                pass
        
        # Method 3: Try selecting by visible text
        if not unit_selected:
            try:
                options = unit_type_select.options
                for i, option in enumerate(options):
                    if CONFIG['unit_type'] in option.text:
                        unit_type_select.select_by_index(i)
                        print(f"Unit type selected by text match: {option.text}")
                        unit_selected = True
                        break
            except:
                pass
        
        # Method 4: Print available options for debugging
        if not unit_selected:
            try:
                options = unit_type_select.options
                print("Available unit type options:")
                for i, option in enumerate(options):
                    print(f"Index {i}: {option.text} (value: {option.get_attribute('value')})")
                
                # Try selecting the last option as fallback
                if len(options) > 2:
                    unit_type_select.select_by_index(2)
                    print("Fallback: Selected 3rd option (assuming it's 12 Ft)")
                elif len(options) > 1:
                    unit_type_select.select_by_index(1)
                    print("Fallback: Selected 2nd option")
            except Exception as e:
                print(f"Warning: Could not select unit type: {e}")
        
        time.sleep(1)
        
        # Step 8: Click Next button
        print("Clicking Next button...")
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[4]/div/div[2]/div/div[2]/button"))
        )
        next_btn.click()
        time.sleep(2)
        
        # Step 9: Fill personal information
        print("Filling personal information...")
        
        # First Name
        first_name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[5]/div/div[2]/form/div/div[1]/div/input"))
        )
        first_name_input.clear()
        human_type(first_name_input, CONFIG['first_name'])
        time.sleep(0.5)
        
        # Last Name
        last_name_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[5]/div/div[2]/form/div/div[2]/div/input")
        last_name_input.clear()
        human_type(last_name_input, CONFIG['last_name'])
        time.sleep(0.5)
        
        # Email
        email_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[5]/div/div[2]/form/div/div[3]/div/input")
        email_input.clear()
        human_type(email_input, CONFIG['email'])
        time.sleep(0.5)
        
        # Phone Number
        phone_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[5]/div/div[2]/form/div/div[4]/div/input")
        phone_input.clear()
        human_type(phone_input, CONFIG['phone'])
        time.sleep(1)
        
        # Step 10: Click Get Your Quote button
        print("Clicking Get Your Quote button...")
        get_quote_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[10]/div/div[2]/div[5]/div/div[2]/div/div[2]/button"))
        )
        get_quote_btn.click()
        
        print("Quote form submitted successfully!")
        time.sleep(3)
        
    except Exception as e:
        print(f"Error filling quote form: {e}")
        return False
    
    return True

def clear_browser_data(driver):
    """Clear browsing history and cookies"""
    try:
        print("Clearing browser data...")
        
        # Method 1: Clear via JavaScript
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
        # Method 2: Delete all cookies
        driver.delete_all_cookies()
        
        # Method 3: Navigate to chrome://settings/clearBrowserData and clear
        driver.get("chrome://settings/clearBrowserData")
        time.sleep(3)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "settings-ui"))
        )
        time.sleep(2)
        
        # Click on Advanced tab first
        try:
            # Try different selectors for the Advanced tab
            advanced_selectors = [
                "//div[@id='advancedRadioButton']",
                "//cr-button[@id='advancedRadioButton']",
                "//*[contains(text(), 'Advanced')]",
                "//paper-tab[contains(text(), 'Advanced')]",
                "//div[contains(@class, 'tab') and contains(text(), 'Advanced')]"
            ]
            
            advanced_clicked = False
            for selector in advanced_selectors:
                try:
                    advanced_tab = driver.find_element(By.XPATH, selector)
                    driver.execute_script("arguments[0].click();", advanced_tab)
                    print("Advanced tab clicked")
                    advanced_clicked = True
                    time.sleep(2)
                    break
                except:
                    continue
            
            if not advanced_clicked:
                print("Could not find Advanced tab, proceeding with Basic")
        except:
            print("Advanced tab not found, using Basic settings")
        
        # Select all available checkboxes for data clearing
        try:
            # Wait a bit for checkboxes to load
            time.sleep(2)
            
            # Try different methods to find and select checkboxes
            checkbox_selectors = [
                "input[type='checkbox']",
                "cr-checkbox",
                "[role='checkbox']",
                "paper-checkbox"
            ]
            
            checkboxes_found = False
            for selector in checkbox_selectors:
                try:
                    checkboxes = driver.find_elements(By.CSS_SELECTOR, selector)
                    if checkboxes:
                        print(f"Found {len(checkboxes)} checkboxes with selector: {selector}")
                        for i, checkbox in enumerate(checkboxes):
                            try:
                                # Check if checkbox is not already selected
                                is_checked = checkbox.get_attribute("checked") or checkbox.get_attribute("aria-checked") == "true"
                                if not is_checked:
                                    driver.execute_script("arguments[0].click();", checkbox)
                                    print(f"Checkbox {i+1} selected")
                                    time.sleep(0.5)
                            except Exception as e:
                                print(f"Could not click checkbox {i+1}: {e}")
                        checkboxes_found = True
                        break
                except:
                    continue
            
            if not checkboxes_found:
                print("No checkboxes found with standard selectors")
                
        except Exception as e:
            print(f"Error selecting checkboxes: {e}")
        
        # Set time range to "All time" if possible
        try:
            time_range_selectors = [
                "select[aria-label*='time']",
                "#timeRangeSelect",
                "//select[contains(@aria-label, 'Time range')]",
                "//cr-dropdown-menu"
            ]
            
            for selector in time_range_selectors:
                try:
                    if selector.startswith("//"):
                        time_range = driver.find_element(By.XPATH, selector)
                    else:
                        time_range = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    driver.execute_script("arguments[0].click();", time_range)
                    time.sleep(1)
                    
                    # Try to select "All time" option
                    all_time_options = [
                        "//iron-dropdown//paper-item[contains(text(), 'All time')]",
                        "//option[contains(text(), 'All time')]",
                        "//*[contains(text(), 'All time')]"
                    ]
                    
                    for option_selector in all_time_options:
                        try:
                            all_time_option = driver.find_element(By.XPATH, option_selector)
                            driver.execute_script("arguments[0].click();", all_time_option)
                            print("Selected 'All time' for time range")
                            break
                        except:
                            continue
                    break
                except:
                    continue
        except:
            print("Could not set time range to 'All time'")
        
        time.sleep(2)
        
        # Click Clear Data button
        try:
            clear_button_selectors = [
                "#clearBrowsingDataConfirm",
                "//cr-button[@id='clearBrowsingDataConfirm']",
                "//paper-button[contains(text(), 'Clear data')]",
                "//cr-button[contains(text(), 'Clear data')]",
                "//*[contains(text(), 'Clear data') or contains(text(), 'Delete data')]",
                "//button[contains(text(), 'Clear') or contains(text(), 'Delete')]"
            ]
            
            clear_clicked = False
            for selector in clear_button_selectors:
                try:
                    if selector.startswith("//"):
                        clear_button = driver.find_element(By.XPATH, selector)
                    else:
                        clear_button = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    driver.execute_script("arguments[0].click();", clear_button)
                    print("Clear data button clicked")
                    clear_clicked = True
                    time.sleep(3)
                    break
                except:
                    continue
            
            if not clear_clicked:
                print("Could not find Clear data button")
                
        except Exception as e:
            print(f"Error clicking clear button: {e}")
        
        # Wait for clearing to complete
        time.sleep(5)
        print("Browser data clearing completed!")
        
    except Exception as e:
        print(f"Error clearing browser data: {e}")

def main():
    opt = Options()
    opt.add_experimental_option(name='debuggerAddress', value='localhost:8989')
    driver = webdriver.Chrome(options=opt)
    
    try:
        # Navigate to the website
        print("Navigating to Units Storage website...")
        driver.get('https://unitsstorage.com/')
        time.sleep(3)
        
        # Wait for iframe and switch to it
        if wait_for_iframe_and_switch(driver):
            # Fill the quote form
            success = fill_quote_form(driver)
            
            if success:
                print("Form filling completed successfully!")
                # Switch back to main content
                driver.switch_to.default_content()
                
                # Perform scroll interactions after form completion
                scroll_and_interact(driver)
            else:
                print("Form filling failed!")
        else:
            print("Could not find iframe!")
        
        # Ask user if they want to clear browser data
        print("\nPress Enter to clear browser data, or type 'skip' to skip clearing:")
        user_input = input().strip().lower()
        
        if user_input != 'skip':
            clear_browser_data(driver)
        
        print("Script completed. Browser will remain open for manual inspection.")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    # Keep browser open for inspection
    input("Press Enter to close the browser...")
    driver.quit()

# Start the Chrome profile first
open_chrome_profile()
time.sleep(5)  # Wait for Chrome to start

# Run the main automation
if __name__ == "__main__":
    main()
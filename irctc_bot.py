"""
IRCTC Tatkal Booking Bot
Automates the process of logging in, searching trains, booking tickets, and making payments
"""

import time
import json
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IRCTCBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
        
    def setup_driver(self):
        """Initialize the Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            
            if config.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable images and CSS for faster loading
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            if config.CHROME_DRIVER_PATH:
                self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(config.CHROME_DRIVER_PATH), options=chrome_options)
            else:
                self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, config.IMPLICIT_WAIT)
            
            logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize driver: {str(e)}")
            raise

    def login(self):
        """Login to IRCTC website"""
        try:
            logger.info("Opening IRCTC website...")
            self.driver.get("https://www.irctc.co.in/nget/train-search")
            
            # Wait for page to load and click login
            time.sleep(3)
            
            # Handle popup if exists
            try:
                popup_close = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modalClose")))
                popup_close.click()
                time.sleep(1)
            except TimeoutException:
                pass
            
            # Click on login button
            login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'LOGIN')]")))
            login_btn.click()
            
            logger.info("Entering login credentials...")
            
            # Enter username
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='User Name']")))
            username_field.clear()
            username_field.send_keys(config.IRCTC_USERNAME)
            
            # Enter password
            password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
            password_field.clear()
            password_field.send_keys(config.IRCTC_PASSWORD)
            
            # Handle captcha (manual intervention required)
            input("Please solve the captcha manually and press Enter to continue...")
            
            # Click sign in
            signin_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'SIGN IN')]")
            signin_btn.click()
            
            # Wait for successful login
            time.sleep(5)
            
            # Check if login was successful
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Hi')]")))
                logger.info("Login successful!")
                return True
            except TimeoutException:
                logger.error("Login failed or took too long")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def search_trains(self):
        """Search for trains between source and destination"""
        try:
            logger.info(f"Searching trains from {config.FROM_STATION} to {config.TO_STATION}")
            
            # Enter FROM station
            from_station = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From*']")))
            from_station.clear()
            from_station.send_keys(config.FROM_STATION)
            time.sleep(2)
            
            # Select first suggestion
            first_suggestion = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ng-star-inserted'][1]")))
            first_suggestion.click()
            
            # Enter TO station
            to_station = self.driver.find_element(By.XPATH, "//input[@placeholder='To*']")
            to_station.clear()
            to_station.send_keys(config.TO_STATION)
            time.sleep(2)
            
            # Select first suggestion for destination
            dest_suggestion = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ng-star-inserted'][1]")))
            dest_suggestion.click()
            
            # Select journey date
            date_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Journey Date(DD/MM/YYYY)']")
            date_field.clear()
            date_field.send_keys(config.JOURNEY_DATE)
            
            # Select journey class
            class_dropdown = self.driver.find_element(By.XPATH, "//select[@formcontrolname='journeyClass']")
            select_class = Select(class_dropdown)
            select_class.select_by_value(config.JOURNEY_CLASS)
            
            # Click search
            search_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
            search_btn.click()
            
            logger.info("Train search initiated...")
            time.sleep(5)
            
            return True
            
        except Exception as e:
            logger.error(f"Train search failed: {str(e)}")
            return False

    def select_train_and_book(self):
        """Select available train and proceed to booking"""
        try:
            # Wait for train list to load
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "train-list")))
            
            # Look for Tatkal available trains
            trains = self.driver.find_elements(By.XPATH, "//div[@class='train-list']//div[@class='row']")
            
            for train in trains:
                try:
                    # Check if train has the preferred number (if specified)
                    if config.TRAIN_PREFERENCE:
                        train_number = train.find_element(By.XPATH, ".//div[@class='train-number']").text
                        if config.TRAIN_PREFERENCE not in train_number:
                            continue
                    
                    # Look for available Tatkal quota
                    tatkal_btn = train.find_element(By.XPATH, f".//td[contains(@class, '{config.JOURNEY_CLASS}')]//button[contains(text(),'BOOK NOW')]")
                    
                    if tatkal_btn.is_enabled():
                        logger.info("Found available Tatkal seat, clicking book now...")
                        tatkal_btn.click()
                        time.sleep(3)
                        return True
                        
                except NoSuchElementException:
                    continue
            
            logger.warning("No Tatkal seats available in the preferred class")
            return False
            
        except Exception as e:
            logger.error(f"Train selection failed: {str(e)}")
            return False

    def fill_passenger_details(self):
        """Fill passenger details for booking"""
        try:
            logger.info("Filling passenger details...")
            
            for i, passenger in enumerate(config.PASSENGERS):
                # Fill passenger name
                name_field = self.driver.find_element(By.XPATH, f"//input[@placeholder='Passenger Name {i+1}']")
                name_field.clear()
                name_field.send_keys(passenger['name'])
                
                # Select age
                age_field = self.driver.find_element(By.XPATH, f"//input[@placeholder='Age {i+1}']")
                age_field.clear()
                age_field.send_keys(str(passenger['age']))
                
                # Select gender
                gender_dropdown = Select(self.driver.find_element(By.XPATH, f"//select[@formcontrolname='passengerGender{i+1}']"))
                gender_dropdown.select_by_value(passenger['gender'])
                
                # Select berth preference
                berth_dropdown = Select(self.driver.find_element(By.XPATH, f"//select[@formcontrolname='berthChoice{i+1}']"))
                berth_dropdown.select_by_value(passenger['berth_preference'])
                
                # Select food choice
                food_dropdown = Select(self.driver.find_element(By.XPATH, f"//select[@formcontrolname='foodChoice{i+1}']"))
                food_dropdown.select_by_value(passenger['food_choice'])
                
                # Fill ID details
                id_type_dropdown = Select(self.driver.find_element(By.XPATH, f"//select[@formcontrolname='idType{i+1}']"))
                id_type_dropdown.select_by_visible_text(passenger['id_card_type'])
                
                id_number_field = self.driver.find_element(By.XPATH, f"//input[@placeholder='ID Number {i+1}']")
                id_number_field.clear()
                id_number_field.send_keys(passenger['id_card_number'])
            
            # Accept terms and conditions
            terms_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not terms_checkbox.is_selected():
                terms_checkbox.click()
            
            # Click continue
            continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
            continue_btn.click()
            
            logger.info("Passenger details filled successfully")
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Failed to fill passenger details: {str(e)}")
            return False

    def make_payment(self):
        """Handle payment process"""
        try:
            logger.info("Processing payment...")
            
            # Select payment method
            if config.PAYMENT_METHOD == "UPI":
                upi_radio = self.driver.find_element(By.XPATH, "//input[@value='UPI']")
                upi_radio.click()
                
                upi_id_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter UPI ID']")
                upi_id_field.send_keys(config.UPI_ID)
                
            elif config.PAYMENT_METHOD == "DEBIT_CARD":
                card_radio = self.driver.find_element(By.XPATH, "//input[@value='DEBIT_CARD']")
                card_radio.click()
                
                # Fill card details
                card_number_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Card Number']")
                card_number_field.send_keys(config.CARD_NUMBER)
                
                expiry_month = Select(self.driver.find_element(By.XPATH, "//select[@name='expiryMonth']"))
                expiry_month.select_by_value(config.CARD_EXPIRY_MONTH)
                
                expiry_year = Select(self.driver.find_element(By.XPATH, "//select[@name='expiryYear']"))
                expiry_year.select_by_value(config.CARD_EXPIRY_YEAR)
                
                cvv_field = self.driver.find_element(By.XPATH, "//input[@placeholder='CVV']")
                cvv_field.send_keys(config.CARD_CVV)
                
                cardholder_name = self.driver.find_element(By.XPATH, "//input[@placeholder='Cardholder Name']")
                cardholder_name.send_keys(config.CARD_HOLDER_NAME)
            
            # Click make payment
            pay_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Make Payment')]")
            pay_btn.click()
            
            logger.info("Payment initiated. Please complete the payment process manually if required.")
            
            # Wait for payment completion (manual intervention may be required)
            input("Please complete the payment process and press Enter when done...")
            
            return True
            
        except Exception as e:
            logger.error(f"Payment process failed: {str(e)}")
            return False

    def wait_for_tatkal_time(self):
        """Wait until Tatkal booking time (10:00 AM or 11:00 AM)"""
        current_time = datetime.now()
        tatkal_time = datetime.strptime(config.TATKAL_TIME, "%H:%M").time()
        tatkal_datetime = datetime.combine(current_time.date(), tatkal_time)
        
        if current_time.time() < tatkal_time:
            wait_seconds = (tatkal_datetime - current_time).total_seconds()
            logger.info(f"Waiting {wait_seconds:.0f} seconds until Tatkal time ({config.TATKAL_TIME})")
            time.sleep(wait_seconds)
        
        logger.info("Tatkal booking time reached!")

    def run_booking_process(self):
        """Main method to run the complete booking process"""
        try:
            logger.info("Starting IRCTC Tatkal booking process...")
            
            # Step 1: Login
            if not self.login():
                logger.error("Login failed. Exiting...")
                return False
            
            # Step 2: Wait for Tatkal time (if needed)
            self.wait_for_tatkal_time()
            
            # Step 3: Search trains
            if not self.search_trains():
                logger.error("Train search failed. Exiting...")
                return False
            
            # Step 4: Select train and book
            attempt = 1
            while attempt <= config.BOOKING_ATTEMPTS:
                logger.info(f"Booking attempt {attempt}/{config.BOOKING_ATTEMPTS}")
                
                if self.select_train_and_book():
                    # Step 5: Fill passenger details
                    if self.fill_passenger_details():
                        # Step 6: Make payment
                        if self.make_payment():
                            logger.info("Booking completed successfully!")
                            return True
                        else:
                            logger.error("Payment failed")
                            return False
                    else:
                        logger.error("Failed to fill passenger details")
                        return False
                else:
                    logger.warning(f"Booking attempt {attempt} failed. Retrying...")
                    attempt += 1
                    time.sleep(2)
                    
                    # Refresh the page and search again
                    self.driver.refresh()
                    time.sleep(3)
                    self.search_trains()
            
            logger.error("All booking attempts failed")
            return False
            
        except Exception as e:
            logger.error(f"Booking process failed: {str(e)}")
            return False
        
        finally:
            # Keep browser open for manual verification
            input("Press Enter to close the browser...")
            self.close()

    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

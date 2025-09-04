#!/usr/bin/env python3
"""
WiFi Hotspot Auto-Connect Agent
Automatically connects to WiFi hotspots and handles captive portal authentication.
"""

import json
import logging
import os
import subprocess
import sys
import time
from typing import Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WiFiHotspotAgent:
    """Main class for WiFi hotspot automation."""
    
    def __init__(self, config_file: str = "wifi_config.json", headless: bool = None):
        """Initialize the WiFi agent with configuration.
        
        Args:
            config_file: Path to the configuration file
            headless: If True, run browser invisibly. If False, show browser for debugging.
                     If None, read from config file.
        """
        self.config_file = config_file
        self.setup_logging()
        self.config = self._load_config()
        
        # Set headless mode from config if not specified
        if headless is None:
            self.headless = self.config.get('headless_browser', True)
        else:
            self.headless = headless
            
        # Override with debug mode if enabled (but respect headless_browser setting)
        if self.config.get('debug_mode', False) and not self.config.get('headless_browser', True):
            self.headless = False
            self.logger.info("Debug mode enabled - browser will be visible")
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('wifi_agent.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file {self.config_file} not found!")
            self.logger.error("Please copy wifi_config_template.json to wifi_config.json and configure it.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            sys.exit(1)
            
    def get_available_networks(self) -> List[str]:
        """Get list of available WiFi networks."""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'profiles'],
                capture_output=True,
                text=True,
                check=True
            )
            
            networks = []
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    network = line.split(':')[1].strip()
                    networks.append(network)
                    
            self.logger.info(f"Found {len(networks)} available networks")
            return networks
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get WiFi networks: {e}")
            return []
            
    def connect_to_network(self, ssid: str) -> bool:
        """Connect to a specific WiFi network."""
        try:
            self.logger.info(f"Attempting to connect to {ssid}")
            
            # Try to connect to the network
            result = subprocess.run(
                ['netsh', 'wlan', 'connect', f'name={ssid}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Wait a moment for connection
            time.sleep(5)
            
            # Check if connection was successful
            if self._is_connected_to_network(ssid):
                self.logger.info(f"Successfully connected to {ssid}")
                return True
            else:
                self.logger.warning(f"Failed to connect to {ssid}")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error connecting to {ssid}: {e}")
            return False
            
    def _is_connected_to_network(self, ssid: str) -> bool:
        """Check if currently connected to a specific network."""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True,
                text=True,
                check=True
            )
            
            return ssid in result.stdout
            
        except subprocess.CalledProcessError:
            return False
            
    def check_internet_connectivity(self) -> bool:
        """Check if internet is accessible."""
        import requests
        
        test_urls = [
            'http://www.google.com',  # Use HTTP first for captive portal detection
            'https://8.8.8.8',
            'https://1.1.1.1',
            'https://www.google.com'
        ]
        
        for url in test_urls:
            try:
                self.logger.debug(f"Testing connectivity to {url}")
                response = requests.get(url, timeout=3, allow_redirects=False)
                self.logger.debug(f"Response status: {response.status_code}")
                if response.status_code == 200:
                    self.logger.info(f"Internet connectivity confirmed via {url}")
                    return True
            except Exception as e:
                self.logger.debug(f"Failed to connect to {url}: {e}")
                continue
                
        self.logger.info("No internet connectivity detected")
        return False
        
    def _try_local_driver(self) -> Optional[Service]:
        """Try to use the local ChromeDriver in the current directory."""
        import os
        
        try:
            self.logger.info("Trying local ChromeDriver...")
            
            # Local ChromeDriver in the same directory as the script
            local_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
            
            if os.path.exists(local_path):
                self.logger.info(f"Found local ChromeDriver at: {local_path}")
                return Service(local_path)
            else:
                self.logger.warning(f"Local ChromeDriver not found at: {local_path}")
                return None
                
        except Exception as e:
            self.logger.warning(f"Error with local ChromeDriver: {e}")
            return None
        
    def _try_webdriver_manager(self) -> Optional[Service]:
        """Try to use webdriver-manager to get Chrome driver."""
        try:
            self.logger.info("Trying webdriver-manager...")
            driver_path = ChromeDriverManager().install()
            return Service(driver_path)
        except Exception as e:
            self.logger.warning(f"WebDriver manager failed: {e}")
            # Try to find cached driver manually
            return self._try_cached_driver()
    
    def _try_cached_driver(self) -> Optional[Service]:
        """Try to find cached Chrome driver from webdriver-manager."""
        import os
        import glob
        
        try:
            self.logger.info("Searching for cached Chrome driver...")
            
            # Common cache locations for webdriver-manager
            cache_paths = [
                os.path.expanduser("~/.wdm/drivers/chromedriver"),
                os.path.expanduser("~/.cache/selenium/chromedriver"),
                os.path.join(os.getcwd(), ".wdm", "drivers", "chromedriver")
            ]
            
            for cache_path in cache_paths:
                if os.path.exists(cache_path):
                    # Find the latest version
                    version_dirs = glob.glob(os.path.join(cache_path, "*", "*"))
                    if version_dirs:
                        latest_dir = max(version_dirs, key=os.path.getmtime)
                        driver_files = glob.glob(os.path.join(latest_dir, "**", "chromedriver.exe"), recursive=True)
                        if driver_files:
                            driver_path = driver_files[0]
                            self.logger.info(f"Found cached driver at: {driver_path}")
                            return Service(driver_path)
            
            self.logger.warning("No cached Chrome driver found")
            return None
            
        except Exception as e:
            self.logger.warning(f"Error searching for cached driver: {e}")
            return None
    
    def _try_system_chromedriver(self) -> Optional[Service]:
        """Try to use system Chrome driver."""
        try:
            self.logger.info("Trying system Chrome driver...")
            return Service()  # Let Selenium find chromedriver in PATH
        except Exception as e:
            self.logger.warning(f"System Chrome driver failed: {e}")
            return None
    
    def _try_chromedriver_in_path(self) -> Optional[Service]:
        """Try to find chromedriver in common locations."""
        import shutil
        
        try:
            self.logger.info("Searching for chromedriver in PATH...")
            chromedriver_path = shutil.which('chromedriver')
            if chromedriver_path:
                self.logger.info(f"Found chromedriver at: {chromedriver_path}")
                return Service(chromedriver_path)
            else:
                self.logger.warning("chromedriver not found in PATH")
                return None
        except Exception as e:
            self.logger.warning(f"PATH search failed: {e}")
            return None
        
    def handle_captive_portal(self, hotspot_config: Dict) -> bool:
        """Handle captive portal authentication."""
        self.logger.info(f"Handling captive portal for {hotspot_config['ssid']}")
        
        try:
            # Setup Chrome driver with multiple fallback options
            service = None
            driver = None
            
            # Try multiple approaches to get Chrome driver
            driver_attempts = [
                self._try_local_driver,
                self._try_webdriver_manager,
                self._try_system_chromedriver,
                self._try_chromedriver_in_path
            ]
            
            for attempt_func in driver_attempts:
                try:
                    service = attempt_func()
                    if service:
                        break
                except Exception as e:
                    self.logger.debug(f"Driver attempt failed: {e}")
                    continue
            
            if not service:
                raise Exception("Could not initialize Chrome driver with any method")
            
            options = webdriver.ChromeOptions()
            
            # Always add these basic options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-web-security')  # Disable web security for captive portals
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if self.headless:
                # Headless mode options
                options.add_argument('--headless')  # Run browser invisibly
                options.add_argument('--disable-gpu')  # Disable GPU for headless mode
                options.add_argument('--window-size=1920,1080')  # Set window size for headless
                options.add_argument('--disable-extensions')  # Disable extensions for headless
                options.add_argument('--disable-plugins')  # Disable plugins for headless
                options.add_argument('--disable-images')  # Disable images for faster loading
                options.add_argument('--disable-background-timer-throttling')
                options.add_argument('--disable-backgrounding-occluded-windows')
                options.add_argument('--disable-renderer-backgrounding')
                options.add_argument('--disable-features=TranslateUI')
                options.add_argument('--disable-ipc-flooding-protection')
                options.add_argument('--hide-scrollbars')
                options.add_argument('--mute-audio')
                self.logger.info("Running browser in headless (invisible) mode")
            else:
                # Visible mode options
                options.add_argument('--window-size=1200,800')  # Reasonable window size for visible mode
                self.logger.info("Running browser in visible mode for debugging")
            
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 1)
            
            # Navigate to a test page to trigger captive portal
            driver.get("http://www.google.com")
            time.sleep(1)
            
            # Check if we're redirected to a captive portal
            current_url = driver.current_url
            self.logger.info(f"Current URL: {current_url}")
            
            if hotspot_config['login_type'] == 'bt_business':
                success = self._handle_bt_business_login(driver, wait, hotspot_config)
            elif hotspot_config['login_type'] == 'form_based':
                success = self._handle_form_based_login(driver, wait, hotspot_config)
            elif hotspot_config['login_type'] == 'click_through':
                success = self._handle_click_through_login(driver, wait)
            else:
                self.logger.error(f"Unknown login type: {hotspot_config['login_type']}")
                success = False
                
            driver.quit()
            return success
            
        except Exception as e:
            self.logger.error(f"Error handling captive portal: {e}")
            return False
            
    def _handle_bt_business_login(self, driver, wait, config) -> bool:
        """Handle BT Business Broadband login flow."""
        try:
            self.logger.info("Starting BT Business login flow")
            
            # Take a screenshot for debugging
            try:
                driver.save_screenshot("captive_portal_debug.png")
                self.logger.info("Screenshot saved as captive_portal_debug.png")
            except:
                pass
            
            # Wait a bit for page to load
            time.sleep(0.5)
            
            # Accept cookies if present - handle EE WiFi cookie banner
            try:
                cookie_selectors = [
                    "//button[contains(@class, 'btn--acceptAll')]",
                    "//button[contains(text(), 'Accept all cookies')]",
                    "//button[contains(text(), 'OK')]",
                    "//button[contains(text(), 'Accept')]",
                    "//button[contains(text(), 'Accept All')]",
                    "//button[contains(text(), 'I Accept')]",
                    "//a[contains(text(), 'Accept')]"
                ]
                
                for selector in cookie_selectors:
                    try:
                        cookie_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        cookie_button.click()
                        self.logger.info("Clicked cookie acceptance button")
                        time.sleep(0.5)
                        break
                    except:
                        continue
            except:
                pass
                
            # Click "Log in now" button - use specific ID from EE WiFi
            try:
                login_selectors = [
                    "//a[@id='customer-login']",
                    "//button[contains(text(), 'Log in now')]",
                    "//button[contains(text(), 'Login')]",
                    "//button[contains(text(), 'Sign in')]",
                    "//a[contains(text(), 'Log in')]",
                    "//a[contains(text(), 'Login')]"
                ]
                
                for selector in login_selectors:
                    try:
                        login_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        login_button.click()
                        self.logger.info("Clicked login button")
                        time.sleep(0.5)
                        break
                    except:
                        continue
            except:
                pass
                
            # Select BT Business Broadband tab - use specific ID from EE WiFi
            try:
                bt_selectors = [
                    "//button[@id='customer-login-btbb']",
                    "//button[contains(text(), 'BT Business Broadband')]",
                    "//button[contains(text(), 'BT Business')]",
                    "//a[contains(text(), 'BT Business')]",
                    "//div[contains(text(), 'BT Business')]"
                ]
                
                for selector in bt_selectors:
                    try:
                        bt_tab = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        bt_tab.click()
                        self.logger.info("Clicked BT Business tab")
                        time.sleep(0.5)
                        break
                    except:
                        continue
            except:
                pass
                
            # For BT Business Broadband, just click the submit button (no email/password fields)
            try:
                submit_selectors = [
                    "//input[@id='submit-btb']",
                    "//button[contains(text(), 'Click here to log in')]",
                    "//input[@type='submit']",
                    "//button[@type='submit']",
                    "//button[contains(text(), 'Log in')]",
                    "//button[contains(text(), 'Sign in')]",
                    "//button[contains(text(), 'Login')]"
                ]
                
                submit_clicked = False
                for selector in submit_selectors:
                    try:
                        submit_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        submit_button.click()
                        self.logger.info(f"Clicked submit button using selector: {selector}")
                        submit_clicked = True
                        time.sleep(0.5)
                        break
                    except:
                        continue
                
                if not submit_clicked:
                    self.logger.error("Could not find submit button with any selector")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Error clicking submit button: {e}")
                return False
            
            # After clicking submit, wait for page to load and handle any additional steps
            self.logger.info("Waiting for page to load after submit...")
            time.sleep(0.5)  # Reduced time for page transition
            
            # Take another screenshot to see what page we're on now
            try:
                driver.save_screenshot("after_submit_debug.png")
                self.logger.info("Screenshot saved as after_submit_debug.png")
            except:
                pass
            
            # Check current URL to see if we were redirected
            current_url = driver.current_url
            self.logger.info(f"Current URL after submit: {current_url}")
            
            # Check if we're on a different domain (likely redirected to BT login)
            if "bt.com" in current_url or "btbusiness" in current_url or "saf" in current_url or "auth.bt.com" in current_url:
                self.logger.info("Redirected to BT login page - this is expected for BT Business")
                
                # Wait for the page to fully load
                time.sleep(3)
                
                # Enhanced email field detection for BT OAuth2 pages
                username_selectors = [
                    # Standard input selectors
                    "//input[@type='text' or @type='email' or @name='username' or @name='email' or @id='username' or @id='email']",
                    "//input[@placeholder*='username' or @placeholder*='email' or @placeholder*='Username' or @placeholder*='Email']",
                    # BT-specific selectors
                    "//input[@name='loginfmt']",  # Microsoft/BT OAuth2 email field
                    "//input[@id='loginfmt']",    # Microsoft/BT OAuth2 email field
                    "//input[@name='email']",     # Generic email field
                    "//input[@id='email']",       # Generic email field
                    "//input[@type='email']",     # HTML5 email input
                    "//input[contains(@class, 'email')]",  # Email class-based selector
                    "//input[contains(@class, 'username')]", # Username class-based selector
                    # More specific BT OAuth2 selectors
                    "//input[@data-bind*='email']",
                    "//input[@data-bind*='username']",
                    "//input[@aria-label*='email' or @aria-label*='Email']",
                    "//input[@aria-label*='username' or @aria-label*='Username']"
                ]
                
                username_filled = False
                for selector in username_selectors:
                    try:
                        username_field = wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if username_field.is_displayed() and username_field.is_enabled():
                            username_field.clear()
                            username_field.send_keys(config['username'])
                            self.logger.info(f"Filled username field: {selector}")
                            username_filled = True
                            time.sleep(1)
                            break
                    except:
                        continue
                
                if username_filled:
                    # Enhanced Next/Continue button detection for BT OAuth2 pages
                    next_selectors = [
                        # Standard button text selectors
                        "//button[contains(text(), 'Next')]",
                        "//button[contains(text(), 'Continue')]",
                        "//button[contains(text(), 'Proceed')]",
                        "//button[contains(text(), 'Sign in')]",
                        "//button[contains(text(), 'Login')]",
                        "//button[contains(text(), 'Submit')]",
                        # BT/Microsoft OAuth2 specific selectors
                        "//input[@type='submit']",
                        "//button[@type='submit']",
                        "//input[@value='Next']",
                        "//input[@value='Continue']",
                        "//input[@value='Sign in']",
                        "//input[@value='Login']",
                        # ID and class-based selectors
                        "//button[@id='idSIButton9']",  # Microsoft OAuth2 Next button
                        "//input[@id='idSIButton9']",   # Microsoft OAuth2 Next button
                        "//button[contains(@class, 'btn-primary')]",
                        "//button[contains(@class, 'btn-submit')]",
                        "//button[contains(@class, 'next')]",
                        "//button[contains(@class, 'continue')]",
                        # Data attribute selectors
                        "//button[@data-bind*='next']",
                        "//button[@data-bind*='continue']",
                        "//button[@data-bind*='submit']",
                        # Aria-label selectors
                        "//button[@aria-label*='Next' or @aria-label*='Continue']",
                        "//input[@aria-label*='Next' or @aria-label*='Continue']",
                        # Form submission selectors
                        "//form//button[@type='submit']",
                        "//form//input[@type='submit']"
                    ]
                    
                    next_clicked = False
                    for selector in next_selectors:
                        try:
                            next_button = wait.until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            if next_button.is_displayed() and next_button.is_enabled():
                                next_button.click()
                                self.logger.info(f"Clicked Next button: {selector}")
                                next_clicked = True
                                time.sleep(0.5)
                                break
                        except:
                            continue
                    
                    if not next_clicked:
                        self.logger.warning("Could not find Next button, trying alternative approach...")
                        # Try pressing Enter on the email field as fallback
                        try:
                            username_field.send_keys("\n")
                            self.logger.info("Pressed Enter on email field as fallback")
                            time.sleep(0.5)
                        except:
                            pass
                    
                    # Enhanced password field detection for BT OAuth2 pages
                    password_selectors = [
                        # Standard password selectors
                        "//input[@type='password']",
                        "//input[@name='password']",
                        "//input[@id='password']",
                        # BT/Microsoft OAuth2 specific selectors
                        "//input[@name='passwd']",     # Microsoft OAuth2 password field
                        "//input[@id='passwd']",       # Microsoft OAuth2 password field
                        "//input[@name='pwd']",        # Alternative password field name
                        "//input[@id='pwd']",          # Alternative password field ID
                        # Class and attribute-based selectors
                        "//input[contains(@class, 'password')]",
                        "//input[contains(@class, 'pwd')]",
                        "//input[@placeholder*='password' or @placeholder*='Password']",
                        "//input[@aria-label*='password' or @aria-label*='Password']",
                        # Data attribute selectors
                        "//input[@data-bind*='password']",
                        "//input[@data-bind*='pwd']"
                    ]
                    
                    for selector in password_selectors:
                        try:
                            password_field = wait.until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                            if password_field.is_displayed() and password_field.is_enabled():
                                password_field.clear()
                                password_field.send_keys(config['password'])
                                self.logger.info(f"Filled password field: {selector}")
                                time.sleep(1)
                                
                                # Enhanced final submit button detection for BT OAuth2 pages
                                submit_selectors = [
                                    # BT-specific: Next button is used for final submission
                                    "//button[contains(text(), 'Next')]",
                                    "//button[@id='next']",
                                    "//input[@id='next']",
                                    # Standard button text selectors
                                    "//button[contains(text(), 'Sign in')]",
                                    "//button[contains(text(), 'Login')]",
                                    "//button[contains(text(), 'Submit')]",
                                    "//button[contains(text(), 'Sign In')]",
                                    "//button[contains(text(), 'Log In')]",
                                    "//button[contains(text(), 'Continue')]",
                                    # BT/Microsoft OAuth2 specific selectors
                                    "//input[@type='submit']",
                                    "//button[@type='submit']",
                                    "//input[@value='Sign in']",
                                    "//input[@value='Login']",
                                    "//input[@value='Submit']",
                                    "//input[@value='Continue']",
                                    "//input[@value='Next']",
                                    # ID and class-based selectors
                                    "//button[@id='idSIButton9']",  # Microsoft OAuth2 submit button
                                    "//input[@id='idSIButton9']",   # Microsoft OAuth2 submit button
                                    "//button[contains(@class, 'btn-primary')]",
                                    "//button[contains(@class, 'btn-submit')]",
                                    "//button[contains(@class, 'btn-signin')]",
                                    "//button[contains(@class, 'btn-login')]",
                                    # Data attribute selectors
                                    "//button[@data-bind*='submit']",
                                    "//button[@data-bind*='signin']",
                                    "//button[@data-bind*='login']",
                                    # Aria-label selectors
                                    "//button[@aria-label*='Sign in' or @aria-label*='Login']",
                                    "//input[@aria-label*='Sign in' or @aria-label*='Login']",
                                    # Form submission selectors
                                    "//form//button[@type='submit']",
                                    "//form//input[@type='submit']"
                                ]
                                
                                for submit_selector in submit_selectors:
                                    try:
                                        submit_button = wait.until(
                                            EC.element_to_be_clickable((By.XPATH, submit_selector))
                                        )
                                        submit_button.click()
                                        self.logger.info(f"Clicked final submit button: {submit_selector}")
                                        time.sleep(0.5)
                                        break
                                    except:
                                        continue
                                break
                        except:
                            continue
                else:
                    self.logger.warning("Could not find username field on redirected page")
            else:
                # Still on EE WiFi page, look for additional login elements
                self.logger.info("Still on EE WiFi page, looking for additional login elements...")
                
                additional_login_selectors = [
                    "//input[@type='text' or @type='email' or @name='username' or @name='email']",
                    "//input[@type='password']",
                    "//button[contains(text(), 'Continue')]",
                    "//button[contains(text(), 'Next')]",
                    "//button[contains(text(), 'Proceed')]",
                    "//button[contains(text(), 'Submit')]",
                    "//input[@type='submit']",
                    "//button[@type='submit']"
                ]
                
                for selector in additional_login_selectors:
                    try:
                        element = wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if element.is_displayed() and element.is_enabled():
                            self.logger.info(f"Found additional login element: {selector}")
                            
                            # If it's a username/email field, try to fill it
                            if 'username' in selector or 'email' in selector or 'text' in selector:
                                element.clear()
                                element.send_keys(config['username'])
                                self.logger.info("Filled username field")
                                time.sleep(1)
                                
                                # Look for Next button
                                next_button_selectors = [
                                    "//button[contains(text(), 'Next')]",
                                    "//button[contains(text(), 'Continue')]",
                                    "//input[@type='submit']",
                                    "//button[@type='submit']"
                                ]
                                
                                for next_selector in next_button_selectors:
                                    try:
                                        next_button = wait.until(
                                            EC.element_to_be_clickable((By.XPATH, next_selector))
                                        )
                                        next_button.click()
                                        self.logger.info(f"Clicked Next button: {next_selector}")
                                        time.sleep(1)
                                        break
                                    except:
                                        continue
                                continue

                            # If it's a password field, try to fill it
                            elif 'password' in selector:
                                element.clear()
                                element.send_keys(config['password'])
                                self.logger.info("Filled password field")
                                time.sleep(1)
                                
                                # Look for final submit button
                                submit_button_selectors = [
                                    "//button[contains(text(), 'Sign in')]",
                                    "//button[contains(text(), 'Login')]",
                                    "//button[contains(text(), 'Submit')]",
                                    "//input[@type='submit']",
                                    "//button[@type='submit']"
                                ]
                                
                                for submit_selector in submit_button_selectors:
                                    try:
                                        submit_button = wait.until(
                                            EC.element_to_be_clickable((By.XPATH, submit_selector))
                                        )
                                        submit_button.click()
                                        self.logger.info(f"Clicked final submit button: {submit_selector}")
                                        time.sleep(1)
                                        break
                                    except:
                                        continue
                                break

                            # If it's a button, try to click it
                            elif 'button' in selector:
                                element.click()
                                self.logger.info(f"Clicked additional button: {selector}")
                                time.sleep(1)
                                break
                    except:
                        continue
                
            # Final wait and verification
            self.logger.info("Final verification...")
            time.sleep(0.5)
            
            # Browser will be closed by the main handle_captive_portal method
            self.logger.info("Login process completed, browser will be closed...")
            
            return self.check_internet_connectivity()
            
        except Exception as e:
            self.logger.error(f"Error in BT Business login: {e}")
            return False
            
    def _handle_form_based_login(self, driver, wait, config) -> bool:
        """Handle form-based login."""
        try:
            # Find username field
            username_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='email' or @name='username' or @name='email']"))
            )
            username_field.clear()
            username_field.send_keys(config['username'])
            
            # Find password field
            password_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(config['password'])
            
            # Find and click submit button
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
            )
            submit_button.click()
            
            time.sleep(5)
            return self.check_internet_connectivity()
            
        except Exception as e:
            self.logger.error(f"Error in form-based login: {e}")
            return False
            
    def handle_direct_bt_auth_url(self, auth_url: str, config: Dict) -> bool:
        """Handle direct BT authentication URL (like OAuth2 authorization URLs)."""
        self.logger.info(f"Handling direct BT authentication URL: {auth_url}")
        
        try:
            # Setup Chrome driver with multiple fallback options
            service = None
            driver = None
            
            # Try multiple approaches to get Chrome driver
            driver_attempts = [
                self._try_local_driver,
                self._try_webdriver_manager,
                self._try_system_chromedriver,
                self._try_chromedriver_in_path
            ]
            
            for attempt_func in driver_attempts:
                try:
                    service = attempt_func()
                    if service:
                        break
                except Exception as e:
                    self.logger.debug(f"Driver attempt failed: {e}")
                    continue
            
            if not service:
                raise Exception("Could not initialize Chrome driver with any method")
            
            options = webdriver.ChromeOptions()
            
            # Always add these basic options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if self.headless:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-images')
                options.add_argument('--disable-background-timer-throttling')
                options.add_argument('--disable-backgrounding-occluded-windows')
                options.add_argument('--disable-renderer-backgrounding')
                options.add_argument('--disable-features=TranslateUI')
                options.add_argument('--disable-ipc-flooding-protection')
                options.add_argument('--hide-scrollbars')
                options.add_argument('--mute-audio')
                self.logger.info("Running browser in headless (invisible) mode")
            else:
                options.add_argument('--window-size=1200,800')
                self.logger.info("Running browser in visible mode for debugging")
            
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 10)
            
            # Navigate directly to the authentication URL
            driver.get(auth_url)
            time.sleep(3)
            
            # Take a screenshot for debugging
            try:
                driver.save_screenshot("bt_auth_debug.png")
                self.logger.info("Screenshot saved as bt_auth_debug.png")
            except:
                pass
            
            # Handle the authentication flow
            success = self._handle_bt_oauth2_flow(driver, wait, config)
            
            driver.quit()
            return success
            
        except Exception as e:
            self.logger.error(f"Error handling direct BT auth URL: {e}")
            return False
    
    def _handle_bt_oauth2_flow(self, driver, wait, config) -> bool:
        """Handle BT OAuth2 authentication flow."""
        try:
            self.logger.info("Starting BT OAuth2 authentication flow")
            
            # Wait for page to load
            time.sleep(0.5)
            
            # Look for email field
            email_selectors = [
                "//input[@name='loginfmt']",     # Microsoft OAuth2 email field
                "//input[@id='loginfmt']",       # Microsoft OAuth2 email field
                "//input[@type='email']",        # HTML5 email input
                "//input[@name='email']",        # Generic email field
                "//input[@id='email']",          # Generic email field
                "//input[@type='text' and contains(@placeholder, 'email')]",
                "//input[@type='text' and contains(@placeholder, 'Email')]",
                "//input[@type='text' and contains(@placeholder, 'username')]",
                "//input[@type='text' and contains(@placeholder, 'Username')]"
            ]
            
            email_filled = False
            for selector in email_selectors:
                try:
                    email_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if email_field.is_displayed() and email_field.is_enabled():
                        email_field.clear()
                        email_field.send_keys(config['username'])
                        self.logger.info(f"Filled email field: {selector}")
                        email_filled = True
                        time.sleep(1)
                        break
                except:
                    continue
            
            if not email_filled:
                self.logger.error("Could not find email field")
                return False
            
            # Look for Next button
            next_selectors = [
                "//input[@type='submit']",
                "//button[@type='submit']",
                "//input[@value='Next']",
                "//button[contains(text(), 'Next')]",
                "//input[@id='idSIButton9']",
                "//button[@id='idSIButton9']"
            ]
            
            next_clicked = False
            for selector in next_selectors:
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if next_button.is_displayed() and next_button.is_enabled():
                        next_button.click()
                        self.logger.info(f"Clicked Next button: {selector}")
                        next_clicked = True
                        time.sleep(3)
                        break
                except:
                    continue
            
            if not next_clicked:
                self.logger.warning("Could not find Next button, trying Enter key...")
                try:
                    email_field.send_keys("\n")
                    self.logger.info("Pressed Enter on email field")
                    time.sleep(3)
                except:
                    pass
            
            # Now look for password field
            password_selectors = [
                "//input[@name='passwd']",       # Microsoft OAuth2 password field
                "//input[@id='passwd']",         # Microsoft OAuth2 password field
                "//input[@type='password']",     # Standard password field
                "//input[@name='password']",     # Generic password field
                "//input[@id='password']"        # Generic password field
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    password_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if password_field.is_displayed() and password_field.is_enabled():
                        password_field.clear()
                        password_field.send_keys(config['password'])
                        self.logger.info(f"Filled password field: {selector}")
                        password_filled = True
                        time.sleep(1)
                        break
                except:
                    continue
            
            if not password_filled:
                self.logger.error("Could not find password field")
                return False
            
            # Look for final submit button
            submit_selectors = [
                # BT-specific: Next button is used for final submission
                "//button[contains(text(), 'Next')]",
                "//button[@id='next']",
                "//input[@id='next']",
                # Standard submit selectors
                "//input[@type='submit']",
                "//button[@type='submit']",
                "//input[@value='Sign in']",
                "//button[contains(text(), 'Sign in')]",
                "//input[@id='idSIButton9']",
                "//button[@id='idSIButton9']"
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    submit_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        submit_button.click()
                        self.logger.info(f"Clicked submit button: {selector}")
                        submit_clicked = True
                        time.sleep(3)
                        break
                except:
                    continue
            
            if not submit_clicked:
                self.logger.warning("Could not find submit button, trying Enter key...")
                try:
                    password_field.send_keys("\n")
                    self.logger.info("Pressed Enter on password field")
                    time.sleep(3)
                except:
                    pass
            
            # Wait for authentication to complete
            time.sleep(5)
            
            # Check if we were redirected to a success page
            current_url = driver.current_url
            self.logger.info(f"Final URL after authentication: {current_url}")
            
            # Take final screenshot
            try:
                driver.save_screenshot("bt_auth_final.png")
                self.logger.info("Final screenshot saved as bt_auth_final.png")
            except:
                pass
            
            # Check if authentication was successful
            if "error" not in current_url.lower() and "fail" not in current_url.lower():
                self.logger.info("BT OAuth2 authentication appears successful")
                return True
            else:
                self.logger.warning("BT OAuth2 authentication may have failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in BT OAuth2 flow: {e}")
            return False

    def _handle_click_through_login(self, driver, wait) -> bool:
        """Handle click-through login (terms acceptance)."""
        try:
            # Look for common terms acceptance buttons
            button_texts = [
                "Accept", "Agree", "Continue", "I Agree", "Accept Terms",
                "Get Started", "Connect", "Login", "Sign In"
            ]
            
            for text in button_texts:
                try:
                    button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')] | //a[contains(text(), '{text}')]"))
                    )
                    button.click()
                    time.sleep(3)
                    break
                except:
                    continue
                    
            time.sleep(5)
            return self.check_internet_connectivity()
            
        except Exception as e:
            self.logger.error(f"Error in click-through login: {e}")
            return False
            
    def run(self) -> bool:
        """Main execution method."""
        self.logger.info("Starting WiFi Hotspot Agent")
        
        # Check if already connected to internet
        if self.check_internet_connectivity():
            self.logger.info("Internet is already available")
            return True
            
        # For Ethernet + AP setup, we don't need to connect to WiFi networks
        # The AP is already connected to EE WiFi, we just need to handle captive portal
        self.logger.info("Ethernet mode: Handling captive portal for AP router re-authentication")
        
        # Try to handle captive portal for configured hotspots
        for hotspot in self.config['hotspots']:
            ssid = hotspot['ssid']
            
            # Skip Profile network as it's not a hotspot
            if ssid == "Profile":
                continue
                
            self.logger.info(f"Attempting captive portal login for {ssid}")
            
            # Handle captive portal directly (AP is already connected to EE WiFi)
            if self.handle_captive_portal(hotspot):
                self.logger.info(f"Successfully logged into {ssid} via captive portal")
                return True
            else:
                self.logger.warning(f"Failed to login to {ssid} via captive portal")
                
        self.logger.error("No internet connection established via captive portal")
        return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='WiFi Hotspot Auto-Connect Agent')
    parser.add_argument('--config', default='wifi_config.json', help='Configuration file path')
    parser.add_argument('--debug', action='store_true', help='Run browser in visible mode for debugging')
    
    args = parser.parse_args()
    
    # Set headless mode: False for debug (visible), True for production (invisible)
    headless = not args.debug
    
    agent = WiFiHotspotAgent(args.config, headless=headless)
    success = agent.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

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
    
    def __init__(self, config_file: str = "wifi_config.json", headless: bool = True):
        """Initialize the WiFi agent with configuration.
        
        Args:
            config_file: Path to the configuration file
            headless: If True, run browser invisibly. If False, show browser for debugging.
        """
        self.config_file = config_file
        self.headless = headless
        self.setup_logging()
        self.config = self._load_config()
        
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
            
            # Look for additional login elements that might appear after submit
            try:
                # Check if we need to handle a different login form
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
                        self.logger.info(f"Found additional login element: {selector}")
                        
                        # If it's a username/email field, try to fill it
                        if 'username' in selector or 'email' in selector or 'text' in selector:
                            if 'config' in locals() and 'username' in config:
                                element.clear()
                                element.send_keys(config['username'])
                                self.logger.info("Filled username field")
                                time.sleep(0.5)
                                
                                # After filling email, look for and click the Next button
                                try:
                                    next_button_selectors = [
                                        "//button[contains(text(), 'Next')]",
                                        "//button[contains(text(), 'Continue')]",
                                        "//button[contains(text(), 'Proceed')]",
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
                                            time.sleep(0.5)
                                            break
                                        except:
                                            continue
                                except Exception as e:
                                    self.logger.info(f"Could not find or click Next button: {e}")
                                
                                # Don't break here - continue to look for password field
                                continue

                        # If it's a password field, try to fill it
                        elif 'password' in selector:
                            if 'config' in locals() and 'password' in config:
                                element.clear()
                                element.send_keys(config['password'])
                                self.logger.info("Filled password field")
                                time.sleep(0.5)
                                
                                # After filling password, look for and click Next button
                                try:
                                    next_button_selectors = [
                                        "//button[contains(text(), 'Next')]",
                                        "//button[contains(text(), 'Continue')]",
                                        "//button[contains(text(), 'Sign in')]",
                                        "//button[contains(text(), 'Login')]",
                                        "//button[contains(text(), 'Submit')]",
                                        "//input[@type='submit']",
                                        "//button[@type='submit']"
                                    ]
                                    
                                    for next_selector in next_button_selectors:
                                        try:
                                            next_button = wait.until(
                                                EC.element_to_be_clickable((By.XPATH, next_selector))
                                            )
                                            next_button.click()
                                            self.logger.info(f"Clicked Next/Submit button: {next_selector}")
                                            time.sleep(0.5)
                                            break
                                        except:
                                            continue
                                except Exception as e:
                                    self.logger.info(f"Could not find or click Next/Submit button: {e}")
                                
                                # After clicking Next/Submit, we're done with this flow
                                break

                        # If it's a button, try to click it
                        elif 'button' in selector:
                            element.click()
                            self.logger.info(f"Clicked additional button: {selector}")
                            time.sleep(0.5)
                            break
                    except:
                        continue
                        
            except Exception as e:
                self.logger.info(f"No additional login elements found or error: {e}")
                
            # Final wait and verification
            self.logger.info("Final verification...")
            time.sleep(2)
            
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
            
        # Get available networks
        available_networks = self.get_available_networks()
        
        # Try to connect to configured hotspots
        for hotspot in self.config['hotspots']:
            ssid = hotspot['ssid']
            
            if ssid in available_networks:
                self.logger.info(f"Found configured hotspot: {ssid}")
                
                # Connect to the network
                if self.connect_to_network(ssid):
                    # Wait for connection to stabilize
                    time.sleep(1)
                    
                    # Check if internet is available
                    self.logger.info(f"Checking internet connectivity after connecting to {ssid}...")
                    if self.check_internet_connectivity():
                        self.logger.info(f"Internet available on {ssid}")
                        return True
                    else:
                        # Handle captive portal
                        self.logger.info(f"No internet detected - handling captive portal for {ssid}")
                        if self.handle_captive_portal(hotspot):
                            self.logger.info(f"Successfully logged into {ssid}")
                            return True
                        else:
                            self.logger.warning(f"Failed to login to {ssid}")
                else:
                    self.logger.warning(f"Failed to connect to {ssid}")
            else:
                self.logger.info(f"Configured hotspot {ssid} not available")
                
        self.logger.error("No internet connection established")
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

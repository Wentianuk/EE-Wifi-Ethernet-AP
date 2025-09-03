#!/usr/bin/env python3
"""
Internet Connectivity Monitor
Continuously monitors internet connectivity and automatically runs WiFi agent when needed.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from typing import Dict, List, Optional

import requests

# Import the logbook
try:
    from internet_logbook import InternetLogbook
    LOGBOOK_AVAILABLE = True
except ImportError:
    LOGBOOK_AVAILABLE = False


class InternetMonitor:
    """Monitors internet connectivity and triggers WiFi agent when needed."""
    
    def __init__(self, config_file: str = "wifi_config.json", check_interval: int = 30, debug: bool = False):
        """Initialize the internet monitor.
        
        Args:
            config_file: Path to the configuration file
            check_interval: Interval between connectivity checks in seconds
            debug: If True, run WiFi agent in visible mode for debugging
        """
        self.config_file = config_file
        self.check_interval = check_interval
        self.debug = debug
        self.failure_count = 0
        self.max_failures = 3
        self.setup_logging()
        self.config = self._load_config()
        
        # Initialize logbook if available
        if LOGBOOK_AVAILABLE:
            self.logbook = InternetLogbook()
            self.logger.info("Internet logbook initialized")
        else:
            self.logbook = None
            self.logger.warning("Internet logbook not available")
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('internet_monitor.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Optional[Dict]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.warning(f"Configuration file {self.config_file} not found. Using defaults.")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            return None
            
    def check_internet_connectivity(self) -> bool:
        """Check if internet is accessible using multiple reliable hosts."""
        test_urls = [
            'https://8.8.8.8',           # Google DNS
            'https://1.1.1.1',           # Cloudflare DNS
            'https://www.google.com',     # Google
            'https://www.cloudflare.com', # Cloudflare
            'https://httpbin.org/get'     # HTTPBin
        ]
        
        successful_connections = 0
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    successful_connections += 1
                    if successful_connections >= 2:  # Need at least 2 successful connections
                        return True
            except requests.exceptions.RequestException:
                continue
                
        return False
        
    def get_current_wifi_network(self) -> Optional[str]:
        """Get the currently connected WiFi network name."""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if 'Profile' in line and ':' in line:
                    network = line.split(':')[1].strip()
                    if network and network != 'Not configured':
                        return network
                        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get current WiFi network: {e}")
            
        return None
        
    def is_configured_hotspot(self, network_name: str) -> bool:
        """Check if the current network is a configured hotspot."""
        if not self.config or 'hotspots' not in self.config:
            return False
            
        configured_ssids = [hotspot['ssid'] for hotspot in self.config['hotspots']]
        return network_name in configured_ssids
        
    def run_wifi_agent(self) -> bool:
        """Run the WiFi hotspot agent."""
        try:
            self.logger.info("Running WiFi hotspot agent...")
            
            # Import and run the WiFi agent
            from wifi_hotspot_agent import WiFiHotspotAgent
            
            # Set headless mode: False for debug (visible), True for production (invisible)
            headless = not self.debug
            agent = WiFiHotspotAgent(self.config_file, headless=headless)
            success = agent.run()
            
            if success:
                self.logger.info("WiFi agent completed successfully")
                self.failure_count = 0  # Reset failure count on success
            else:
                self.logger.warning("WiFi agent failed")
                
            return success
            
        except ImportError:
            self.logger.error("WiFi hotspot agent not found. Make sure wifi_hotspot_agent.py is in the same directory.")
            return False
        except Exception as e:
            self.logger.error(f"Error running WiFi agent: {e}")
            return False
            
    def monitor_once(self) -> bool:
        """Perform a single connectivity check."""
        self.logger.info("Checking internet connectivity...")
        
        is_connected = self.check_internet_connectivity()
        current_network = self.get_current_wifi_network()
        
        # Log to logbook if available
        if self.logbook:
            self.logbook.monitor_once()
        
        if is_connected:
            self.logger.info("Internet is available")
            self.failure_count = 0
            return True
        else:
            self.failure_count += 1
            self.logger.warning(f"Internet not available (failure #{self.failure_count})")
            
            # Only run WiFi agent if we're on a configured hotspot or no specific network
            if current_network is None or self.is_configured_hotspot(current_network):
                if self.failure_count >= 1:  # Trigger after 1st failure (30 seconds)
                    self.logger.info(f"Reached {self.failure_count} consecutive failures. Running WiFi agent...")
                    return self.run_wifi_agent()
            else:
                self.logger.info(f"Connected to {current_network} (not a configured hotspot). Skipping WiFi agent.")
                
        return False
        
    def monitor_continuous(self):
        """Continuously monitor internet connectivity."""
        self.logger.info(f"Starting continuous internet monitoring (interval: {self.check_interval}s)")
        
        try:
            while True:
                self.monitor_once()
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in monitoring loop: {e}")
            
    def run(self, once: bool = False, background: bool = False):
        """Main execution method."""
        if once:
            self.logger.info("Running single connectivity check")
            success = self.monitor_once()
            sys.exit(0 if success else 1)
        else:
            if background:
                self.logger.info("Starting background monitoring")
                # In a real implementation, you might want to daemonize the process
                # For now, we'll just run in the background
                import threading
                monitor_thread = threading.Thread(target=self.monitor_continuous)
                monitor_thread.daemon = True
                monitor_thread.start()
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.logger.info("Background monitoring stopped")
            else:
                self.monitor_continuous()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Internet Connectivity Monitor')
    parser.add_argument('--config', default='wifi_config.json', help='Configuration file path')
    parser.add_argument('--interval', type=int, default=30, help='Check interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--background', action='store_true', help='Run in background')
    parser.add_argument('--debug', action='store_true', help='Run WiFi agent in visible mode for debugging')
    
    args = parser.parse_args()
    
    monitor = InternetMonitor(args.config, args.interval, debug=args.debug)
    monitor.run(once=args.once, background=args.background)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Chrome Process Cleanup Utility
Monitors and cleans up stuck Chrome/ChromeDriver processes to prevent WiFi agent issues.
"""

import logging
import subprocess
import sys
import time
from typing import List, Tuple

class ChromeProcessCleanup:
    """Utility class for cleaning up Chrome processes."""
    
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('chrome_cleanup.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_chrome_processes(self) -> List[Tuple[str, int, str]]:
        """Get list of running Chrome processes.
        
        Returns:
            List of tuples (process_name, pid, memory_usage)
        """
        try:
            result = subprocess.run(
                ['tasklist', '/fi', 'imagename eq chrome.exe', '/fo', 'csv'],
                capture_output=True, text=True, check=True
            )
            
            processes = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 5:
                        name = parts[0].strip('"')
                        pid = int(parts[1].strip('"'))
                        memory = parts[4].strip('"')
                        processes.append((name, pid, memory))
            
            return processes
            
        except Exception as e:
            self.logger.error(f"Error getting Chrome processes: {e}")
            return []
    
    def get_chromedriver_processes(self) -> List[Tuple[str, int, str]]:
        """Get list of running ChromeDriver processes.
        
        Returns:
            List of tuples (process_name, pid, memory_usage)
        """
        try:
            result = subprocess.run(
                ['tasklist', '/fi', 'imagename eq chromedriver.exe', '/fo', 'csv'],
                capture_output=True, text=True, check=True
            )
            
            processes = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 5:
                        name = parts[0].strip('"')
                        pid = int(parts[1].strip('"'))
                        memory = parts[4].strip('"')
                        processes.append((name, pid, memory))
            
            return processes
            
        except Exception as e:
            self.logger.error(f"Error getting ChromeDriver processes: {e}")
            return []
    
    def kill_chrome_processes(self, force: bool = False) -> int:
        """Kill Chrome processes.
        
        Args:
            force: If True, use /f flag for force kill
            
        Returns:
            Number of processes killed
        """
        try:
            if force:
                # Force kill immediately
                cmd = ['taskkill', '/f', '/im', 'chrome.exe']
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            else:
                # Try graceful shutdown first
                self.logger.info("Attempting graceful shutdown of Chrome processes...")
                graceful_cmd = ['taskkill', '/im', 'chrome.exe']
                graceful_result = subprocess.run(graceful_cmd, capture_output=True, text=True, check=False)
                
                # Wait for graceful shutdown
                time.sleep(3)
                
                # Check if Chrome processes are still running
                chrome_check = subprocess.run(['tasklist', '/fi', 'imagename eq chrome.exe'], 
                                            capture_output=True, text=True, check=False)
                
                if 'chrome.exe' in chrome_check.stdout:
                    self.logger.warning("Chrome processes still running, using force kill...")
                    cmd = ['taskkill', '/f', '/im', 'chrome.exe']
                    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                else:
                    self.logger.info("Chrome processes shut down gracefully")
                    return graceful_result.stdout.count('SUCCESS') if graceful_result.returncode == 0 else 0
            
            if result.returncode == 0:
                # Count successful kills from output
                killed_count = result.stdout.count('SUCCESS')
                self.logger.info(f"Killed {killed_count} Chrome processes")
                return killed_count
            else:
                self.logger.warning(f"Failed to kill Chrome processes: {result.stderr}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error killing Chrome processes: {e}")
            return 0
    
    def kill_chromedriver_processes(self, force: bool = False) -> int:
        """Kill ChromeDriver processes.
        
        Args:
            force: If True, use /f flag for force kill
            
        Returns:
            Number of processes killed
        """
        try:
            cmd = ['taskkill']
            if force:
                cmd.append('/f')
            cmd.extend(['/im', 'chromedriver.exe'])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                # Count successful kills from output
                killed_count = result.stdout.count('SUCCESS')
                self.logger.info(f"Killed {killed_count} ChromeDriver processes")
                return killed_count
            else:
                self.logger.warning(f"Failed to kill ChromeDriver processes: {result.stderr}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error killing ChromeDriver processes: {e}")
            return 0
    
    def cleanup_stuck_processes(self, max_chrome_processes: int = 5, force: bool = False) -> bool:
        """Clean up stuck Chrome/ChromeDriver processes.
        
        Args:
            max_chrome_processes: Maximum number of Chrome processes allowed
            force: If True, force kill processes
            
        Returns:
            True if cleanup was performed, False otherwise
        """
        self.logger.info("Checking for stuck Chrome processes...")
        
        # Check Chrome processes
        chrome_processes = self.get_chrome_processes()
        chromedriver_processes = self.get_chromedriver_processes()
        
        chrome_count = len(chrome_processes)
        chromedriver_count = len(chromedriver_processes)
        
        self.logger.info(f"Found {chrome_count} Chrome processes and {chromedriver_count} ChromeDriver processes")
        
        cleanup_performed = False
        
        # Clean up Chrome processes if too many
        if chrome_count > max_chrome_processes:
            self.logger.warning(f"Too many Chrome processes ({chrome_count} > {max_chrome_processes}), cleaning up...")
            killed = self.kill_chrome_processes(force=force)
            if killed > 0:
                cleanup_performed = True
                time.sleep(2)  # Wait for processes to terminate
        
        # Clean up ChromeDriver processes if any
        if chromedriver_count > 0:
            self.logger.warning(f"Found {chromedriver_count} ChromeDriver processes, cleaning up...")
            killed = self.kill_chromedriver_processes(force=force)
            if killed > 0:
                cleanup_performed = True
                time.sleep(2)  # Wait for processes to terminate
        
        if not cleanup_performed:
            self.logger.info("No cleanup needed - process counts are normal")
        
        return cleanup_performed
    
    def monitor_and_cleanup(self, check_interval: int = 300, max_chrome_processes: int = 5):
        """Continuously monitor and clean up Chrome processes.
        
        Args:
            check_interval: Interval between checks in seconds
            max_chrome_processes: Maximum number of Chrome processes allowed
        """
        self.logger.info(f"Starting Chrome process monitoring (interval: {check_interval}s, max processes: {max_chrome_processes})")
        
        try:
            while True:
                self.cleanup_stuck_processes(max_chrome_processes, force=False)
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in monitoring loop: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chrome Process Cleanup Utility')
    parser.add_argument('--check', action='store_true', help='Check process counts and clean up if needed')
    parser.add_argument('--force', action='store_true', help='Force kill processes')
    parser.add_argument('--monitor', action='store_true', help='Start continuous monitoring')
    parser.add_argument('--max-processes', type=int, default=5, help='Maximum Chrome processes allowed')
    parser.add_argument('--interval', type=int, default=300, help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    cleanup = ChromeProcessCleanup()
    
    if args.check:
        # One-time check and cleanup
        cleanup.cleanup_stuck_processes(args.max_processes, force=args.force)
    elif args.monitor:
        # Continuous monitoring
        cleanup.monitor_and_cleanup(args.interval, args.max_processes)
    else:
        # Default: one-time cleanup
        cleanup.cleanup_stuck_processes(args.max_processes, force=args.force)


if __name__ == "__main__":
    main()

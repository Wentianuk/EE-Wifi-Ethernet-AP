#!/usr/bin/env python3
"""
Internet Connectivity Logbook
Tracks internet disconnect and reconnect timestamps with detailed logging.
"""

import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import requests


class InternetLogbook:
    """Manages internet connectivity logging with database storage."""
    
    def __init__(self, db_file: str = "internet_logbook.db"):
        """Initialize the logbook with SQLite database."""
        self.db_file = db_file
        self.setup_logging()
        self.setup_database()
        self.last_status = None
        self.last_check_time = None
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('internet_logbook.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """Create SQLite database and tables."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create connectivity_events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connectivity_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration_seconds INTEGER,
                    network_name TEXT,
                    error_message TEXT,
                    recovery_attempts INTEGER DEFAULT 0
                )
            ''')
            
            # Create daily_summary table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    total_checks INTEGER DEFAULT 0,
                    successful_checks INTEGER DEFAULT 0,
                    failed_checks INTEGER DEFAULT 0,
                    total_disconnect_time INTEGER DEFAULT 0,
                    disconnect_count INTEGER DEFAULT 0,
                    avg_recovery_time REAL DEFAULT 0
                )
            ''')
            
            # Create network_stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    network_name TEXT NOT NULL,
                    total_usage_time INTEGER DEFAULT 0,
                    disconnect_count INTEGER DEFAULT 0,
                    avg_recovery_time REAL DEFAULT 0,
                    last_used TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            self.logger.info(f"Database initialized: {self.db_file}")
            
        except Exception as e:
            self.logger.error(f"Error setting up database: {e}")
            
    def check_internet_connectivity(self) -> Tuple[bool, str, Optional[str]]:
        """Check internet connectivity and return status, error message, and network name."""
        test_urls = [
            'https://8.8.8.8',           # Google DNS
            'https://1.1.1.1',           # Cloudflare DNS
            'https://www.google.com',     # Google
            'https://www.cloudflare.com', # Cloudflare
        ]
        
        # Get current network name
        network_name = self.get_current_network()
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    return True, None, network_name
            except requests.exceptions.RequestException as e:
                continue
                
        return False, "All connectivity tests failed", network_name
        
    def get_current_network(self) -> Optional[str]:
        """Get the currently connected WiFi network name."""
        try:
            import subprocess
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
                        
        except Exception:
            pass
            
        return None
        
    def log_connectivity_event(self, status: str, duration: Optional[int] = None, 
                              network_name: Optional[str] = None, error_message: Optional[str] = None):
        """Log a connectivity event to the database and text file."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO connectivity_events 
                (timestamp, status, duration_seconds, network_name, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, status, duration, network_name, error_message))
            
            conn.commit()
            conn.close()
            
            # Log to file as well
            if status == "DISCONNECTED":
                self.logger.warning(f"DISCONNECTED at {timestamp} | Network: {network_name} | Error: {error_message}")
            elif status == "RECONNECTED":
                self.logger.info(f"RECONNECTED at {timestamp} | Network: {network_name} | Duration: {duration}s")
            elif status == "CONNECTED":
                self.logger.info(f"CONNECTED at {timestamp} | Network: {network_name}")
            
            # Also save to comprehensive text file
            self.save_to_text_file(status, timestamp, duration, network_name, error_message)
                
        except Exception as e:
            self.logger.error(f"Error logging connectivity event: {e}")
            
    def save_to_text_file(self, status: str, timestamp: str, duration: Optional[int] = None,
                         network_name: Optional[str] = None, error_message: Optional[str] = None):
        """Save connectivity event to a comprehensive text file."""
        try:
            text_file = "internet_connectivity_records.txt"
            readable_time = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            with open(text_file, 'a', encoding='utf-8') as f:
                if status == "DISCONNECTED":
                    f.write(f"[DISCONNECTED] {readable_time} | Network: {network_name} | Error: {error_message}\n")
                elif status == "RECONNECTED":
                    f.write(f"[RECONNECTED] {readable_time} | Network: {network_name} | Downtime: {duration} seconds\n")
                elif status == "CONNECTED":
                    f.write(f"[CONNECTED] {readable_time} | Network: {network_name}\n")
                    
        except Exception as e:
            self.logger.error(f"Error saving to text file: {e}")
            
    def update_daily_summary(self, date: str, successful: bool):
        """Update daily summary statistics."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get or create daily summary
            cursor.execute('SELECT * FROM daily_summary WHERE date = ?', (date,))
            row = cursor.fetchone()
            
            if row:
                # Update existing record
                cursor.execute('''
                    UPDATE daily_summary 
                    SET total_checks = total_checks + 1,
                        successful_checks = successful_checks + ?,
                        failed_checks = failed_checks + ?
                    WHERE date = ?
                ''', (1 if successful else 0, 0 if successful else 1, date))
            else:
                # Create new record
                cursor.execute('''
                    INSERT INTO daily_summary 
                    (date, total_checks, successful_checks, failed_checks)
                    VALUES (?, 1, ?, ?)
                ''', (date, 1 if successful else 0, 0 if successful else 1))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error updating daily summary: {e}")
            
    def monitor_once(self) -> bool:
        """Perform a single connectivity check and log the result."""
        current_time = time.time()
        is_connected, error_message, network_name = self.check_internet_connectivity()
        
        # Update daily summary
        today = datetime.now().strftime('%Y-%m-%d')
        self.update_daily_summary(today, is_connected)
        
        # Check for status changes
        if self.last_status is not None and self.last_status != is_connected:
            if is_connected:
                # Just reconnected
                if self.last_check_time:
                    duration = int(current_time - self.last_check_time)
                    self.log_connectivity_event("RECONNECTED", duration, network_name)
            else:
                # Just disconnected
                self.log_connectivity_event("DISCONNECTED", None, network_name, error_message)
        elif is_connected and self.last_status is None:
            # First check and connected
            self.log_connectivity_event("CONNECTED", None, network_name)
            
        self.last_status = is_connected
        self.last_check_time = current_time
        
        return is_connected
        
    def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Get recent connectivity events."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, status, duration_seconds, network_name, error_message
                FROM connectivity_events
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'timestamp': row[0],
                    'status': row[1],
                    'duration_seconds': row[2],
                    'network_name': row[3],
                    'error_message': row[4]
                })
            
            conn.close()
            return events
            
        except Exception as e:
            self.logger.error(f"Error getting recent events: {e}")
            return []
            
    def get_daily_summary(self, days: int = 7) -> List[Dict]:
        """Get daily summary for the last N days."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT date, total_checks, successful_checks, failed_checks, 
                       disconnect_count, total_disconnect_time, avg_recovery_time
                FROM daily_summary
                ORDER BY date DESC
                LIMIT ?
            ''', (days,))
            
            summaries = []
            for row in cursor.fetchall():
                summaries.append({
                    'date': row[0],
                    'total_checks': row[1],
                    'successful_checks': row[2],
                    'failed_checks': row[3],
                    'disconnect_count': row[4],
                    'total_disconnect_time': row[5],
                    'avg_recovery_time': row[6]
                })
            
            conn.close()
            return summaries
            
        except Exception as e:
            self.logger.error(f"Error getting daily summary: {e}")
            return []
            
    def generate_report(self, days: int = 7) -> str:
        """Generate a comprehensive connectivity report."""
        try:
            events = self.get_recent_events(100)
            summaries = self.get_daily_summary(days)
            
            report = []
            report.append("=" * 60)
            report.append("INTERNET CONNECTIVITY LOGBOOK REPORT")
            report.append("=" * 60)
            report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Database: {self.db_file}")
            report.append("")
            
            # Daily Summary
            report.append("DAILY SUMMARY (Last 7 Days)")
            report.append("-" * 40)
            for summary in summaries:
                success_rate = (summary['successful_checks'] / summary['total_checks'] * 100) if summary['total_checks'] > 0 else 0
                report.append(f"{summary['date']}: {summary['successful_checks']}/{summary['total_checks']} checks ({success_rate:.1f}% success)")
            report.append("")
            
            # Recent Events
            report.append("RECENT CONNECTIVITY EVENTS")
            report.append("-" * 40)
            for event in events[:20]:  # Show last 20 events
                timestamp = datetime.fromisoformat(event['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                if event['status'] == 'DISCONNECTED':
                    report.append(f"[DISCONNECTED] {timestamp} | {event['network_name']} | {event['error_message']}")
                elif event['status'] == 'RECONNECTED':
                    report.append(f"[RECONNECTED] {timestamp} | {event['network_name']} | {event['duration_seconds']}s downtime")
                elif event['status'] == 'CONNECTED':
                    report.append(f"[CONNECTED] {timestamp} | {event['network_name']}")
            
            report.append("")
            report.append("=" * 60)
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return f"Error generating report: {e}"
            
    def export_all_records_to_text(self, filename: str = "internet_connectivity_full_export.txt"):
        """Export all records to a comprehensive text file."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get all events
            cursor.execute('''
                SELECT timestamp, status, duration_seconds, network_name, error_message
                FROM connectivity_events
                ORDER BY timestamp ASC
            ''')
            
            events = cursor.fetchall()
            
            # Get daily summaries
            cursor.execute('''
                SELECT date, total_checks, successful_checks, failed_checks, 
                       disconnect_count, total_disconnect_time, avg_recovery_time
                FROM daily_summary
                ORDER BY date ASC
            ''')
            
            summaries = cursor.fetchall()
            
            conn.close()
            
            # Write to text file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("INTERNET CONNECTIVITY FULL RECORDS EXPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Events: {len(events)}\n")
                f.write(f"Database: {self.db_file}\n")
                f.write("=" * 80 + "\n\n")
                
                # Daily Summary Section
                f.write("DAILY SUMMARY\n")
                f.write("-" * 40 + "\n")
                for summary in summaries:
                    date, total, successful, failed, disconnects, downtime, avg_recovery = summary
                    success_rate = (successful / total * 100) if total > 0 else 0
                    f.write(f"{date}: {successful}/{total} checks ({success_rate:.1f}% success)\n")
                    if disconnects > 0:
                        f.write(f"  - Disconnects: {disconnects}, Total downtime: {downtime}s, Avg recovery: {avg_recovery:.1f}s\n")
                f.write("\n")
                
                # All Events Section
                f.write("ALL CONNECTIVITY EVENTS\n")
                f.write("-" * 40 + "\n")
                for event in events:
                    timestamp, status, duration, network_name, error_message = event
                    readable_time = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
                    if status == "DISCONNECTED":
                        f.write(f"[DISCONNECTED] {readable_time} | Network: {network_name} | Error: {error_message}\n")
                    elif status == "RECONNECTED":
                        f.write(f"[RECONNECTED] {readable_time} | Network: {network_name} | Downtime: {duration} seconds\n")
                    elif status == "CONNECTED":
                        f.write(f"[CONNECTED] {readable_time} | Network: {network_name}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("END OF EXPORT\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"All records exported to: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error exporting records: {e}")
            return None


def main():
    """Main entry point for testing the logbook."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Internet Connectivity Logbook')
    parser.add_argument('--check', action='store_true', help='Perform a single connectivity check')
    parser.add_argument('--report', action='store_true', help='Generate and display report')
    parser.add_argument('--events', type=int, default=20, help='Number of recent events to show')
    parser.add_argument('--days', type=int, default=7, help='Number of days for summary')
    parser.add_argument('--export', action='store_true', help='Export all records to text file')
    parser.add_argument('--export-file', default='internet_connectivity_full_export.txt', help='Export filename')
    
    args = parser.parse_args()
    
    logbook = InternetLogbook()
    
    if args.check:
        print("Checking internet connectivity...")
        is_connected = logbook.monitor_once()
        print(f"Status: {'Connected' if is_connected else 'Disconnected'}")
        
    elif args.report:
        report = logbook.generate_report(args.days)
        print(report)
        
    elif args.export:
        print("Exporting all records to text file...")
        filename = logbook.export_all_records_to_text(args.export_file)
        if filename:
            print(f"✅ All records exported to: {filename}")
        else:
            print("❌ Export failed")
        
    else:
        # Show recent events
        events = logbook.get_recent_events(args.events)
        print(f"\nLast {len(events)} Connectivity Events:")
        print("-" * 50)
        for event in events:
            timestamp = datetime.fromisoformat(event['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            status_icon = "[DISCONNECTED]" if event['status'] == 'DISCONNECTED' else "[CONNECTED]"
            print(f"{status_icon} {timestamp} | {event['status']} | {event['network_name']}")


if __name__ == "__main__":
    main()

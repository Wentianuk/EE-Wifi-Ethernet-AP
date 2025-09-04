#!/usr/bin/env python3
"""
Check Monitor Status
Script to check the status of the internet monitoring system
"""

import os
import time
import json
from datetime import datetime

def check_log_file():
    """Check the monitor log file for recent activity."""
    log_file = "internet_monitor.log"
    
    if not os.path.exists(log_file):
        return "❌ Log file not found"
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return "❌ Log file is empty"
        
        # Get last few lines
        last_lines = lines[-5:]
        last_activity = last_lines[-1].strip()
        
        # Extract timestamp from log line
        if " - INFO - " in last_activity:
            timestamp_str = last_activity.split(" - INFO - ")[0]
            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                time_diff = datetime.now() - timestamp
                
                if time_diff.total_seconds() < 60:  # Less than 1 minute ago
                    return f"✅ Monitor active (last check: {time_diff.seconds}s ago)"
                elif time_diff.total_seconds() < 300:  # Less than 5 minutes ago
                    return f"⚠️  Monitor may be slow (last check: {time_diff.seconds}s ago)"
                else:
                    return f"❌ Monitor appears stopped (last check: {time_diff.seconds}s ago)"
            except:
                return f"✅ Monitor running (last activity: {last_activity[:50]}...)"
        else:
            return f"✅ Monitor running (last activity: {last_activity[:50]}...)"
            
    except Exception as e:
        return f"❌ Error reading log: {e}"

def check_config():
    """Check the configuration file."""
    config_file = "wifi_config.json"
    
    if not os.path.exists(config_file):
        return "❌ Configuration file not found"
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        interval = config.get('check_interval', 'unknown')
        mode = config.get('connection_mode', 'unknown')
        debug = config.get('debug_mode', False)
        
        return f"✅ Config OK (interval: {interval}s, mode: {mode}, debug: {debug})"
        
    except Exception as e:
        return f"❌ Error reading config: {e}"

def check_database():
    """Check the logbook database."""
    db_file = "internet_logbook.db"
    
    if not os.path.exists(db_file):
        return "❌ Database file not found"
    
    try:
        # Check if database is accessible
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM connectivity_records")
        count = cursor.fetchone()[0]
        conn.close()
        
        return f"✅ Database OK ({count} records)"
        
    except Exception as e:
        return f"❌ Database error: {e}"

def main():
    """Check monitor status."""
    print("📊 Internet Monitor Status Check")
    print("=" * 50)
    
    print(f"🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 Configuration:")
    print(f"   {check_config()}")
    print()
    
    print("📊 Database:")
    print(f"   {check_database()}")
    print()
    
    print("📝 Monitor Activity:")
    print(f"   {check_log_file()}")
    print()
    
    print("=" * 50)
    print("💡 To start monitoring: python start_continuous_monitor.py")
    print("💡 To stop monitoring: Press Ctrl+C in the monitor window")
    print("💡 To check logs: Get-Content internet_monitor.log -Tail 20")

if __name__ == "__main__":
    main()

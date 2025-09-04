#!/usr/bin/env python3
"""
Start Continuous Internet Monitor
Simple script to start the internet connectivity monitor with 30-second intervals
"""

import sys
import os
import time
from internet_monitor import InternetMonitor

def main():
    """Start continuous internet monitoring."""
    print("🌐 Starting Continuous Internet Monitor")
    print("=" * 50)
    print("This will:")
    print("• Check internet connectivity every 30 seconds")
    print("• Monitor Ethernet connection (Ethernet + AP setup)")
    print("• Automatically trigger BT Business login when needed")
    print("• Run in invisible browser mode (production)")
    print("=" * 50)
    print("Press Ctrl+C to stop monitoring")
    print("=" * 50)
    
    try:
        # Initialize monitor with 30-second intervals
        monitor = InternetMonitor(
            config_file="wifi_config.json",
            check_interval=30,
            debug=False  # Production mode with invisible browser
        )
        
        # Start continuous monitoring
        monitor.run(once=False, background=False)
        
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error starting monitor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

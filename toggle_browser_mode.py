#!/usr/bin/env python3
"""
Toggle Browser Mode
Switch between visible (debug) and invisible (production) browser modes
"""

import json
import os

def toggle_browser_mode():
    """Toggle between debug and production browser modes."""
    config_file = "wifi_config.json"
    
    if not os.path.exists(config_file):
        print("❌ Configuration file not found")
        return
    
    try:
        # Load current configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Get current settings
        current_debug = config.get('debug_mode', False)
        current_headless = config.get('headless_browser', True)
        
        # Toggle settings
        new_debug = not current_debug
        new_headless = not current_headless
        
        # Update configuration
        config['debug_mode'] = new_debug
        config['headless_browser'] = new_headless
        
        # Save configuration
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        # Display results
        if new_debug:
            print("🔍 DEBUG MODE ENABLED")
            print("• Browser: VISIBLE (for debugging)")
            print("• Debug logging: ENABLED")
            print("• Use this mode for troubleshooting")
        else:
            print("🚀 PRODUCTION MODE ENABLED")
            print("• Browser: INVISIBLE (headless)")
            print("• Debug logging: DISABLED")
            print("• Use this mode for normal operation")
        
        print(f"\n✅ Configuration updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")

def show_current_mode():
    """Show current browser mode."""
    config_file = "wifi_config.json"
    
    if not os.path.exists(config_file):
        print("❌ Configuration file not found")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        debug_mode = config.get('debug_mode', False)
        headless_mode = config.get('headless_browser', True)
        
        print("📊 Current Browser Mode:")
        print(f"• Debug Mode: {'ON' if debug_mode else 'OFF'}")
        print(f"• Headless Browser: {'ON' if headless_mode else 'OFF'}")
        
        if debug_mode and not headless_mode:
            print("• Status: 🔍 DEBUG MODE (Visible Browser)")
        elif not debug_mode and headless_mode:
            print("• Status: 🚀 PRODUCTION MODE (Invisible Browser)")
        else:
            print("• Status: ⚠️  MIXED MODE (Check configuration)")
            
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        show_current_mode()
    else:
        print("🔄 Toggling Browser Mode...")
        print("=" * 40)
        show_current_mode()
        print("\n" + "=" * 40)
        toggle_browser_mode()
        print("=" * 40)
        show_current_mode()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Newfiles - Automatic content generation for new files
Monitors a directory and generates content for newly created files using OpenAI
"""

import os
import sys
import argparse
from dotenv import load_dotenv

from config.settings import Settings
from core.monitor import FileMonitor
from core.processor import FileProcessor
from utils.logger import default_logger

def main():
    """Main entry point for the application"""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Newfiles - Automatic content generation for new files")
    parser.add_argument("--config", default="config/config.json", help="Path to configuration file")
    parser.add_argument("--directory", help="Directory to monitor (overrides config)")
    args = parser.parse_args()
    
    try:
        # Load settings
        settings = Settings(args.config)
        
        # Override directory if specified in command line
        if args.directory:
            # Update the settings object with the command line directory
            settings._settings["monitored_directory"] = args.directory
        
        # Validate monitored directory exists
        if not os.path.exists(settings.monitored_directory):
            default_logger.error(f"Monitored directory does not exist: {settings.monitored_directory}")
            sys.exit(1)
        
        # Create file processor
        processor = FileProcessor(settings)
        
        # Create and start file monitor
        monitor = FileMonitor(settings, processor)
        
        default_logger.info("Newfiles application started")
        print(f"Monitoring directory: {settings.monitored_directory}")
        print("Press Ctrl+C to stop")
        
        # Start monitoring
        monitor.start()
        
    except KeyboardInterrupt:
        default_logger.info("Application interrupted by user")
        print("\nStopping monitor...")
    except Exception as e:
        default_logger.error(f"Application error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

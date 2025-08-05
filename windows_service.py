import os
import sys
import time
import logging
import json
from pathlib import Path
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from core.processor import FileProcessor
from utils.logger import default_logger

class NewfilesHandler(FileSystemEventHandler):
    """Handles file creation events"""
    
    def __init__(self, settings: Settings, processor: FileProcessor):
        """Initialize with settings and processor"""
        self.settings = settings
        self.processor = processor
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            try:
                # Apply delay before processing
                time.sleep(self.settings.delay)
                
                # Process the new file
                self.processor.process_new_file(event.src_path)
            except Exception as e:
                default_logger.error(f"Error processing file {event.src_path}: {str(e)}")

class NewfilesService:
    """Windows service for Newfiles application"""
    
    def __init__(self):
        self.observer = Observer()
        self.settings = Settings("config/config.json")
        self.processor = FileProcessor(self.settings)
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start the file monitoring service"""
        try:
            # Create event handler
            event_handler = NewfilesHandler(self.settings, self.processor)
            
            # Schedule the observer
            self.observer.schedule(
                event_handler, 
                self.settings.monitored_directory, 
                recursive=self.settings.monitor_subdirectories
            )
            
            # Start the observer
            self.observer.start()
            self.is_running = True
            
            default_logger.info(f"Newfiles service started, monitoring: {self.settings.monitored_directory}")
            
            # Keep the service running
            while self.is_running:
                time.sleep(1)
                
        except Exception as e:
            default_logger.error(f"Error starting service: {str(e)}")
            raise
    
    def stop(self):
        """Stop the file monitoring service"""
        try:
            self.is_running = False
            
            # Stop the observer
            self.observer.stop()
            self.observer.join()
            
            default_logger.info("Newfiles service stopped")
        except Exception as e:
            default_logger.error(f"Error stopping service: {str(e)}")
            raise

def main():
    """Main entry point for the service"""
    try:
        service = NewfilesService()
        service.start()
    except KeyboardInterrupt:
        print("Service interrupted by user")
    except Exception as e:
        print(f"Service error: {str(e)}")
        default_logger.error(f"Service error: {str(e)}")

if __name__ == "__main__":
    main()

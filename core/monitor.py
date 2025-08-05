import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.logger import default_logger
from config.settings import Settings
from core.processor import FileProcessor

class NewFileHandler(FileSystemEventHandler):
    """Handles file creation and rename events"""
    
    def __init__(self, settings: Settings, processor: FileProcessor):
        """Initialize with settings and processor"""
        self.settings = settings
        self.processor = processor
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            # Apply delay before processing
            time.sleep(self.settings.delay)
            
            # Process the new file
            self.processor.process_new_file(event.src_path)
    
    def on_moved(self, event):
        """Handle file rename/move events"""
        if not event.is_directory:
            # Apply delay before processing
            time.sleep(self.settings.delay)
            
            # Check if the file is empty and has a supported extension
            if self._is_empty_file_with_supported_extension(event.dest_path):
                # Process the renamed file
                self.processor.process_new_file(event.dest_path)
    
    def _is_empty_file_with_supported_extension(self, file_path: str) -> bool:
        """
        Check if a file is empty and has a supported extension
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file is empty and has a supported extension, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Check if file is empty
            if os.path.getsize(file_path) > 0:
                return False
            
            # Check if extension is supported
            filename = os.path.basename(file_path)
            extension = os.path.splitext(filename)[1].lower()
            
            # Remove the dot if present
            if extension.startswith('.'):
                extension = extension[1:]
            
            # Check if extension is in supported extensions
            supported_extensions = self.settings.extension_settings.keys()
            return extension in supported_extensions
            
        except Exception as e:
            default_logger.error(f"Error checking if file is empty with supported extension: {str(e)}")
            return False

class FileMonitor:
    """Monitors a directory for new file creations"""
    
    def __init__(self, settings: Settings, processor: FileProcessor):
        """Initialize the file monitor"""
        self.settings = settings
        self.processor = processor
        self.observer = Observer()
    
    def start(self):
        """Start monitoring the directory"""
        # Create event handler
        event_handler = NewFileHandler(self.settings, self.processor)
        
        # Schedule the observer
        self.observer.schedule(
            event_handler, 
            self.settings.monitored_directory, 
            recursive=self.settings.monitor_subdirectories
        )
        
        # Start the observer
        self.observer.start()
        default_logger.info(f"Started monitoring directory: {self.settings.monitored_directory}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop monitoring the directory"""
        self.observer.stop()
        self.observer.join()
        default_logger.info("Stopped monitoring directory")

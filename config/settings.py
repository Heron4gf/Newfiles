import json
import os
from typing import Dict, Any

class Settings:
    """Configuration settings for the Newfiles application"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize settings from config file"""
        self.config_path = config_path
        self._settings = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    @property
    def monitored_directory(self) -> str:
        """Get the directory to monitor"""
        return self._settings.get("monitored_directory", os.path.expanduser("~/Desktop"))
    
    @property
    def delay(self) -> float:
        """Get the delay before processing new files"""
        return self._settings.get("delay", 0.5)
    
    @property
    def monitor_subdirectories(self) -> bool:
        """Check if subdirectories should be monitored"""
        return self._settings.get("monitor_subdirectories", True)
    
    @property
    def default_text_prompt_file(self) -> str:
        """Get the path to the default text prompt file"""
        return self._settings.get("default_text_prompt_file", "prompts/default_text.md")
    
    @property
    def default_image_prompt_file(self) -> str:
        """Get the path to the default image prompt file"""
        return self._settings.get("default_image_prompt_file", "prompts/default_image.md")
    
    @property
    def extension_settings(self) -> Dict[str, Dict[str, str]]:
        """Get extension-specific settings"""
        return self._settings.get("extension_settings", {})
    
    def get_extension_settings(self, extension: str) -> Dict[str, str]:
        """Get settings for a specific file extension"""
        # Remove the dot if present
        if extension.startswith('.'):
            extension = extension[1:]
        
        return self.extension_settings.get(extension, {
            "model": "gpt-4.1-nano",
            "prompt_file": self.default_text_prompt_file
        })

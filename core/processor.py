import os
from typing import List, Dict

from utils.logger import default_logger
from utils.helpers import get_reference_files
from core.generator import ContentGenerator
from config.settings import Settings

class FileProcessor:
    """Processes new files based on their extension and settings"""
    
    def __init__(self, settings: Settings):
        """Initialize with settings"""
        self.settings = settings
        self.generator = ContentGenerator()
    
    def process_new_file(self, file_path: str):
        """
        Process a newly created file
        
        Args:
            file_path: Path to the newly created file
        """
        try:
            # Get file information
            filename = os.path.basename(file_path)
            directory = os.path.dirname(file_path)
            extension = os.path.splitext(filename)[1].lower()
            
            default_logger.info(f"Processing new file: {filename}")
            
            # Get extension-specific settings
            ext_settings = self.settings.get_extension_settings(extension)
            
            # Check if this is an image file
            if extension in ['.png', '.jpg', '.jpeg']:
                self._process_image_file(file_path, filename, ext_settings)
            else:
                # Process as text file
                self._process_text_file(file_path, filename, extension, directory, ext_settings)
                
        except Exception as e:
            default_logger.error(f"Error processing file {file_path}: {str(e)}")
    
    def _process_image_file(self, file_path: str, filename: str, settings: Dict[str, str]):
        """
        Process an image file by generating content
        
        Args:
            file_path: Path to the file
            filename: Name of the file
            settings: Extension settings
        """
        try:
            # Generate image content
            image_bytes = self.generator.generate_image_content(
                filename=filename,
                prompt_file=settings.get("prompt_file", self.settings.default_image_prompt_file)
            )
            
            # Write the generated image to the file
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            
            default_logger.info(f"Generated image content for: {filename}")
            
        except Exception as e:
            default_logger.error(f"Error processing image file {filename}: {str(e)}")
    
    def _process_text_file(self, file_path: str, filename: str, extension: str, 
                          directory: str, settings: Dict[str, str]):
        """
        Process a text file by generating content
        
        Args:
            file_path: Path to the file
            filename: Name of the file
            extension: File extension
            directory: Directory containing the file
            settings: Extension settings
        """
        try:
            # For dynamic prompts, get reference files
            reference_files = None
            prompt_file = settings.get("prompt_file", self.settings.default_text_prompt_file)
            
            # Check if we should use dynamic prompting (based on filename convention)
            if "dynamic" in prompt_file.lower() or "dynamic" in filename.lower():
                reference_files = get_reference_files(directory, extension, filename)
            
            # Get model from settings
            model = settings.get("model", "gpt-4.1-nano")
            
            # Generate text content
            content = self.generator.generate_text_content(
                filename=filename,
                extension=extension,
                prompt_file=prompt_file,
                reference_files=reference_files,
                model=model
            )
            
            # Write the generated content to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            default_logger.info(f"Generated text content for: {filename}")
            
        except Exception as e:
            default_logger.error(f"Error processing text file {filename}: {str(e)}")

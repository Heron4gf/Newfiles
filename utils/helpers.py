import os
import time
from typing import List, Dict, Any

def get_reference_files(directory: str, extension: str, exclude_file: str) -> List[Dict[str, Any]]:
    """
    Get reference files of the same extension from the directory
    
    Args:
        directory: Directory to search in
        extension: File extension to look for
        exclude_file: Filename to exclude from results
        
    Returns:
        List of dictionaries containing filename and content of reference files
    """
    reference_files = []
    
    # Ensure the extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Search for files with the same extension
    for filename in os.listdir(directory):
        if filename.endswith(extension) and filename != exclude_file:
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                reference_files.append({
                    'filename': filename,
                    'content': content
                })
            except Exception:
                # Skip files that can't be read as text
                continue
    
    return reference_files

def safe_delay(delay: float) -> None:
    """
    Safely wait for the specified delay
    
    Args:
        delay: Time to wait in seconds
    """
    if delay > 0:
        time.sleep(delay)

def format_reference_files(reference_files: List[Dict[str, Any]]) -> str:
    """
    Format reference files for inclusion in prompt
    
    Args:
        reference_files: List of reference files with filename and content
        
    Returns:
        Formatted string of reference files
    """
    if not reference_files:
        return "No reference files found."
    
    formatted = ""
    for file_info in reference_files:
        formatted += f"\n--- {file_info['filename']} ---\n"
        formatted += f"{file_info['content']}\n"
    
    return formatted

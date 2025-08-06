import os
import base64
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

from utils.logger import default_logger
from utils.helpers import format_reference_files

# Load environment variables
load_dotenv()

class ContentGenerator:
    """Generates content using OpenAI API based on file extension and prompts"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_text_content(self, filename: str, extension: str, prompt_file: str, 
                            reference_files: list = None, model: str = "gpt-4.1-nano") -> str:
        """
        Generate text content for a file using OpenAI
        
        Args:
            filename: Name of the file being created
            extension: File extension
            prompt_file: Path to the prompt file
            reference_files: List of reference files for dynamic prompts
            model: The model to use for generation
            
        Returns:
            Generated text content
        """
        try:
            # Read the prompt template
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Format the prompt with filename and reference files
            reference_content = format_reference_files(reference_files) if reference_files else "No reference files found."
            
            prompt = prompt_template.format(
                filename=filename,
                reference_files=reference_content
            )
            
            # Generate content using OpenAI
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            default_logger.error(f"Error generating text content for {filename}: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def generate_image_content(self, filename: str, prompt_file: str) -> bytes:
        """
        Generate image content using OpenAI GPT-Image-1
        
        Args:
            filename: Name of the file being created
            prompt_file: Path to the prompt file
            
        Returns:
            Generated image bytes
        """
        try:
            # Read the prompt template
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Format the prompt with filename
            prompt = prompt_template.format(filename=filename)
            
            # Generate image using GPT-Image-1
            img = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # Decode the base64 image
            image_bytes = base64.b64decode(img.data[0].b64_json)
            return image_bytes
            
        except Exception as e:
            default_logger.error(f"Error generating image content for {filename}: {str(e)}")
            raise

"""
Azure OpenAI Image Editing Module

This module provides functionality to edit images using Azure OpenAI's image editing API.
It follows the project's authentication patterns and Azure best practices.
"""

import os
import base64
import logging
from typing import Optional, Union
from pathlib import Path
import requests
from azure.identity import DefaultAzureCredential, AzureDeveloperCliCredential
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)


class AzureImageEditor:
    """
    Azure OpenAI Image Generator using the project's authentication patterns.
    
    Supports both API key and managed identity authentication.
    Follows Azure best practices for security and error handling.
    """
    
    def __init__(self):
        """Initialize the Azure OpenAI client with appropriate authentication."""
        self._load_environment()
        self._setup_authentication()
        self._initialize_client()
    
    def _load_environment(self):
        """Load environment variables from .env file in development."""
        if not os.environ.get("RUNNING_IN_PRODUCTION"):
            logger.info("Running in development mode, loading from .env file")
            load_dotenv()
    
    def _setup_authentication(self):
        """Setup authentication using the same pattern as other modules."""
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.environ.get("AZURE_API_KEY")
        self.api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
        self.deployment_name = os.environ.get("AZURE_OPENAI_IMAGE_DEPLOYMENT_NAME", "gpt-image-1")
        
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        
        # Use the same authentication pattern as other modules
        if not self.api_key:
            if tenant_id := os.environ.get("AZURE_TENANT_ID"):
                logger.info("Using AzureDeveloperCliCredential with tenant_id %s", tenant_id)
                self.credential = AzureDeveloperCliCredential(
                    tenant_id=tenant_id, process_timeout=60
                )
            else:
                logger.info("Using DefaultAzureCredential")
                self.credential = DefaultAzureCredential()
        else:
            self.credential = AzureKeyCredential(self.api_key)
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client."""
        try:
            if isinstance(self.credential, AzureKeyCredential):
                self.client = AzureOpenAI(
                    api_key=self.credential.key,
                    api_version=self.api_version,
                    azure_endpoint=self.endpoint
                )
            else:
                self.client = AzureOpenAI(
                    azure_ad_token_provider=lambda: self.credential.get_token(
                        "https://cognitiveservices.azure.com/.default"
                    ).token,
                    api_version=self.api_version,
                    azure_endpoint=self.endpoint
                )
            logger.info("Azure OpenAI client initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Azure OpenAI client: %s", e)
            raise
    
    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "medium",
        output_format: str = "png",
        output_compression: int = 100,
        n: int = 1
    ) -> Optional[bytes]:
        """
        Generate an image using Azure OpenAI's image generation API.
        
        Args:
            prompt: Text description of the image to generate
            size: Image size (e.g., "1024x1024", "512x512")
            quality: Image quality ("standard" or "hd")
            output_format: Output format ("png" or "jpeg")
            output_compression: Compression level (1-100)
            n: Number of images to generate (1-10)
        
        Returns:
            bytes: Image data as bytes, or None if generation failed
        
        Raises:
            ValueError: If parameters are invalid
            Exception: If API call fails
        """
        # Validate parameters
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        if size not in ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]:
            raise ValueError(f"Invalid size: {size}")
        
        if quality not in ["standard", "hd", "medium"]:
            raise ValueError(f"Invalid quality: {quality}")
        
        if output_format not in ["png", "jpeg"]:
            raise ValueError(f"Invalid output format: {output_format}")
        
        if not 1 <= output_compression <= 100:
            raise ValueError("Output compression must be between 1 and 100")
        
        if not 1 <= n <= 10:
            raise ValueError("Number of images must be between 1 and 10")
        
        try:
            logger.info("Generating image with prompt: %s", prompt)
            
            response = self.client.images.generate(
                model=self.deployment_name,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            
            if response.data:
                # Return the first image as bytes
                image_b64 = response.data[0].b64_json
                image_bytes = base64.b64decode(image_b64)
                logger.info("Image generated successfully, size: %d bytes", len(image_bytes))
                return image_bytes
            else:
                logger.error("No image data returned from API")
                return None
                
        except Exception as e:
            logger.error("Failed to generate image: %s", e)
            raise
    
    def save_image(self, image_bytes: bytes, filename: str) -> str:
        """
        Save image bytes to a file.
        
        Args:
            image_bytes: Image data as bytes
            filename: Output filename
        
        Returns:
            str: Full path to saved file
        """
        try:
            with open(filename, 'wb') as f:
                f.write(image_bytes)
            
            abs_path = os.path.abspath(filename)
            logger.info("Image saved to: %s", abs_path)
            return abs_path
        except Exception as e:
            logger.error("Failed to save image: %s", e)
            raise
    
    def edit_image(
        self,
        prompt: str,
        image_path: Union[str, Path],
        image_path2: Union[str, Path],
        output_file: str = "edited_image.png"
    ) -> Optional[str]:
        """
        Edit an existing PNG image using Azure OpenAI's image edit API.

        Args:
            prompt: Edit prompt
            image_path: Path to the first image to edit (PNG)
            image_path2: Path to the second image to edit (PNG)
            output_file: Output filename for the edited image

        Returns:
            str: Path to the saved edited image, or None if failed

        Raises:
            ValueError: If parameters are invalid
            Exception: If API call fails
        """
        try:
            logger.info("Editing images using Azure OpenAI API...")
            with open(image_path, "rb") as img1, open(image_path2, "rb") as img2:
                result_edit = self.client.images.edit(
                    model=self.deployment_name,
                    image=img1,
                    prompt=prompt,
                    # size="1024x1536"
                )
                if result_edit.data and result_edit.data[0].b64_json:
                    print(f"Image edit result: {result_edit.data[0].b64_json}"  )
                    image_b64 = result_edit.data[0].b64_json
                    image_bytes = base64.b64decode(image_b64)
                    with open(output_file, "wb") as f:
                        f.write(image_bytes)
                    logger.info(f"Edited image saved to: {output_file}")
                    return os.path.abspath(output_file)
                else:
                    logger.error("No image data returned from API")
                    return None
        except Exception as e:
            logger.error(f"Failed to edit image: {e}")
            raise


def main():
    """
    Example usage of the Azure Image Generator.
    
    This replicates the curl command functionality:
    - Generates an image from a text prompt
    - Saves it as a PNG file
    """
    try:
        
        # Initialize the editor
        editor = AzureImageEditor()
        # Example: Edit an existing PNG file
        image_path = "image_to_edit.png"
        additional_path = "Subject.png"   # Path to your PNG file        # Path to your mask PNG file
        prompt = "Merge the photo with the subject"
        output_file = "edited_image.png"
        if os.path.exists(image_path):
            edited_path = editor.edit_image(prompt, image_path, additional_path, output_file)
            if edited_path:
                print(f"Edited image saved to: {edited_path}")
            else:
                print("Failed to edit image")
        else:
            print("Image or mask file not found. Skipping edit example.")
            
    except Exception as e:
        logger.error("Error in main: %s", e)
        print(f"Error: {e}")


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()


https://github.com/andreaskopp/visionary-lab/blob/main/notebooks/gpt-image-1.ipynb
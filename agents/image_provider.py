import base64
import os
from typing import Optional


class ImageProvider:
    def __init__(self, base_url: str, model: str, api_key: str, client: Optional[any] = None):
        self.base_url = base_url
        self.model = model
        self.api_key = api_key
        self.client = client
        self._ensure_assets_directory()
        
    def _ensure_assets_directory(self):
        """Ensure the assets directory exists"""
        os.makedirs("assets", exist_ok=True)
        
    async def generate_image(self, prompt: str, output_path: str = "assets/location.png") -> bool:
        """Generate an image from a prompt and return base64 encoded image"""
        try:
            response = self.client.images.generate(
                prompt=prompt,
                model=self.model,
                size="1024x1024",
                quality="standard",
                n=1,
                response_format="b64_json"
            )
            
            # Get base64 string from response
            image_b64 = response.data[0].b64_json
            
            # Save the decoded image
            image_data = base64.b64decode(image_b64)
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"Image saved to {output_path}")
            return True
                            
        except Exception as e:
            # Silently fail unless it's a critical error
            if "API key" in str(e) or "authentication" in str(e).lower():
                print(f"Critical OpenAI API error: {e}")
            return False
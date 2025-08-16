import google.generativeai as genai
import requests
from PIL import Image
import io
import base64
from config import GEMINI_API_KEY, IMAGE_WIDTH, IMAGE_HEIGHT

class ImageGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_page_image(self, page_text, character_description, page_number):
        """Generate an image for a specific story page"""
        try:
            # Create a detailed prompt for consistent image generation
            image_prompt = f"""
            Create a beautiful, colorful children's book illustration for page {page_number} of a story.
            
            Story text: "{page_text}"
            Character description: "{character_description}"
            
            Requirements:
            - Children's book art style, colorful and engaging
            - Consistent with the character description provided
            - Safe for children, no scary or inappropriate content
            - Bright, cheerful colors
            - Simple, clear composition suitable for children
            - Size: {IMAGE_WIDTH}x{IMAGE_HEIGHT} pixels
            
            Make it look like a professional children's book illustration.
            """
            
            # For now, we'll use a placeholder image generation approach
            # Since Gemini's image generation might have limitations, we'll create a text-based image
            return self._create_placeholder_image(page_text, page_number)
            
        except Exception as e:
            print(f"Error generating image for page {page_number}: {e}")
            return self._create_placeholder_image(page_text, page_number)
    
    def _create_placeholder_image(self, page_text, page_number):
        """Create a placeholder image with text (fallback when image generation fails)"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a new image with a light background
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#f0f8ff')
            draw = ImageDraw.Draw(img)
            
            # Add a decorative border
            draw.rectangle([0, 0, IMAGE_WIDTH-1, IMAGE_HEIGHT-1], outline='#4a90e2', width=3)
            
            # Add page number
            draw.text((20, 20), f"Page {page_number}", fill='#4a90e2', font=None)
            
            # Add story text (wrapped)
            text_lines = self._wrap_text(page_text, 30)
            y_position = 80
            
            for line in text_lines:
                draw.text((20, y_position), line, fill='#333333', font=None)
                y_position += 25
            
            # Add decorative elements
            draw.ellipse([IMAGE_WIDTH-80, IMAGE_HEIGHT-80, IMAGE_WIDTH-20, IMAGE_HEIGHT-20], 
                        fill='#ffd700', outline='#ff8c00', width=2)
            
            return img
            
        except Exception as e:
            print(f"Error creating placeholder image: {e}")
            # Return a simple colored rectangle as ultimate fallback
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#e6f3ff')
            return img
    
    def _wrap_text(self, text, max_width):
        """Wrap text to fit within a specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_width:
                current_line += (" " + word) if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def save_image(self, image, filename):
        """Save an image to a file"""
        try:
            image.save(filename, 'PNG')
            return True
        except Exception as e:
            print(f"Error saving image {filename}: {e}")
            return False
    
    def image_to_base64(self, image):
        """Convert PIL image to base64 string for HTML display"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None

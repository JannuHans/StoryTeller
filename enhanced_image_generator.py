import google.generativeai as genai
import requests
from PIL import Image
import io
import base64
import time
from config import GEMINI_API_KEY, IMAGE_WIDTH, IMAGE_HEIGHT

class EnhancedImageGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Use Gemini 1.5 Flash for image generation
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_page_image(self, page_text, character_description, page_number, story_context=""):
        """Generate a high-quality AI image for a specific story page"""
        try:
            # Create a detailed, artistic prompt for image generation
            image_prompt = self._create_artistic_prompt(page_text, character_description, page_number, story_context)
            
            # Generate image using Gemini
            response = self.model.generate_content(image_prompt)
            
            # Check if response contains image data
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Convert the generated image data to PIL Image
                                image_data = part.inline_data.data
                                image_bytes = base64.b64decode(image_data)
                                image = Image.open(io.BytesIO(image_bytes))
                                
                                # Resize to our standard dimensions
                                image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
                                return image
            
            # Fallback to enhanced placeholder if AI generation fails
            return self._create_enhanced_placeholder_image(page_text, page_number, character_description)
            
        except Exception as e:
            print(f"Error generating AI image for page {page_number}: {e}")
            # Return enhanced placeholder as fallback
            return self._create_enhanced_placeholder_image(page_text, page_number, character_description)
    
    def _create_artistic_prompt(self, page_text, character_description, page_number, story_context):
        """Create a detailed, artistic prompt for AI image generation"""
        prompt = f"""
        Create a beautiful, high-quality children's book illustration for page {page_number}.
        
        STORY CONTEXT: {story_context}
        PAGE TEXT: "{page_text}"
        CHARACTER DESCRIPTION: "{character_description}"
        
        ARTISTIC REQUIREMENTS:
        - Children's book illustration style, similar to Eric Carle or Dr. Seuss
        - Bright, vibrant, warm colors that appeal to children
        - Soft, rounded shapes and friendly expressions
        - Rich details and textures
        - Professional illustration quality
        - Safe and appropriate for children aged 4-8
        
        COMPOSITION:
        - Main character prominently featured
        - Engaging background with environmental details
        - Balanced composition with clear focal point
        - Depth and perspective
        - Whimsical and magical atmosphere
        
        TECHNICAL SPECS:
        - High resolution, detailed artwork
        - Professional children's book quality
        - Consistent with character design
        - Suitable for printing and digital display
        
        Make this illustration captivating and memorable for young readers!
        """
        return prompt
    
    def _create_enhanced_placeholder_image(self, page_text, page_number, character_description):
        """Create an enhanced placeholder image with better design"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a larger canvas for better quality
            canvas_width = IMAGE_WIDTH * 2
            canvas_height = IMAGE_HEIGHT * 2
            
            # Create background with gradient effect
            img = Image.new('RGB', (canvas_width, canvas_height), color='#e8f4fd')
            draw = ImageDraw.Draw(img)
            
            # Create gradient background
            for y in range(canvas_height):
                # Create a subtle gradient from top to bottom
                r = int(232 + (y / canvas_height) * 20)  # Blue to lighter blue
                g = int(244 + (y / canvas_height) * 10)  # Light blue
                b = int(253 + (y / canvas_height) * 2)   # Very light blue
                color = (r, g, b)
                draw.line([(0, y), (canvas_width, y)], fill=color)
            
            # Add decorative border with rounded corners effect
            border_color = '#4a90e2'
            border_width = 8
            
            # Main border
            draw.rectangle([border_width, border_width, canvas_width-border_width, canvas_height-border_width], 
                         outline=border_color, width=border_width)
            
            # Add inner decorative border
            inner_border = border_width * 2
            draw.rectangle([inner_border, inner_border, canvas_width-inner_border, canvas_height-inner_border], 
                         outline='#6baed6', width=3)
            
            # Add page number with decorative background
            page_num_bg = (canvas_width - 120, 20, canvas_width - 20, 80)
            draw.ellipse(page_num_bg, fill='#ffd700', outline='#ff8c00', width=3)
            draw.text((canvas_width - 100, 35), f"Page {page_number}", fill='#8b4513', font=None)
            
            # Add story text with better formatting
            text_lines = self._wrap_text(page_text, 50)
            y_position = 120
            
            for line in text_lines:
                # Add text shadow for better readability
                draw.text((25, y_position + 2), line, fill='#2c3e50', font=None)
                draw.text((23, y_position), line, fill='#34495e', font=None)
                y_position += 35
            
            # Add decorative elements
            # Sun/moon in top left
            sun_pos = (80, 80)
            draw.ellipse([sun_pos[0], sun_pos[1], sun_pos[0] + 60, sun_pos[1] + 60], 
                        fill='#ffd700', outline='#ff8c00', width=3)
            
            # Add sun rays
            for i in range(8):
                angle = i * 45
                x = sun_pos[0] + 30 + int(40 * (angle % 90) / 90)
                y = sun_pos[1] + 30 + int(40 * (angle % 90) / 90)
                draw.line([(sun_pos[0] + 30, sun_pos[1] + 30), (x, y)], fill='#ff8c00', width=2)
            
            # Add character silhouette placeholder
            char_pos = (canvas_width - 200, canvas_height - 200)
            draw.ellipse([char_pos[0], char_pos[1], char_pos[0] + 80, char_pos[1] + 80], 
                        fill='#ffb6c1', outline='#ff69b4', width=3)
            
            # Add some floating elements
            for i in range(5):
                x = 50 + i * 80
                y = canvas_height - 100 + (i % 2) * 20
                draw.ellipse([x, y, x + 20, y + 20], fill='#98fb98', outline='#32cd32', width=2)
            
            # Resize back to original dimensions
            img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            return img
            
        except Exception as e:
            print(f"Error creating enhanced placeholder image: {e}")
            # Ultimate fallback
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#e6f3ff')
            draw = ImageDraw.Draw(img)
            draw.text((20, 20), f"Page {page_number}", fill='#4a90e2')
            draw.text((20, 60), "Image generation in progress...", fill='#666666')
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
        """Save an image to a file with high quality"""
        try:
            image.save(filename, 'PNG', quality=95, optimize=True)
            return True
        except Exception as e:
            print(f"Error saving image {filename}: {e}")
            return False
    
    def image_to_base64(self, image):
        """Convert PIL image to base64 string for HTML display"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG', quality=95, optimize=True)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None

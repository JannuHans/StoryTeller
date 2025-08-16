import google.generativeai as genai
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import base64
import time
import random
from config import GEMINI_API_KEY, IMAGE_WIDTH, IMAGE_HEIGHT

class ProfessionalImageGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Use the most advanced Gemini model for image generation
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Professional color palettes for children's books
        self.color_palettes = {
            'warm': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            'cool': ['#A8E6CF', '#DCEDC8', '#FFD3B6', '#FFAAA5', '#FF8B94', '#B8E6B8'],
            'vibrant': ['#FF6B9D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            'pastel': ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFB3F7', '#B3F7FF']
        }
    
    def generate_page_image(self, page_text, character_description, page_number, story_context=""):
        """Generate a professional, high-quality AI image for a specific story page"""
        try:
            # First attempt: Use Gemini's advanced image generation
            ai_image = self._generate_ai_image(page_text, character_description, page_number, story_context)
            if ai_image:
                return self._enhance_image_quality(ai_image)
            
            # Fallback: Create professional hand-drawn style illustration
            return self._create_professional_illustration(page_text, page_number, character_description)
            
        except Exception as e:
            print(f"Error generating professional image for page {page_number}: {e}")
            return self._create_professional_illustration(page_text, page_number, character_description)
    
    def _generate_ai_image(self, page_text, character_description, page_number, story_context):
        """Generate image using Gemini's advanced capabilities"""
        try:
            # Create a sophisticated, artistic prompt
            image_prompt = self._create_advanced_artistic_prompt(page_text, character_description, page_number, story_context)
            
            # Generate content with the advanced prompt
            response = self.model.generate_content(image_prompt)
            
            # Process the response for image data
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Convert to PIL Image
                                image_data = part.inline_data.data
                                image_bytes = base64.b64decode(image_data)
                                image = Image.open(io.BytesIO(image_bytes))
                                
                                # Resize and enhance
                                image = image.resize((IMAGE_WIDTH * 2, IMAGE_HEIGHT * 2), Image.Resampling.LANCZOS)
                                return image
            
            return None
            
        except Exception as e:
            print(f"AI image generation failed: {e}")
            return None
    
    def _create_advanced_artistic_prompt(self, page_text, character_description, page_number, story_context):
        """Create a sophisticated, artistic prompt for AI image generation"""
        
        # Select artistic style based on page number
        styles = [
            "watercolor children's book illustration style",
            "digital art children's book style with soft lighting",
            "hand-drawn children's book illustration with vibrant colors",
            "mixed media children's book art with texture and depth",
            "contemporary children's book illustration style"
        ]
        
        style = styles[(page_number - 1) % len(styles)]
        
        prompt = f"""
        Create a stunning, professional children's book illustration for page {page_number}.
        
        STORY CONTEXT: {story_context}
        PAGE TEXT: "{page_text}"
        CHARACTER DESCRIPTION: "{character_description}"
        
        ARTISTIC STYLE: {style}
        
        COMPOSITION REQUIREMENTS:
        - Main character prominently featured with expressive face and body language
        - Rich, detailed background with environmental storytelling
        - Dynamic lighting with shadows and highlights
        - Multiple layers of depth and perspective
        - Whimsical, magical atmosphere that captivates children
        
        VISUAL ELEMENTS:
        - Bright, harmonious color palette with complementary colors
        - Smooth gradients and soft transitions
        - Textured surfaces and materials
        - Atmospheric effects (light rays, sparkles, mist)
        - Seasonal or time-of-day appropriate lighting
        
        TECHNICAL QUALITY:
        - High resolution, crisp details
        - Professional illustration standards
        - Consistent with children's book publishing quality
        - Suitable for both print and digital formats
        - Clean, polished finish
        
        EMOTIONAL IMPACT:
        - Warm, inviting, and engaging
        - Age-appropriate for children 4-8
        - Inspires imagination and wonder
        - Memorable and distinctive
        
        Make this illustration absolutely magical and professional!
        """
        
        return prompt
    
    def _create_professional_illustration(self, page_text, page_number, character_description):
        """Create a professional hand-drawn style illustration"""
        try:
            # Create high-resolution canvas
            canvas_width = IMAGE_WIDTH * 3
            canvas_height = IMAGE_HEIGHT * 3
            
            # Create base image with professional background
            img = self._create_professional_background(canvas_width, canvas_height, page_number)
            draw = ImageDraw.Draw(img)
            
            # Add sophisticated decorative elements
            self._add_professional_decorations(draw, canvas_width, canvas_height, page_number)
            
            # Add story text with professional typography
            self._add_professional_text(draw, page_text, canvas_width, canvas_height)
            
            # Add character illustration placeholder
            self._add_character_illustration(draw, canvas_width, canvas_height, character_description)
            
            # Add environmental details
            self._add_environmental_details(draw, canvas_width, canvas_height, page_number)
            
            # Apply professional post-processing
            img = self._apply_professional_effects(img)
            
            # Resize to final dimensions
            img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            return img
            
        except Exception as e:
            print(f"Error creating professional illustration: {e}")
            return self._create_fallback_image(page_number)
    
    def _create_professional_background(self, width, height, page_number):
        """Create a sophisticated background with gradients and textures"""
        # Create base image
        img = Image.new('RGB', (width, height), color='#f8f9fa')
        draw = ImageDraw.Draw(img)
        
        # Create multiple gradient layers
        self._create_gradient_layers(draw, width, height, page_number)
        
        # Add subtle texture patterns
        self._add_texture_patterns(draw, width, height)
        
        return img
    
    def _create_gradient_layers(self, draw, width, height, page_number):
        """Create sophisticated gradient layers"""
        # Primary gradient (sky-like)
        for y in range(height):
            # Create a complex gradient with multiple color stops
            if y < height * 0.3:
                # Sky gradient
                r = int(135 + (y / (height * 0.3)) * 40)
                g = int(206 + (y / (height * 0.3)) * 30)
                b = int(235 + (y / (height * 0.3)) * 20)
            elif y < height * 0.7:
                # Middle gradient
                r = int(175 + ((y - height * 0.3) / (height * 0.4)) * 30)
                g = int(236 + ((y - height * 0.3) / (height * 0.4)) * 20)
                b = int(255 + ((y - height * 0.3) / (height * 0.4)) * 10)
            else:
                # Ground gradient
                r = int(205 + ((y - height * 0.7) / (height * 0.3)) * 50)
                g = int(255 + ((y - height * 0.7) / (height * 0.3)) * 20)
                b = int(255 + ((y - height * 0.7) / (height * 0.3)) * 10)
            
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
    
    def _add_texture_patterns(self, draw, width, height):
        """Add subtle texture patterns to the background"""
        # Add cloud-like patterns
        for i in range(8):
            x = random.randint(0, width)
            y = random.randint(0, int(height * 0.4))
            size = random.randint(30, 80)
            opacity = random.randint(20, 40)
            
            # Create soft cloud shapes
            for j in range(size):
                for k in range(size):
                    if (j - size/2)**2 + (k - size/2)**2 < (size/2)**2:
                        px, py = x + j - size/2, y + k - size/2
                        if 0 <= px < width and 0 <= py < height:
                            # Get current pixel color
                            current_color = draw.getpixel((px, py))
                            # Blend with white cloud
                            new_color = tuple(int(c * (1 - opacity/100) + 255 * (opacity/100)) for c in current_color)
                            draw.point((px, py), fill=new_color)
    
    def _add_professional_decorations(self, draw, width, height, page_number):
        """Add sophisticated decorative elements"""
        # Add elegant border
        border_color = '#2E86AB'
        border_width = 12
        
        # Main border with rounded corners effect
        draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                      outline=border_color, width=border_width)
        
        # Inner decorative border
        inner_border = border_width * 2
        draw.rectangle([inner_border, inner_border, width-inner_border, height-inner_border], 
                      outline='#6baed6', width=6)
        
        # Add corner decorations
        corner_size = 60
        corner_color = '#ffd700'
        
        # Top-left corner
        draw.ellipse([20, 20, 20 + corner_size, 20 + corner_size], 
                    fill=corner_color, outline='#ff8c00', width=3)
        
        # Top-right corner
        draw.ellipse([width - 20 - corner_size, 20, width - 20, 20 + corner_size], 
                    fill=corner_color, outline='#ff8c00', width=3)
        
        # Bottom-left corner
        draw.ellipse([20, height - 20 - corner_size, 20 + corner_size, height - 20], 
                    fill=corner_color, outline='#ff8c00', width=3)
        
        # Bottom-right corner
        draw.ellipse([width - 20 - corner_size, height - 20 - corner_size, width - 20, height - 20], 
                    fill=corner_color, outline='#ff8c00', width=3)
        
        # Add page number with elegant design
        page_num_bg = (width - 140, 30, width - 30, 100)
        draw.ellipse(page_num_bg, fill='#ffd700', outline='#ff8c00', width=4)
        
        # Add page number text
        page_text = f"Page {page_number}"
        text_bbox = draw.textbbox((0, 0), page_text)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = page_num_bg[0] + (page_num_bg[2] - page_num_bg[0] - text_width) // 2
        text_y = page_num_bg[1] + 25
        draw.text((text_x, text_y), page_text, fill='#8b4513')
    
    def _add_professional_text(self, draw, page_text, width, height):
        """Add story text with professional typography"""
        # Wrap text professionally
        text_lines = self._wrap_text_professionally(page_text, 60)
        
        # Calculate text positioning
        line_height = 45
        total_text_height = len(text_lines) * line_height
        start_y = height * 0.6
        
        # Add text background for readability
        text_bg_height = total_text_height + 40
        text_bg_y = start_y - 20
        draw.rectangle([30, text_bg_y, width - 30, text_bg_y + text_bg_height], 
                      fill='rgba(255, 255, 255, 0.9)', outline='#4a90e2', width=2)
        
        # Add text with shadow effect
        for i, line in enumerate(text_lines):
            y_pos = start_y + i * line_height
            
            # Text shadow
            draw.text((33, y_pos + 2), line, fill='#2c3e50')
            # Main text
            draw.text((30, y_pos), line, fill='#34495e')
    
    def _wrap_text_professionally(self, text, max_width):
        """Wrap text with professional line breaking"""
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
    
    def _add_character_illustration(self, draw, width, height, character_description):
        """Add a sophisticated character illustration"""
        # Create character silhouette with professional design
        char_center_x = width // 2
        char_center_y = height * 0.35
        char_size = 120
        
        # Character body (rounded rectangle)
        body_rect = [char_center_x - char_size//2, char_center_y - char_size//2,
                    char_center_x + char_size//2, char_center_y + char_size//2]
        
        # Create rounded rectangle effect
        self._draw_rounded_rectangle(draw, body_rect, '#ffb6c1', '#ff69b4', 4)
        
        # Character head
        head_center = (char_center_x, char_center_y - char_size//2 - 30)
        head_radius = 40
        draw.ellipse([head_center[0] - head_radius, head_center[1] - head_radius,
                     head_center[0] + head_radius, head_center[1] + head_radius], 
                    fill='#ffdab9', outline='#daa520', width=3)
        
        # Character eyes
        eye_color = '#4169e1'
        left_eye = (head_center[0] - 15, head_center[1] - 5)
        right_eye = (head_center[0] + 15, head_center[1] - 5)
        
        draw.ellipse([left_eye[0] - 8, left_eye[1] - 8, left_eye[0] + 8, left_eye[1] + 8], 
                    fill=eye_color, outline='#000080', width=2)
        draw.ellipse([right_eye[0] - 8, right_eye[1] - 8, right_eye[0] + 8, right_eye[1] + 8], 
                    fill=eye_color, outline='#000080', width=2)
        
        # Character smile
        smile_bbox = [head_center[0] - 20, head_center[1] + 5, head_center[0] + 20, head_center[1] + 25]
        draw.arc(smile_bbox, start=0, end=180, fill='#ff69b4', width=3)
    
    def _draw_rounded_rectangle(self, draw, rect, fill_color, outline_color, width):
        """Draw a rounded rectangle with professional appearance"""
        x1, y1, x2, y2 = rect
        radius = 20
        
        # Fill the rounded rectangle
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill_color)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill_color)
        
        # Draw corner circles
        draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill_color)
        draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill_color)
        draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill_color)
        draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill_color)
        
        # Outline
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], start=90, end=180, fill=outline_color, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], start=0, end=90, fill=outline_color, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], start=180, end=270, fill=outline_color, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], start=270, end=360, fill=outline_color, width=width)
        
        # Straight edges
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline_color, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline_color, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline_color, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline_color, width=width)
    
    def _add_environmental_details(self, draw, width, height, page_number):
        """Add environmental details for storytelling"""
        # Add floating magical elements
        for i in range(6):
            x = random.randint(50, width - 50)
            y = random.randint(50, int(height * 0.5))
            size = random.randint(15, 30)
            color = random.choice(self.color_palettes['vibrant'])
            
            # Create star-like shapes
            self._draw_star(draw, x, y, size, color)
        
        # Add ground details
        ground_y = height * 0.7
        for i in range(0, width, 40):
            grass_height = random.randint(10, 25)
            grass_color = random.choice(['#228B22', '#32CD32', '#90EE90'])
            draw.line([i, ground_y, i + random.randint(-10, 10), ground_y - grass_height], 
                     fill=grass_color, width=2)
    
    def _draw_star(self, draw, x, y, size, color):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            px = x + radius * (angle * 0.5)
            py = y + radius * (angle * 0.5)
            points.append((px, py))
        
        if len(points) >= 3:
            draw.polygon(points, fill=color, outline='#ffffff', width=1)
    
    def _apply_professional_effects(self, img):
        """Apply professional post-processing effects"""
        try:
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
            
            # Add subtle blur for professional look
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Enhance colors
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            
        except Exception as e:
            print(f"Error applying professional effects: {e}")
        
        return img
    
    def _create_fallback_image(self, page_number):
        """Create a simple but professional fallback image"""
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#e6f3ff')
        draw = ImageDraw.Draw(img)
        
        # Add professional border
        draw.rectangle([0, 0, IMAGE_WIDTH-1, IMAGE_HEIGHT-1], outline='#4a90e2', width=3)
        
        # Add page number
        draw.text((20, 20), f"Page {page_number}", fill='#4a90e2')
        draw.text((20, 60), "Professional illustration", fill='#666666')
        draw.text((20, 90), "coming soon...", fill='#666666')
        
        return img
    
    def _enhance_image_quality(self, image):
        """Enhance the quality of AI-generated images"""
        try:
            # Resize to our standard dimensions
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            # Apply professional enhancement
            image = self._apply_professional_effects(image)
            
            return image
            
        except Exception as e:
            print(f"Error enhancing image quality: {e}")
            return image
    
    def save_image(self, image, filename):
        """Save image with maximum quality"""
        try:
            image.save(filename, 'PNG', quality=100, optimize=False)
            return True
        except Exception as e:
            print(f"Error saving image {filename}: {e}")
            return False
    
    def image_to_base64(self, image):
        """Convert image to high-quality base64"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG', quality=100, optimize=False)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None
